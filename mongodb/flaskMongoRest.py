from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify



# from nameBasics import passgetNameBasicsForTitle
from readNameBasics import getTitleBasics
# from titleCrew import getFbTitleCrew
# from titlePrincipals import getFbTitlePrinicpals
# from getMovieJson import getMovieJson


app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class movie_name(Resource):
    def get(self, tconst):
        # print('Employee id:' + employee_id)
        tempTconstArr=[tconst]
        result = getTitleBasics(tempTconstArr)
        print(result)
        return result

api.add_resource(movie_name,'/title/<tconst>')

if __name__ == '__main__':
	app.run(port=5002)

	# /title/tt2763304