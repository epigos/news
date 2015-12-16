# -*- coding: utf-8 -*-
import pyquery

from scrapy.spiders import Rule

from src.utils import html_value, html_values
from src.utils.linkextractors import LinkExtractor
from src.pipelines import text_processors
from src.utils.mixins.base import NewsSpider


class SmartNewsSpider(NewsSpider):

    #  do not overide this
    default_smart_spider_settings = {
        'news_callback': 'parse_item_wrapper',
    }

    smart_spider_settings = {}

    def __init__(self):
        self.init_smart_settings()
        super(SmartNewsSpider, self).__init__()

    def init_smart_settings(self):
        if hasattr(self, 'default_smart_spider_settings'):
            default = self.default_smart_spider_settings.copy()
            default.update(self.smart_spider_settings)
            self.smart_spider_settings = default

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


class SmartNewsCrawler(SmartNewsSpider):

    def init_smart_settings(self):
        super(SmartNewsCrawler, self).init_smart_settings()

        if not hasattr(self, 'start_urls'):
            self.start_urls = [self.site_domain]

        if not self.rules:
            self.rules = set(self._parse_smart_rules())

    def _parse_smart_rules(self):
        """ Helper method which will create rules based on a settings provided.
        :return LIST:
        """
        rule_types = ['category', 'pagination', 'news']

        parsed_rules = []
        for rule_type in rule_types:
            parsed_rules += self._parse_smart_rule(rule_type)
        return parsed_rules

    def _parse_smart_rule(self, rule_type):
        """
        :param rule_type STR:
        :return LIST:
        """
        rule_setting = '{}_rules'.format(rule_type)
        rules = to_list(self.smart_spider_settings.get(rule_setting))

        if not rules:
            return None

        allow_setting = '{}_allow'.format(rule_type)
        allow = to_list(self.smart_spider_settings.get(allow_setting, []))

        deny_setting = '{}_deny'.format(rule_type)
        deny = to_list(self.smart_spider_settings.get(deny_setting, []))

        # merge specific type allow setting with the general one
        allow = to_list(self.smart_spider_settings.get('allow', [])) + allow
        # merge specific type deny setting with the general one
        deny = to_list(self.smart_spider_settings.get('deny', [])) + deny

        callback_setting = '{}_callback'.format(rule_type)
        callback = self.smart_spider_settings.get(callback_setting)

        if callback and not isinstance(callback, str):
            raise ValueError('Callback must be type of string!')

        process_links_setting = '_process_{}_link'.format(rule_type)
        process_links = self.smart_spider_settings.get(process_links_setting)
        if process_links and not hasattr(self, process_links):
            process_links = None

        parsed_rules = []
        for rule in rules:
            if isinstance(rule, Rule):
                parsed_rules.append(rule)
            elif isinstance(rule, LinkExtractor):
                rule = Rule(rule, callback=callback,
                            process_links=process_links)
                parsed_rules.append(rule)
            elif isinstance(rule, str):
                # check if no selector char is specified
                selector = None if rule == '*' else rule
                link_extractor = LinkExtractor(selector, allow=allow,
                                               deny=deny)
                rule = Rule(link_extractor, callback=callback,
                            process_links=process_links)
                parsed_rules.append(rule)
        return parsed_rules


def to_list(string_or_list):
    """
    Helper function to convert any object into list.

    :param string_or_list STR OR SET OR LIST:
    :return LIST:
    """
    if isinstance(string_or_list, (list, set)):
        return list(string_or_list)
    return [string_or_list]
