## Install CLO on OCP 4.10
- CLO Version: `5.5.3`

### ClusterLogging
- Note the names is always instance
- Note unless the collection and forwarder is added, fluentd is not installed and neither does it try to forward
```
apiVersion: logging.openshift.io/v1
kind: ClusterLogging
metadata:
  name: instance
  namespace: openshift-logging
spec:
  collection:
    logs:
      type: fluentd
  forwarder:
    fluentd:
      buffer:
        chunkLimitSize: 500k
  managementState: Managed
```

### ClusterLogForwarder
- Note the name is always instance.
```
apiVersion: logging.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: instance
  namespace: openshift-logging
spec:
  outputs:
    - name: remote-kafka
      type: kafka
      url: >-
        http://kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092/logs
  pipelines:
    - inputRefs:
        - infrastructure
      name: enable-log-store
      outputRefs:
        - remote-kafka
```
### Log topic
- Note max.message.bytes. This is dependent on strimzi version
```
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  labels:
    strimzi.io/cluster: kafka-brokers-cluster
  name: logs
  namespace: kafka
spec:
  config:
    max.message.bytes: '536870912'
  partitions: 1
  replicas: 1
  topicName: logs
```

### Kafka message formats

```
sh-4.2$ /opt/kafka/bin/kafka-topics.sh --describe --topic logs --bootstrap-server kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092
Topic: logs     PartitionCount: 1       ReplicationFactor: 1    Configs: message.format.version=2.7-IV2,max.message.bytes=536870912
        Topic: logs     Partition: 0    Leader: 1       Replicas: 1     Isr: 1
sh-4.2$ /opt/kafka/bin/kafka-topics.sh --describe --topic metrics --bootstrap-server kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092
Topic: metrics  PartitionCount: 1       ReplicationFactor: 1    Configs: message.format.version=2.7-IV2
        Topic: metrics  Partition: 0    Leader: 2       Replicas: 2     Isr: 2
```

## To Launch SparkJob

(base) ➜  spark ./bin/spark-submit \
--master k8s://https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443 \
--deploy-mode cluster \
--conf spark.kubernetes.namespace=default \
--conf spark.app.name=spark-kafka-jb \
--conf spark.kubernetes.driver.pod.name=spark-kafka-jb-driver \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.0.1,org.apache.commons:commons-pool2:2.6.2 \
--conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest \
--conf spark.kubernetes.container.image.pullPolicy=Always \
--conf spark.kubernetes.submission.waitAppCompletion=false \
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-kafka-jb \
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark \
--conf spark.driver.cores=1 \
--conf spark.kubernetes.driver.limit.cores=1200m \
--conf spark.driver.memory=512m \
--conf spark.kubernetes.driver.label.version=3.0.1 \
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-kafka-jb \
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true \
--conf spark.executor.instances=1 \
--conf spark.executor.cores=1 \
--conf spark.executor.memory=512m \
--conf spark.kubernetes.executor.label.version=3.0.1 \
-v local:///opt/spark/work-dir/simpleLogConsumer.py

