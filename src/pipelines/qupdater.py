# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from src.utils.database.quarantine import QuarantineDatabase


class QuarantinePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        return ext

    def __init__(self, *args, **kwargs):
        self.processed_items = 0
        self.db = QuarantineDatabase()
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.db.create_conn(spider)

    def spider_closed(self, spider):
        spider.log('Closing scrape for spider: {}'.format(spider.publisher))

    def process_item(self, item, spider):
        self.db.save_item(item)
        return item
