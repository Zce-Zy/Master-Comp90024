import tweepy
import json
from textblob import TextBlob
import time
import couchdb
import json
import pandas as pd
import sys


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
def getDate(string_tweet):
    data = string_tweet['created_at']
    split = data.split(' ')
    date = str(split[1]) + ' ' + str(split[2]) + ' ' + str(split[5]) + ' ' + str(split[3])
    return date


#######################################################################
# get the require information from tweets
# only consider tweet with place type == city
# get user_id (timeline), tweet id, place name, create time, and text
def get_info(tweets_v1):
    tweet_list = []
    for tweet in tweets_v1:
        tweet_dic = {}
        string = tweet._json
        try:
            if string['place']['place_type'] == 'city':
                tweet_dic['user_Id'] = string['user']['id']
                tweet_dic['id'] = string['id_str']
                tweet_dic['city_name'] = string['place']['name']
                tweet_dic['date'] = getDate(string)
                tweet_dic['place_type'] = string['place']['place_type']
                tweet_dic['text'] = string['text']
                # print(tweet_dic)
                tweet_list.append(tweet_dic)
        # handle Type Error
        except TypeError:
            pass
    return tweet_list


tweet_all_dic = {}
all_list = []
json_file = './city_7days_0523.json'
# vic: 0ec0c4fcacbd0083
#######################################################################
# harvest tweet for Victoria
count = 0
max_id = 9999999999999999999
# for i in range(500):
while True:
    try:
        tweets_v1 = api.search(q='place:0ec0c4fcacbd0083 lang:en', count=100, max_id=max_id)
        tweet_list = get_info(tweets_v1)
        # print(tweet_list)
        for j in range(0, len(tweet_list)):
            all_list.append(tweet_list[j])
        count += 1
        print("current iter #:", count)
        print("list len is:", len(all_list))
        try:
            length = len(all_list) - 1
            current_id = int(all_list[length]['id']) - 1
            # check if id is decreasing
            if current_id == max_id:
                print("no more request:reach 7 days with current_id: ", current_id)
                break
            # set the current min id as max id
            max_id = current_id
            print("max id is:", (max_id + 1))
            time.sleep(5)
        except IndexError:
            print('Index error. No record')
            break
    # handle rate limit
    except tweepy.RateLimitError as e:
        print(e)
        print('exceed limit :( sleep more than 15 mins to restart')
        # sleep 15 minutes
        time.sleep(16*60)
        print('sleep ended :)')
        continue


print("##################")
print('finish harvesting. Save to json file')
for item in range(0, len(all_list)):
    tweet_all_dic[item] = all_list[item]

with open(json_file, 'w') as f:
    json.dump(tweet_all_dic, f, indent=2)
print('All tweet saved :)')
