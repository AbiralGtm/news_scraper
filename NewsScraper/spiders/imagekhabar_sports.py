# -*- coding: utf-8 -*-
import datetime
import scrapy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from scrapy import Request





class ImagekhabarSportsSpider(scrapy.Spider):
    name = 'imagekhabar_sports'
    allowed_domains = ['imagekhabar.com']
    start_urls = ['http://imagekhabar.com/category/8/sports']

    def parse(self, response):
        cred = credentials.Certificate('nepali-epapers-firebase-adminsdk-x93g2-6820548d04.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        news_item_list = response.xpath('//*[@class="row"]/div[@class="col-xl-12 col-lg-6 col-md-6 col-sm-12 mt-30"]')
        category = "sports"
        site_name="imagekhabar.com"
        author="anonymous"
        num_reads=0
        for news in news_item_list:
            thumb = news.xpath('.//img[@class="img-fluid"]/@src').extract()[0]
            news_url = news.xpath('.//h3/a/@href').extract()[0]
            url = response.urljoin(news_url)
            self.first_contents = {'thumb': thumb,
                                      'category': category,
                                      'site_name':site_name,
                                      'author':author,
                                      'num_reads':num_reads}
            url = response.urljoin(news_url)
            final_content = Request(url, callback=self.get_items_details)
            yield final_content

    def get_items_details(self,response):
        title = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]/h1[@class="title-semibold-dark size-c30"]/text()').extract_first()
        id= "imgkbr-"+response.url.split('/')[-2]
        id_original = response.url.split('/')[-2]
        desc_original = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]').extract_first()
        desc_formatted_scrape = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/p').extract()
        desc_formatted=" ".join(desc_formatted_scrape)
        original_content = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]')
        images = original_content.xpath('.//img/@src').extract()
        paragraphs = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/p/text()').extract()
        all_text =" ".join(paragraphs)
        descr_split = all_text.split('।')
        purnabiram = '।'
        desc_list = [x + purnabiram for x in descr_split]
        tags= title.split(' ')
        published_date = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]/ul[@class="post-info-dark mb-30"]/li/text()').extract()[2]
        get_items_details = {
            'id':id,
            'id_original': int(id_original),
            'news_url':response.url,
            'category': self.first_contents['category'],
            'site_name':self.first_contents['site_name'],
            'title':title,
            'desc_original':desc_original,
            'desc_formatted':desc_formatted,
            'desc_list':desc_list,
            'images':images,
            'thumb_url': self.first_contents['thumb'],
            'published_date':published_date,
            'created_date': datetime.datetime.now(),
            'author':self.first_contents['author'],
            'tags':tags,
            'num_reads':self.first_contents['num_reads']
        }
        doc_ref = self.db.collection(u'news_feeds').document(get_items_details['id']).set(get_items_details)
        return get_items_details
