#User Ziyang Zhang
#Restful-API
#2020/05/11


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd
import DBdata
from importlib import reload
import json

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

SA4data = DBdata.ovall()
##Import AUR-Labor-Data
#Labdata = pd.read_csv('./AURData/Labour.csv')

#set SA_4 return if not exit
def abort_if_notexit(SA4name):
    if SA4name not in SA4data:
        abort(404, message="Can not find {} data".format(SA4name))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Group25 Data API</h1><p>This site is a prototype API for Tweet Data.</p>"

@app.route('/api/overview', methods=['GET'], endpoint = "overview")
def get_data():
        return SA4data


##get general2019
class General2019(Resource):
    def get(self):
        reload(DBdata)
        data = son.dumps(DBdata.ov2019())
        return data

##get general2020
class General2020(Resource):
    def get(self):
        reload(DBdata)
        data = json.dumps(DBdata.ov2020())
        return data

##get general2021
class General2021(Resource):
    def get(self):
        reload(DBdata)
        data = json.dumps(DBdata.ov2021())
        return data

## post.get all data
class General(Resource):
    def get(self):
        reload(DBdata)
        data = json.dumps(DBdata.ovall())
        return data

## post.individual  data
class individual(Resource):
    def get(self, SA4name):
        abort_if_notexit(SA4name)
        return DBdata.ovall()[SA4name]

##Get SA4_Count
class SA4_TweetCount(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_SA4Sum()
        return data.to_json()

class SA4_TweetCountInd(Resource):
    def get(self, SA4name):
        reload(DBdata)
        abort_if_notexit(SA4name)
        data = DBdata.get_SA4Sum().to_dict()
        return data[SA4name]

##Get City Tweet Count
class City_TweetCount(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_CitySum()
        return data.to_json()

class City_TweetCountInd(Resource):
    def get(self, CityName):
        reload(DBdata)
        data = DBdata.get_CitySum().to_dict()
        return data[CityName]

#SA4 Sentiment data
class SA4_Senti_Overview(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_SA4_Senti_Overview()
        return data.to_json()

class SA4_Senti_OverviewInd(Resource):
    def get(self, SA4name):
        reload(DBdata)
        data = DBdata.get_SA4_Senti_Overview().to_dict()
        return data[SA4name]




#set Api
api.add_resource(General, '/api/overview')
api.add_resource(General2019,'/api/overview2019')
api.add_resource(General2020,'/api/overview2020')
api.add_resource(General2021,'/api/overview2021')     
api.add_resource(individual, '/api/overview/<SA4name>')
##From DB_tweetcount
api.add_resource(SA4_TweetCount, '/api/SA4TweetCount')
api.add_resource(SA4_TweetCountInd, '/api/SA4TweetCount/<SA4name>')
api.add_resource(City_TweetCount, '/api/CityTweetCount')
api.add_resource(City_TweetCountInd, '/api/CityTweetCount/<Cityname>')
##Sentiment data overall
api.add_resource(SA4_Senti_Overview, '/api/SA4_Senti_Overview')
api.add_resource(SA4_Senti_OverviewInd, '/api/SA4_Senti_Overview/<SA4name>')



if __name__ == '__main__':
    app.run(debug=True)