# 

# Part·1 任务背景

2023年8月24日，日本罔顾国际社会和组织的质疑和反对，强行启动了核污水排海计划，正式开始将福岛第一核电站的核污水排放至太平洋。根据该计划，核污水排海时间将至少持续30年，2023年度将把约3.12万吨核污水分4次排放，每次约排放7800吨，完成首次排放需要17天左右。核污水排海带来的危害将是不可逆的，造成安全威胁是多方面的，产生的影响更是全世界和长期的。世界人民对此的看法众说纷纭，我们希望能得到一些确切的看法。

## 数据获取

1. 利用爬虫B站爬取所需弹幕数据，搜索关键词“日本核污染水排海”，爬取综合排序前300的所有视频弹幕。

## 数据统计

1. 统计每种弹幕数量，并输出数量排名前20的弹幕。
2. 将统计的数据利用编程工具或开发包自动写入Excel表中。

# Part·2 任务实现

## 任务流程

整个程序分为三个部分，第一步是使用selenium实现自动化，获取视频的链接和自动点击下一页的操作。第二步是使用requests和bs4获取并解析网页，获取我想要的弹幕内容。在保存了所有爬取的弹幕后，第三步是分析数据并找到top20，然后使用pandas导入excel中。

## 配置需求（建议使用python虚拟环境和chrome浏览器）

```
pip install -r requirements.txt
```

还需要下载浏览器驱动程序，用来实现自动化爬虫(下载好对应的驱动版本之后要把驱动程序放在python解释器即python.exe所在的目录下)

https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-cn



