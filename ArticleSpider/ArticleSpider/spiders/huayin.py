# -*- coding: utf-8 -*-
import scrapy
import itertools
from scrapy.http import Request
from urllib import parse
from  ArticleSpider.items import HuayingItem,Defaultloader
from ArticleSpider.utils.common import convert


class HuayinSpider(scrapy.Spider):
    i=1
    name = 'huayin'
    allowed_domains = ['www.chinahr.com']
    start_urls = ['http://www.chinahr.com/sou/?city=25%2C292&industrys=1100%2C11006&companyType=0&degree=-1&refreshTime=-1&workAge=-1']

    def parse(self, response):
        conjob_urls = response.css('.resultList .jobList .e1 a ::attr(href)').extract()
        for job_url in conjob_urls:
            print(response.url)
            print(job_url)
            yield Request(url=parse.urljoin(response.url,job_url),callback=self.parse_datail)
        next_url=response.css(".pageList a::attr(href)").extract()[-1]
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_datail(self,response):
        item_loader= Defaultloader(item=HuayingItem(),response=response)

        con_type = response.css(".company_intro span ::text ").extract()
        con_type = convert(con_type)
        item_loader.add_value('con_type',con_type)

        item_loader.add_css('con_name',".company_intro h4 a ::text ")
        con_name=response.css(".company_intro h4 a ::text ").extract_first()
        if not con_name:
            con_name='break name'
        item_loader.add_value('con_name', con_name)



        item_loader.add_css('con_zhiye',".job_name::text")
        item_loader.add_css('con_xinshui',".job_price::text")

        con_jds = response.css(".job_intro_info::text").extract()
        con_jd = convert(con_jds)
        item_loader.add_value('con_jd',con_jd)

        item_loader.add_css('con_ar',".job_require   .job_loc ::text")

        ariticle_item = item_loader.load_item()

        yield ariticle_item
        #con_type= response.css(".company_intro span ::text ").extract()
        #con_name =  response.css(".company_intro h4 a ::text ").extract_first()
        #con_zr = response.css(".job_name::text").extract_first()
        #con_xinshui =  response.css(".job_price::text").extract_first()
        #con_jds = response.css(".job_intro_info::text").extract()
        #con_jd = "".join(itertools.chain(*con_jds))
        #con_ar = response.css(".job_require   .job_loc ::text").extract_first()
        #print(con_ar)
       # pass

