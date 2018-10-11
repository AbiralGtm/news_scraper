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

        yield scrapy.Request(url = url , callback  = self.data, meta = {'contents': contents} )
    def data(self,response):
        data = []
        contents = response.meta['contents'];
        images = response.xpath('//div[@class="my-gallery"]/figure/img/@src').extract()
        cover_img = images[0]
        num_pages = len(images)
        date_extract = response.xpath('//p/i/text()').extract_first()
        date_parse = parse(date_extract)
        date = datetime.datetime.strptime(date_parse, '%Y-%m-%d')

        date_other = datetime.datetime(date_other_get)
        id_segment = response.url.rpartition('/')
        id = id_segment[2]
        epaper_id = contents['epaper_id']

        data['id'] = id
        data['cover_img'] = cover_img
        data['thumb'] =images
        data['images']=images
        data['num_pages']= num_pages
        data['name']= contents['name']
        data['name_np']= contents['name_np']
        data['date']= date
        data['publication']= contents['publication']
        data['publication_other']= contents['publication_other']
        data['type'] = contents['type']
        data['num_reads'] = 0
        data['created_date'] = firestore.SERVER_TIMESTAMP

        epaper_home = {
            'id':epaper_id,
            'cover_img':cover_img,
            'latest_date':date,
            'latest_date_other': date_other,
            'modified_date':firestore.SERVER_TIMESTAMP,
            'name':contents['name'],
            'publication':contents['publication'],
            'publication_other':contents['publication_other'],
            'thumb_url':cover_img,
            'title':contents['name'],
            'title_other':contents['name_np'],
            'type':type
        }
        doc_ref_epaper_home = self.db.collection(u'epapers_home').document(epaper_id).set(epaper_home)
        doc_ref = self.db.collection(u'epapers').document(epaper_id +'_'+ date_parse).set(data)
        yield data
        return data
        return epaper_home

