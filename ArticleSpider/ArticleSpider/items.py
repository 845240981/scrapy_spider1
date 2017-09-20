# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst
from scrapy.loader import ItemLoader
import re

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass





class Defaultloader(ItemLoader):

    default_output_processor=TakeFirst()





class ArticleItem(scrapy.Item):

    def add_not(self,value):

        return value+'not'



    def get_nums(nums):

        match_re = re.match(".*?(\d+).*", nums)
        if match_re:
            nums = int(match_re.group(1))
        else:
            nums = 0
        return nums



    def date_convert(time):
        try:
            create_date=datetime.datetime.strptime(time,'%Y/%m/%d').date()
        except Exception as e :
            create_date=datetime.datetime.now().date()

        return create_date



    def return_value(value):
        return value


    title=scrapy.Field(
        input_processor =MapCompose(lambda x :x+'ok'),
        output_processor = TakeFirst()
    )
    create_date = scrapy.Field(input_processor = MapCompose(date_convert),
        output_processor= TakeFirst())
    url=scrapy.Field()
    url_id=scrapy.Field()
    #content =scrapy.Field()
    image =scrapy.Field( output_processor= MapCompose(return_value))####cover before default_output function
    image_path=scrapy.Field()

    p_nums=scrapy.Field(input_processor =MapCompose(get_nums))
    c_nums = scrapy.Field(input_processor =MapCompose(get_nums))
    f_nums = scrapy.Field(input_processor =MapCompose(get_nums))
    tags = scrapy.Field()


class HuayingItem(scrapy.Item):

    def jdhandle(value):
        value= value.replace('\r','')
        value= value.replace('\n','').strip()

        return value




    con_name = scrapy.Field()
    con_type = scrapy.Field()
    con_zhiye = scrapy.Field()
    con_xinshui = scrapy.Field()
    con_jd = scrapy.Field(input_processor=MapCompose(jdhandle))
    con_ar = scrapy.Field()

