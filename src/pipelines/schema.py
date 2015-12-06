import jsonschema


class SchemaValidationException(Exception):
    pass


class DuplicateValidationException(SchemaValidationException):
    pass


class Validator(object):

    def __init__(self):
        self.item_schema = self._load_schema()
        # validate schema itself
        try:
            jsonschema.Draft4Validator.check_schema(self.item_schema)
        except jsonschema.SchemaError, e:
            # This is a critical error and needs to get noticed asap
            print e.__dict__
            raise RuntimeError(e)
        checker = jsonschema.FormatChecker()
        self.json_validator = jsonschema.Draft4Validator(
            self.item_schema, format_checker=checker)

    def validate(self, spider, item):
        new_item = dict(item).copy()
        self.json_validator.validate(new_item)

    def _load_schema(self):
        return {
            'type': 'object',
            'properties': {
                'link': {'type': 'string', 'minLength:': 1},
                'content': {'type': 'string'},
                'title': {'type': 'string', 'minLength:': 1},
                'code': {'type': 'string'},
                'category': {'type': 'string'},
                'comments': {'type': 'number'},
                'source': {'type': 'string'},
                'images': {'type': 'array', 'uniqueItems': True},
                'date_published': {'type': 'string'},
                'publisher': {'type': 'string'}
            },
            'required': ['code', 'link', 'content', 'title', 'images']
        }


class SchemaValidationPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        return ext

    def __init__(self):
        self.validator = Validator()

    def process_item(self, item, spider):
        spider.log('Schema validation')

        # preprocess item and validate against schema
        try:
            self.validator.validate(spider, item)
        except jsonschema.ValidationError, exn:
            spider.log('++ Schema Exception details. Path %s, Validator %s, Message %s, Cause %s' %
                       (exn.path, exn.message, exn.validator, exn.cause))

            spider.crawler.stats.inc_value('validation_exceptions')

            raise SchemaValidationException(exn)

        # add code
        self._add_primary_key(item, spider)

        # item passed validation
        return item

    def _add_primary_key(self, item, spider):
        """Adds primary key of item to a given spider. """
        code = spider.build_item_code(product_code=item['code'])
        item_link = item.get('link', '')

        if code in spider.codes:
            spider.crawler.stats.inc_value('duplicate_exceptions')

            raise DuplicateValidationException(
                "Duplicate product with code: '%s'"
                "original_link: '%s' duplicated_link: '%s'",
                item['code'],
                spider.codes[code],
                item_link
            )
        else:
            spider.codes[code] = item_link
