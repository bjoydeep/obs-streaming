## Launch Spark Job
Recall we installed Spark in 2 different ways - 
- Google Spark Operator on the OpenShift cluster directly
- Spark on the laptop

If you want to test the Google Spark Operator, you will have to create a Spark Application CR as [shown below](#Create-a-real-Spark-Application-CR).

If you want to test the Spark installed on laptop, you will run a Spark submit job as [shown below](#Create-a-real-Spark-Application-by-submitting-to-a-local-Spark-install).

### Create a real Spark Application CR
Spark Application can be created by creating the CR of kind `SparkApplication` as shown below. 
#### Calculate Pi
The snip below creates a CR for launching out of the box Spark example of calculating value of pi.

```
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: spark-pi-jb
  namespace: default
spec:
  type: Python
  mode: cluster
  image: "quay.io/bjoydeep/pyspark:latest"
  imagePullPolicy: Always
  mainApplicationFile: "local:///opt/spark/examples/src/main/python/pi.py"
  sparkVersion: "3.0.1"
  restartPolicy:
    type: Never
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: 3.0.1
    serviceAccount: my-release-spark
  executor:
    cores: 1
    instances: 1
    memory: "512m"
    labels:
      version: 3.0.1
  batchSchedulerOptions:
    resources:
        cpu: "2"
        memory: "4096m"
```        

#### HelloWorld example
The snip below creates a CR for launching  __HelloWorld__  Spark example as shown in [helloworld.py](spark/helloworld.py) . Note this file is also a part of the Spark Driver docker image built earlier.
```
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: spark-hello-jb
  namespace: default
spec:
  type: Python
  mode: cluster
  image: "quay.io/bjoydeep/pyspark:latest"
  imagePullPolicy: Always
  mainApplicationFile: "local:///opt/spark/work-dir/helloworld.py"
  sparkVersion: "3.0.1"
  restartPolicy:
    type: Never
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: 3.0.1
    serviceAccount: my-release-spark
  executor:
    cores: 1
    instances: 1
    memory: "512m"
    labels:
      version: 3.0.1
  batchSchedulerOptions:
    resources:
        cpu: "2"
        memory: "4096m"
```
#### TO CHECK
_Is this needed Application level RBAC?_: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/manifest/spark-application-rbac/spark-application-rbac.yaml

#### Simple Kafka Streaming Example
Trying to launch home grown [simpleKafkaConsumer.py](spark/simpleKafkaConsumer.py) but __Kafka starts erroring out__ while using Operator. We are still debugging this. It appears to be some permission related issue  - we will get to the bottom of this soon.

```
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: spark-kafka-jb
  namespace: default
spec:
  type: Python
  mode: cluster
  image: "quay.io/bjoydeep/pyspark:latest"
  imagePullPolicy: Always
  mainApplicationFile: "local:///opt/spark/work-dir/simpleKafkaConnsumer.py"
  sparkVersion: "3.0.1"
  restartPolicy:
    type: Never
  deps:
    packages: 
    - "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1"
  #javaOptions: spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp
  sparkConf:
    #this should work but but does not!
    #this comes out perfect in spark-submit from the logs
    #--conf spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp
    #why does it not work?
    spark.driver.extraJavaOptions: "-Divy.cache.dir=/tmp -Divy.home=/tmp"
    #spark.driver.extraJavaOptions: "-Divy.home=/tmp"
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: 3.0.1
    serviceAccount: my-release-spark
    #JavaOptions: "-Divy.cache.dir=/tmp -Divy.home=/tmp"
  executor:
    cores: 1
    instances: 1
    memory: "512m"
    labels:
      version: 3.0.1
  batchSchedulerOptions:
    resources:
        cpu: "2"
        memory: "4096m"
```        

__The above results in Spark Submit as shown below (we find this out from the Operator logs)__
```
/opt/spark/bin/spark-submit 
--master k8s://https://172.30.0.1:443 
--deploy-mode cluster 
--conf spark.kubernetes.namespace=default 
--conf spark.app.name=spark-hello-jb 
--conf spark.kubernetes.driver.pod.name=spark-hello-jb-driver 
--conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest 
--conf spark.kubernetes.container.image.pullPolicy=Always 
--conf spark.kubernetes.submission.waitAppCompletion=false 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-hello-jb 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/submission-id=60a0a134-4d8d-4a05-b888-a6cbf6487434 
--conf spark.driver.cores=1 
--conf spark.kubernetes.driver.limit.cores=1200m 
--conf spark.driver.memory=512m 
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark 
--conf spark.kubernetes.driver.label.version=3.0.1
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-hello-jb 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/submission-id=60a0a134-4d8d-4a05-b888-a6cbf6487434 
--conf spark.executor.instances=1 
--conf spark.executor.cores=1 
--conf spark.executor.memory=512m 
--conf spark.kubernetes.executor.label.version=3.0.1 
local:///opt/spark/work-dir/helloworld.py
```
\

--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
--jars /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar \
--conf spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp \




```
/opt/spark/bin/spark-submit 
--master k8s://https://172.30.0.1:443 
--deploy-mode cluster 
--conf spark.kubernetes.namespace=default 
--conf spark.app.name=spark-kafka-jb 
--conf spark.kubernetes.driver.pod.name=spark-kafka-jb-driver
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 
--conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest 
--conf spark.kubernetes.container.image.pullPolicy=Always 
--conf spark.kubernetes.submission.waitAppCompletion=false 
--conf spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-kafka-jb 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/submission-id=33783ebc-2289-4c10-9bf9-dd54eff9e988 
--conf spark.driver.cores=1 
--conf spark.kubernetes.driver.limit.cores=1200m 
--conf spark.driver.memory=512m 
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark 
--conf spark.kubernetes.driver.label.version=3.0.1 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-kafka-jb 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/submission-id=33783ebc-2289-4c10-9bf9-dd54eff9e988 
--conf spark.executor.instances=1 
--conf spark.executor.cores=1 
--conf spark.executor.memory=512m 
--conf spark.kubernetes.executor.label.version=3.0.1 
local:///opt/spark/work-dir/simpleKafkaConnsumer.py
```
It still errors out at:
```
WARNING: All illegal access operations will be denied in a future release
Ivy Default Cache set to: /opt/spark/.ivy2/cache
The jars for the packages stored in: /opt/spark/.ivy2/jars
```
```
/opt/spark/bin/spark-submit --master k8s://https://172.30.0.1:443 --deploy-mode cluster --conf spark.kubernetes.namespace=default --conf spark.app.name=spark-kafka-jb --conf spark.kubernetes.driver.pod.name=spark-kafka-jb-driver --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 --conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest --conf spark.kubernetes.container.image.pullPolicy=Always --conf spark.kubernetes.submission.waitAppCompletion=false --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" --conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-kafka-jb --conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true --conf spark.kubernetes.driver.label.sparkoperator.k8s.io/submission-id=569edc7b-7453-44db-a390-9009c34460d0 --conf spark.driver.cores=1 --conf spark.kubernetes.driver.limit.cores=1200m --conf spark.driver.memory=512m --conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark --conf spark.kubernetes.driver.label.version=3.0.1 --conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-kafka-jb --conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true --conf spark.kubernetes.executor.label.sparkoperator.k8s.io/submission-id=569edc7b-7453-44db-a390-9009c34460d0 --conf spark.executor.instances=1 --conf spark.executor.cores=1 --conf spark.executor.memory=512m --conf spark.kubernetes.executor.label.version=3.0.1 local:///opt/spark/work-dir/simpleKafkaConnsumer.py
```

```
/opt/spark/bin/spark-submit 
--master k8s://https://172.30.0.1:443 
--deploy-mode cluster 
--conf spark.kubernetes.namespace=default 
--conf spark.app.name=spark-kafka-jb 
--conf spark.kubernetes.driver.pod.name=spark-kafka-jb-driver 
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 
--conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest 
--conf spark.kubernetes.container.image.pullPolicy=Always --conf spark.kubernetes.submission.waitAppCompletion=false 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-kafka-jb 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/submission-id=b8819519-073b-4c7b-8d13-67d4d0e411e1 
--conf spark.driver.cores=1 
--conf spark.kubernetes.driver.limit.cores=1200m 
--conf spark.driver.memory=512m 
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark
--conf spark.kubernetes.driver.label.version=3.0.1 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-kafka-jb 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true 
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/submission-id=b8819519-073b-4c7b-8d13-67d4d0e411e1 
--conf spark.executor.instances=1 
--conf spark.executor.cores=1 
--conf spark.executor.memory=512m 
--conf spark.kubernetes.executor.label.version=3.0.1 
local:///opt/spark/work-dir/simpleKafkaConnsumer.py
```


### Create a real Spark Application by submitting to a local Spark install

Note that before you launch this, you must do a `oc login` to your cluster using the certificates.  Else you will see an error like: 
```
https://api.xx.yy.zz:6443
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark \
Caused by: javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```
#### Launching a simple job

Launching home grown [helloworld.py](spark/helloworld.py)
```
/bin/spark-submit \
--master k8s://https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443 \
--deploy-mode cluster \
--conf spark.kubernetes.namespace=default \
--conf spark.app.name=spark-hello-jb-rem \
--conf spark.kubernetes.driver.pod.name=spark-hello-jb-rem-driver \
--conf spark.kubernetes.container.image=quay.io/bjoydeep/pyspark:latest \
--conf spark.kubernetes.container.image.pullPolicy=Always \
--conf spark.kubernetes.submission.waitAppCompletion=false \
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name=spark-hello-jb-rem \
--conf spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator=true \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark \
--conf spark.driver.cores=1 \
--conf spark.kubernetes.driver.limit.cores=1200m \
--conf spark.driver.memory=512m \
--conf spark.kubernetes.driver.label.version=3.0.1 \
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name=spark-hello-jb-rem \
--conf spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator=true \
--conf spark.executor.instances=1 \
--conf spark.executor.cores=1 \
--conf spark.executor.memory=512m \
--conf spark.kubernetes.executor.label.version=3.0.1 \
-v local:///opt/spark/work-dir/helloworld.py
```

#### Launching a Kafka streaming job

Launching home grown [simpleKafkaConsumer.py](spark/simpleKafkaConsumer.py)
 1. Look at the packages to see all the spark packages needed.
 1. Look at how the ivy2 works on the home dir. The Spark google operator pod does not allow that.
```
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
-v local:///opt/spark/work-dir/simpleKafkaConsumer.py
Using properties file: null
Parsed arguments:
  master                  k8s://https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443
  deployMode              cluster
  executorMemory          512m
  executorCores           1
  totalExecutorCores      null
  propertiesFile          null
  driverMemory            512m
  driverCores             1
  driverExtraClassPath    null
  driverExtraLibraryPath  null
  driverExtraJavaOptions  null
  supervise               false
  queue                   null
  numExecutors            1
  files                   null
  pyFiles                 null
  archives                null
  mainClass               null
  primaryResource         local:///opt/spark/work-dir/simpleKafkaConsumer.py
  name                    spark-kafka-jb
  childArgs               []
  jars                    null
  packages                org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.0.1,org.apache.commons:commons-pool2:2.6.2
  packagesExclusions      null
  repositories            null
  verbose                 true

Spark properties used, including those specified through
 --conf and those from the properties file null:
  (spark.app.name,spark-kafka-jb)
  (spark.driver.cores,1)
  (spark.driver.memory,512m)
  (spark.executor.cores,1)
  (spark.executor.instances,1)
  (spark.executor.memory,512m)
  (spark.kubernetes.authenticate.driver.serviceAccountName,my-release-spark)
  (spark.kubernetes.container.image,quay.io/bjoydeep/pyspark:latest)
  (spark.kubernetes.container.image.pullPolicy,Always)
  (spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name,spark-kafka-jb)
  (spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator,true)
  (spark.kubernetes.driver.label.version,3.0.1)
  (spark.kubernetes.driver.limit.cores,1200m)
  (spark.kubernetes.driver.pod.name,spark-kafka-jb-driver)
  (spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name,spark-kafka-jb)
  (spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator,true)
  (spark.kubernetes.executor.label.version,3.0.1)
  (spark.kubernetes.namespace,default)
  (spark.kubernetes.submission.waitAppCompletion,false)


:: loading settings :: url = jar:file:/opt/spark/jars/ivy-2.5.0.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /Users/jbanerje/.ivy2/cache
The jars for the packages stored in: /Users/jbanerje/.ivy2/jars
org.apache.spark#spark-sql-kafka-0-10_2.12 added as a dependency
org.apache.spark#spark-token-provider-kafka-0-10_2.12 added as a dependency
org.apache.commons#commons-pool2 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-3a1e09b5-0f24-46e0-b5a9-11b41ad1fdba;1.0
	confs: [default]
	found org.apache.spark#spark-sql-kafka-0-10_2.12;3.0.1 in central
	found org.apache.spark#spark-token-provider-kafka-0-10_2.12;3.0.1 in central
	found org.apache.kafka#kafka-clients;2.4.1 in central
	found com.github.luben#zstd-jni;1.4.4-3 in central
	found org.lz4#lz4-java;1.7.1 in central
	found org.xerial.snappy#snappy-java;1.1.7.5 in central
	found org.slf4j#slf4j-api;1.7.30 in central
	found org.spark-project.spark#unused;1.0.0 in central
	found org.apache.commons#commons-pool2;2.6.2 in central
:: resolution report :: resolve 462ms :: artifacts dl 24ms
	:: modules in use:
	com.github.luben#zstd-jni;1.4.4-3 from central in [default]
	org.apache.commons#commons-pool2;2.6.2 from central in [default]
	org.apache.kafka#kafka-clients;2.4.1 from central in [default]
	org.apache.spark#spark-sql-kafka-0-10_2.12;3.0.1 from central in [default]
	org.apache.spark#spark-token-provider-kafka-0-10_2.12;3.0.1 from central in [default]
	org.lz4#lz4-java;1.7.1 from central in [default]
	org.slf4j#slf4j-api;1.7.30 from central in [default]
	org.spark-project.spark#unused;1.0.0 from central in [default]
	org.xerial.snappy#snappy-java;1.1.7.5 from central in [default]
	---------------------------------------------------------------------
	|                  |            modules            ||   artifacts   |
	|       conf       | number| search|dwnlded|evicted|| number|dwnlded|
	---------------------------------------------------------------------
	|      default     |   9   |   0   |   0   |   0   ||   9   |   0   |
	---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-3a1e09b5-0f24-46e0-b5a9-11b41ad1fdba
	confs: [default]
	0 artifacts copied, 9 already retrieved (0kB/11ms)
22/10/16 07:50:38 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Main class:
org.apache.spark.deploy.k8s.submit.KubernetesClientApplication
Arguments:
--primary-py-file
local:///opt/spark/work-dir/simpleKafkaConsumer.py
--main-class
org.apache.spark.deploy.PythonRunner
Spark config:
(spark.app.name,spark-kafka-jb)
(spark.app.submitTime,1665931838410)
(spark.driver.cores,1)
(spark.driver.memory,512m)
(spark.executor.cores,1)
(spark.executor.instances,1)
(spark.executor.memory,512m)
(spark.jars.packages,*********(redacted))
(spark.kubernetes.authenticate.driver.serviceAccountName,my-release-spark)
(spark.kubernetes.container.image,quay.io/bjoydeep/pyspark:latest)
(spark.kubernetes.container.image.pullPolicy,Always)
(spark.kubernetes.driver.label.sparkoperator.k8s.io/app-name,spark-kafka-jb)
(spark.kubernetes.driver.label.sparkoperator.k8s.io/launched-by-spark-operator,true)
(spark.kubernetes.driver.label.version,3.0.1)
(spark.kubernetes.driver.limit.cores,1200m)
(spark.kubernetes.driver.pod.name,spark-kafka-jb-driver)
(spark.kubernetes.executor.label.sparkoperator.k8s.io/app-name,spark-kafka-jb)
(spark.kubernetes.executor.label.sparkoperator.k8s.io/launched-by-spark-operator,true)
(spark.kubernetes.executor.label.version,3.0.1)
(spark.kubernetes.namespace,default)
(spark.kubernetes.submission.waitAppCompletion,false)
(spark.master,k8s://https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443)
(spark.submit.deployMode,cluster)
(spark.submit.pyFiles,)
Classpath elements:
/Users/jbanerje/.ivy2/jars/org.apache.spark_spark-sql-kafka-0-10_2.12-3.0.1.jar
/Users/jbanerje/.ivy2/jars/org.apache.spark_spark-token-provider-kafka-0-10_2.12-3.0.1.jar
/Users/jbanerje/.ivy2/jars/org.apache.commons_commons-pool2-2.6.2.jar
/Users/jbanerje/.ivy2/jars/org.apache.kafka_kafka-clients-2.4.1.jar
/Users/jbanerje/.ivy2/jars/org.spark-project.spark_unused-1.0.0.jar
/Users/jbanerje/.ivy2/jars/com.github.luben_zstd-jni-1.4.4-3.jar
/Users/jbanerje/.ivy2/jars/org.lz4_lz4-java-1.7.1.jar
/Users/jbanerje/.ivy2/jars/org.xerial.snappy_snappy-java-1.1.7.5.jar
/Users/jbanerje/.ivy2/jars/org.slf4j_slf4j-api-1.7.30.jar

```