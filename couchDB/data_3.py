import couchdb
import json
# from datetime import datetime

#connect to couchDB
def collect_server(user, password):
    try:
        couchServer = couchdb.Server('http://%s:%s@172.26.129.241:5984/' % (user, password))
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


user = 'admin'
password = '9988'

couchServer = collect_server(user, password)
db = get_database(couchServer, 'tweets_dic')

old_tweet_file_3 = '/home/ubuntu/comp90024/Master-Comp90024-main/couchDB/old_data_3.json'


with open(old_tweet_file_3) as f:
    data = json.load(f)
    print('start upload tweets')
    for i in range(0, len(data['docs'])):
        index = i
        string = data['docs'][index]
        db.save(string)
