import pyquery

from scrapy.linkextractors.sgml import SgmlLinkExtractor


class LinkExtractor(SgmlLinkExtractor):

    def __init__(self, selector=None, type='css', *args, **kwargs):
        if selector:
            if type not in ['css', 'xpath']:
                raise Exception('Selector type not supported.')
            if type == 'xpath':
                kwargs['restrict_xpaths'] = selector
            else:
                kwargs['restrict_xpaths'] = pyquery.PyQuery('a')._css_to_xpath(selector)
        SgmlLinkExtractor.__init__(self, *args, **kwargs)
