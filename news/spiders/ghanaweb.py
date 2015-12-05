
from scrapy.contrib.spiders import Rule

from news.utils.linkextractors import LinkExtractor
from news.mixins.base import NewsSpider


class GhanawebSpider(NewsSpider):

    name = 'ghanaweb.com'
    publisher = "GhanaWeb"
    allowed_domains = ['ghanaweb.com']
    start_urls = ['http://www.ghanaweb.com/']

    rules = (
        Rule(LinkExtractor('#mainnavinner')),
        Rule(LinkExtractor('.date-breakout'), callback='parse_item_wrapper')
    )

    crawl_only_url = 'http://www.ghanaweb.com/GhanaHomePage/health/National-Sanitation-Day-Exercise-waning-398741'
