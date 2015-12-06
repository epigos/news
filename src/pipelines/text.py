from scrapy.loader.processors import Compose

from .text_processors import (
    enforce_unicode, capitalisation, append_fullstop, capitalise_sentences,
    normalise_internal_space, remove_empty_sentences, strip_tags
)


# transformations applied to all retailers. Each transformer takes
# one argument, the input text
all_spiders = {
    'name': [enforce_unicode,
             unicode.strip,
             capitalisation,
             normalise_internal_space,
             strip_tags],
    'content': [enforce_unicode,
                unicode.strip,
                strip_tags,
                append_fullstop,
                normalise_internal_space,
                capitalise_sentences,
                remove_empty_sentences
                ],
}


class TextTransformationPipeline(object):

    """Applies a number of text transformation to each retailer and item
    in the pipeline."""

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        return ext

    def __init__(self, all_spiders=all_spiders):
        self.all_spiders = all_spiders

    def _process(self, item, mapping, logger, with_item=False):
        for field, transform in mapping.iteritems():
            if field in item:
                if item[field]:  # Only transforming non empty fields
                    transformer = Compose(*transform)
                    item[field] = transformer(item[field])

        return item

    def process_item(self, item, spider):
        item = self._process(item, self.all_spiders, spider.log)

        if hasattr(spider, 'text_filters'):
            item = self._process(item, spider.text_filters, spider.log)

        return item

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.all_spiders)
