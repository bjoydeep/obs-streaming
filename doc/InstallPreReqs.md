## Prereq

Have a OpenShift (we have tested this against OpenShift cluster only thus far) cluster ready.


### Install ACM 
For downloading and installing the latest ACM release - at the time of creating this README - follow the instructions [here](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/install/installing#installing-while-connected-online).
#### Configure Observability
For configuring Observability for ACM, follow the instructions [here](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/observability/observing-environments-intro#enabling-observability).

### Install Kafka
Using [kafka.yaml](../deploy-using-acm-policy/kafka.yaml) create a `ACM Policy` to deploy Kafka. This will create:
1. Namespace kafka
1. Deploy Strimzi Operator
1. Create Kafka cluster
1. Create `metrics` topic
### Install Vector
After installing `Kafka`,install `Vector` using this [deployment](../deploy/vector.yaml). This will install:
1. Vector
1. Create required service
1. Configure it to listen for Prometheus RemoteWrite and send data to `Kafka` metrics topic.
1. Create secret called `vector` in `open-cluster-management-observability` namespace which will allow ACM Observability to send data to vector.

We have not explored [prometheus-kafka-adapter](https://github.com/Telefonica/prometheus-kafka-adapter). But this could be another viable alertnative to Vector. The metric parsing off Kafka could be simpler by leveraging some capabilities of this adapter.
#### Configure Observability to send data to Vector
Now that you have Observability enabled, you can configure the RemoteWrite endpoint to Vector as mentioned [here](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/observability/observing-environments-intro#export-metrics-to-external-endpoints).
 Note the [secret](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/observability/observing-environments-intro#creating-the-kubernetes-secret-for-external-endpoint) needed has already been created when we installed Vector. So this step can be skipped. Therefore only step needed is to change the MCO CR as explained [here](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/observability/observing-environments-intro#updating-the-multiclusterobservability-cr). For our example, it means adding the `writeStorage` section as below.
```
  storageConfig:
    ....
    ....
    writeStorage:
      - key: ep.yaml
        name: vector
```


#### Test data flow to Kafka

Now data should be flowing into `Kafka` topic `metrics`. To test this, log into the Terminal of the `kafka-brokers-cluster-kafka-*` pod created in the namespace `kafka` in your OpenShift cluster. Run this command to use the Kafka commandline consumer and you will see data flow in within maximum of 5 min.
```
/opt/kafka/bin/kafka-console-consumer.sh --topic metrics --bootstrap-server kafka-brokers-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092
```

### Install ClusterLoggingOperator

1. Install CLO on OCP 4.10 - CLO Version: `5.5.3`
1. Create [ClusterLogging CR](../deploy/clusterLogging_cr.yaml)
1. Create [ClusterLogForwarder CR](../deploy/clusterLogForwarder_cr.yaml). Notes this forwards to "internal kafka service". We will need to change it for forward to external kafka (just did not have the time!)
1. Create [KafkaTopic CR](../deploy/kafkaTopic_for_log_cr.yaml) for logs
