"""Path Spider Middleware Displays the URL path to get to current request."""

from scrapy import log
from scrapy.http import Request


class PathMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        return ext

    def process_spider_input(self, response, spider):
        # if the spider doesn't wish to print paths, then just return
        if not hasattr(spider, 'print_scraping_paths') or not spider.print_scraping_paths:
            return None

        if 'crawling_path' not in response.meta:
            response.meta['crawling_path'] = ''

        formatting_function = spider.print_scraping_paths if spider.print_scraping_paths in [
            'verbose', 'simple'] else 'simple'
        log.msg(format=getattr(self, formatting_function)(
            response.meta['crawling_path']), level=log.DEBUG, spider=spider)
        return None

    def process_spider_output(self, response, result, spider):
        def _add_path(request):
            if isinstance(request, Request):
                # because of some weird anomaly, only strings are possible here?!
                crawling_path = response.meta['crawling_path']
                request.meta['crawling_path'] = crawling_path + \
                    ('>>>' if crawling_path != '' else '') + self.remove_server_path(request.url)
            return True

        if 'crawling_path' not in response.meta:
            response.meta['crawling_path'] = ''

        for request in result:
            _add_path(request)
            yield request

    def remove_server_path(self, url):
        return '/' + '/'.join(url.split('/')[3:])

    def verbose(self, crawling_path):
        paths = crawling_path.split('>>>')
        output = ''
        depth = 0
        for path in paths:
            output += ('|   ' * depth) + '|-- ' + path + '\n'
            depth += 1
        return 'Path for this product:\n' + output

    def simple(self, crawling_path):
        return 'Path for this product: ' + crawling_path.replace('>>>', ' > ')
