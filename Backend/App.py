#User Ziyang Zhang
#Restful-API
#2020/05/11


from flask import Flask
from flask_restful import abort, Api, Resource
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


#//TODO
##Have not change the data rigth now
##Sentiment data overall
api.add_resource(Lga_Senti_Overview, '/api/Lga_Senti_Overview')
api.add_resource(Lga_Senti_OverviewInd, '/api/Lga_Senti_Overview/<Lganame>')



if __name__ == '__main__':
    app.run(debug=True)