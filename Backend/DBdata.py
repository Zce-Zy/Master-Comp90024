import pandas as pd
import couchdb
import json
couch = couchdb.Server('http://admin:password@172.26.133.251:5984')
db = couch['tweets_dic']

#Give SA4_CentralPoint Location
SA4_location = {"Ballarat" : [-37.549999, 143.850006],
                "Bendigo":[-36.757786, 144.278702],
                "Geelong":[-38.150002, 144.350006],
                "Hume":[-36.1050, 147.0253],
                "Latrobe - Gippsland":[-38.255603, 146.471993],
                "Melbourne":[-37.8136, 144.9036],
                "Mornington Peninsula":[-38.285405, 145.093449],
                "North West":[-36.716667, 142.199997],
                "Shepparton":[-36.383331, 145.399994],
                "Warrnambool and South West":[-38.3818, 142.4880],
                "Unknown":[0,0]}



##Get SA4 Tweet Count Data
def get_SA4Sum():
    SA4 = []
    for item in db.view('CountOrSum/CountTweetsSA_name', group=True, stale = "update_after"):
        dic = {"SA_name": item["key"], "Count": item["value"]}
        SA4.append(dic)
        df = pd.DataFrame(SA4)
    return df.set_index("SA_name").T

##Get City Tweet Count Data
def get_CitySum():
    SA4 = []
    for item in db.view('CountOrSum/CountTweetscity_name', group=True, stale = "update_after"):
        dic = {"City_name": item["key"], "Count": item["value"]}
        SA4.append(dic)
        df = pd.DataFrame(SA4)
    return df.set_index("City_name").T

##Get SA4 Overall sentiment data
def get_SA4_Senti_Overview():
    SA4 = []
    for item in db.view('SummaryByRegion/SentimentScoreStat_BySA4NameTime', group=True, group_level = 1,stale = "update_after"):
            lis = [item["key"][0],item["value"]['sum'],item["value"]['count'],item["value"]['sum']/item["value"]['count'],
            item["value"]['sumsqr'],SA4_location[item["key"][0]][0],SA4_location[item["key"][0]][1]]
            SA4.append(lis)
    df = pd.DataFrame(SA4)
    return df.rename(columns = {0:"SA_name",1:"Sum",2:"Cunt",3:"Average",4:"Sumsqr",5:"latitude",6:"longitude"}).set_index("SA_name").T

##get sentiratio overview
overalldata = []
for item in db.view('SummaryByRegion/Count_BySA4NameYearSentimentType', group=True,stale = "update_after"):
        lis = [item["key"][0],item["key"][1], item["key"][2], item["value"]]
        overalldata.append(lis)

##Format we want to output
def get_overview(listdata):
    new_dic = {}
    for element in listdata:
        new_dic[element[0]] = {}

    for element in listdata:
        new_dic[element[0]] [element[2]] = element[3]
    for element in listdata:
        new_dic[element[0]] ["total"] = new_dic[element[0]]["negative"] + new_dic[element[0]]["neutral"] + new_dic[element[0]]["positive"]
        new_dic[element[0]] ["neg_per"] = new_dic[element[0]]["negative"]/new_dic[element[0]] ["total"]
        new_dic[element[0]] ["neu_per"] = new_dic[element[0]]["neutral"]/new_dic[element[0]] ["total"]
        new_dic[element[0]] ["pos_per"] = new_dic[element[0]]["positive"]/new_dic[element[0]] ["total"]
        new_dic[element[0]] ["latitu"] = SA4_location[element[0]][0]
        new_dic[element[0]] ["longti"] = SA4_location[element[0]][1]

    return new_dic

def ovall():
    Lis_all = []
    for element in overalldata:
        if int(element[1]) >= 2018 :
            Lis_all.append(element)
    return get_overview(Lis_all)

def ov2019():
    Lis_2019 = []
    for element in overalldata:
        if int(element[1]) == 2019 :
            Lis_2019.append(element)
    return get_overview(Lis_2019)

def ov2020():
    Lis_2020 = []
    for element in overalldata:
        if int(element[1]) == 2020 :
            Lis_2020.append(element)
    return get_overview(Lis_2020)

def ov2021():
    Lis_2021 = []
    for element in overalldata:
        if int(element[1]) == 2021 :
            Lis_2021.append(element)
    return get_overview(Lis_2021)

###之前写的 不一定用得到的data
gfile = pd.ExcelFile('./AURData/senType.xlsx')
sheetnames = gfile.sheet_names
df1 = gfile.parse(sheet_name=gfile.sheet_names[0])
sumdata = df1.groupby('SA_name').sum()
sumdata = sumdata.T

def get_general():
    g_data = df1.to_json()
    return g_data

def get_general_2020():
    general2020 = df1.loc[df1["year"] == 2020].set_index("SA_name")
    return general2020.to_json()

def get_general_2021():
    general2021 = df1.loc[df1["year"] == 2021].set_index("SA_name")
    return general2021.to_json()
def get_individual():
    return sumdata.to_dict()