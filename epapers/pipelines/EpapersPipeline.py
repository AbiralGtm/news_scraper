# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import GCSFilesStore
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum
import time
import six
from twisted.internet import defer, threads
from firebase_admin import storage


class EpapersPipeline(object):
    def process_item(self, item, spider):
        if "thumb" in item.keys():
            final_images = []
            for image in item['thumb']:
                if image:
                    path = image['path'].split("/")[-1]

                    final_images. \
                        append(spider.settings.get("IMAGE_PREFIX_URL") +r"thumbs/small/{}".format(path))

            item['thumb'] = final_images
        return item


