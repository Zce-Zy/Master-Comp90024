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

Lgadata = DBdata.ovall()
##Import AUR-Labor-Data
#Labdata = pd.read_csv('./AURData/Labour.csv')

#set SA_4 return if not exit
def abort_if_notexit(Lganame):
    if Lganame not in Lgadata:
        abort(404, message="Can not find {} data".format(Lganame))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Group25 Data API</h1><p>This site is a prototype API for Tweet Data.</p>"

@app.route('/api/overview', methods=['GET'], endpoint = "overview")
def get_data():
        return Lgadata


##get general2019
class General2019(Resource):
    def get(self):
        reload(DBdata)
        data = json.dumps(DBdata.ov2019())
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
    def get(self, Lganame):
        abort_if_notexit(Lganame)
        return DBdata.ovall()[Lganame]

##Get LGA_Count
class LGA_TweetCount(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_lgaCount()
        return data

class LGA_TweetCountInd(Resource):
    def get(self, LGAname):
        reload(DBdata)
        abort_if_notexit(LGAname)
        data = DBdata.get_lgaCount()
        return data[LGAname]

##Get City Tweet Count
class City_TweetCount(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_CityCount()
        return data.to_json()

class City_TweetCountInd(Resource):
    def get(self, CityName):
        reload(DBdata)
        data = DBdata.get_CityCount().to_dict()
        return data[CityName]

#Get Citydata with Location
class City_Location(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_Citylocation()
        return data


#Lga Sentiment data
class Lga_Senti_Overview(Resource):
    def get(self):
        reload(DBdata)
        data = DBdata.get_ovlga()
        return data

class Lga_Senti_OverviewInd(Resource):
    def get(self, Lganame):
        reload(DBdata)
        data = DBdata.get_oneCity(Lganame)
        return data




#set Api
##Get count of senttype (Tested not add location)
api.add_resource(General, '/api/overview')
api.add_resource(General2019,'/api/overview2019')
api.add_resource(General2020,'/api/overview2020')
api.add_resource(General2021,'/api/overview2021')     
api.add_resource(individual, '/api/overview/<Lganame>')
##From DB_tweetcount Get some count

#Return LGA Name & Tweet Count (Tested)
api.add_resource(LGA_TweetCount, '/api/LGATweetCount')
#Return one LGA Name & Tweet Count(Tested)
api.add_resource(LGA_TweetCountInd, '/api/LGATweetCount/<LGAname>')
#Return City Name & Tweet Count(Tested no location)
api.add_resource(City_TweetCount, '/api/CityTweetCount')
#Return One City Name & Tweet Count
api.add_resource(City_TweetCountInd, '/api/CityTweetCount/<Cityname>')
#Return city data with Location(Tested with Location)
api.add_resource(City_Location, '/api/CityTweetLocation')

#//TODO
##Have not change the data rigth now
##Sentiment data overall
api.add_resource(Lga_Senti_Overview, '/api/Lga_Senti_Overview')
api.add_resource(Lga_Senti_OverviewInd, '/api/Lga_Senti_Overview/<Lganame>')



if __name__ == '__main__':
    app.run(debug=True)