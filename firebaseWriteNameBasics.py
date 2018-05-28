import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#write to fire base : TitleBasics
jsonTitleBasicsFileName='datadump/jsonNameBasics2018_05_28_05_59.json'
print('data from file:'+jsonTitleBasicsFileName)
with open(jsonTitleBasicsFileName) as json_TitleBasics:  
    data = json.load(json_TitleBasics)
    for p in data['nconst']:
        print(p)
        db.collection(u'name_basics').document(p['nconst']).set(p)

