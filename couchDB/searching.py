import tweepy
import json
from textblob import TextBlob
import time
import couchdb
import json
# import pandas as pd
from http.client import IncompleteRead as http_incompleteRead
from urllib3.exceptions import IncompleteRead as urllib3_incompleteRead
# import sys

# LZT tweeter key
consumer_key = 'syvBAqd7spC9PbV622K3UNaB6'
consumer_secret = 'IPcGyK1Op8MH1etJeVlmxOnaNg6t5zYoifSr1bOb0lxI179n3z'
access_token = '1385155978996322307-63mBdQYfKG6KEOElbh3HiPmW0XOyMH'
access_token_secret = 'BNy1fEx2I4TpKkVra491uNm5W2dlqxAhYgxnVO6UQZW89'

# ZZY tweeter key
# consumer_key ='3wAdEar8Px22CvWbhNl60yJqN'
# consumer_secret = 'Gaz6EAliDHiaKcWgPL1xMaegvnFxOxxAJPG0tPkFNAwtvnzbyA'
# access_token = '1387033033266450438-zu35I5yeHO2eKnYPACCww4kUIX1WO8'
# access_token_secret = 'Yftt0BuEyVwICOk21aAYoQYReRnkgHi8utncFszT3LFan'

# authorization of tweet API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#######################################################################
# get hours, month and year from tweets
# date process function
def monthDayYear(string_tweet):
    data = string_tweet['created_at']
    split = data.split(' ')
    time_split = split[3].split(':')
    month = split[1]
    year = split[5]
    hours = time_split[0]
    return hours, month, year


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

#######################################################################
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


#######################################################################
# get the require information from tweets
# only consider tweet with place type == city

def get_info(tweets_v1):
    # tweet_list = []
    for tweet in tweets_v1:
        string = tweet._json
        try:
            if string['place']['place_type'] == 'city':
                tweet_dic = {}
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
                tweet_dic['subjectivity'] = info[1]
                # tweet_dic['text'] = text_string
            else:
                pass
        # handle Type Error
        except TypeError:
            pass
    return tweet_dic

#######################################################################
all_list = []
# vic: 0ec0c4fcacbd0083
# harvest tweet for Victoria
max_id = 9999999999999999999
while True:
    try:
        # 10 requests per city
        tweets_v1 = api.search(q='place:0ec0c4fcacbd0083 lang:en', max_id=max_id)
        tweet_dic = get_info(tweets_v1)
        # print(tweet_dic)
        if len(tweet_dic) == 0:
            print('empty dic. pass')
            pass
        elif tweet_dic['lga_name'] == 'Unknown':
            print('Unknown lga_name. pass.')
            pass
        else:
            new_tweet_id = tweet_dic['tweet_id']
            # print(new_tweet_id)
            all_list.append(new_tweet_id)
            match = None
            for item in db.view('CountOrSum/CountTweetID', key=new_tweet_id):
                match = item
            if match is None:
                # db_id.save(id_dic)
                db.save(tweet_dic)
                print('new tweet save in db with tweet_id: ', new_tweet_id)
            else:
                print('duplicated tweet. pass with tweet_id: ', new_tweet_id)
            try:
                length = len(all_list) - 1
                current_id = int(all_list[length]) - 1
                # check if id is decreasing
                if current_id == max_id:
                    print("no more request:reach 7 days with current_id: ", current_id)
                    #################
                    #sleep
                    print('Sleep 20 mins. Sleep start.')
                    time.sleep(20 * 60)
                    print('sleep end :) reset max id')
                    max_id = 9999999999999999999
                    continue
                # set the current min id as max id
                max_id = current_id
                #print("max id is:", (max_id + 1))
                time.sleep(5)
            except IndexError:
                print('Index error. No record')
                break

    # handle rate limit
    except tweepy.RateLimitError as e:
        print(e)
        print('exceed limit :( sleep more than 15 mins to restart')
        # sleep 15 minutes
        time.sleep(16 * 60)
        print('sleep ended :)')
        continue
    except BaseException as e:
        print(e)
        time.sleep(15)
        continue
    except http_incompleteRead as e:
        print(e)
        print('http.client incomplete read')
        time.sleep(15)
        continue
    except urllib3_incompleteRead as e:
        print(e)
        print('urllib3 incomplete read')
        time.sleep(15)
        continue

    except couchdb.http.ResourceConflict as e:
        print(e)
        time.sleep(10)
        continue

    except Exception as e:
        print(e)
        print('sleep 15 mins to restart :(')
        time.sleep(15 * 60)
        print('sleep end :)')
        continue
