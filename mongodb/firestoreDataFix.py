from hddGetFileNames import getFileNames
from hddReadTitleBasics import getTitleBasics
import pprint

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
firebase_admin.initialize_app(cred)
firestoredb = firestore.client()

firestoreWrite = firestore.client()

docs = firestoredb.collection(u'movie_list').get()

mlist=[]
for doc in docs:
	# print(doc.id)
	
	storedDoc =doc.to_dict()
	docid=doc.id
	datef= storedDoc['titleBasics']['dataFindTime']
	durdiff=storedDoc['titleBasics']['durationDiff']
	fuzz = storedDoc['titleBasics']['fuzzyScore']

	# if doc.id=='tt4635372':
	movieDataCollected = getTitleBasics(docid)
	movieDataCollected['titleBasics']['dataFindTime']=datef
	movieDataCollected['titleBasics']['durationDiff']=durdiff
	movieDataCollected['titleBasics']['fuzzyScore']=fuzz
	# pprint.pprint(movieDataCollected)

	mlist.append(movieDataCollected)

	# firestoreWrite.collection(u'movie_list').document(docid).set(movieDataCollected)

for m in mlist:
	print(m['titleBasics']['tconst'])
	# if m['titleBasics']['tconst']=='tt7581902':
	firestoreWrite.collection(u'movie_list').document(m['titleBasics']['tconst']).set(m)


# {'titlePrincipals': 
# [{'category': 'actor', 'tconst': 'tt7581902', 'characters': '["Sonu"]', 'nconst': 'nm4449711', 'primaryName': 'Kartik Aaryan'}, 
# {'category': 'actress', 'tconst': 'tt7581902', 'characters': '["Sweety"]', 'nconst': 'nm2410391', 'primaryName': 'Nushrat Bharucha'}, 
# {'category': 'actor', 'tconst': 'tt7581902', 'characters': '["Titu"]', 'nconst': 'nm5478232', 'primaryName': 'Sunny Singh Nijjar'}, 
# {'category': 'actor', 'tconst': 'tt7581902', 'characters': '["Girl 3 at House Party"]', 'nconst': 'nm9791556', 'primaryName': 'Alexandra'}, 
# {'category': 'director', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm3060331', 'primaryName': 'Luv Ranjan'}, 
# {'category': 'writer', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm5303169', 'primaryName': 'Rahul Mody'}, 
# {'category': 'producer', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm8249430', 'primaryName': 'Ankur Garg'}, 
# {'category': 'producer', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm1024685', 'primaryName': 'Bhushan Kumar'}, 
# {'category': 'producer', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm0474824', 'primaryName': 'Krishan Kumar'}, 
# {'category': 'composer', 'tconst': 'tt7581902', 'characters': '\\N', 'nconst': 'nm1249155', 'primaryName': 'Hitesh Sonik'}], 
# 'titleCrew': [{'role': 'Director', 'tconst': 'tt7581902', 'nconst': 'nm3060331', 'primaryName': 'Luv Ranjan'}, 
# {'role': 'Writer', 'tconst': 'tt7581902', 'nconst': 'nm3060331', 'primaryName': 'Luv Ranjan'}, 
# {'role': 'Writer', 'tconst': 'tt7581902', 'nconst': 'nm5303169', 'primaryName': 'Rahul Mody'}], 
# 'titleBasics': {'runtimeMinutes': 138, 'isAdult': 0, 'titleType': 'movie', 'dataFindTime': '2018-06-05 08:28:08', 'genres': 'Comedy,Romance', 
# 'durationDiff': 0, 'originalTitle': 'Sonu Ke Titu Ki Sweety', 'fuzzyScore': 100, 'primaryTitle': 'Sonu Ke Titu Ki Sweety', 
# 'tconst': 'tt7581902', 'startYear': 2018, 'endYear': '\\N'}}

