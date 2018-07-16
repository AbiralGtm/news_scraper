from bs4 import BeautifulSoup

from Nagarik.NagarikAbstractClass import NagarikAbstract
from Util.Utility import Utility


class NagarikLatest(NagarikAbstract):
    def __init__(self, name, url, image_url_prefix, type):
        super(NagarikLatest, self).__init__()
        self.url = url
        self.name = name
        self.type  = type
        self.img_url_prefix = image_url_prefix

    @staticmethod
    def make_soup(given_url):
        content = Utility().get_source(given_url)
        return BeautifulSoup(content, 'html.parser')

    """
              title:""
              date:""
              thumb_url:""
              url: ""
              name: ""
    """

    def get_latest(self):
        result = super(NagarikLatest, self).get_latest_data(name=self.name, soup=self.make_soup(self.url))
        return result

    def get_detail(self, detail_url):
        thumbs_list, images_list = super(NagarikLatest, self).get_details(detail_url, self.img_url_prefix)
        return thumbs_list, images_list

    def get_data(self):
        name = self.name.decode('utf-8')
        content = self.get_latest()
        content['name'] = name
        content['type'] = self.type
        thumbs, images = self.get_detail(content['url'])
        content['thumbs'] = thumbs
        content['images'] = images
        content['publication'] = name
        content['no_of_pages'] = len(thumbs)
        content['cover_image'] = thumbs[0]
        self.put_to_database(content)






