import re
from dateutil.parser import parse as date_parser

from scrapy.conf import settings

from pymongo import MongoClient


def get_quarantine_database(spider):
    qr = QuarantineDatabase()
    return qr.create_conn(spider)


class QuarantineDatabase(object):

    def __init__(self):
        self.database = None
        self.db_uri = settings['MONGODB']
        self.uniq_key = settings['MONGODB_UNIQ_KEY']
        self.safe = bool(settings['DEBUG'])

    def create_conn(self, spider):
        client = MongoClient(self.db_uri)
        dbname = re.sub(r'\W+', '', spider.name)
        self.database = client[dbname]
        # self.database.items.ensure_index([('code', 1)], unique=True)

    def save_exception(self, e):
        errors = self.database.errors
        errors.insert(e)

    def save_item(self, item):
        items = self.database.items
        item = dict(item)
        item['date_published'] = date_parser(item['date_published'])
        items.update_one(
            {self.uniq_key: item[self.uniq_key]},
            {'$set': item},
            upsert=True, bypass_document_validation=self.safe
        )
