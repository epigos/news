# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import pprint

from scrapy.item import Field, Item


class NewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    title = Field()
    content = Field()
    category = Field()
    comments = Field()
    source = Field()
    images = Field()
    date_published = Field()
    publisher = Field()

    def __repr__(self):
        return "\n%s\n" % pprint.pformat(dict(self))

    def __str__(self):
        return "\n%s\n" % pprint.pformat(dict(self))
