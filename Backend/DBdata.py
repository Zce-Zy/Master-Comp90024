import pandas as pd
import couchdb

# couch =couchdb.Server('https://user:pass@localhost:5984/')

# db = couch['twitter']

# rows = db.view('_all_docs', include_docs = True)

# data = [row['doc'] for row in rows]

# df = pd.DataFrame(data)

# print(df.head())
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