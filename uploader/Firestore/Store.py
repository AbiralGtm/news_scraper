import os
from google.cloud import firestore


class Store(object):
    def __init__(self):
        path = os.path.abspath(os.path.curdir)
        file_path = os.path.join(path, 'cloudfirestore-2c4b976bb375.json')
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = file_path
        self.db = firestore.Client()

    def get_rashifal_url(self):
        doc_ref = self.db.collection(u'urls').document(u'rashifal_url')
        doc = doc_ref.get()
        return doc.to_dict()

    def put_epapers_to_db(self, name, date, content):
        doc_ref = self.db.collection(u'epapers').document('daily')
        doc_ref = doc_ref.collection(name.decode('utf-8')).document(date)
        content[u'timestamp'] = firestore.SERVER_TIMESTAMP
        doc_ref.update(content, firestore.CreateIfMissingOption(True))

    def put_forex_to_db(self, contents):
        for content in contents:
            doc_ref = self.db.collection(u"forex").document(str(contents.index(content)))
            content[u'timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(content, firestore.CreateIfMissingOption(True))

    def put_daily_rashifal(self, contents):
        for content in contents:
            doc_ref = self.db.collection(u"rashifal").document(u'nepali')
            doc_ref = doc_ref.collection(u"daily").document(content['name'])
            content[u'timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(content, firestore.CreateIfMissingOption(True))

    def put_yearly_rashifal(self, contents, _type):
        for content in contents:
            doc_ref = self.db.collection(u"rashifal").document(u'nepali')
            doc_ref = doc_ref.collection(_type).document(str(contents.index(content)))
            content[u'timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(content, firestore.CreateIfMissingOption(True))



