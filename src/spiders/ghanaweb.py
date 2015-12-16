
import re

from src.utils.mixins.smart import SmartNewsCrawler

from src.pipelines import text_processors


class GhanawebSpider(SmartNewsCrawler):

    name = 'ghanaweb.com'
    publisher = "GhanaWeb"
    allowed_domains = ['ghanaweb.com']

    start_urls = ['http://www.ghanaweb.com/GhanaHomePage/NewsArchive/browse.archive.php']

    smart_spider_settings = {
        'news_rules': '#medsection1 > ul li',
        'category_rules': ['#month-breakdown ul li', '#year-breakdown ul li'],
        'item_code': '#topnav b',
        'item_title': '#medsection1 > h1',
        'item_content': '#medsection1 > p:nth-child(8)',
        'item_images': ('#medsection1 .article-image img', 'src'),
        'item_source': '#medsection1 > p.floatRight',
        'item_category': '#topnav > a:nth-child(2)',
        'item_date_published': '#date'
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

    # crawl_only_url = 'http://www.ghanaweb.com/GhanaHomePage/crime/Drugs-are-being-sold-by-pupils-in-Sunyani-West-District-400171'

    def item_comments(self, response):
        comments = self.pq('#medsection1 .option-bar > p.last > a').text()
        match = re.search(r'\d+', comments)
        if match:
            return int(match.group(0))
