import json
import pprint
import pymongo
from pymongo import MongoClient
from readTitlePrincipals import getTitlePrincipals
from readTitleCrew import getTitleCrew

client = MongoClient('mongodb://10.0.0.2:27017/')
db = client['imdb']

# tconst
# primaryTitle
# startYear
# runtimeMinutes
# genres

class TitleBasics(object):
	"""docstring for TitleBasics"""
	def __init__(self, tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres):
		#super(TitleBasics, self).__init__()
		self.tconst = tconst
		self.titleType = titleType
		self.primaryTitle = primaryTitle
		self.originalTitle = originalTitle
		self.isAdult = isAdult
		self.startYear = startYear
		self.endYear = endYear
		self.runtimeMinutes = runtimeMinutes
		self.genres = genres

	@staticmethod
	def from_dict(source):
		titleBasics = TitleBasics(source[u'tconst'],source[u'titleType'],source[u'primaryTitle'],source[u'originalTitle'],source[u'isAdult'],
			source[u'startYear'],source[u'endYear'],source[u'runtimeMinutes'],source[u'genres']
			)
		return titleBasics

	def to_dict(self):
		        # [START_EXCLUDE]
		dest = {
			u'tconst': self.tconst,
			u'titleType':self.titleType,
			u'primaryTitle': self.primaryTitle,
			u'originalTitle':self.originalTitle,
			u'isAdult':self.isAdult,
			u'startYear': self.startYear,
			u'endYear':self.endYear,
			u'runtimeMinutes':self.runtimeMinutes,
			u'genres':self.genres
		}
		return dest
	def __repr__(self):
		return u'TitleBasics(tconst={},titleType={},primaryTitle={},originalTitle={},isAdult={},startYear={},endYear={},runtimeMinutes={},genres={})'.format(self.tconst,
			self.titleType,self.primaryTitle,self.originalTitle,self.isAdult,self.startYear,self.endYear,self.runtimeMinutes,self.genres)


#def getTitleBasics(tconst):
def getTitleBasics(inpTconst):
	#tconst = ["tt4154756","tt0214915"]
	title_basics = db.title_basics

	for titles in title_basics.find({"tconst":inpTconst }):
		objTitleBasics = TitleBasics(titles['tconst'],titles['titleType'],titles['primaryTitle'],titles['originalTitle'],titles['isAdult'],titles['startYear'],titles['endYear'],titles['runtimeMinutes'],titles['genres'])

		# print(objTitleBasics.to_dict())
		# print(titles['tconst'])
		# title_basics = titles

		# tempArr as the functions are using an IN clause in the $MATCH(For future bulk calls)
		tempArr= [titles['tconst']]
		titlePrincipals = getTitlePrincipals(tempArr)
		titleCrew = getTitleCrew(tempArr)
		# print(objTitleBasics)
		# print(titlePrincipals)
		# print(titleCrew)
		
		#declare dict to return
		movieDetails={}
		movieDetails['titleBasics']=objTitleBasics.to_dict()
		movieDetails['titlePrincipals']=titlePrincipals
		movieDetails['titleCrew']=titleCrew
		return(movieDetails)
