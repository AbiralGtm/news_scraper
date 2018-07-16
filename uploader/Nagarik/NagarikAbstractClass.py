import json
from abc import ABCMeta, abstractmethod

from Firestore.Store import Store
from PaperModel import Paper
from Util.Utility import Utility


class NagarikAbstract:
    def __init__(self):
        pass

    __metaclass__ = ABCMeta

    @staticmethod
    def check_if_exists(name, date):
        return False

    @staticmethod
    def put_to_database(content):
        if not NagarikAbstract.check_if_exists(content['name'], content['date']):
            store = Store()
            paper = Paper(content['name'], content['title'], content['publication'], content['date'],
                          content['no_of_pages'], content['cover_image'], content['thumbs'], content['images'],
                          content['type'])
            date_list = content['date'].split(' ')
            mnth_name = date_list[1]
            mnth_nummber = Utility.get_mnth_from_mnth_name(mnth_name)
            date = date_list[0].strip() + mnth_nummber + date_list[2].strip()
            store.put_epapers_to_db(content['name'], date, paper.to_dict())

    @staticmethod
    def get_latest_data(soup, name):
        first_div = soup.find_all('div', {'class': 'col-md-2'})
        all_a_tags = first_div[0].find_all('a')
        selected_a_tag = all_a_tags[1] if len(all_a_tags) > 1 else None
        if selected_a_tag is not None:
            title = selected_a_tag['title']
            url = selected_a_tag['href']
            thumb_url = selected_a_tag.img['src']
            date_list = title.split(' ')
            date = date_list[3] + " " + date_list[2] + " " + date_list[1]
            title = name.title()
            result = {'title': title.decode('utf-8'),
                      'url': url,
                      'thumb_url': thumb_url,
                      'date': date.decode('utf-8')}
            return result

    @staticmethod
    def get_details(url, image_prefix):
        content = Utility.get_source(url)
        content = str(content)
        start_index = content.index("var epapers")
        sub_content = content[start_index:]
        second_start_index = sub_content.index('[')
        end_index = sub_content.index(']') + 1
        final_content = sub_content[second_start_index: end_index]
        json_content = json.loads(final_content)
        thumbs = []
        images = []
        for j in json_content:
            img_url = image_prefix + j['zoom_url'].replace(r'\\', '')
            thumb_url = image_prefix + j['file'].replace(r'\\', '')
            thumbs.append(thumb_url)
            images.append(img_url)
        return thumbs, images

    @staticmethod
    def get_formatted_date(string):
        date_list = string.split(" ")
        pass
