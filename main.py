import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from collections import Counter
import pandas as pd


def get_bilibili_api(new_url):
    url='https://www.i'+new_url[12:]
    return url

def get_vedio_link(page,vedio,driver):
        if page==1:
            button=driver.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div:nth-child({vedio}) > div > div.bili-video-card__wrap.__scale-wrap > a')
        else:
            button=driver.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.video-list.row > div:nth-child({vedio}) > div > div.bili-video-card__wrap.__scale-wrap > a')
        link=button.get_attribute('href')
        return link

def get_danmu_url(new_url,headers):
    response=requests.get(url=new_url,headers=headers)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    find=soup.select('#dtl > div:nth-child(5) > input') # 找到弹幕地址的标签
    for elment in find:
        target_url=elment.attrs.get("value")
    return target_url

def get_danmu(target_url,headers):
    response=requests.get(url=target_url,headers=headers)
    response.encoding='utf-8'  # 没有这个步骤会乱码
    soup=BeautifulSoup(response.text,'html.parser')
    all_danmu=soup.find_all('d')
    return all_danmu
     

def download_danmu(all_danmu):
    for danmu in all_danmu:
        with open('danmu.txt','a',encoding='utf-8') as f:
            f.write(danmu.get_text()+'\n')



def get_next_page(page,driver):
    js_bottom="document.documentElement.scrollTop=100000" 
    driver.execute_script(js_bottom) # 滑到底部
    time.sleep(7)
    if page==1:
        button=driver.find_element(By.CSS_SELECTOR,'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(11)')
    else:
        button=driver.find_element(By.CSS_SELECTOR,'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(11)')
    button.click()
    WebDriverWait(driver, 10)

def find_top_twenty_danmu():
    # 读取弹幕文件
    with open('danmu.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 统计每条弹幕出现的次数
    danmu_counts = Counter(lines)

    # 找到出现次数最多的前二十条弹幕
    top_twenty_danmu = danmu_counts.most_common(20)
    return top_twenty_danmu


def danmu_analysis():
    top_twenty_danmu=find_top_twenty_danmu()

    # 打印结果
    for i, (danmu, count) in enumerate(top_twenty_danmu, 1):
        print(f'{i}. 弹幕: {danmu.strip()}, 出现次数: {count}')

    # 保存结果
    danmu_counts_dict=dict()
    danmu_list=list()
    count_list=list()
    for i, (danmu, count) in enumerate(top_twenty_danmu, 1):
        danmu.strip("\n")
        danmu_list.append(danmu)
        count_list.append(count)

    danmu_counts_dict['弹幕']=danmu_list
    danmu_counts_dict['出现次数'] = count_list

    df=pd.DataFrame(danmu_counts_dict)
    df.to_excel("top20_danmu.xlsx",index=False)


def main():
    count=0
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 使用headless实现selenium的无界面操作
    # 获取在b站搜索"日本核污染水排海"的首页
    url='https://search.bilibili.com/all?vt=88752164&keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%9F%93%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=3' 
    driver=webdriver.Chrome(options=chrome_options) 
    driver.get(url) 
    # 一页30个视频（目测法）
    for page in range(1,11):
        driver.get(driver.current_url)
        WebDriverWait(driver, 10)
        time.sleep(11)
        for vedio in range(1,31):
            # 获取视频链接
            link=get_vedio_link(page,vedio,driver)

            # 获取b站api接口
            new_url=get_bilibili_api(link)
            
            # 进行伪装
            headers = {
                    # 请自行查找自己的"User-Agent"
                }
            
            # 获取弹幕地址
            target_url=get_danmu_url(new_url,headers)

            # 解析网页内容-->得到所有弹幕
            all_danmu=get_danmu(target_url,headers)
            
            # 下载所有的弹幕
            download_danmu(all_danmu)

            count+=1
            time.sleep(7)

        # 跳转到下一页
        get_next_page(page,driver)
        
    print(f"本程序共爬取{count}视频的弹幕")
    
    print("两秒后进行弹幕分析")
    time.sleep(2)
    danmu_analysis()



if __name__ == "__main__":
    main()