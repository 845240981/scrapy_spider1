# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
    header = {

        "Host": "www.zhihu.com",
        'User-Agent': agent
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin',headers=self.header, callback=self.prepare_login)]




    def prepare_login(self,response):
        text =response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', text, re.DOTALL)

        if match_obj:
            xsrf = (match_obj.group(1))

            post_url = 'https://www.zhihu.com/login/email'
            post_data = {
                '_xsrf':xsrf,
                'phone_num': '15817302742',
                'password': 'pk11215717',
                'captcha':''
            }

        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"

        return [scrapy.Request(url=captcha_url,headers=self.header,meta={'post_data':post_data},callback=self.login_in)]






    def login_in(self,response):
        with open('captcha.jpg','wb') as f:
            f.write(response.body)
            f.close()
        try:
            from PIL import Image
            piture = Image.open('captcha.jpg')
            piture.show()
            piture.close()
        except:
            print('fail to load yanzheng')

        captcha = input('请输入你的验证码:   ')

        post_data= response.meta.get('post_data')
        post_data['captcha']=captcha
        post_url= 'https://www.zhihu.com/login/phone_num'



        return [scrapy.FormRequest(
                url=post_url,
                headers=self.header,
                formdata =post_data,
                callback=self.check_login
                )]




    def check_login(self,response):
        print(response.text)
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        else:
            print('fail to login')




