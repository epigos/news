
import re

from scrapy.spiders import Rule

from src.utils.linkextractors import LinkExtractor
from src.mixins.smart import SmartNewsSpider

from src.pipelines import text_processors


class GhanawebSpider(SmartNewsSpider):

    name = 'ghanaweb.com'
    publisher = "GhanaWeb"
    allowed_domains = ['ghanaweb.com']

    start_urls = ['http://www.ghanaweb.com/GhanaHomePage/NewsArchive/browse.archive.php']

    rules = (
        Rule(LinkExtractor('#month-breakdown ul li')),
        Rule(LinkExtractor('#year-breakdown ul li')),
        Rule(LinkExtractor('#medsection1 > ul li'),
             callback='parse_item_wrapper')
    )

    smart_spider_settings = {
        'item_code': '#topnav b',
        'item_title': '#medsection1 > h1',
        'item_content': '#medsection1 > p:nth-child(8)',
        'item_images': ('#medsection1 .article-image img', 'src'),
        'item_source': '#medsection1 > p.floatRight',
        'item_category': '#topnav > a:nth-child(2)',
        'item_date_published': '#topnav > a:nth-child(3)'
    }

    text_filters = {
        'code': [
            text_processors.remove_string('Article '),
        ],
        'source': [
            text_processors.remove_string('Source:'),
            text_processors.normalise_internal_space
        ]
    }

    # crawl_only_url = 'http://www.ghanaweb.com/GhanaHomePage/NewsArchive/Another-NPP-Big-Fish-In-Drug-Deal-158848'

    def item_comments(self, response):
        comments = self.pq('#medsection1 .option-bar > p.last > a').text()
        match = re.search(r'\d+', comments)
        if match:
            return int(match.group(0))
