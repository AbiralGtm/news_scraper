# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import Request

class ImagekhabarPoliticsSpider(scrapy.Spider):
    name = 'imagekhabar_politics'
    allowed_domains = ['imagekhabar.com']
    start_urls = ['http://imagekhabar.com/category/5/politics']

    def parse(self, response):
        news_item_list = response.xpath('//*[@class="row"]/div[@class="col-xl-12 col-lg-6 col-md-6 col-sm-12 mt-30"]')
        category = "politics"
        site_name="imagekhabar.com"
        author="anymonous"

        for news in news_item_list:
            title = news.xpath('.//h3/a/text()').extract()[0]
            thumb = news.xpath('.//img[@class="img-fluid"]/@src').extract()[0]
            news_url = news.xpath('.//h3/a/@href').extract()[0]
            self.first_contents = {'thumb': thumb,
                                      'title': title,
                                      'news_url': news_url,
                                      'category': category,
                                      'site_name':site_name}
            url = response.urljoin(news_url)
            final_content = Request(url, callback=self.get_items_details)
            yield final_content

    def get_items_details(self,response):
        id= "imgkbr-"+response.url.split('/')[-2]
        id_original = response.url.split('/')[-2]
        desc_original = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]').extract_first()
        original_content = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/*[@class="position-relative mb-30"]')
        images = original_content.xpath('.//img/@src').extract()
        all_text = response.xpath('//*[@class="col-lg-8 col-md-12 mb-30"]/*[@class="news-details-layout1"]/p/text()').extract()

        return{
            'id':id,
            'id_original': int(id_original),
            'news_url': self.first_contents['news_url'],
            'category': self.first_contents['category'],
            'site_name':self.first_contents['site_name'],
            'title': self.first_contents['title'],
            'desc_original':desc_original,
            
            'desc_list':all_text,
            'images':images,
            'thumb_url': self.first_contents['thumb'],
            'crawled_time': datetime.datetime.now(),
        }
