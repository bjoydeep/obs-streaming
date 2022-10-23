# Notes

## Objectives
 Our goal is to take Prometheus style metrics, stream it to Kafka and apply streaming analytics in Spark. Very soon we would be expanding this to include key cluster events (not to be confused with alerts; alerts already come in through the metric stream) like cluster scaling, node memory pressure, cluster upgrade etc. Speaking in a more generic way - the goal is to build AI/ML/Statistical models around streaming observability data. We could stray to data at rest aka batch processing as well.
 
 The set up here is as below.

 ![](proposed_architecture.png)

 As you could easily guess, we could easily do this same flow using Prometheus RemoteWrite API instead of ACM. Pros and cons of the above two different methods are really not relevant to the objective of this repository.

 If you used a different metric stream (non-Prometheus) principles applied would be exactly the same. In the python module called in Spark - [simpleKafkaConsumer.py](spark/simpleKafkaConsumer.py) in this example - the schema as seen in `metrics` topic would need to be changed.
## Spark Streaming

We will follow [Spark Structured Streaming](https://spark.apache.org/docs/3.3.0/structured-streaming-programming-guide.html).
## Getting Started
### Prereq

For installing the pre-requistes, follow [this](InstallPreReqs.md).

### Install and Test Spark

For installing and Testing Spark, follow [this](InstallSpark.md).

### Building the Docker Driver for Spark

For building docker container for Spark Driver, follow [this](CreateSparkDockerDriver.md).

### Create a real Spark Application CR

For launching a real Spark Application, follow [this](LaunchSparkJob.md).

### Initial motivating example

For details of the intial example, follow follow [this](ParsingMetrics.md).

 