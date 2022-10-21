## Install and Test Spark

For background knowledge, or those familiar with Spark but in a non-Kubernetes environment, [Running Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html) is an excellent reference material. Infact this is a must for understanding the steps below.

Spark can be installed in at least 2 different ways for the scenarios below. 
1. You can install [Spark Operator](#Spark-Operator-Install). This will allow us to launch a spark job by directly creating a CR. We have had some success with this. Launching complex jobs which require Kafka jars in classpath etc have failed. This looks like some errors related to permissions - we will be figuring this out in the near future.
1. You can install [Spark locally on your laptop](#Spark-Install-in-the-laptop). Then you can lauch spark-submit from your machine pointing it out to a kube-api server. This has worked out well as shown [here](LaunchSparkJob.md#Create-a-real-Spark-Application-by-submitting-to-a-local-Spark-install).

#### Spark Install in the laptop
Follow these simple steps to get Spark running on your macOS laptop.
1. Follow [Download Spark](https://spark.apache.org/downloads.html) to get it onto your laptop.
1. Untar it to /opt/spark
    ```
    tar -xzf spark-*.tgz
    mv spark-* /opt/spark

    ```
    _Substitute * with details of your spark image_
1. Install Java Runtime JRE
    ```
    brew install java
    ```
1. Install Apache Maven
    ```
    brew install maven
    ```
1. Add path and classpath
    _Not sure if this all is needed, but nevertheless :_
    
    Edit ~/.zshrc and add
    ```
    export SPARK_HOME=/opt/spark
    export PATH=＄SPARK_HOME/bin:＄PATH
    export JAVA_HOME="/usr/local/Cellar/openjdk/19/libexec/openjdk.jdk/Contents/Home
    ```
1. Make sure you have python 3.9 (for the Spark Version I downloaded)
1. Run simple Spark example to test.
    ```
    cd /opt/spark
    ./bin/spark-submit examples/src/main/python/pi.py 10
    ```
1. Have a OpenShift (we have tested this against OpenShift cluster only thus far) cluster ready against which we can launch the Spark Jobs in `kubernetes` mode.
1. Have the certificate authorities for the OpenShift cluster on your machine such that you can run `oc login` with certificates as shown below 
    ```
    oc login -u kubeadmin -p password https://api.xx.yy.zz:6443 --certificate-authority=/etc/ssl/certs/your-cert.crt
    ```
    To prepare `your-cert.crt` file:
    1. In any namespace of the OpenShift cluster, there is a configmap called `kube-root-ca.crt `. This has the authority chain
    1. Just copy the contents and create `your-cert.crt`. In my macOS, this file needed to be created under /etc/ssl/certs/

This will install latest Spark. At the time of writing this, it installs __Spark Version 3.3.0__    
#### Spark Operator Install
Install Spark Operator following : [GoogleCloudPlatform/spark-on-k8s-operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/quick-start-guide.md)
We actually had to run: 
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install my-release spark-operator/spark-operator --namespace spark-operator --set webhook.enable=true --set sparkJobNamespace=default
```
- without webhook, CRD for SparkApplication was not even getting created apart from other things mentioned in the above got repo.
- without sparkJobNamespace, the right service accounts to launch the SparkApplication was not getting created.
- to test installation success. we ran an [example](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/quick-start-guide.md#running-the-examples). Though the example did not run  - they were for other reasons which I did not debug.

It installs __Spark Version 3.1.1__
