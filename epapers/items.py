# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EpapersItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    cover_img = scrapy.Field()
    thumb = scrapy.Field()
    images = scrapy.Field()
    num_pages = scrapy.Field()
    name = scrapy.Field()
    name_np = scrapy.Field()
    date = scrapy.Field()
    publication = scrapy.Field()
    publication_other = scrapy.Field()
    type = scrapy.Field()
    num_reads = scrapy.Field()
    created_date = scrapy.Field()
    pass
