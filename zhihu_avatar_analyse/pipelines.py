# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings
# then use settings.get('MONGO_DATABASE') to get setting fields


class MongoPipeline(object):
  collection = "users"

  def __init__(self, uri, port, dbname):
    self.mongo_uri = uri
    self.mongo_port = port
    self.db_name = dbname

  @classmethod
  def from_crawler(cls, crawler):
    uri = crawler.settings.get("MONGO_URI")
    return cls(
      uri.get("MONGO_HOST"),
      uri.get("MONGO_PORT"),
      crawler.settings.get("MONGO_DATABASE").get("DB_NAME"))

  def open_spider(self, spider):
    self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
    print(">>>> conect to db : {}:{}/{}".format(
      self.mongo_uri, self.mongo_port, self.db_name))
    self.db = self.client[self.db_name]

  def close_spider(self, spider):
    self.client.close()

  def process_item(self, item, spider):
    self.db[self.collection].update(
      {"url_token": item["url_token"]},
      {"$set": dict(item)}, True) # update insert

    return item
