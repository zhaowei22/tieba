# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class BaiduPipeline(object):
    InsertSql = '''
                    insert into tieba
                    (title,tag,name,user_num,topic_num,description,img,url)
                    values
                    ('{title}','{tag}','{name}','{user_num}','{topic_num}','{description}','{img}','{url}')
                '''

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        sql_syntax = self.InsertSql.format(
            title=pymysql.escape_string(item.get('title')),
            tag=pymysql.escape_string(item.get('tag')),
            name=pymysql.escape_string(item.get('name')),
            user_num=pymysql.escape_string(item.get('user_num')),
            topic_num=pymysql.escape_string(item.get('topic_num')),
            description=pymysql.escape_string(item.get('description')),
            img=pymysql.escape_string(item.get('img')),
            url=pymysql.escape_string(item.get('url')))
        self.cursor.execute(sql_syntax)
        
        return item

    # def _conditional_insert(self, tx, item):
    #     # print item['name']
    #     sql = "insert into testpictures(name,url) values(%s,%s)"
    #     params = (item["name"], item["url"])
    #     tx.execute(sql, params)

    # def _handle_error(self, failue, item, spider):
    #     # 错误处理方法
    #     print failue

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
