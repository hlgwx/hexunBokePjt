# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HexunpjtPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",user="root",passwd="root",db="hexun")
    def process_item(self, item, spider):
        for j in range(0,len(item["name"])):
            name=item["name"][j]
            url=item["url"][j]
            hits=item["hits"][j]
            comment=item["comment"][j]
            sql="insert into myhexun (name,url,hits,comment)values('"+name+"','"+url+"','"+hits+"','"+comment+"')"
            self.conn.query(sql)
        return item
    def close_spider(self,spider):
        self.conn.close()
