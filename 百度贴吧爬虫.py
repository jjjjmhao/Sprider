import requests
from lxml import etree
import re
import os

class TieBa:
    def __init__(self,a):
        self.base_url = "https://tieba.baidu.com/f"
        self.para = {'kw':a}

    def send_request(self,url,para={}):
        response = requests.get(url,params=para)
        return response.content

    def write_file(self,data,name):
        print(name)
        #image_path = 'img\\' + name
        with open('img/','wb') as f:
            f.write(data)

    def parse_data(self,data,rule):
        element = etree.HTML(data)
        result = element.xpath(rule)
        return result

    # def change_title(title):
    #     pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")
    #     new_title = re.sub(pattern,"_",title)
    #     return new_title

    def run(self):
        list_data = self.send_request(self.base_url,self.para)
        detail_rule = '//div[@class="t_con cleafix"]/div/div/div/a/@href'
        detail_url_list = self.parse_data(list_data,detail_rule)
        for detail in detail_url_list:
            detail_url = "https://tieba.baidu.com/" + detail
            detail_data = self.send_request(detail_url)
            image_rule = '//img[@class="BDE_Image"]/@src'
            image_url_list = self.parse_data(detail_data, image_rule)

            for image_url in image_url_list:
                image_data = self.send_request(image_url)
                image_name = image_url[-15:]
                self.write_file(image_data, image_name)


if __name__ == '__main__':
    a = input('请输入吧名：')
    tieba = TieBa(a)
    tieba.run()

