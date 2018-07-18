# -*- coding: utf-8 -*-
import datetime
import scrapy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from scrapy.http import Request


class OkBusinessSpider(scrapy.Spider):
    name = 'ok_business'
    allowed_domains = ['onlinekhabar.com']
    start_urls = ['https://www.onlinekhabar.com/business']

    def parse(self, response):
        cred = credentials.Certificate('nepali-epapers-firebase-adminsdk-x93g2-6820548d04.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        news_item_list = response.xpath('//*[@class="news_loop"]')
        category = "business"
        for news in news_item_list:
            thumb = news.xpath('.//img/@data-original').extract()
            link = news.xpath('.//h2/a/@href').extract()
            if len(link) is not 0:
                thumb = thumb[0]
                link = link[0]
                title = news.xpath('.//h2/a/text()').extract()[0]
                self.main_content_dict = {'thumb': thumb,
                                          'title': title,
                                          'link': link,
                                          'category': category}
                final_content = Request(link, callback=self.get_items_details)
                yield final_content

        # next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        # yield response.follow(next_page_url)

    def get_items_details(self, response):
        original_content = response.xpath('//*[@id="sing_cont"]/*[@class="ok-single-content"]').extract_first()
        ok_single_content = response.xpath('//*[@id="sing_cont"]/*[@class="ok-single-content"]')
        desc_formatted = ok_single_content.xpath('.//p').extract()
        all_images = ok_single_content.xpath('.//img/@src').extract()
        id = "ok-"+response.url.split('/')[-1]
        paragraphs = response.xpath('//*[@id="sing_cont"]/*[@class="ok-single-content"]/p/text()').extract()
        all_text =" ".join(paragraphs)
        descr_split = all_text.split('।')
        purnabiram = '।'
        desc_list = [x + purnabiram for x in descr_split]
        published_date = response.xpath('.//span[@class="updated_date"]/text()').extract_first()
        tags= self.main_content_dict['title'].split(' ')
        author = response.xpath('.//*[@class="dline_left"]/span/text()').extract_first()
        get_items_details = {'id':id,
                'id_original': response.url.split('/')[-1],
                'news_url': self.main_content_dict['link'],
                'category': self.main_content_dict['category'],
                'site_name':'onlinekhabar.com',
                'title': self.main_content_dict['title'],
                'desc_original': original_content,
                'desc_formatted':desc_formatted,
                'desc_list': desc_list,
                'images': all_images,
                'thumb_url': self.main_content_dict['thumb'],
                'published_date':published_date,
                'created_date': datetime.datetime.now(),
                'author':author,
                'tags': tags,
                'num_reads': 0
                }
        doc_ref = self.db.collection(u'news_feeds').document(get_items_details['id']).set(get_items_details)
        return get_items_details
