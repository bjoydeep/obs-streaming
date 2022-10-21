# Notes

## Objectives
 Our goal is to take Prometheus style metrics, stream it to Kafka and apply streaming analytics in Spark. The set up here is as below.

 As you could easily guess, we could easily do this same flow using Prometheus RemoteWrite API instead of ACM. Pros and cons of the above 2 are really not relevant to the objective of this repository.

 If you used a different metric stream (non-Prometheus) principles applied would be exactly the same. In the python module called in Spark - `simpleKafkaConsumer.py` in this example - the schema as seen in `metrics` topic would need to be changed.
### Prereq

For installing the pre-requistes, follow [this](https://github.com/bjoydeep/obs-streaming/blob/main/InstallPreReqs.md).

### Install and Test Spark

For installing and Testing Spark, follow [this](https://github.com/bjoydeep/obs-streaming/blob/main/InstallSpark.md).

### Building the Docker Driver for Spark

For building docker container for Spark Driver, follow [this](https://github.com/bjoydeep/obs-streaming/blob/main/CreateSparkDockerDriver.md).

### Create a real Spark Application CR

For launching a real Spark Application, follow [this](https://github.com/bjoydeep/obs-streaming/blob/main/LaunchSparkJob.md).

### Spark Streaming

We will follow [Spark Structured Streaming](https://spark.apache.org/docs/3.3.0/structured-streaming-programming-guide.html) in this repository. 