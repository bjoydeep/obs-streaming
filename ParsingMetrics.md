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
- split this metric stream to timestamp, metric, value format
    - timestamp: `2022-10-21T14:55:53.806Z`
    - metric: `"node_namespace_pod_container:container_cpu_usage_seconds_total:sum"{cluster="local-cluster",clusterID="5882a201-a139-4a25-8f84-dba8f8c2a9b2",namespace="openshift-apiserver-operator"}`
    - value: `0.010692756633701114`
- filter out by metric called ALERTS that are in alertstate=firing.

More involved processing follows.
