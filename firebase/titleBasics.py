import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

# from titleCrew import getTitleCrew
# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()


class TitleBasics(object):
	"""docstring for TitleBasics"""
	def __init__(self, tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres, fuzzyScore, durationDiff, dataFindTime):
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
		self.fuzzyScore = fuzzyScore
		self.durationDiff = durationDiff
		self.dataFindTime = dataFindTime

	@staticmethod
	def from_dict(source):
		titleBasics = TitleBasics(source[u'tconst'],source[u'titleType'],source[u'primaryTitle'],source[u'originalTitle'],source[u'isAdult'],
			source[u'startYear'],source[u'endYear'],source[u'runtimeMinutes'],source[u'genres'],source[u'fuzzyScore'],
			source[u'durationDiff'],source[u'dataFindTime'],
			)
		return titleBasics

	def to_dict(self):
		        # [START_EXCLUDE]
		dest = {
			u'tconst': self.tconst,
			u'primaryTitle': self.primaryTitle,
			u'startYear': self.startYear
		}
		return dest
	def __repr__(self):
		return u'TitleBasics(tconst={},titleType={},primaryTitle={},originalTitle={},isAdult={},startYear={},endYear={},runtimeMinutes={},genres={},fuzzyScore={},durationDiff={},dataFindTime={})'.format(self.tconst,
			self.titleType,self.primaryTitle,self.originalTitle,self.isAdult,self.startYear,self.endYear,self.runtimeMinutes,self.genres,self.fuzzyScore,self.durationDiff,self.dataFindTime)


#get info for particular title
def getFbTitleBasics(tconst):
	docs = db.collection(u'title_basics').document(tconst)
	doc = docs.get()
	titleBasics = TitleBasics.from_dict(doc.to_dict())
	# print(titleBasics)
	titleDict = titleBasics.to_dict()
	return titleDict