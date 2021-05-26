from textblob import TextBlob
import json

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

import pandas as pd
sa4_data = pd.read_csv('city_LGA.csv')
def match_lgaLocation(city_name):
    sa4_location = sa4_data[sa4_data['city_name']==city_name]['LGA_name']
    if len(sa4_location) == 0:
        sa4_location = 'Unknown'
    else:
        sa4_location = sa4_location.to_string(index = False)
    return(sa4_location)



filtered_list = []
#filtering process
from tqdm import tqdm
with open ('result_all_1_20_cityCollection_7523_0523added.json', "r") as f:
    data = json.load(f)
    for i in tqdm(range(0, len(data))):
        filter_info = {}
        index = str(i)
        string = data[index]
        text_string = string['text']
        score_polarity, score_subjectivity, type_sentiment = sentiment_score(text_string)
        filter_info['tweet_id'] = string['id']
        split_date = string['date'].split()
        split_time = split_date[3].split(":")
        hours = split_time[0]
        filter_info['hours'] = hours
        filter_info['month'] = split_date[0]
        filter_info['year'] = split_date[2]
        city = string['city_name']
        filter_info['city_name'] = city
        filter_info['lga_name'] = match_lgaLocation(city)
        filter_info['sentiment_type'] = type_sentiment
        filter_info['sentiment_score'] = score_polarity
        filter_info['subjectivity_score'] = score_subjectivity
#         filter_info['text'] = string['text']
        if filter_info['lga_name'] == "Unknown":
            pass
        else:
            filtered_list.append(filter_info)

        
filtered_list_1 = {}
filtered_list_1['docs'] = filtered_list

with open('old_data.json', 'w') as f:
    json.dump(filtered_list_1, f, indent = 2)
