# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from ArticleSpider.items import ArticleItem
import re
from ArticleSpider.utils.common import  get_md5
import datetime
from scrapy.loader import  ItemLoader
from scrapy.loader.processors import MapCompose

class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        post_nodes=response.css(".grid-8 .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url), meta={'image':image}, callback=self.parse_detail)
            ##因为异步机制,只用函数名就可以,自己调用
            print(post_url)
        next_url =response.css(".next.page-numbers::attr(href)").extract_first("")
        print(next_url)
        if next_url:
            print(next_url)
            #yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)


    def parse_detail(self, response):
        article_item = ArticleItem()



        image=response.meta.get('image','')
        #print(image)
        #title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        #create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()"
                                     #).extract()[0].strip().replace("·",'')
        #p_nums = response.css(".vote-post-up h10::text").extract()[0]
        #fav_nums = response.css(".bookmark-btn::text").extract()[0]
        #match_re = re.match(".*?(\d+).*", fav_nums)
        #if match_re:
            #f_nums = int(match_re.group(1))
        #else:
            #f_nums = 0

        #comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        #match_re = re.match(".*?(\d+).*", comment_nums)
        #if match_re:
            #c_nums = int(match_re.group(1))
        #else:
            #c_nums = 0
        #content = response.xpath("//div[@class='entry']").extract()[0]


        #tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        #tag_list = list(set(tag_list))
        #tag_list = [ element for element in tag_list if not element.strip().endswith('评论')]


       # article_item['title'] = title
       # article_item['url']= response.url
        #try:
            #create_date=datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
       # except Exception as e :
           # create_date=datetime.datetime.now().date()

        #article_item['create_date']= create_date
        #article_item['image']= [image]
        #article_item['content']= content
        #article_item['p_nums']= p_nums
        #article_item['c_nums']= c_nums
       # article_item['f_nums']= f_nums
        #article_item['url_id'] = get_md5(response.url)
        #article_item['tags']=tag_list
        #print('ok')



       # yield article_item
        item_loader =AticlrItemloader(item=ArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("image", [image])
        item_loader.add_css("p_nums", ".vote-post-up h10::text")
        item_loader.add_css("c_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("f_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")



        # 调用这个方法来对规则进行解析生成item对象
        article_item = item_loader.load_item()
        yield article_item






