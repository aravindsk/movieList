import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()


# from nameBasics import passgetNameBasicsForTitle
from titleBasics import getFbTitleBasics
from titleCrew import getFbTitleCrew
from titlePrincipals import getFbTitlePrinicpals

def getMovieJson(tconst):
	dictFullMovie={}
	directors=[]
	writers=[]
	principalCast=[]

	titleBasics=getFbTitleBasics(tconst)

	dictFullMovie['titleBasics']=titleBasics
	# print(dictFullMovie)

	crew = getFbTitleCrew(tconst)

	i=0
	for j in crew['directors']:
		print(crew['directors'][i].to_dict())
		directors.append(crew['directors'][i].to_dict())
		i=i+1

	dictFullMovie['directors']=directors

	i=0
	for writerList in crew['writers']:
		print(crew['writers'][i].to_dict())
		writers.append(crew['writers'][i].to_dict())
		i=i+1
	dictFullMovie['writers']=writers
	# 	i=i+1


	principals = getFbTitlePrinicpals(tconst)
	for priList in principals:
		# print(priList.to_dict())
		principalCast.append(priList.to_dict())
	# print(principalCast)
	dictFullMovie['principals']=principalCast
	return dictFullMovie
