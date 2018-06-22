# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class CalenderPipeline(object):

    def __init__(self):
        self.filename = open("calender.json","w");

        self.calenderList = [];

    def process_item(self, item, spider):
        dictContent = dict(item);
        text = json.dumps(dictContent, ensure_ascii=False) + '\n';
        # self.calenderList.append(dictContent);
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()
