import couchdb
import json
from datetime import datetime

#connect to couchDB
def collect_server(user, password):
    try:
        couchServer = couchdb.Server('http://%s:%s@172.26.133.48:5984/' % (user, password))
        print('Couchdb is conllected')
        return couchServer
    except Exception as e:
        print(e)

def get_database(server_name, database_name):
    if database_name in server_name:
        db = server_name[database_name]
        print('get database: %s' % database_name)
        return db
    else:
        #create new database
        db = server_name.create(database_name)
        print('Database: %s not found. Created database' % database_name)
        return db


user = 'user'
password = 'pass'

couchServer = collect_server(user, password)
db = get_database(couchServer, 'tweets_dic')

old_tweet_zip = 'old_data.json.zip'
with zipfile.ZipFile(old_tweet_zip, "r") as z:
    for filename in z.namelist():
        print(filename)
        with z.open(filename) as f:
            input_data = f.read()
            data = json.loads(input_data)
            for i in range(0, len(data['docs'])):
                index = i
                string = data['docs'][index]
                db.save(string)
            print('finished upload process. end :)')
            
#######################################################################
# upload views
print('start to upload views to couchDB')
with open('CountOrSum.json') as f:
    view_1 = json.load(f)
    db.save(view_1)

with open('SummaryByRegion.json') as f:
    view_2 = json.load(f)
    db.save(view_2)
print('finished upload process. All required information is uploaded to couchDB.')
#######################################################################

