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

from flask import Flask, jsonify, request
from flask import render_template
import os
from flask_cors import CORS, cross_origin

from config import *

#os.system('fuser -k 2999/tcp')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



def create_url(keyword, end_date, next_token=None, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'tweet.fields': 'id,text,author_id,geo,conversation_id,created_at,lang,entities',
                    }
    return (search_url, query_params)

def get_response(url, headers, params):
    response = requests.get(url, headers = headers, params = params)
    #print(f"Endpoint Response Code: {str(response.status_code)}")
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweet_data(next_token=None, query='corona', max_results=20):
    bearer_token = BEAR_TOKEN
    headers = {"Authorization": f"Bearer {bearer_token}"}
    keyword = f"{query} has:hashtags"
    end_time = f"{str(date.today() - timedelta(days=6))}T00:00:00.000Z"
    url: tuple = create_url(keyword, end_time, next_token=next_token, max_results=20)
    json_response = get_response(url=url[0], headers=headers, params=url[1])
    return json_response

def get_tag(tag_info: dict):
    tag = str(tag_info['tag']).strip()
    hashtag = str('#' + tag + '\n')
    #print(f"Hashtag: {hashtag.strip()}")
    return hashtag

def send_tweets_to_spark(http_resp, tcp_connection):
    data: list = http_resp["data"]
    for tweet in data:
        try:
            hashtag_list = tweet['entities']['hashtags']
            for tag_info in hashtag_list:
                # sending only hashtag
                hashtag = get_tag(tag_info)
                #print(hashtag)
                tcp_connection.send(hashtag.encode("utf-8"))
        except KeyError:
            #print("No hashtag found in current tweet, moving on...")
            continue
        except BrokenPipeError:
            print('Try to ')
            #exit("Pipe Broken, Exiting...")
        except KeyboardInterrupt:
            exit("Keyboard Interrupt, Exiting...")
        except Exception as e:
            traceback.print_exc()

ON_ACTIVE = False

@app.route("/", methods=['POST', 'OPTION'])
@cross_origin()
def real():
    send_ready = requests.get(f'{URL}:{FLASK_PORT}/clearData')
    data = request.get_json()
    prompt = data["tweet"].strip('\n')
    print(prompt)
    TCP_IP = '127.0.0.1'
    TCP_PORT = SOCKET_PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    send_ready = requests.get(f'{URL}:{SPARK_PORT}/ready')
    

    print('Send ready command to Spark')
    try:
        print("Waiting for the TCP connection...")
        no_of_pages = 3
        max_results = 30
        sleep_timer = 5
        queries = prompt.split('\n')
        conn, addr = s.accept()
        print("Connected successfully... Starting getting tweets.")
        
        for _ in range(no_of_pages):
            for query in queries:
                try:
                    print(query)
                    resp = get_tweet_data(query = query, max_results = max_results)
                    
                    #print(resp)
                    send_tweets_to_spark(http_resp = resp, tcp_connection = conn)
                    time.sleep(sleep_timer)
                except KeyboardInterrupt:
                    exit("Keyboard Interrupt, Exiting..")
                except:
                    print('cant fetch')
    except:
        print('Stopping now')
    conn.close()
    send_stop = requests.get(f'{URL}:{SPARK_PORT}/stop')

    return 'server running done'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = TW_PORT)

    