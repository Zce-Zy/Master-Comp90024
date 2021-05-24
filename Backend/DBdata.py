import pandas as pd
import couchdb
import json
import csv
import re
import numpy as np

couch = couchdb.Server('http://user:pass@127.0.0.1:5984')
db = couch['wh_db']
city_location = pd.read_csv("AURData/location.csv")


##Get lgaOverall sentiment data
def get_lga_Senti_Overview():
    SA4 = []
    for item in db.view('SummaryByRegion/SentimentScoreStat_BylgaNameTime', group=True, group_level = 1,stale = "update_after"):
        lis = [item["key"][0].strip('\\t'),item["value"]['sum'],item["value"]['count'],item["value"]['sum']/item["value"]['count'],item["value"]['sumsqr']]
        SA4.append(lis)
    df = pd.DataFrame(SA4)
    df.rename(columns = {0:"Lga_name",1:"Sum",2:"Cunt",3:"Average",4:"Sumsqr",}).set_index("Lga_name").T

##get sentiratio overview
overalldata = []
for item in db.view('SummaryByRegion/Count_BylgaNameYearSentimentType', group=True,stale = "update_after"):
        lis = [item["key"][0].strip('\\t'),item["key"][1], item["key"][2], item["value"]]
        overalldata.append(lis)

##Format we want to output
def get_overview(listdata):
    new_dic = {}
    for element in listdata:
        new_dic[element[0]] = {}

    for element in listdata:
        new_dic[element[0]] ["negative"] = 0
        new_dic[element[0]] ["positive"] = 0
        new_dic[element[0]] ["neutral"] = 0
    for element in listdata:
        new_dic[element[0]] [element[2]] += element[3]
    for element in listdata:
        new_dic[element[0]] ["total"] = new_dic[element[0]]["negative"] + new_dic[element[0]]["neutral"] + new_dic[element[0]]["positive"]
        new_dic[element[0]] ["neg_per"] = new_dic[element[0]]["negative"]/new_dic[element[0]] ["total"]
        new_dic[element[0]] ["neu_per"] = new_dic[element[0]]["neutral"]/new_dic[element[0]] ["total"]
        new_dic[element[0]] ["pos_per"] = new_dic[element[0]]["positive"]/new_dic[element[0]] ["total"]
    return new_dic


def ovall():
    Lis_all = []
    for element in overalldata:
        if int(element[1]) >= 2018 :
            Lis_all.append(element)
    return get_overview(Lis_all)


#OverView of Individual LGA
def get_crimeLis(name):
    #Data Process&Clean
    df = pd.read_csv('AURData/crime_rate.csv')
    df["Local Government Area"] = df["Local Government Area"].str.lstrip()
    df = df.drop(["Year ending","Police Region"],axis=1)
    ##Process Data only remain what we wan
    df = df.fillna(0)
    df['Offence Count'] = df['Offence Count'].str.replace(",","").astype(int)
    df['Rate per 100,000 population'] = df['Rate per 100,000 population'].str.replace(",","").astype(float)
    df = df.fillna(0)
    ##Get the data we want in particular City
    datalis = df[df["Local Government Area"] == name].groupby("Year").sum().reset_index().values.tolist()
    
    #Create the List of dic data
    crimeRate = []
    for element in datalis:
        dic = {}
        dic["year"] = int(element[0])
        dic["totalCount"] = element[1]
        dic["ratePer100000population"] = element[2]
        crimeRate.append(dic)
    return crimeRate

##get un employment data
def get_unedata():
    with open('AURData/unemp_rate.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    total = {}
    year = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    quater = [1,2,3,4]
    for element in data:
        i = 2
        name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", element[0]).rstrip()
        total[name] = []
        for num in year:
            onequt = {}
            onequt["year"] = num
            onequt["data"] = {}
            for qut in quater:
                onequt["data"]["quater"] = qut
                onequt["data"]["rate"] = element[i]
                z = onequt["data"].copy()
                a = onequt.copy()
                a["data"] = z
                i+=1
                total[name].append(a)
                
    total.pop("LGA")
    return total

##Format we want to output
def get_indicity(listdata):
    new_dic = {}
    for element in listdata:
        new_dic[element[0]] = {}

    for element in listdata:
        new_dic[element[0]] ["negative"] = 0
        new_dic[element[0]] ["positive"] = 0
        new_dic[element[0]] ["neutral"] = 0
    for element in listdata:
        new_dic[element[0]] [element[2]] += element[3]
    return new_dic

##Over view for one city
def get_oneCity(name):
    overview = {}
    for key,value in get_indicity(overalldata).items():
        if name in key:
            overview["Sentiment"] = value
    
    #overview["crimeRates"] = get_crimeLis(name)
    for key,value in get_unedata().items():
        if key in name:
            name = key
            break
    overview["unemploymentRates"] = get_unedata()[name]
    overview["crimeRates"] = get_crimeLis(name)
    return overview

##get un employment data
def get_untotal():
    with open('AURData/unemp_rate.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
    for element in data:
        element.pop(0)
        element.pop(0)
    final = [float(0)]*40
    final = np.array(final)
    for element in data:
        list_new = []
        for num in element:
            if num == "-":
                num =0
            list_new.append(float(num))  
        final +=np.array(list_new)
    rt = final/len(data)
    total = []
    year = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    quater = [1,2,3,4]
    i=0
    for num in year:
        onequt = {}
        onequt["year"] = num
        onequt["data"] = {}
        for qut in quater:
            onequt["data"]["quater"] = qut
            onequt["data"]["rate"] = rt[i]
            z = onequt["data"].copy()
            a = onequt.copy()
            a["data"] = z
            i+=1
            total.append(a)
                
    return total

def get_count_total():
    ovd = {"positive":0,"negative":0,"neutral":0}
    for element in overalldata:
        if element[2] == "positive":
            ovd['positive'] += int(element[3])
        if element[2] == "negative":
            ovd['negative'] += int(element[3])
        if element[2] == "neutral":
            ovd['neutral'] += int(element[3])
    return ovd

##get over all
def get_ovlga():
    overview = {}
    overview["Sentiment"] = get_count_total()
    overview["unemploymentRates"] = get_unedata()
    overview["crimeRates"] = get_crimeLis("Total")
    return overview

