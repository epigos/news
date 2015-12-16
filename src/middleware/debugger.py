"""Debugger Middleware A spider debugging friend."""

import json

from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher


class DebuggerMiddleware(object):
    body_text = []
    items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        return ext

    def __init__(self):
        dispatcher.connect(self._item_scraped, signals.item_scraped)
        dispatcher.connect(self._spider_closed, signals.spider_closed)

    def process_spider_input(self, response, spider):
        # only append text if debugger is set to true, this is useful for when we don't know
        # why scraping for some runs isn't initialized. For instance, most runs run OK, but some
        # runs just don't, even if there is not error in the response.
        if hasattr(spider, 'debugger') and spider.debugger:
            self.body_text.append({
                'response.url': response.url,
                'body': response.body.strip()
            })

    def _item_scraped(self, item, response, spider):
        self.items_scraped += 1

    def _spider_closed(self, spider, reason):
        # if 0 items are scraped make the log, otherwise don't, because the file could get really
        # huge and messy
        if self.items_scraped < 1:
            log.msg('Spider debugger dump: %s' % json.dumps(self.body_text, indent=4))
