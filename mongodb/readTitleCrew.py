import pprint
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://10.0.0.2:27017/')
db = client['imdb']

# tconst
# role
# directorList.nconst||writerList.nconst
# directorList.primaryName||writerList.primaryName



class TitleCrew(object):
  """docstring for TitleBasics"""
  def __init__(self, tconst, role, nconst,primaryName):
    #super(TitleBasics, self).__init__()
    self.tconst = tconst
    self.role = role
    self.nconst = nconst
    self.primaryName = primaryName


  @staticmethod
  def from_dict(source):
    titleCrew = TitleCrew(source[u'tconst'],source[u'role'],source[u'nconst'],source[u'primaryName']
      )
    return titleCrew

  def to_dict(self):
            # [START_EXCLUDE]
    dest = {
      u'tconst': self.tconst,
      u'role': self.role,
      u'nconst': self.nconst,
      u'categor#y': self.primaryName
    }
    return dest
  def __repr__(self):
    return u'TitleCrew(tconst={},role={},nconst={},primaryName={})'.format(self.tconst,self.role,self.nconst,self.primaryName)

def getTitleCrew(tconst):
#get principal titles for tconst
  title_crew = db.title_crew
  # tconst = ["tt4154756","tt0214915"]
  pipeline =[
  	{"$match":{"tconst":{"$in":tconst }}
  	}
    ,
    {"$project":
        {  "_id":0,
           "tconst" : 1, 
           "directorList":{
           "$split":["$directors",","]
           },
           "writersList" : {
             "$split":["$writers",","]
            },
         }
     }
   ,
       {"$unwind":"$directorList"
       },
       {
            "$lookup":{
            "from": "name_basics",
            "localField": "directorList",
            "foreignField": "nconst",
            "as": "DirectorDetails"
            }
         }
         ,
          {"$unwind":"$DirectorDetails"
       }
       ,
       {"$unwind":"$writersList"
       },
       {
            "$lookup":{
            "from": "name_basics",
            "localField": "writersList",
            "foreignField": "nconst",
            "as": "WriterDetails"
            }
         }, 
             {"$unwind":"$WriterDetails"
       },
       {
        "$group": {
              "_id" : "$tconst",
             "directorList": { "$addToSet": "$DirectorDetails" },
             "writerList": { "$addToSet": "$WriterDetails" }
     }
   }

  ]

  crewList=[]
  for crew in title_crew.aggregate(pipeline):
    tconst = crew['_id']
    for directorList in crew['directorList']:
      role = 'Director'
      objTitleCrew = TitleCrew(tconst,role,directorList['nconst'],directorList['primaryName'])
      crewList.append(objTitleCrew.to_dict())
    for writerList in crew['writerList']:
      role = 'Writer'
      objTitleCrew = TitleCrew(tconst,role,writerList['nconst'],writerList['primaryName'])
      crewList.append(objTitleCrew.to_dict())
  # print(crewList)
  return crewList
