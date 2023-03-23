
import pyspark
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import os
import time

from flask import Flask, jsonify, request
from flask import render_template
from flask_cors import CORS, cross_origin

from config import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"



def send_data(tags: dict) -> None:
    url = f'http://localhost:{FLASK_PORT}/updateData'
    print(tags)
    response = requests.post(url, json=tags)

def process_row(row: pyspark.sql.types.Row) -> None:
    tags = row.asDict()
    send_data(tags)

ON_ACTIVE = False

@app.route("/ready")
@cross_origin()
def ready():
    print('Server waiting tcp now')
    global ON_ACTIVE
    ON_ACTIVE = True
    return 'ok'
    
@app.route("/stop")
@cross_origin()
def stop():
    global ON_ACTIVE
    print('Server stopping tcp now')
    ON_ACTIVE = False
    return 'ok'

def new():
    while not ON_ACTIVE:
        print(ON_ACTIVE, time.time())
        time.sleep(1)

    print('Connecting start')
   
    spark = SparkSession.builder.appName("vietdoo twitter").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("OFF")
    lines = spark.readStream.format("socket").option("host", "127.0.0.1").option("port", SOCKET_PORT).load()
    words = lines.select(explode(split(lines.value, " ")).alias("hashtag"))
    wordCounts = words.groupBy("hashtag").count()
    query = wordCounts.writeStream.foreach(process_row).outputMode('Update').start()

    while (ON_ACTIVE):
        time.sleep(1)
    query.stop()

    print('CLosing now')
    #query.awaitTermination()

@app.route("/")
@cross_origin()
def run():
    print('START SPARK')
    try:
        new()
    except KeyboardInterrupt :
        exit('\n--- FORCE STOP BY USER ---')
    except:
        print('Trying reconnect')
    return 'ok'
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = SPARK_PORT)
    

     