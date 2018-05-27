from os import walk
from fuzzywuzzy import fuzz
import re
import csv
import subprocess
import subprocess32 as sp
import json

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
    print('FILENAME :',vid_file_path)
    print('EXTENSION :',file_format)
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
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


    	


fuzzyCount = 0
normalCount = 0
tConstCount = 0

def findMovieInAKAS(movieName,movieDuration):
	with open('/home/sk/coding/imdb/akas_data.tsv', newline='') as movieListFile:
		print("calling findMovieInAKAS for "+str(movieName)+":"+str(movieDuration))
		processedList =[]
		movieList = csv.reader(movieListFile, delimiter='\t', quotechar='|')
		next(movieList)
		for movieLine in movieList:
	#			if movieLine[7]:
				#if int(line[1])>1:
					#if movieLine[0] not in processedList:
					#if movieLine[1]=='1':
					#processedList.append(movieLine[0])
					
	#		movieName = 'faces places'
			#if movieLine[2]== '3 Iron': #movieLine[2]== 'Thenmavin Kombath' or movieLine[2]== 'Swades' or movieLine[2]== 'Avengers: Infinity War':
			if fuzz.ratio(movieName, movieLine[2]) > 80:

				print("fuzz.ratio:"+str(fuzz.ratio(movieName, movieLine[2])))
				processedList.append(movieLine[0])
				print(int(movieLine[0][2:]))
				#db.collection(u'imdb_akas').document(movieLine[0]).set(movieLineDetails)
				print('------------BEGINNING-----------')
				print('Movie name: '+movieLine[2])
				print('titleId: '+movieLine[0])
				print('ordering: '+movieLine[1])
				print('title: '+movieLine[2])
				print('region: '+movieLine[3])
				print('language: '+movieLine[4])
				print('types: '+movieLine[5])
				print('attributes: '+movieLine[6])
				print('isOriginalTitle: '+movieLine[7])
				tconst=movieLine[0]
				if findMovieNameByTconst(tconst,movieDuration):
					print("FOUND IN findMovieNameByTconst(None,tconst,movieDuration):"+str(tconst)+":"+str(movieDuration))
					return True
				else:
					print("NOT FOUND in findMovieInAKAS")
					return False


def findMovieNameByTconst (movieTconst,movieDuration):
	global fuzzyCount
	global normalCount
	global tConstCount
	print('Function findMovieNameByTconst call for:'+str(movieTconst))#+ str(movieYear[0]))
	with open('/home/sk/coding/imdb/basics_data.tsv', newline='') as basicMovieListFile:
		basicMovieList2 = csv.reader(basicMovieListFile, delimiter='\t', quotechar='|')
		#for x in range(0, basicMovieListPointer): 
		#	next(basicMovieList)
		for basicMovieLine in basicMovieList2:
			if movieTconst == basicMovieLine[0]:
				#DO NOT check for movie duration in tConst match
				# if is_number(basicMovieLine[7]):
				# 	if abs(movieDuration - int(basicMovieLine[7]))<10 :
						print("PERFECT tConst MATCH")
						print(basicMovieLine[2])
						print(basicMovieLine[3])
						# print(fuzz.ratio(movieName,basicMovieLine[3]))
						tConstCount = tConstCount+1
						print('originalTitle: '+basicMovieLine[3])
						# print('isAdult: '+basicMovieLine[4])
						print('startYear: '+basicMovieLine[5])
						print('runtimeMinutes: '+basicMovieLine[7])
						return True

def findMovieNameByDuration (movieName,movieDuration):
	global fuzzyCount
	global normalCount
	print('Function findMovieNameByDuration call for:'+str(movieName))#+ str(movieYear[0]))
	with open('/home/sk/coding/imdb/basics_data.tsv', newline='') as basicMovieListFile:
		basicMovieList = csv.reader(basicMovieListFile, delimiter='\t', quotechar='|')
		#for x in range(0, basicMovieListPointer): 
		#	next(basicMovieList)
		for basicMovieLine in basicMovieList:
		#	basicMovieListPointer = basicMovieListPointer+1
			#Best match condition as of 12:00,May 28
			#fuzzy search basic name

			if fuzz.ratio(movieName,basicMovieLine[3]) > 95:
				#check for movie duration
				if is_number(basicMovieLine[7]):
					if abs(movieDuration - int(basicMovieLine[7]))<10 :
						print("PERFECT FUZZY name MATCH with duration")
						print("--------fuzz.ratio---------")
						print(movieName)
						print(basicMovieLine[3])
						print(fuzz.ratio(movieName,basicMovieLine[3]))
						fuzzyCount = fuzzyCount+1
						print('originalTitle: '+basicMovieLine[3])
						# print('isAdult: '+basicMovieLine[4])
						print('startYear: '+basicMovieLine[5])
						print('runtimeMinutes: '+basicMovieLine[7])
						return True

				# if fuzz.partial_ratio(movieName,basicMovieLine[3]) > 96:
				# 	print("--------fuzz.partial_ratio---------")
				# 	print(movieName)
				# 	print(basicMovieLine[3])
				# 	print(fuzz.partial_ratio(movieName,basicMovieLine[3]))

				# elif basicMovieLine[3]==movieName:
				# 	if is_number(basicMovieLine[7]):
				# 	 if abs(movieDuration - int(basicMovieLine[7]))<10: # and int(movieYear[0]) == int(basicMovieLine[5]): # and basicMovieLine[5]==movieYear:
				# 			print("PERFECT BASIC NAME MATCH")
				# 	#		print(basicMovieListPointer)
				# 			# print('primaryTitle : '+basicMovieLine[3]+'('+basicMovieLine[5]+')')
				# 			# print('tconst: '+basicMovieLine[0])
				# 			# print('titleType: '+basicMovieLine[1])
				# 			# print('primaryTitle: '+basicMovieLine[2])
				# 			print('originalTitle: '+basicMovieLine[3])
				# 			# print('isAdult: '+basicMovieLine[4])
				# 			print('startYear: '+basicMovieLine[5])
				# 			# print('endYear: '+basicMovieLine[6])
				# 			print('runtimeMinutes: '+basicMovieLine[7])
				# 			# print('genres: '+basicMovieLine[8])
				# 			print('------------ENDING-----------')
				# 			normalCount= normalCount+1
				# 			return True

			# elif movieTconst is not None:
			# 	if findMovieInAKAS(movieName,movieDuration):
			# 		return True
			# else:
			# 	if movieTconst == basicMovieLine[0]:
			# 		#check for movie duration
			# 		if is_number(basicMovieLine[7]):
			# 			if abs(movieDuration - int(basicMovieLine[7]))<10 :
			# 				print("PERFECT FUZZY tConst MATCH with duration")
			# 				print("--------fuzz.ratio---------")
			# 				print(movieName)
			# 				print(basicMovieLine[3])
			# 				print(fuzz.ratio(movieName,basicMovieLine[3]))
			# 				fuzzyCount = fuzzyCount+1
			# 				print('originalTitle: '+basicMovieLine[3])
			# 				# print('isAdult: '+basicMovieLine[4])
			# 				print('startYear: '+basicMovieLine[5])
			# 				print('runtimeMinutes: '+basicMovieLine[7])
			# 				return True 
		if findMovieInAKAS(movieName,movieDuration):
			return True
	return False


pathList = ['/media/sk/WD_Blue01/Movies/World']#,'/media/sk/WD_Blue01/Movies','/media/sk/WD_others/Movies','/media/sk/WD_movies']

for mypath in pathList:
	print(mypath)

mypath='/media/sk/WD_Blue01/Movies'
#new external drive 2
#'/media/sk/WD_others/Movies'
#new external drive 1
#'/media/sk/WD_movies'
#internal all
#'/media/sk/WD_Blue01/Movies'

#mypath='/home/sk/coding/foldertraversal'


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
for mypath in pathList:

	for (dirpath, dirnames, filenames) in walk(mypath):
		#print("dirpath :"+str(dirpath))
		#print("dirpath mov name :"+str(dirpath.split('/')[-1]))
		#print("dirnames:"+str(dirnames))
		#print("filenames:"+str(filenames))
		
		for filelist in filenames :
			#print (filelist)
			#print(filelist.split('.')[-1])
			fileExtension = filelist.split('.')[-1]
			extensions.append(filelist.split('.')[-1])
			

			if fileExtension in videoFileTypes:
				#print("FULL PATH :"+dirpath+'/'+filelist)
				fullFilePath = dirpath+'/'+filelist
				movieDuration = probeFileMetadata(fullFilePath,fileExtension)
				print("FileRuntime:"+str(movieDuration))
				
				
				# #replace special characters from name
				# filelist = filelist.replace ("."," ").replace("-"," ").replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("_"," ")
				
				# #clean file name of stopwords listed in fileNameStopWords
				# querywords = filelist.split()
				# resultwords  = [word for word in querywords if word.lower() not in fileNameStopWords]
				# result = ' '.join(resultwords)


				# #split year and substring before year
				# movieYear = re.findall(r"\d\d\d\d\b" ,result)
				# for x in movieYear:
				# 	result = result.split(x,1)[0].rstrip()
				# print ('cleaned filename:'+result)

				result = filenameCleanup(filelist)
				#print ('year:'+str(movieYear))
				if result!='' and movieDuration>5:
					if findMovieNameByDuration(result,movieDuration):
						print("FOUND")
						foundList.append(fullFilePath)
					else:
						print("NOT FOUND!!!")
						notFoundList.append(fullFilePath)
					
					#if result not empty and already present in list
					if(result!='' and ('result' in diskFilenames) == False):
						diskFilenames.append(result)

	print ("***PATH LOCATION : "+mypath)
	print("***FILE NAMES : "+str(diskFilenames))
	print("***NUMBER OF FILES : "+str(len(diskFilenames)))
	print("fuzzyCount:" +str(fuzzyCount))
	print("normalCount:" +str(normalCount))
	print("tConstCount:" +str(tConstCount))
	# for movieName in diskFilenames:

	# 	print(movieName)
	print('FOUND count:'+str(len(foundList)))
	print('NOT FOUND count:'+str(len(notFoundList)))
	print('NOT FOUND list:')
	print(notFoundList)
		#findMovieName(movieName,100)
#	findMovieName('Guardians Of The Galaxy')
