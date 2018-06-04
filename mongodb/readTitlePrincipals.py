import pprint
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://10.0.0.2:27017/')
db = client['imdb']


# nconst
# tconst
# category
# characters
# PrincipalDetails.primaryName

class TitlePrincipals(object):
  def __init__(self, tconst, primaryName, nconst,category,characters):
    #super(TitleBasics, self).__init__()
    self.tconst = tconst
    self.primaryName = primaryName
    self.nconst = nconst
    self.category = category
    self.characters = characters

  @staticmethod
  def from_dict(source):
    titleprincipals = TitlePrincipals(source[u'tconst'],source[u'primaryName'],source[u'nconst'],source[u'category'],source[u'characters'])
    return titleprincipals


  def to_dict(self):
            # [START_EXCLUDE]
    dest = {
      u'tconst': self.tconst,
      u'primaryName': self.primaryName,
      u'nconst': self.nconst,
      u'category': self.category,
      u'characters': self.characters,
    }
    return dest
  def __repr__(self):
    return u'TitlePrincipals(tconst={},primaryName={},nconst={},category={},characters={})'.format(self.tconst,self.primaryName,self.nconst,self.category
      ,self.characters)


def getTitlePrincipals(tconst):
#get principal titles for tconst
  title_principals = db.title_principals
  pipeline =[
  	{"$match":{"tconst":{"$in":tconst }}
  	},
  	{
       "$lookup":
       	{
  	         "from":"name_basics",
  	         "localField":"nconst",
  	         "foreignField":"nconst",
  	         "as" :"PrincipalDetails"
       	}
    	},
    	{
    		"$unwind":"$PrincipalDetails"
    	},
    	{
    	 "$project":
    	 	{
    	 		"_id":0
    	 	}
    	}


  ]
  #build array of principal objects
  principalsList =[]
  for principals in title_principals.aggregate(pipeline):
    objTitlePrincipals = TitlePrincipals(principals['tconst'],principals['PrincipalDetails']['primaryName'],principals['nconst'],principals['category'],principals['characters'])
    principalsList.append(objTitlePrincipals.to_dict())

  # print(principalsList)
  return principalsList