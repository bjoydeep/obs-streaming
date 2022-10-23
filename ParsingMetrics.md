### Metric format on Kafka:

#### Examples
```
2022-10-21T14:50:43.433Z workqueue_queue_duration_seconds_bucket{apiserver="kube-apiserver",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",endpoint="https",instance="10.0.169.137:6443",job="apiserver",le="1e-07",name="non_structural_schema_condition_controller",namespace="default",service="kubernetes"} = 0
```
```
2022-10-21T14:55:53.806Z "node_namespace_pod_container:container_cpu_usage_seconds_total:sum"{cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",namespace="openshift-apiserver-operator"} = 0.010692756633701114
```

#### Initial motivating example

In the initial motivating example [simpleKafkaConsumer.py](spark/simpleKafkaConsumer.py) we :
- split this stream to timestamp, metric, value format
    - timestamp: `2022-10-21T14:55:53.806Z`
    - metric: `"node_namespace_pod_container:container_cpu_usage_seconds_total:sum"{cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",namespace="openshift-apiserver-operator"}`
    - value: `0.010692756633701114`
- filter out by metric called ALERTS that are in alertstate=firing.

Concretely, when you run this initial example you will see `only alerts that are firing now` - ie which is happening currently. You will see output which looks like as below:
```
Kafka data stream schema -----
root
 |-- key: binary (nullable = true)
 |-- value: binary (nullable = true)
 |-- topic: string (nullable = true)
 |-- partition: integer (nullable = true)
 |-- offset: long (nullable = true)
 |-- timestamp: timestamp (nullable = true)
 |-- timestampType: integer (nullable = true)

Processed or Resultant Kafka data stream schema (with data filtered) -----
root
 |-- timestamp: string (nullable = true)
 |-- metric: string (nullable = true)
 |-- value: string (nullable = true)

2022-10-23 15:01:50,893 WARN streaming.StreamingQueryManager: Temporary checkpoint location created which is deleted normally when the query didn't fail: /tmp/temporary-945417e7-2890-4394-bf55-0690ede2176a. If it's required to delete it under any circumstances, please set spark.sql.streaming.forceDeleteTempCheckpointLocation to true. Important to know deleting temp checkpoint folder is best effort.
-------------------------------------------
Batch: 0
-------------------------------------------
+---------+------+-----+
|timestamp|metric|value|
+---------+------+-----+
+---------+------+-----+

-------------------------------------------
Batch: 1
-------------------------------------------
+---------+------+-----+
|timestamp|metric|value|
+---------+------+-----+
+---------+------+-----+

-------------------------------------------
Batch: 2
-------------------------------------------
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|timestamp               |metric                                                                                                                                                                                                                                                                                                                                                                                                                               |value|
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|2022-10-23T15:05:11.586Z|ALERTS{alertname="UpdateAvailable",alertstate="firing",channel="stable-4.10",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",severity="info",upstream="<default>"}                                                                                                                                                                                                                              |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="telemeter-client",namespace="openshift-monitoring",service="telemeter-client",severity="warning"}                                                                                                                                                                                        |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="alertmanager-main",namespace="openshift-monitoring",service="alertmanager-main",severity="warning"}                                                                                                                                                                                      |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="grafana",namespace="openshift-monitoring",service="grafana",severity="warning"}                                                                                                                                                                                                          |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="thanos-querier",namespace="openshift-monitoring",service="thanos-querier",severity="warning"}                                                                                                                                                                                            |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="prometheus-k8s-thanos-sidecar",namespace="openshift-monitoring",service="prometheus-k8s-thanos-sidecar",severity="warning"}                                                                                                                                                              |1    |
|2022-10-23T15:05:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="prometheus-k8s",namespace="openshift-monitoring",service="prometheus-k8s",severity="warning"}                                                                                                                                                                                            |1    |
|2022-10-23T15:05:28.101Z|ALERTS{alertname="Watchdog",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",namespace="openshift-monitoring",severity="none"}                                                                                                                                                                                                                                               |1    |
|2022-10-23T15:05:35.273Z|ALERTS{alertname="SimpleContentAccessNotAvailable",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",condition="SCANotAvailable",endpoint="metrics",instance="10.0.150.45:9099",job="cluster-version-operator",name="insights",namespace="openshift-cluster-version",pod="cluster-version-operator-86d76b9b7d-hj6tr",reason="NotFound",service="cluster-version-operator",severity="info"}|1    |
|2022-10-23T15:05:39.896Z|ALERTS{alertname="AlertmanagerClusterDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",namespace="openshift-monitoring",service="alertmanager-main",severity="warning"}                                                                                                                                                                                                 |1    |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+

-------------------------------------------
Batch: 3
-------------------------------------------
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|timestamp               |metric                                                                                                                                                                                                                                                                                                                                                                                                                               |value|
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|2022-10-23T15:10:11.586Z|ALERTS{alertname="UpdateAvailable",alertstate="firing",channel="stable-4.10",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",severity="info",upstream="<default>"}                                                                                                                                                                                                                              |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="telemeter-client",namespace="openshift-monitoring",service="telemeter-client",severity="warning"}                                                                                                                                                                                        |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="alertmanager-main",namespace="openshift-monitoring",service="alertmanager-main",severity="warning"}                                                                                                                                                                                      |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="grafana",namespace="openshift-monitoring",service="grafana",severity="warning"}                                                                                                                                                                                                          |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="thanos-querier",namespace="openshift-monitoring",service="thanos-querier",severity="warning"}                                                                                                                                                                                            |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="prometheus-k8s-thanos-sidecar",namespace="openshift-monitoring",service="prometheus-k8s-thanos-sidecar",severity="warning"}                                                                                                                                                              |1    |
|2022-10-23T15:10:24.434Z|ALERTS{alertname="TargetDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",job="prometheus-k8s",namespace="openshift-monitoring",service="prometheus-k8s",severity="warning"}                                                                                                                                                                                            |1    |
|2022-10-23T15:10:28.101Z|ALERTS{alertname="Watchdog",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",namespace="openshift-monitoring",severity="none"}                                                                                                                                                                                                                                               |1    |
|2022-10-23T15:10:35.273Z|ALERTS{alertname="SimpleContentAccessNotAvailable",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",condition="SCANotAvailable",endpoint="metrics",instance="10.0.150.45:9099",job="cluster-version-operator",name="insights",namespace="openshift-cluster-version",pod="cluster-version-operator-86d76b9b7d-hj6tr",reason="NotFound",service="cluster-version-operator",severity="info"}|1    |
|2022-10-23T15:10:39.896Z|ALERTS{alertname="AlertmanagerClusterDown",alertstate="firing",cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",instance="",namespace="openshift-monitoring",service="alertmanager-main",severity="warning"}                                                                                                                                                                                                 |1    |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+

-------------------------------------------
Batch: 4
-------------------------------------------
+---------+------+-----+
|timestamp|metric|value|
+---------+------+-----+
+---------+------+-----+

```

More involved processing follows. However, if you are wondering at the art of possible now, read [Spark Structured Streaming](https://spark.apache.org/docs/3.3.0/structured-streaming-programming-guide.html)
