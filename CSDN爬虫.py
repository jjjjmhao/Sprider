import requests
from lxml import etree
from selenium import webdriver
import time

path = r'/home/jmhao/chromedriver'
driver = webdriver.Chrome(path)
#因为正常抓取无法获得链接信息,所以使用模拟浏览器抓取
driver.get(url = 'https://blog.csdn.net/tuoshao123')
time.sleep(2)
#将页面源码保存到变量response中
response = driver.page_source
driver.quit()
html = etree.HTML(response)
#提取所有的url
tuoeg_urls = html.xpath("//div[@class='article-item-box csdn-tracking-statistics']/h4/a/@href")
#以列表的形式遍历其中的元素
for i in range(0,len(tuoeg_urls)):
    article = requests.get(tuoeg_urls[i]).text
    html_article = etree.HTML(article)
    #提取文本标题
    tuo_title = '\n'.join(html_article.xpath("//h1[@class='title-article']/text()"))
    #提取文章文本内容
    tuo_article = html_article.xpath("string(//div[@id='content_views'])")
    #提取文章中的图片链接
    tuo_src = '\n'.join(html_article.xpath("//div[@id='content_views']/p/img/@src"))
    with open('tuoge/' + tuo_title + '.txt','w') as f:
        print('正在下载 ' + tuo_title + ' ......')
        f.write(tuo_article)
        f.write(tuo_src)