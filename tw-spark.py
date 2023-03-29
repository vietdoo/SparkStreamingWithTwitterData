from pyspark.sql import SparkSession
import os
spark_version = '3.2.0'
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.apache.kafka:kafka-clients:3.2.3 tw-spark.py' 
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:{} tw-spark.py'.format(spark_version)

spark = SparkSession.builder.appName("KafkaStream")\
        .getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "20.51.150.2:9092") \
    .option("subscribe", "my-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# xử lý dữ liệu
def write_to_csv(row):
    
    hashtag = row.value().decode("utf-8") 
    print(hashtag)

query = df.writeStream.foreach(write_to_csv).start()


query.awaitTermination()

spark.stop()
