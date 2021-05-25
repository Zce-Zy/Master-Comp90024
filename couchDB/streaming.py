import tweepy
import pandas as pd
from textblob import TextBlob
import couchdb
import json
import sys
import time
import http.client
from http.client import IncompleteRead as http_incompleteRead
from urllib3.exceptions import IncompleteRead as urllib3_incompleteRead

###################################################################
# account_3
API_key = 'vtO77uYB0i29ChyIsoqEsuuxX'
API_secretKey = 'txztbWuEPCVsyKQYGMhGZX5YX5IxkvMFp1aOzH6FStNCnmKEWY'
access_token = '1389930407034986499-w1Z2Npaj2VmjsFLPoFU9plZh2EbNg6'
access_tokenSecret = 'm63TWKlAabjouVyye4INjuaAZgG3yA7qjoUIJanBSmMMF'

####################################################################
# Auth
auth = tweepy.OAuthHandler(API_key, API_secretKey)
auth.set_access_token(access_token, access_tokenSecret)
api = tweepy.API(auth)

####################################################################

# match SA4 function
# sa4_data = pd.read_csv('sa4-locationFiltering.csv')
# def match_sa4Location(city_name):
#     sa4_location = sa4_data[sa4_data['city'] == city_name]['sa4']
#     if len(sa4_location) == 0:
#         sa4_location = 'Unknown'
#     else:
#         sa4_location = sa4_location.to_string(index=False)
#     return (sa4_location)

lga_data = pd.read_csv('city_LGA.csv')
def match_lgaLocation(city_name):
    lga_location = lga_data[lga_data['city_name'] == city_name]['LGA_name']
    if len(lga_location) == 0:
        lga_location = 'Unknown'
    else:
        lga_location = lga_location.to_string(index = False)
    return lga_location



# date process function
def monthDayYear(string_tweet):
    data = string_tweet['created_at']
    split = data.split(' ')
    time_split = split[3].split(':')
    month = split[1]
    year = split[5]
    hours = time_split[0]
    return hours, month, year


# emotion process
def sentiment_score(text_string):
    analysis = TextBlob(text_string)
    score_polarity = analysis.sentiment.polarity
    score_subjectivity = analysis.sentiment.subjectivity
    type_sentiment = 'neutral'
    if score_polarity > 0:
        type_sentiment = 'positive'
    elif score_polarity < 0:
        type_sentiment = 'negative'
    return score_polarity, score_subjectivity, type_sentiment


# object process
# only consider tweet with place type == city
def objectProcess(string):
    try:
        tweet_dic = {}
        if string['place']['place_type'] == 'city':
            tweet_dic['tweet_id'] = string['id_str']
            tweet_time = monthDayYear(string)
            tweet_dic['hours'] = tweet_time[0]
            tweet_dic['month'] = tweet_time[1]
            tweet_dic['year'] = tweet_time[2]
            city_name = string['place']['name']
            tweet_dic['city_name'] = city_name
            tweet_dic['lga_name'] = match_lgaLocation(city_name)
            text_string = string['text']
            info = sentiment_score(text_string)
            tweet_dic['sentiment_type'] = info[2]  # type_sentiment
            tweet_dic['sentiment_score'] = info[0]  # sentiment_score
            tweet_dic['subjectivity'] = info[1]  # subjectivity
            # tweet_dic['text'] = text_string
        else:
            pass
    except TypeError:
        pass
    return tweet_dic


####################################################################
# couchdb connection

def collect_server(user, password):
    try:
        couchServer = couchdb.Server('http://%s:%s@172.26.129.241:5984/' % (user, password))
        print('Couchdb is conllected')
        return couchServer
    except Exception as e:
        print(e)
        print('unable to connect to couchdb server. Check internet')


def get_database(server_name, database_name):
    try:
        if database_name in server_name:
            db = server_name[database_name]
            print('get database: %s' % database_name)
            return db
        else:
            print('database not exist.')
            # db = server_name.create(database_name)
            # print('Database: %s not found. Created database' % database_name)
            # return db
    except Exception as e:
        print(e)
        print('Unable to get')


user = 'admin'
password = '9988'
db_name = 'tweets_dic'
couchServer = collect_server(user, password)
db = get_database(couchServer, db_name)

##########################################################################

class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            string = json.loads(data)
            tweet_dic = objectProcess(string)
            # print(tweet_dic)
            # the tweet does not satify condition: i.e. no city
            if len(tweet_dic) == 0:
                print('empty dic. pass')
                pass
            elif tweet_dic['lga_name'] == 'Unknown':
                print('Unknown lga_name. pass.')
                pass
            else:
                new_tweet_id = tweet_dic['tweet_id']
                print(new_tweet_id)
                match = None
                for item in db.view('CountOrSum/CountTweetID', key=new_tweet_id):
                    match = item
                if match is None:
                    # db_id.save(id_dic)
                    db.save(tweet_dic)
                    print('new tweet save in db with tweet_id: ', new_tweet_id)
                else:
                    print('duplicated tweet. pass with tweet_id: ', new_tweet_id)
            return True

        #handleing errors
        except BaseException as e:
            print(e)
            time.sleep(15)
            return True

        except couchdb.http.ResourceConflict as e:
            print(e)
            time.sleep(10)
            return True

        except http_incompleteRead as e:
            print(e)
            print('http.client incomplete read')
            time.sleep(15)
            return True

        except urllib3_incompleteRead as e:
            print(e)
            print('urllib3 incomplete read')
            time.sleep(15)
            return True

    def on_limit(self, status):
        print("Rate Limit Has Exceeded, Sleep for more than 15 Mins")
        time.sleep(16 * 60)
        return True

    def on_timeout(self):
        print('live stream time out')
        time.sleep(10)
        return True

myStreamListener = MyStreamListener()
while True:
    try:
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(locations=[140.9208, -39.1876, 150.0834, -33.9502], languages=['en'])
    except Exception as e:
        print(e)
        pass
