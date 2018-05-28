import csv
import json
import datetime
from time import gmtime, strftime

from getNameBasics import fnGetNameBasics
from firebaseWriteTitleCrew import fnFBWriteTitleCrew

jsonTitleCrew = {}  
jsonTitleCrew['tconst'] = []

def findTitleCrewName (tConst):
	print('call findTitleCrewName :'+str(tConst))
	with open('/home/sk/coding/imdb/title_crew.tsv', newline='') as titleCrewListFile:
		crewList = csv.reader(titleCrewListFile, delimiter='\t', quotechar='|')
		for crewLine in crewList:
			if crewLine[0]==tConst:	
				crewDetails = {
							'tconst':crewLine[0],
							'directors':crewLine[1],
							'writers':crewLine[2],
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}
	return crewDetails


def fnGetTitleCrew(jsonTitleBasicsFileName):
#read jsonTitleBasics and get title.cre
#jsonTitleBasicsFileName='datadump/jsonTitleBasics2018_05_28_04_55_40.json'
	print('get TITLE BASICS filename:'+jsonTitleBasicsFileName)
	with open(jsonTitleBasicsFileName) as json_TitleBasics:  
	    data = json.load(json_TitleBasics)
	    for p in data['tconst']:
	        # print('tconst: ' + p['tconst'])
	        # print('originalTitle: ' + p['originalTitle'])
	        tconst = p['tconst']
	        titleCrewDetails = findTitleCrewName(tconst)
	        #print(titleCrewDetails)
	        jsonTitleCrew['tconst'].append(titleCrewDetails)


	# print("TITLE CREW details")
	# print(jsonTitleCrew)
	timeStamp = strftime("%Y_%m_%d_%H_%M", gmtime())
	jsonTitleCrewFileName = 'datadump/jsonTitleCrew'+str(timeStamp)+'.json'
	with open(jsonTitleCrewFileName, 'w') as outfile:  
		json.dump(jsonTitleCrew, outfile)
	fnFBWriteTitleCrew(jsonTitleCrewFileName)
	fnGetNameBasics(jsonTitleCrewFileName)