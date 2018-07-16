import datetime

from Util.Utility import Utility


class Paper(object):
    def __init__(self, name, title, publication, date, no_of_pages, cover_image, thumbs, images, type):
        self.type = type.decode('utf-8')
        self.images = images
        self.thumbs = thumbs
        self.cover_image = cover_image
        self.no_of_pages = no_of_pages
        self.date = date
        self.publication = publication.decode('utf-8')
        self.title = title.decode('utf-8')
        self.name = name.decode('utf-8')

    def to_dict(self):
        date = self.date
        date_list = date.split(' ')
        mnth_name = date_list[1]
        mnth_nummber = Utility.get_mnth_from_mnth_name(mnth_name)
        date = date_list[0].strip() + mnth_nummber + date_list[2].strip()
        date_obj = datetime.datetime.strptime(date, '%Y%m%d').date()
        date_final = datetime.datetime.combine(date_obj, datetime.time.min)
        return {
            u'name': self.name,
            u'title': self.title,
            u'publication': self.publication,
            u'date': date_final,
            u'no_of_pages': self.no_of_pages,
            u'cover_image': self.cover_image,
            u'thumbs': self.thumbs,
            u'images': self.images,
            u'type': self.type
        }
