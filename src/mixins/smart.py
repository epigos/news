# -*- coding: utf-8 -*-
import pyquery

from src.utils import html_value, html_values
from src.pipelines import text_processors
from src.mixins.base import NewsSpider


class SmartNewsSpider(NewsSpider):

    smart_spider_settings = {}

    def init_pyquery(self, response):
        if response.body:
            pq = pyquery.PyQuery(response.body)
            return pq
        return None

    def item_code(self, response):
        if 'item_code' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_code')
        return super(SmartNewsSpider, self).item_code(response)

    def item_title(self, response):
        if 'item_title' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_title')
        return super(SmartNewsSpider, self).item_title(response)

    def item_content(self, response):
        if 'item_content' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_content')
        return super(SmartNewsSpider, self).item_content(response)

    def item_category(self, response):
        if 'item_category' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_category')
        return super(SmartNewsSpider, self).item_category(response)

    def item_source(self, response):
        if 'item_source' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_source')
        return super(SmartNewsSpider, self).item_source(response)

    def item_date_published(self, response):
        if 'item_date_published' in self.smart_spider_settings:
            return self._parse_smart_item_value(
                response, 'item_date_published')
        return super(SmartNewsSpider, self).item_date_published(response)

    def item_comments(self, response):
        if 'item_comments' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_comments')
        return super(SmartNewsSpider, self).item_comments(response)

    def item_images(self, response):
        if 'item_images' in self.smart_spider_settings:
            return self._parse_smart_item_values(response, 'item_images')
        return super(SmartNewsSpider, self).item_images(response)

    def item_publisher(self, response):
        if 'item_publisher' in self.smart_spider_settings:
            return self._parse_smart_item_value(response, 'item_publisher')
        return super(SmartNewsSpider, self).item_publisher(response)

    def _parse_smart_item_value(self, response, setting, **format_attr):
        selectors = self.smart_spider_settings.get(setting)
        value = html_value(response.body, selectors, **format_attr)
        return text_processors.fix_text(value) if value else None

    def _parse_smart_item_values(self, response, setting, **format_attr):
        selectors = self.smart_spider_settings.get(setting)
        return html_values(response.body, selectors, **format_attr)
