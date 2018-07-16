import glob
import os
import shutil

import datetime
import pyrebase
import requests
import urllib3
from bs4 import BeautifulSoup

# http://www.enayapatrika.com/enayapatrika.com/ep/2017/12/6/files/pdfsam_merge.pdf
from wand.image import Image


from Firestore.Store import Store


class NayaPatrika:
    def __init__(self):
        self.main_url = "http://www.enayapatrika.com/epapers"
        self.page_number = 0
        self.base_path = os.path.join(os.curdir, 'naya_patrika')
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def firebase_storage(self, date):
        config = {
            "apiKey": "AIzaSyBQJ_T64P25sErLx9HL00c862tfVoMeiYk",
            "authDomain": "cloudfirestore-184914.firebaseapp.com",
            "databaseURL": "https://cloudfirestore-184914.firebaseio.com",
            "storageBucket": "cloudfirestore-184914.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        cover_image_link = None
        thumbs = []
        images = []
        for i in range(self.page_number):
            print('{page_no} uploading to storage'.format(page_no=i))
            image_name = str(i) + ".png"
            thumb_name = str(i) + "_small.png"
            image_name = os.path.join(self.base_path, image_name)
            thumb_name = os.path.join(self.base_path, thumb_name)
            if i == 0:
                cover_image_name = '{page_no}_cover.png'.format(page_no=i)
                cover_image_name = os.path.join(self.base_path, cover_image_name)
                cover_location = 'images/nayapatrika/{date}/{name}'.format(date=date, name=cover_image_name)
                storage.child(cover_location).put(cover_image_name)
                cover_image_link = storage.child(cover_location).get_url(None)
            image_location = 'images/nayapatrika/{date}/{name}'.format(date=date, name=image_name)
            storage.child(image_location).put(image_name)
            thumb_location = 'images/nayapatrika/{date}/{name}'.format(date=date, name=thumb_name)
            storage.child(thumb_location).put(thumb_name)
            thumbs.append(storage.child(thumb_location).get_url(None))
            images.append(storage.child(image_location).get_url(None))
        return {'cover_image': cover_image_link,
                'thumbs': thumbs,
                'images': images}

    def get_latest(self):
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        headers = {'User-Agent': user_agent}
        content = requests.get(self.main_url, headers=headers).content
        soup = BeautifulSoup(content, 'html.parser')
        first_div = soup.find('div', {'class': 'col-sm-2'})
        a_href = first_div.a['href']
        date_list = a_href.split('/')
        date = date_list[-3] + "/" + date_list[-2] + "/" + date_list[-1]
        file_url = "http://www.enayapatrika.com/enayapatrika.com/ep/{date}/files/pdfsam_merge.pdf".format(date=date)
        date = date.replace("/", "-")
        file_name = os.path.join(self.base_path, '{date}.pdf'.format(date=date))
        if not os.path.exists(file_name):
            # download pdf

            self.download_pdf(date, file_url)

            # extract pdf
            self.pdf_2_png(date)

            # upload images to firebase storage
            # get_links
            result = self.firebase_storage(date)

            final_result = {'cover_image': result['cover_image'],
                            'images': result['images'],
                            'thumbs': result['thumbs'],
                            'name': 'nayapatrika',
                            'no_of_pages': len(result['images']),
                            'publication': 'nayapatrika',
                            'title': 'Naya Patrika',
                            'type': 'daily',
                            'date': datetime.datetime.strptime(date, '%Y-%m-%d')
                            }
            # upload to cloud firestore
            # print(final_result)
            store = Store()
            store.put_epapers_to_db("nayapatrika", date.replace("-", ""), final_result)
        self.delete_pngs(self.base_path)

    def delete_pngs(self, path):
        for filename in glob.glob('{}/*.png'.format(path)):
            os.remove(filename)

    def download_pdf(self, date, url):
        print('downloading pdf')
        c = urllib3.PoolManager()
        file_name = os.path.join(self.base_path, "{date}.pdf".format(date=date))
        with c.request('GET', url, preload_content=False) as resp, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)
        print('download completed')

    def pdf_2_png(self, date):
        print('converting pdf 2 images')
        file_name = os.path.join(self.base_path, '{}.pdf'.format(date))
        im = Image(filename=file_name, resolution=150)
        self.page_number = len(im.sequence)
        for i, page in enumerate(im.sequence):
            with Image(page) as page_image:
                page_image.format = 'png'
                page_image.alpha_channel = False
                page_image.save(filename=os.path.join(self.base_path, '{pageno}.png'.format(pageno=i)))
                if i == 0:
                    cover_image = page_image
                    cover_image.transform("", "150")
                    cover_image.save(filename=os.path.join(self.base_path, '{pageno}_cover.png'.format(pageno=i)))
                page_image.transform("", "120")
                page_image.save(filename=os.path.join(self.base_path, '{pageno}_small.png'.format(pageno=i)))


np = NayaPatrika()
np.get_latest()
