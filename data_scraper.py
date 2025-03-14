import requests
import json
import pandas as pd
from datetime import datetime

#Base URL for fetching Hacker New data with firebase API
base_ulr = 'https://hacker-news.firebaseio.com/v0/'
top_stories_url = 'topstories.json?print=pretty'


# Define API functions
## gets top stories
def get_top_story_ids(limit=10):
    #get story ids
    response = requests.get(f'{base_ulr}{top_stories_url}')
    print(response)
    #Check response
    if response.status_code == 200:
        json_response = response.json()
        return json_response[:limit]
    else:
        print('Failed get: Response status code {}'.format(response.status_code))
## get articles from id
def get_item_by_id(id,type='item'):
    response = requests.get(f'{base_ulr}{type}/{id}.json?print=pretty')
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        print('Failed get: Response status code {}'.format(response.status_code))
## Build dataframe from list of ids
def build_df_from_id_list(article_ids):
    #Create empty diction to store all article data
    data_list_of_dicts = []
    for id in article_ids:
        data_list_of_dicts.append(get_item_by_id(id))
    return pd.DataFrame(data_list_of_dicts)
## Function get all data and save as csv
def get_hacker_news_data(num_articles,csv_file_name):
    ids_list = get_top_story_ids(num_articles)
    df = build_df_from_id_list(ids_list)
    #This is if you want a timestamp sufix on file name. Might be useful later
    #csv_file_name = csv_file_name + '_' + str(datetime.now()).split('.')[0].replace(' ','T').replace(':','-')
    df.to_csv(f'./data/raw/{csv_file_name}',index=False)

# Get Live Hacker New Data:
## 1. enter number of articles you would like to get (up to 500 from the most recent article)
## 2. Enter a file name for csv. 
num_of_top_artciles_to_get = 5
csv_file_name = 'hn_data'
get_hacker_news_data(num_of_top_artciles_to_get,csv_file_name)