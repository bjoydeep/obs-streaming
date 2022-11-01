from __future__ import print_function

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, ArrayType,StructType,StructField



if __name__ == "__main__":


    spark = SparkSession \
        .builder \
        .appName("SimpleStreamingLogConsumerKafka") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")    

    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092") \
    .option("subscribe", "logs") \
    .load()

    print("Kafka data stream schema -----")
    df.printSchema()


    # Focus only the value column of the schema. That is the only one which has data
    topicDF= df.selectExpr("CAST(value AS STRING)")
    
    #Extracting Events only.
    topicCleanDF=topicDF.select("value") \
    .filter(col("value").contains('"namespace_name":"openshift-logging"') & col("value").contains('"container_name":"kube-eventrouter"'))
    
    #print("Processed or Resultant Kafka data stream schema (with data filtered) -----")
    topicCleanDF.printSchema()

    
    topicCleanDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()


    
    

