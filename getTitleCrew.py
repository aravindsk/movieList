import csv
import json
import datetime
from time import gmtime, strftime

jsonTitleCrew = {}  
jsonTitleCrew['tConst'] = []

def findTitleCrewName (tConst):
	print('call findTitleCrewName :'+str(tConst))
	with open('/home/sk/coding/imdb/title_crew_data.tsv', newline='') as titleCrewListFile:
		crewList = csv.reader(titleCrewListFile, delimiter='\t', quotechar='|')
		for crewLine in crewList:
			if crewLine[0]==tConst:	
				crewDetails = {
							'tConst':crewLine[0],
							'directors':crewLine[1],
							'writers':crewLine[2],
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}
	return crewDetails

#read jsonTitleBasics and get title.cre
jsonTitleBasicsFileName='datadump/jsonTitleBasics2018_05_28_04_55_40.json'
print('data from file:'+jsonTitleBasicsFileName)
with open(jsonTitleBasicsFileName) as json_TitleBasics:  
    data = json.load(json_TitleBasics)
    for p in data['tConst']:
        print('tConst: ' + p['tConst'])
        print('originalTitle: ' + p['originalTitle'])
        tConst = p['tConst']
        titleCrewDetails = findTitleCrewName(tConst)
        #print(titleCrewDetails)
        jsonTitleCrew['tConst'].append(titleCrewDetails)


print("JSON title basics details")
print(jsonTitleCrew)
timeStamp = strftime("%Y_%m_%d_%H_%M", gmtime())
jsonTitleCrewFileName = 'datadump/jsonTitleCrew'+str(timeStamp)+'.json'
with open(jsonTitleCrewFileName, 'w') as outfile:  
	json.dump(jsonTitleCrew, outfile)