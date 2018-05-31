import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

# cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
# firebase_admin.initialize_app(cred)
from nameBasics import getFbNameBasics
db = firestore.client()


class TitlePrincipals(object):
	"""docstring for TitleBasics"""
	def __init__(self, tconst, ordering, nconst#,category
		,job,characters):
		#super(TitleBasics, self).__init__()
		self.tconst = tconst
		self.ordering = ordering
		self.nconst = nconst
		# self.category = category
		self.job = job
		self.characters = characters

	@staticmethod
	def from_dict(source):
		titleprincipals = TitlePrincipals(source[u'tconst'],source[u'ordering'],source[u'nconst']#,source[u'category']
			,source[u'job'],source[u'characters']
			)
		return titleprincipals

	def to_dict(self):
		        # [START_EXCLUDE]
		dest = {
			u'tconst': self.tconst,
			u'ordering': self.ordering,
			u'nconst': self.nconst,
			u'categor#y': self.category,
			u'job': self.job,
			u'characters': self.characters,
		}
		return dest
	def __repr__(self):
		return u'TitlePrincipals(tconst={},ordering={},nconst={},job={},characters={})'.format(self.tconst,
			self.ordering,self.nconst#,self.category
			,self.job,self.characters)


#get info for particular title
def getFbTitlePrinicpals(tconst):
	# lstTitlePrincipals = [TitlePrincipals('','','','','') for _ in range(100)]
	lstTitlePrincipals=[]
	docs = db.collection(u'title_principals').where(u'tconst', u'==', tconst).get()
	for doc in docs:
	    # print(u'{} => {}'.format(doc.id, doc.to_dict()))
	    titleprincipals = TitlePrincipals.from_dict(doc.to_dict())
	    # lstTitlePrincipals.append(titleprincipals)
	    # print(titleprincipals)
	    lstTitlePrincipals.append(getFbNameBasics(titleprincipals.nconst))
	return(lstTitlePrincipals)