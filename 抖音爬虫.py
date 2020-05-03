from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options
import requests
import json
import time

class Douyin:
    def page_num(self,max_cursor):
        #网址后面的随机参数（我实在分析不出规律）
        # 设置谷歌无界面浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chromdriver地址
        path = r'/home/jmhao/chromedriver'
        #随机码
        random_field = ''
        #网址的主体
        url = '' + str(max_cursor) + '&aid=1128&_signature=' + random_field
        #请求头
        headers = {
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        }
        response = requests.get(url,headers=headers).text
        #转换成json数据
        resp = json.loads(response)
        #提取到max_cursor
        max_cursor = resp['max_cursor']
        #遍历
        for data in resp["aweme_list"]:
            # id值
            video_id = data['aweme_id']
            # 视频简介
            video_title = data['desc']
            # 构造视频网址
            video_url = 'https://www.iesdouyin.com/share/video/{}/?mid=1'
            # 填充内容
            video_douyin = video_url.format(video_id)
            driver = webdriver.Chrome(executable_path=path, options=chrome_options)
            # 打开视频界面
            driver.get(video_douyin)
            # 点击播放按钮
            driver.find_element_by_class_name('play-btn').click()
            time.sleep(2)
            # 将网页源码存放到变量中
            information = driver.page_source
            # 退出
            driver.quit()
            html = etree.HTML(information)
            # 提取视频地址
            video_adress = html.xpath("//video[@class='player']/@src")
            for i in video_adress:
                # 请求视频
                video = requests.get(i, headers=headers).content
                with open('douyin/' + video_title, 'wb') as f:
                    print('正在下载：', video_title)
                    f.write(video)

        #判断停止构造网址的条件
        if max_cursor==0:
            return 1
        else:
            douyin.page_num(max_cursor)
            return url

if __name__ == '__main__':
     douyin = Douyin()
     douyin.page_num(max_cursor=0)