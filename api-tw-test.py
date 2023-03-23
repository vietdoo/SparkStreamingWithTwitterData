import socket
import sys
import requests
import requests_oauthlib
import json
import socket
import traceback
import time
from datetime import date
from datetime import timedelta

def create_url(keyword, end_date, next_token=None, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'tweet.fields': 'id,text,author_id,geo,conversation_id,created_at,lang,entities',
                    }
    return (search_url, query_params)

def get_response(url, headers, params):
    response = requests.get(url, headers = headers, params = params)
    print(f"Endpoint Response Code: {str(response.status_code)}")
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweet_data(next_token=None, query='iphone', max_results=20):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKZUjAEAAAAAFPb8d%2BSCK7rMJ6rUuoJ06bSujGk%3DjbCUjBczxCmlfTbaGoTeuC8pDNvcU4c7BuyTRC743UOXcnT55h'
    headers = {"Authorization": f"Bearer {bearer_token}"}
    keyword = f"{query} lang:en has:hashtags"
    end_time = f"{str(date.today() - timedelta(days=6))}T00:00:00.000Z"
    url: tuple = create_url(keyword, end_time, next_token=next_token, max_results=20)
    json_response = get_response(url=url[0], headers=headers, params=url[1])
    return json_response

print(get_tweet_data())