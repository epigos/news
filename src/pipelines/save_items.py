# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class SaveItemsPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        return ext

    # def __init__(self, *args, **kwargs):
    #     self.processed_items = 0
    #     dispatcher.connect(self.spider_opened, signals.spider_opened)
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_opened(self, spider):
    #     create_quarantine_database(spider)

    # def spider_closed(self, spider):
    #     get_quarantine_database().finish_database(spider)

    # def process_item(self, item, spider):
    #     get_quarantine_database().save_item(item)
    #     return item