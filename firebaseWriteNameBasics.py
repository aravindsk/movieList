import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()

def fnFBWriteNameBasics(jsonNameBasicsFileName):
	#write to fire base : TitleBasics
	#jsonTitleBasicsFileName='datadump/jsonNameBasics2018_05_28_05_59.json'
	# print('data from file:'+jsonNameBasicsFileName)
	with open(jsonNameBasicsFileName) as json_NameBasics:  
	    data = json.load(json_NameBasics)
	    for p in data['nconst']:
	        print(p)
	        db.collection(u'name_basics').document(p['nconst']).set(p)

