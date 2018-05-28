import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()

def fnFBWriteTitleCrew(jsonTitleCrewFileName):
	#write to fire base : TitleBasics
	#jsonTitleBasicsFileName='datadump/jsonTitleCrew2018_05_28_05_17.json'
	print('data from file:'+jsonTitleCrewFileName)
	with open(jsonTitleCrewFileName) as json_TitleCrew:  
	    data = json.load(json_TitleCrew)
	    for p in data['tconst']:
	        print(p)
	        db.collection(u'title_crew').document(p['tconst']).set(p)

