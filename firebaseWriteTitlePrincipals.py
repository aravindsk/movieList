import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()

def fnFBWriteTitlePrincipals(jsonTitlePrincipalsFileName):
	#write to fire base : TitleBasics
	#jsonTitleBasicsFileName='datadump/jsonTitlePrincipals2018_05_28_06_57.json'
	print('data from file:'+jsonTitlePrincipalsFileName)
	with open(jsonTitlePrincipalsFileName) as json_TitlePrincipals:  
	    data = json.load(json_TitlePrincipals)
	    for p in data['tconst']:
	        print(p)
	        fsDocName = p['tconst']+'-'+p['nconst']
	        db.collection(u'title_principals').document(fsDocName).set(p)

