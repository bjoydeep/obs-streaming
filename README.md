# Notes

## Objectives
 Our goal is to take Prometheus style metrics, stream it to Kafka and apply streaming analytics in Spark. We are also looking at key cluster events (not to be confused with alerts; alerts already come in through the metric stream) like cluster scaling, node memory pressure, cluster upgrade etc. Speaking in a more generic way - the goal is to build AI/ML/Statistical models around streaming observability data. We could stray to data at rest aka batch processing as well. If you are in a TLDR; mode and want to understand more about the ouput of the motivating example, look [below](#Initial-motivating-example)
 
 The data flow set up as implemented by the code here is as below.

 ![](doc/images/implemented_architecture.png)

 As you could easily guess, we could easily do this same flow using Prometheus RemoteWrite API instead of ACM. Pros and cons of the above two different methods are really not relevant to the objective of this repository.

 If you used a different metric stream (non-Prometheus) principles applied would be exactly the same. In the python module called in Spark - [simpleKafkaConsumer.py](spark/streaming/simpleKafkaLogConsumer.py) in this example - the schema as seen in `metrics` topic would need to be changed.

 So, a data flow like shown below could be achieved very easily. ![](doc/images/possible_architecture.png)

## Spark Streaming

We will follow [Spark Structured Streaming](https://spark.apache.org/docs/3.3.0/structured-streaming-programming-guide.html).
## Getting Started
### Prereq

For installing the pre-requistes, follow [this](doc/InstallPreReqs.md).

### Install and Test Spark

For installing and Testing Spark, follow [this](doc/InstallSpark.md).

### Building the Docker Driver for Spark

For building docker container for Spark Driver, follow [this](doc/CreateSparkDockerDriver.md).

### Create a real Spark Application CR

For launching a real Spark Application, follow [this](doc/LaunchSparkJob.md).

### Initial motivating example

For details of the intial example, follow [this](doc/ParsingMetrics.md).

 