import csv
import json
import datetime
from time import gmtime, strftime

jsonNameBasics = {}  
jsonNameBasics['nconst'] = []

def findNameBasics (nConst):
	print('call findNameBasics :'+str(nConst))
	with open('/home/sk/coding/imdb/name_basics.tsv', newline='') as nameBasicsListFile:
		nameBasicsList = csv.reader(nameBasicsListFile, delimiter='\t', quotechar='|')
		for nameBasicsLine in nameBasicsList:
			if nameBasicsLine[0]==nConst:	
				nameBasicsDetails = {
							'nconst':nameBasicsLine[0],
							'primaryName':nameBasicsLine[1],
							'birthYear':nameBasicsLine[2],
							'deathYear':nameBasicsLine[3],
							'primaryProfession':nameBasicsLine[4],
							'knownForTitles':nameBasicsLine[5],
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}
	return nameBasicsDetails

#read jsonTitleBasics and get title.cre
jsonTitleCrewFileName='datadump/jsonTitleCrew2018_05_28_05_17.json'
print('data from file:'+jsonTitleCrewFileName)
with open(jsonTitleCrewFileName) as json_CrewFile:  
	data = json.load(json_CrewFile)
	for p in data['tconst']:
		print('directors: ' + p['directors'])
		directorsnConstList = p['directors'].split(",")	
		for directorsnconst in directorsnConstList:
			print(directorsnconst)
			nameBasicsDetails = findNameBasics(directorsnconst)
			jsonNameBasics['nconst'].append(nameBasicsDetails)

		print('writers: ' + p['writers'])        
		writersnConstList = p['writers'].split(",")	
		for writersnconst in writersnConstList:
			print(writersnconst)
			nameBasicsDetails = findNameBasics(writersnconst)
			jsonNameBasics['nconst'].append(nameBasicsDetails)




print("JSON name basics details")
print(jsonNameBasics)
timeStamp = strftime("%Y_%m_%d_%H_%M", gmtime())
jsonNameBasicsFileName = 'datadump/jsonNameBasics'+str(timeStamp)+'.json'
with open(jsonNameBasicsFileName, 'w') as outfile:  
	json.dump(jsonNameBasics, outfile)