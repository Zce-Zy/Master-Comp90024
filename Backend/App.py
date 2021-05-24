#User Ziyang Zhang
#Restful-API
#2020/05/11


from flask import Flask, render_template
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

# render the index.html
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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


##Have not change the data rigth now
##Sentiment data overall
api.add_resource(Lga_Senti_Overview, '/api/Lga_Senti_Overview')
api.add_resource(Lga_Senti_OverviewInd, '/api/Lga_Senti_Overview/<Lganame>')



if __name__ == '__main__':
    app.run(debug=True)