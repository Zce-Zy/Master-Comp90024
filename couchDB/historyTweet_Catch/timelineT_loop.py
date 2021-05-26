import tweepy
import json
import pandas as pd
import time

file_input= 'C:/uniMelb/ccc/assginment2/python/area/user_list_0517.csv'
file_output= 'C:/uniMelb/ccc/assginment2/python/area/user_0517_all.json'
# file_input = './area/sa4-warrnambool and south west/user_list_Warrnambool.csv'
# file_output = './area/sa4-warrnambool and south west/userTime_Warrnambool.json'

# load user list csv file
user_list = pd.read_csv(file_input)
user_list = list(user_list['userID'])

# choose 30 of them one time
# min_id = 6301
# max_id = 6500
# user_id = []
# for i in range(min_id,max_id):
#     user_id.append(user_list[i])

user_id = []
for i in range(0,len(user_list)):
    user_id.append(user_list[i])

# print(user_id)

# api auth

# account_1
API_key = 'Yrzo3I1wJa73sQyQzHWrFyz72'
API_secretKey = 'wHleYPIZaG2cn0DuUGYVpILYzN6hciibrRh1jDIJWPtFORKEEc'
access_token = '1388743775397158917-wYDgiPDSYf3fKOkudQ1oVsoWAubKNK'
access_tokenSecret = '07YQUD4p4LymDOLDcWZ0YNsTdKkIGx3nKUxeBdwaV6UcV'

# account_2
# API_key = 'O7FWHSPzL576P9tluXnxaRj3g'
# API_secretKey = '7XA9jPo7a5USW6RQq6gag0ukHHHhEm3wx5lv8RZB1NWYlqomyG'
# access_token = '1389078844330500096-SSmYoa9f0knh9IrUxGO9qsw9LZxpbD'
# access_tokenSecret = 'ng6hmWj4YHvwScSuHVrLz5LL99dQLwR7vQoSKZQbBZDeL'

# account_3
# API_key = 'vtO77uYB0i29ChyIsoqEsuuxX'
# API_secretKey = 'txztbWuEPCVsyKQYGMhGZX5YX5IxkvMFp1aOzH6FStNCnmKEWY'
# access_token = '1389930407034986499-w1Z2Npaj2VmjsFLPoFU9plZh2EbNg6'
# access_tokenSecret = 'm63TWKlAabjouVyye4INjuaAZgG3yA7qjoUIJanBSmMMF'

# account_lizzy
# API_key = 'syvBAqd7spC9PbV622K3UNaB6'
# API_secretKey = 'IPcGyK1Op8MH1etJeVlmxOnaNg6t5zYoifSr1bOb0lxI179n3z'
# access_token = '1385155978996322307-63mBdQYfKG6KEOElbh3HiPmW0XOyMH'
# access_tokenSecret = 'BNy1fEx2I4TpKkVra491uNm5W2dlqxAhYgxnVO6UQZW89'

auth = tweepy.OAuthHandler(API_key, API_secretKey)
auth.set_access_token(access_token, access_tokenSecret)
api = tweepy.API(auth)

# function area

def monthDayYear(string_tweet):
    data = string_tweet['created_at']
    split = data.split(' ')
    date = split[1] +' '+ split[2] + ' ' + split[5] + ' ' + split[3]
    return(date)

def getOneUsertweets(user):
    one_user_limit = 100
    tweets_perU = []
    tCursor = tweepy.Cursor(api.user_timeline, id=user).items(one_user_limit)
    for item in tCursor:
        tweet_dic = {}
        string = item._json
        # print(string)
        try:
            tweet_dic['id'] = string['id_str']
            tweet_dic['city_name'] = string['place']['name']
            tweet_dic['date'] = monthDayYear(string)
            tweet_dic['place_type'] = string['place']['place_type']
            tweet_dic['text'] = string['text']
            # print(tweet_dic)
            tweets_perU.append(tweet_dic)
        except TypeError:
            # print('error in key')
            pass
    return tweets_perU

# timeline by user_id

all_tweet_list = []
for user in user_id:
    try:
        user_o = getOneUsertweets(user)
        for t in user_o:
            all_tweet_list.append(t)
        print('successfully get user_info')
    except tweepy.error.TweepError as e:
        print(e)
        print('exceed limit :( sleep more than 15 mins to restart')
        # sleep 15 minutes
        time.sleep(16 * 60)
        print('sleep ended :)')
        continue
    # except tweepy.RateLimitError as e:
    #     print(e)
    #     print('exceed limit :( sleep more than 15 mins to restart')
    #     # sleep 15 minutes
    #     time.sleep(16 * 60)
    #     print('sleep ended :)')
    #     continue

# start_date = datetime.datetime(2021, 1, 1, 00, 00, 00)
# end_date = datetime.datetime(2021, 1, 31, 23, 59, 59)
# for item in tweepy.Cursor(api.user_timeline, id=test_id, since=start_date, until=end_date).items():
#     print(len(item._json))
#     print(item._json)


tweet_all_dic = {}
for i in range(0, len(all_tweet_list)):
    tweet_all_dic[i] = all_tweet_list[i]

#print(tweet_all_dic)

with open(file_output, 'w') as f:
    json.dump(tweet_all_dic, f, indent=2)


