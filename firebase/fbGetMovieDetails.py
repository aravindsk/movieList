import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# from nameBasics import passgetNameBasicsForTitle
from titleBasics import getFbTitleBasics
from titleCrew import getFbTitleCrew
from titlePrincipals import getFbTitlePrinicpals


dictFullMovie={}
directors=[]
writers=[]
principalCast=[]
# print('TITLE')
# titleBasics=getFbTitleBasics(u'tt2763304')
# print(titleBasics)
# dictFullMovie['titleBasics']=titleBasics
# print(dictFullMovie)

# crew = getFbTitleCrew(u'tt2763304')
# print("crew")
# print(crew)
# print("crew['directors'][0].to_dict()")
# directors = crew['directors'][0].to_dict()
# dictFullMovie['directors']=directors

# i=0
# for j in crew['directors']:
# 	print(crew['directors'][i].to_dict())
# 	directors.append(crew['directors'][i].to_dict())
# 	i=i+1
# print('directors')
# print(directors)
# dictFullMovie['directors']=directors
# # print("crew['writers']")
# # print(crew['writers'])
# i=0
# for writerList in crew['writers']:
# 	print(crew['writers'][i].to_dict())
# 	writers.append(crew['writers'][i].to_dict())
# 	i=i+1
# print('writers')
# print(writers)

# dictFullMovie['writers']=writers
# print (writers)

# dictFullMovie['writers']=writers
# print(dictFullMovie)

#print(crew['directors'][0].to_dict()['primaryName'])
# for dirList in crew['directors'][0].to_dict():
# 	print(dirList)
print('PRINCIPALS')
principals = getFbTitlePrinicpals(u'tt2763304')
i=0
for priList in principals:
	# print(priList.to_dict())
	principalCast.append(priList.to_dict())
	i=i+1
print(principalCast)