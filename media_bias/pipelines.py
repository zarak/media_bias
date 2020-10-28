# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
import logging

from media_bias.models import DeepBlue, db_connect, create_table


class MediaBiasPipeline:
    def process_item(self, item, spider):
        return item

class DeepBluePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        deepblue = DeepBlue()
        deepblue.text = item["text"]

        try:
            session.add(deepblue)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
