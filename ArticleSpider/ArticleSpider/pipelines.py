# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import time


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):

        return item

class JsonfilePipeline(object):
    def __init__(self):
        self.file = open('jssa.txt','a',encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item
    def spider_close(self,spider):
        self.file.close()

class JsonEXporterPipleline(object):
    def __init__(self):
        self.file= open('1.json','wb')###并不太懂这个为啥是wb
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn=MySQLdb.connect('192.168.0.113','root','pk123456','article_databases',charset='utf8',use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self, item, spider):

        try:
            insert_sql = """
                        insert into ok(title, url, create_date, f_nums)
                        VALUES (%s, %s, %s, %s)
                    """
            self.cursor.execute(insert_sql, (item["title"],
                                             item["url"],
                                             item["create_date"],
                                             item["f_nums"]))
            self.conn.commit()
        except Exception as e:
            time.sleep(10000)

            return item

class mysqlPipeline(object):
    def __init__(self):
        self.conn=MySQLdb.connect('172.30.110.100','root','pk123456','article_databases',charset='utf8',use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self,item,spider):

        try:
            insert_sql = """
                            insert into xiaozhao(con_name,con_type,con_zhiye,con_xinshui,con_jd,con_ar)
                            VALUES (%s,%s,%s,%s,%s,%s)
                """
            self.cursor.execute(insert_sql, (item['con_name'],
                                                item['con_type'],
                                                item['con_zhiye'],
                                                item['con_xinshui'],
                                                item['con_jd'],

                                                item['con_ar']))
        except Exception as e:

            self.conn.commit()






class MysqlyibuPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool



    @classmethod
    def from_settings(cls,settings):
        dbparms =dict(
            host = settings["MYSQL_HOST"],
            db = settings['MYSQL_DANAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset = 'utf8',

            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparms)
        return cls(dbpool)






    def process_item(self, item, spider):
        query =self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self, failure,item,spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                           insert into ok_copy(title, url, create_date, f_nums)
                           VALUES (%s, %s, %s, %s)
                       """

        cursor.execute(insert_sql, (item["title"],
                                         item["url"],
                                         item["create_date"],
                                         item["f_nums"]))






class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'image' in item:###item is similar to dict
            for ok , value in results:
                image_path =value['path']
                item['image_path']=image_path
            return item


