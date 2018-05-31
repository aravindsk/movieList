import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()


class NameBasics(object):
	"""docstring for TitleBasics"""
	def __init__(self, nconst, primaryName, birthYear,deathYear,primaryProfession,knownForTitles):
		#super(TitleBasics, self).__init__()
		self.nconst = nconst
		self.primaryName = primaryName
		self.birthYear = birthYear
		self.deathYear = deathYear
		self.primaryProfession = primaryProfession
		self.knownForTitles = knownForTitles

	@staticmethod
	def from_dict(source):
		nameBasics = NameBasics(source[u'nconst'],source[u'primaryName'],source[u'birthYear'],source[u'deathYear'],source[u'primaryProfession'],source[u'knownForTitles']
			)
		return nameBasics

	def to_dict(self):
		        # [START_EXCLUDE]
		dest = {
			u'nconst': self.nconst,
			u'primaryName': self.primaryName,
			u'birthYear': self.birthYear,
			u'deathYear': self.deathYear,
			u'primaryProfession': self.primaryProfession,
			u'knownForTitles': self.knownForTitles,
		}
		return dest
	def __repr__(self):
		return u'NameBasics(nconst={},primaryName={},birthYear={},deathYear={},primaryProfession={},knownForTitles={})'.format(self.nconst,
			self.primaryName,self.birthYear,self.deathYear,self.primaryProfession,self.knownForTitles)


#get info for particular title
def getFbNameBasics(nconst):
	docs = db.collection(u'name_basics').document(nconst)
	doc = docs.get()
	namebasics = NameBasics.from_dict(doc.to_dict())
	return(namebasics)