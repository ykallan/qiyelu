# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
pymysql.install_as_MySQLdb()


class QiyeluPipeline(object):

    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.cursor.execute('''INSERT INTO qyl(com_name, cont_name, dianhua, chuanzhen, mobile, address) VALUES(%s, %s, %s, %s, %s, %s)''',
                            (item['com_name'], item['cont_name'], item['dianhua'], item['chuanzhen'], item['mobile'], item['address']))
        self.conn.commit()
        return item

        # item['com_name'] = com_name
        # item['cont_name'] = cont_name
        # item['dianhua'] = dianhua
        # item['chuanzhen'] = chuanzhen
        # item['mobile'] = mobile
        # item['address'] = address

    def close(self, spider):

        pass
