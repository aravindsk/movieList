import csv
from fuzzywuzzy import fuzz
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/sk/coding/moviereleases/MovieReleases-82b81f9e6917.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
basicMovieListPointer = 0

#test commiting a new comment

def findCrewName (crewnConst, crewType):
	print(crewnConst)
	with open('/home/sk/coding/imdb/name_data.tsv', newline='') as nameListFile:
		nameList = csv.reader(nameListFile, delimiter='\t', quotechar='|')
		for nameLine in nameList:
			if nameLine[0]==crewnConst:	
		#if nameLine[0]==crewLine[1]:
				print('Role : '+crewType)
				print('Name : '+nameLine[1])
				print('primaryProfession : '+nameLine[4])
				print('knownForTitles : '+nameLine[5])
				titleIdList = nameLine[5].split(",")	
				for titleId in titleIdList:
					findMovieName(titleId)


def findMovieName (movietConst):
	global basicMovieListPointer
	with open('/home/sk/coding/imdb/basics_data.tsv', newline='') as basicMovieListFile:
		basicMovieList = csv.reader(basicMovieListFile, delimiter='\t', quotechar='|')
		#for x in range(0, basicMovieListPointer): 
		#	next(basicMovieList)
		for basicMovieLine in basicMovieList:
		#	basicMovieListPointer = basicMovieListPointer+1
			if basicMovieLine[0]==movietConst:# and basicMovieLine[5]==movieYear:
		#		print(basicMovieListPointer)
				# print('primaryTitle : '+basicMovieLine[3]+'('+basicMovieLine[5]+')')
				# print('tconst: '+basicMovieLine[0])
				# print('titleType: '+basicMovieLine[1])
				# print('primaryTitle: '+basicMovieLine[2])
				print('originalTitle: '+basicMovieLine[3])
				# print('isAdult: '+basicMovieLine[4])
				print('startYear: '+basicMovieLine[5])
				# print('endYear: '+basicMovieLine[6])
				# print('runtimeMinutes: '+basicMovieLine[7])
				# print('genres: '+basicMovieLine[8])
				print('------------ENDING-----------')




with open('/home/sk/coding/imdb/akas_data.tsv', newline='') as movieListFile:

	loopExit=0
	processedList =[]
	movieList = csv.reader(movieListFile, delimiter='\t', quotechar='|')
	#skip x rows
	#3591948
	#3572000):
	#for x in range(0, 3610782): 
	next(movieList)
	for movieLine in movieList:
		#continue broken Firestore write
		#if int(movieLine[0][2:])>7630164:
			#fieldnames=['titleId','ordering','title','region','language','types','attributes','isOriginalTitle']
			if movieLine[7]:
			#if int(line[1])>1:
				#if movieLine[0] not in processedList:
				#if movieLine[1]=='1':
				#processedList.append(movieLine[0])
				
				movieName = 'mclaren'
				#if movieLine[2]== '3 Iron': #movieLine[2]== 'Thenmavin Kombath' or movieLine[2]== 'Swades' or movieLine[2]== 'Avengers: Infinity War':
				if fuzz.ratio(movieName, movieLine[2]) > 80:
					print(fuzz.ratio(movieName, movieLine[2]))
					processedList.append(movieLine[0])
					print(processedList)
					movieLineDetails = {
						'titleId': movieLine[0],
						'titleIdInt': int(movieLine[0][2:]),
						'ordering' : int(movieLine[1]),
						'title':movieLine[2],
						'region':movieLine[3],
						'language':movieLine[4],
						'types':movieLine[5],
						'attributes':movieLine[6],
						'isOriginalTitle':movieLine[7]
					}
					#Last id : 8407512
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
					findMovieName(movieLine[0])
					
					# loopExit= loopExit+1;
					# if loopExit ==2:
					# 	quit()


	print('processedList size :'+str(len(processedList)))
	my_dict = {i:processedList.count(i) for i in processedList}

	print (my_dict)

	#reader = csv.DictReader(csvfile,fieldnames=['titleId','ordering','title','region','language','types','attributes','isOriginalTitle'])
	#for row in reader:
		#if row['isOriginalTitle']==1:
		#print(row['titleId'],row['title'],row['region'])
	#	print(row['title'],row['region'])
#print(reader.line_num)
#tconst (string) 
#directors (array of nconsts)
#writers (array of nconsts)