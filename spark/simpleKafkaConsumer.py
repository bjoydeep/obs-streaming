from __future__ import print_function

import sys

from pyspark.sql import SparkSession



if __name__ == "__main__":


    spark = SparkSession \
        .builder \
        .appName("SimpleStreamingMetricConsumerKafka") \
        .getOrCreate()

    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092") \
    .option("subscribe", "metrics") \
    .load()

    df.printSchema()



    topicDF= df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
     # Start running the query that prints the running counts to the console

    
    topicDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .start() \
    .awaitTermination() \
    
    

