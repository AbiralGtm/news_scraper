import os

from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\Users\Promise\Desktop\KhabarSanjal\cloudfirestore-2c4b976bb375.json"
db = firestore.Client()
doc_ref = db.collection(u'epapers').document(u'alovelace')
