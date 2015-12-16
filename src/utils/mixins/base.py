import traceback

import pyquery

from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem
from scrapy.link import Link

from src.items import NewsItem


class NewsSpider(CrawlSpider):

    """
    Base News Spider which every spider should inherit from.
    """

    def __init__(self):
        super(NewsSpider, self).__init__()

        if not hasattr(self, 'name'):
            raise ValueError('name required')

        if not hasattr(self, 'publisher'):
            raise ValueError('publisher required')

        if not hasattr(self, 'allowed_domains'):
            raise ValueError('allowed_domains required')

        self.log_exceptions = 0
        self.codes = {}
        self.scraped = 0
        # reference to pyquery instance
        self.pq = None

        # default evaluation order for normal fields
        self.field_order = [
            ('link', self.item_link),
            ('code', self.item_code),
            ('title', self.item_title),
            ('content', self.item_content),
            ('category', self.item_category),
            ('source', self.item_source),
            ('date_published', self.item_date_published),
            ('comments', self.item_comments),
            ('images', self.item_images),
            ('publisher', self.item_publisher)
        ]

        # override crawling rules with only one URL?
        if hasattr(self, 'crawl_only_url') and settings.get('DEBUG'):

            class CustomLink(object):

                def __init__(self, url):
                    self.url = url

                def extract_links(self, response):
                    return [Link(url=self.url)]

            self.rules = (
                Rule(CustomLink(self.crawl_only_url),
                     callback='parse_item_wrapper'),
            )
            self._compile_rules()

    def init_pyquery(self, response):
        if response.body:
            return pyquery.PyQuery(response.body)
        return None

    def parse_item(self, response):
        pq = self.init_pyquery(response)
        if pq:
            self.pq = pq.clone()
        # if the deriving class inherits from a mixin then we initialise
        # the mixin in that way
        if hasattr(self, 'init_mixin_response'):
            self.init_mixin_response(response)

        item = NewsItem()

        exception = None
        try:
            for field_name, field_method in self.field_order:
                item[field_name] = field_method(response)
            yield item
        except DropItem as exception:
                # first parse all the variations and raise the Drop
                # exceptions after
                pass
        # override to ensure consistency
        self.pq = pq

        if exception:
            raise exception

    def init_request(self):
        self.log('Initialized ProductSpider')
        return self.initialized()

    def parse_item_wrapper(self, response):
        """Wrapper for parse_item enabling exception notifications."""
        try:
            item = self.parse_item(response)
            return item
        except Exception, ex:
            url = None
            if response.url:
                url = response.url

            if settings.get('DEBUG'):
                self.log('Spider Exception trying to parse: ' + url)
                self.log(str(type(ex)) + " - " + traceback.format_exc())
            if not isinstance(ex, DropItem):
                self.log_exceptions += 1
            raise
        finally:
            self.scraped += 1

    def start_requests(self):
        self._init()
        return super(NewsSpider, self).start_requests()

    def _init(self):
        """
        Initializes spider.
        """
        self.scraped = 0

    def _conditional_override(self, method_name, *args, **kwargs):
        """
            Checks whether `method_name` exists in a super class of
            the current class. If so
            call it with the given arguments in `*args`.
            If the method does not exist return None.

            If a child class inherits from another class which
            implements those methods then it will use those instead.
        """
        if not hasattr(super(NewsSpider, self), method_name):
            return None
        else:
            method = getattr(super(NewsSpider, self), method_name)
            return method(*args, **kwargs)

    def item_link(self, response):
        return response.url

    def item_code(self, response):
        """Stub implementation of item_code."""
        return self._conditional_override('item_code', response)

    def item_title(self, response):
        """Stub implementation of item_title."""
        return self._conditional_override('item_title', response)

    def item_content(self, response):
        """Stub implementation of item_content."""
        return self._conditional_override('item_content', response)

    def item_category(self, response):
        """Stub implementation of item_category."""
        return self._conditional_override('item_category', response)

    def item_source(self, response):
        """Stub implementation of item_source."""
        return self._conditional_override('item_source', response)

    def item_date_published(self, response):
        """Stub implementation of item_date_published."""
        return self._conditional_override('item_date_published', response)

    def item_comments(self, response):
        """Stub implementation of item_comments."""
        return self._conditional_override('item_comments', response)

    def item_images(self, response):
        """Stub implementation of item_images."""
        return self._conditional_override('item_images', response)

    def item_publisher(self, response):
        """Stub implementation of item_publisher."""
        publisher = self._conditional_override('item_publisher', response)
        if publisher:
            return publisher
        return self.publisher

    def build_item_code(self, product_code):
        """Used to populate self.codes."""
        return ('{0}'.format(product_code)).lower()
