import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from nameBasics import getFbNameBasics
# import google.cloud.exceptions

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
db = firestore.client()


class TitleCrew(object):
	"""docstring for TitleBasics"""
	def __init__(self, tconst, directors, writers):
		#super(TitleBasics, self).__init__()
		self.tconst = tconst
		self.directors = directors
		self.writers = writers

	@staticmethod
	def from_dict(source):
		titleCrew = TitleCrew(source[u'tconst'],source[u'directors'],source[u'writers']
			)
		return titleCrew

	def to_dict(self):
		        # [START_EXCLUDE]
		dest = {
			u'tconst': self.tconst,
			u'directors': self.directors,
			u'writers': self.writers
		}
		return dest
	def __repr__(self):
		return u'TitleCrew(tconst={},directors={},writers={})'.format(self.tconst,
			self.directors,self.writers)



#get info for particular title
def getFbTitleCrew(tconst):
	directorList=[]
	writerList=[]
	crewList=[]
	docs = db.collection(u'title_crew').document(tconst)
	doc = docs.get()
	titlecrew = TitleCrew.from_dict(doc.to_dict())
	for directorNconst in titlecrew.directors.split(","):
		directorList.append(getFbNameBasics(directorNconst))
	for writerNconst in titlecrew.writers.split(","):
		writerList.append(getFbNameBasics(writerNconst))
	crewList = directorList+writerList
	return(crewList)