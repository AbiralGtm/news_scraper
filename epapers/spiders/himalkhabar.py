# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from dateutil.parser import parser
import datetime


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class HimalkhabarSpider(scrapy.Spider):
    name = 'himalkhabar'
    allowed_domains = ['himalkhabar.com/epaper']
    start_urls = ['http://himalkhabar.com/epaper/']

    def parse(self, response):
        cred = credentials.Certificate('nepali-epapers-firebase-adminsdk-x93g2-6820548d04.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        url= response.xpath('//iframe/@src').extract_first()
        type = 'weekly'
        name = 'Himal Khabar'
        name_np = 'हिमाल खबर'
        epaper_id = 'himalkhabar'
        contents = {
            'name': name,
            'name_np':name_np,
            'publication':'Himal Khabar',
            'publication_other':'हिमाल खबर',
            'type':type,
            'epaper_id':epaper_id
        }

        yield scrapy.Request(url = url , callback  = self.epapers_details,dont_filter=True, meta = {'contents': contents} )
    def epapers_details(self,response):

        contents = response.meta['contents'];
        images = response.xpath('//div[@class="my-gallery"]/figure/a/@href').extract()
        thumb = response.xpath('//div[@class="my-gallery"]/figure/a/@href').extract()
        cover_img = images[0]
        num_pages = len(images)
        date_extract = response.xpath('//p/i/text()').extract_first()
        # date_parse = parse(date_extract)
        # date = datetime.datetime.strptime(date_extract, '%Y-%m-%d')
        date="2075-4554-454"

        id_segment = response.url.rpartition('/')
        id = id_segment[2]
        epaper_id = contents['epaper_id']

        epapers_details = {
            'id':id,
            'cover_img':cover_img,
            'thumb':thumb,
            'images':images,
            'num_pages':num_pages,
            'name': contents['name'],
            'name_np':contents['name_np'],
            'date':date,
            'publication':contents['publication'],
            'publication_other':contents['publication_other'],
            'type':contents['type'],
            'num_reads':0,
            'created_date':firestore.SERVER_TIMESTAMP
        }
        epaper_home = {
            'id':epaper_id,
            'cover_img':cover_img,
            'latest_date':date,
            'modified_date':firestore.SERVER_TIMESTAMP,
            'name':contents['name'],
            'publication':contents['publication'],
            'publication_other':contents['publication_other'],
            'thumb_url':cover_img,
            'title':contents['name'],
            'title_other':contents['name_np'],
            'type':contents['type']
        }
        doc_ref_epaper_home = self.db.collection(u'epapers_home').document(epaper_id).set(epaper_home)
        doc_ref = self.db.collection(u'epapers').document(epaper_id +'_'+ date).set(epapers_details)
        yield epapers_details
        return epaper_home

