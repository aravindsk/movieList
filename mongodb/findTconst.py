from hddGetFileNames import getFileNames
from hddReadTitleBasics import getTitleBasics

import pprint
import pymongo
from pymongo import MongoClient

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
firebase_admin.initialize_app(cred)
firestoredb = firestore.client()


client = MongoClient('mongodb://10.0.0.2:27017/')
db = client['imdb']


def findMovieDetails():
	hddMovieList = getFileNames()
	# print(hddMovieList)
	for movie in hddMovieList['tconst']:
		# movieDataCollected['metadataDataCollection'] = movie
		movieDataCollected = getTitleBasics(movie['tconst'])
		#pack hdd data collection stats into the dict
		movieDataCollected['titleBasics']['dataFindTime']=movie['dataFindTime']
		movieDataCollected['titleBasics']['durationDiff']=movie['durationDiff']
		movieDataCollected['titleBasics']['fuzzyScore']=movie['fuzzyScore']
		pprint.pprint(movieDataCollected)
		firestoredb.collection(u'movie_list').document(movie['tconst']).set(movieDataCollected)


	# print(hddMovieList['tconst']['tconst'])
	# for movie in hddMovieList:
	# 	print(movie[0])
	# 	print(movie[1])
	# 	getTitleBasics(movie[0])
		# db.collection(u'name_basics').document(p['nconst']).set(p)
