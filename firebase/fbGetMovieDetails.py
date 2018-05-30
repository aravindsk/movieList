import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.exceptions

cred = credentials.Certificate('/home/sk/coding/imdb/firebase/watchedmoviedb-448c0352da72.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# from nameBasics import passgetNameBasicsForTitle
from titleBasics import getFbTitleBasics
from titleCrew import getFbTitleCrew
from titlePrincipals import getFbTitlePrinicpals

# print('TITLE')
# print(getFbTitleBasics(u'tt2763304'))
# print('CREW')
# print(getFbTitleCrew(u'tt2763304'))
print('PRINCIPALS')
print(getFbTitlePrinicpals(u'tt2763304'))