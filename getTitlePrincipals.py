import csv
import json
import datetime
from time import gmtime, strftime

jsonTitlePrincipals = {}  
jsonTitlePrincipals['tconst'] = []

def findTitlePrincipals (tConst):
	print('call findTitlePrincipals :'+str(tConst))
	with open('/home/sk/coding/imdb/title_principals.tsv', newline='') as titlePrincipalsListFile:
		principalsList = csv.reader(titlePrincipalsListFile, delimiter='\t', quotechar='|')
		for principalsLine in principalsList:
			if principalsLine[0]==tConst:	
				print('nconst:'+principalsLine[2])
				print('job:'+principalsLine[3])
				print('characters:'+principalsLine[4])
				principalsDetails = {
							'tconst':principalsLine[0],
							'ordering':principalsLine[1],
							'nconst':principalsLine[2],
							'job':principalsLine[3],
							'characters':principalsLine[4],
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}
				jsonTitlePrincipals['tconst'].append(principalsDetails)
	return True


#read jsonTitleBasics and get title.cre
jsonTitleBasicsFileName='datadump/jsonTitleBasics2018_05_28_04_55_40.json'
print('data from file:'+jsonTitleBasicsFileName)
with open(jsonTitleBasicsFileName) as json_TitleBasics:  
    data = json.load(json_TitleBasics)
    for p in data['tconst']:
        print('tconst: ' + p['tconst'])
        print('originalTitle: ' + p['originalTitle'])
        tconst = p['tconst']
        findTitlePrincipals(tconst)
        #titlePrincipalsDetails = findTitlePrincipals(tconst)
        #print(titleCrewDetails)
        


print("JSON title basics details")
print(jsonTitlePrincipals)
timeStamp = strftime("%Y_%m_%d_%H_%M", gmtime())
jsonTitlePrincipalsFileName = 'datadump/jsonTitlePrincipals.json'
with open(jsonTitlePrincipalsFileName, 'w') as outfile:  
	json.dump(jsonTitlePrincipals, outfile)