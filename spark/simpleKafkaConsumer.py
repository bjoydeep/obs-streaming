from __future__ import print_function

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, ArrayType,StructType,StructField



if __name__ == "__main__":


    spark = SparkSession \
        .builder \
        .appName("SimpleStreamingMetricConsumerKafka") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")    

    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092") \
    .option("subscribe", "metrics") \
    .load()

    print("Kafka data stream schema -----")
    df.printSchema()


    # Focus only the value column of the schema. That is the only one which has data
    topicDF= df.selectExpr("CAST(value AS STRING)")
    

    #kafschema = StructType([ 
    #StructField("timestamp",StringType(),True), 
    #StructField("name", StringType(), True), 
    #StructField("ignore", StringType(), True),
    #StructField("value", StringType(), True)
    #])

    #kafschema = StructType().add("timestamp", "string").add("name", "string").add("ignore", "string").add("value", "string")

    #lines.withColumn("tmp",split(col("value"),',')).\
    #withColumn("col1",col("tmp")[0]).\
    #withColumn("col2",col("tmp").getItem(1)).\
    #withColumn("col3",element_at(col("tmp"),3))
    #drop("tmp","value").\

    


    #TODO - reduce intermediate DFs - iDF, i2DF
    #TODO - filter by metric name and label name
    #TODO - set the proper units for timestamp and value
    iDF = topicDF.withColumn("tmp",split(topicDF.value," "))
    i2DF = iDF.withColumn("timestamp",iDF.tmp[0]). \
    withColumn("metric",iDF.tmp.getItem(1)). \
    withColumn("value",iDF.tmp.getItem(3))

    topicCleanDF=i2DF.select("timestamp","metric","value").filter(col("metric").contains("ALERTS") & col("metric").contains('alertstate="firing"') )
    
    print("Processed or Resultant Kafka data stream schema (with data filtered) -----")
    topicCleanDF.printSchema()

    
    topicCleanDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()


    
    

