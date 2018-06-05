from os import walk
from fuzzywuzzy import fuzz
from time import gmtime, strftime
import re
import csv
import subprocess
import subprocess32 as sp
import json
import datetime

fuzzyCount = 0
normalCount = 0
tConstCount = 0
bestDurationDiff =10000

jsonTitleBasics = {}  
jsonTitleBasics['tconst'] = []

diskFilenames =[]
notFoundList =[]
foundList =[]
extensions =[]
videoFileTypes = ['webm', 'mkv','sfv', 'mp4','avi','dat','m4v']
fileNameStopWords = ['webm', 'mkv','sfv', 'mp4','avi','dat','m4v','xvid',
'x264','360p','480p','720p','1080p','aac','hdrip','bdrip','brrip','bluray','BRRip','axxo','bluray','dvdrip','hdtv','h264','webrip'
,'ac3','evo','yify','yts','divx','hevc','x265','2ch','10bit','2ch','6ch',
'psa','prince','internal','afg','heteam','mkvcage','shaanig','ettv','eztv'
,'hon3y','tamil','english','malayalam','hindi','esub','www','tamilrockers','tamilmv'
,'rarbg','etrg','ag','web','dl','eng','esubs','ddr','8ch','1ch'
'sujaidr','1cd','700mb','750mb','800mb','extended','dvdr'
,'killers','chamee','lol','fum','nit158','vtv','en','asap','qcf',
'fleet','nf69','2hd','reenc','deejayahmed','batv','blu','ray','dual'
,'audio','limited','subs','gwc','msd','vector','deflate','bipolar','ganool','sujaidr','etrg'
,'sample'

]


	

def findMovieInAKAS(movieName,movieDuration):
	bestFuzzyScore = 0
	bestMatch = None
	global bestDurationDiff
	bestDurationDiff = 10000
	matchList= dict()
	with open('/home/sk/coding/imdb/title_akas.tsv', newline='') as movieListFile:
		print("calling findMovieInAKAS for "+str(movieName)+":"+str(movieDuration))
		processedList =[]
		movieList = csv.reader(movieListFile, delimiter='\t', quotechar='|')
		next(movieList)
		for movieLine in movieList:
			if fuzz.ratio(movieName, movieLine[2]) > 80:
				fuzzyScore = fuzz.ratio(movieName, movieLine[2])
				# print("fuzz.ratio:"+str(fuzzyScore))
				processedList.append(movieLine[0])

				tconst=movieLine[0]
				if fuzzyScore>=bestFuzzyScore:
						bestFuzzyScore=fuzzyScore
						#matchList[tconst]=findMovieNameByTconst(tconst,movieDuration,fuzzyScore)
						temp=findMovieNameByTconst(tconst,movieDuration,fuzzyScore)
						if temp is not None:
							bestMatch = temp

	print("--------BEST FOUND MATCHES--------")
	#print(matchList)
	if bestMatch is not None:
		print(bestMatch)
		jsonTitleBasics['tconst'].append(bestMatch)
		return True
	else:
		print("NOT FOUND")
		return False


def findMovieNameByTconst (movieTconst,movieDuration,fuzzyScore):
	global bestDurationDiff
	global fuzzyCount
	global normalCount
	global tConstCount
	print('Function findMovieNameByTconst call for:'+str(movieTconst))#+ str(movieYear[0]))
	with open('/home/sk/coding/imdb/title_basics.tsv', newline='') as basicMovieListFile:
		basicMovieList2 = csv.reader(basicMovieListFile, delimiter='\t', quotechar='|')
		#for x in range(0, basicMovieListPointer): 
		#	next(basicMovieList)
		for basicMovieLine in basicMovieList2:
			if movieTconst == basicMovieLine[0]:
						durationDiff=1000

						tConstCount = tConstCount+1
						if is_number(basicMovieLine[7]):
							durationDiff = abs(movieDuration - int(basicMovieLine[7]))
						
						if durationDiff<=bestDurationDiff:
							bestDurationDiff=durationDiff
							tConstDetails = {
							'tconst':basicMovieLine[0],
							# 'titleType':basicMovieLine[1],
							# 'primaryTitle':basicMovieLine[2],
							# 'originalTitle':basicMovieLine[3],
							# 'isAdult':basicMovieLine[4],
							# 'startYear':basicMovieLine[5],
							# 'endYear':basicMovieLine[6],
							# 'runtimeMinutes':basicMovieLine[7],
							# 'genres':basicMovieLine[8],
							'fuzzyScore':fuzzyScore,
							'durationDiff':durationDiff,
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}

							return tConstDetails
						else:
							return None

def findMovieNameByDuration (movieName,movieDuration):
	global fuzzyCount
	global normalCount
	print('Function findMovieNameByDuration call for:'+str(movieName))#+ str(movieYear[0]))
	with open('/home/sk/coding/imdb/title_basics.tsv', newline='') as basicMovieListFile:
		basicMovieList = csv.reader(basicMovieListFile, delimiter='\t', quotechar='|')
		#for x in range(0, basicMovieListPointer): 
		#	next(basicMovieList)
		for basicMovieLine in basicMovieList:
		#	basicMovieListPointer = basicMovieListPointer+1
			#Best match condition as of 12:00,May 28
			#fuzzy search basic name
			fuzzyScore =fuzz.ratio(movieName,basicMovieLine[3])
			if fuzzyScore > 95:
				#check for movie duration
				if is_number(basicMovieLine[7]):
					durationDiff=abs(movieDuration - int(basicMovieLine[7]))
					if durationDiff<10 :
						fuzzyCount = fuzzyCount+1
						basicsDetails={
							'tconst':basicMovieLine[0],
							# 'titleType':basicMovieLine[1],
							# 'primaryTitle':basicMovieLine[2],
							# 'originalTitle':basicMovieLine[3],
							# 'isAdult':basicMovieLine[4],
							# 'startYear':basicMovieLine[5],
							# 'endYear':basicMovieLine[6],
							# 'runtimeMinutes':basicMovieLine[7],
							# 'genres':basicMovieLine[8],
							'fuzzyScore':fuzzyScore,
							'durationDiff':durationDiff,
							'dataFindTime':strftime("%Y-%m-%d %H:%M:%S", gmtime())
							}
						print (basicsDetails)
						jsonTitleBasics['tconst'].append(basicsDetails)
						return True

		if findMovieInAKAS(movieName,movieDuration):
			return True
	return False




def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def probeFileMetadata(vid_file_path,file_format):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    # print('FILENAME :',vid_file_path)
    # print('EXTENSION :',file_format)
    if type(vid_file_path) != str:
        raise Exception('Give ffprobe a full file path of the video')
        return

    command = ["ffprobe",
            "-loglevel",  "quiet",
            "-print_format", "json",
             "-show_format",
             "-show_streams",
             vid_file_path
             ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    #print (out.decode("utf-8") )
    #x=out.decode("utf-8") 
    fileMetaData = out.decode("utf-8")
    fileJson = json.loads(out.decode("utf-8"))
    #6264.875000
    if file_format =='sfv' or file_format =='dat':
    	duration = 0
    elif file_format =='mkv' or 'webm':
    	duration = fileJson['format']['duration']
    
    else:
    	duration = fileJson["streams"][0]["duration"] 


    return int(round(float(duration)/60,0))

def filenameCleanup(inputFilename):
	global fileNameStopWords

	#replace special characters from name
	filename = inputFilename.replace ("."," ").replace("-"," ").replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("_"," ")
	
	#clean file name of stopwords listed in fileNameStopWords
	querywords = filename.split()
	resultwords  = [word for word in querywords if word.lower() not in fileNameStopWords]
	result = ' '.join(resultwords)


	#split year and substring before year
	movieYear = re.findall(r"\d\d\d\d\b" ,result)
	for x in movieYear:
		result = result.split(x,1)[0].rstrip()
	return result


def getFileNames():
	pathList =['/media/sk/WD_others/Movies/English',
	'/media/sk/WD_others/Movies/Foreign',
	'/media/sk/WD_others/Movies/Indian']
	#Done exteranl WD_movies
	# ['/media/sk/WD_movies/Documentaries',
	# '/media/sk/WD_movies/English',
	# '/media/sk/WD_movies/Foreign',
	# '/media/sk/WD_movies/Hindi',
	# '/media/sk/WD_movies/Regional',
	# ]
	# #Done inter Blue HDD
	# [
	# '/media/sk/WD_Blue01/Movies/Documentaries',
	# '/media/sk/WD_Blue01/Movies/Indian',
	# '/media/sk/WD_Blue01/Movies/World',
	# '/media/sk/WD_Blue01/Movies/English'
	# ] 

	# for mypath in pathList:
	# 	print(mypath)

	# mypath='/media/sk/WD_Blue01/Movies'
	#new external drive 2
	#'/media/sk/WD_others/Movies'
	#new external drive 1
	#'/media/sk/WD_movies'
	#internal all
	#'/media/sk/WD_Blue01/Movies'

	#mypath='/home/sk/coding/foldertraversal'

	# this needs to be build into a function
	fileNameList=[]
	mediaFilenames=[]
	timeStamp = strftime("%Y_%m_%d_%H_%M", gmtime())
	fileNameRunStats = '/home/sk/coding/imdb/datadump/run_stats_'+timeStamp+'.txt'
	with open(fileNameRunStats, 'a') as runStatsFile:  
		runStatsFile.write('Run start time : '+strftime("%Y-%m-%d %H:%M:%S", gmtime()))


	for mypath in pathList:
		for (dirpath, dirnames, filenames) in walk(mypath):
			#print("dirpath :"+str(dirpath))
			#print("dirpath mov name :"+str(dirpath.split('/')[-1]))
			#print("dirnames:"+str(dirnames))
			#print("filenames:"+str(filenames))

			for filelist in filenames :
				diskFilenames.append(filelist)
				#print (filelist)
				#print(filelist.split('.')[-1])
				fileExtension = filelist.split('.')[-1]
				extensions.append(filelist.split('.')[-1])
				

				if fileExtension in videoFileTypes:
					
					#print("FULL PATH :"+dirpath+'/'+filelist)
					fullFilePath = dirpath+'/'+filelist
					movieDuration = probeFileMetadata(fullFilePath,fileExtension)
					result = filenameCleanup(filelist)
					#print ('year:'+str(movieYear))
					if result!='' and movieDuration>5:

						mediaFilenames.append(filelist)
						# print(result)
						if findMovieNameByDuration(result,movieDuration):
							print("FOUND")
							foundList.append(fullFilePath)
						else:
							print("NOT FOUND!!!")
							notFoundList.append(fullFilePath)
					# if(result!='' and ('result' in diskFilenames) == False):
					# 	diskFilenames.append(result)
	
	with open(fileNameRunStats, 'a') as runStatsFile:  
		runStatsFile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		runStatsFile.write("\n***PATH LOCATION : "+mypath)
		runStatsFile.write("\n***ALL FILE NAMES : "+str(diskFilenames))
		runStatsFile.write("\n***NUMBER OF FILES : "+str(len(diskFilenames)))
		runStatsFile.write("\n***NUMBER OF MEDIA FILES : "+str(len(mediaFilenames)))
		runStatsFile.write("\n***ALL MEDIA FILES : "+str(mediaFilenames))
		runStatsFile.write("\nFuzzyCount:" +str(fuzzyCount))
		runStatsFile.write("\nNormalCount:" +str(normalCount))
		runStatsFile.write("\ntConstCount:" +str(tConstCount))
		runStatsFile.write('\nFOUND count:'+str(len(foundList)))
		runStatsFile.write('\n FOUND list:')
		runStatsFile.write(str(foundList))
		runStatsFile.write('\nNOT FOUND count:'+str(len(notFoundList)))
		runStatsFile.write('\nNOT FOUND list:')
		runStatsFile.write(str(notFoundList))
		runStatsFile.write('\nRun end time : '+strftime("%Y-%m-%d %H:%M:%S", gmtime()))

	# print(jsonTitleBasics)
	# print(fileNameList)
	return(jsonTitleBasics)