# Notes
## Prereq
### Install Vector
### Install Kafka
### Wire them up
### Install Observability
### Configure Observability to talk to Vector
### Test data flow to Kafka

## Install and Test Spark
For background knowledge, or those familiar with Spark but in a non-Kubernetes environment, [Running Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html) is an excellent reference material.

### Spark Operator Install
Install Spark Oprator following : [GoogleCloudPlatform/spark-on-k8s-operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/quick-start-guide.md)
We actually had to run: 
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install my-release spark-operator/spark-operator --namespace spark-operator --set webhook.enable=true --set sparkJobNamespace=default
```
- without webhook, CRD for SparkApplication was not even getting created apart from other things mentioned in the above got repo.
- without sparkJobNamespace, the right service accounts to launcg the SparkApplication was not getting created.
- for running an [example](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/quick-start-guide.md#running-the-examples), this was good. The example did not run for other reasons which I did not debug.

### Installed Version
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.1.1
      /_/
                        
https://spark.apache.org/docs/3.1.1/#:~:text=Spark%20runs%20on%20Java%208,3.6%2B%20and%20R%203.5%2B.

So we can use this image: https://github.com/opendatahub-io-contrib/spark-on-openshift/blob/main/spark-images/pyspark-3.0.1_hadoop-3.3.0.Dockerfile

### Building the Docker
```
docker build -t pyspark .
```

### Testing the Docker
```
(base) ➜  spark docker run -it pyspark /bin/bash
++ id -u
+ myuid=185
++ id -g
+ mygid=0
+ set +e
++ getent passwd 185
+ uidentry='jboss:x:185:0:JBoss user:/home/jboss:/sbin/nologin'
+ set -e
+ '[' -z 'jboss:x:185:0:JBoss user:/home/jboss:/sbin/nologin' ']'
+ SPARK_CLASSPATH=':/opt/spark/jars/*'
+ env
+ grep SPARK_JAVA_OPT_
+ sort -t_ -k4 -n
+ sed 's/[^=]*=\(.*\)/\1/g'
+ readarray -t SPARK_EXECUTOR_JAVA_OPTS
+ '[' -n '/opt/hadoop/etc/hadoop:/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/common/*:/opt/hadoop/share/hadoop/hdfs:/opt/hadoop/share/hadoop/hdfs/lib/*:/opt/hadoop/share/hadoop/hdfs/*:/opt/hadoop/share/hadoop/yarn:/opt/hadoop/share/hadoop/yarn/lib/*:/opt/hadoop/share/hadoop/yarn/*:/opt/hadoop/share/hadoop/mapreduce/lib/*:/opt/hadoop/share/hadoop/mapreduce/*:/contrib/capacity-scheduler/*.jar:/opt/hadoop/share/hadoop/tools/lib/*' ']'
+ SPARK_CLASSPATH=':/opt/spark/jars/*:/opt/hadoop/etc/hadoop:/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/common/*:/opt/hadoop/share/hadoop/hdfs:/opt/hadoop/share/hadoop/hdfs/lib/*:/opt/hadoop/share/hadoop/hdfs/*:/opt/hadoop/share/hadoop/yarn:/opt/hadoop/share/hadoop/yarn/lib/*:/opt/hadoop/share/hadoop/yarn/*:/opt/hadoop/share/hadoop/mapreduce/lib/*:/opt/hadoop/share/hadoop/mapreduce/*:/contrib/capacity-scheduler/*.jar:/opt/hadoop/share/hadoop/tools/lib/*'
+ '[' '' == 2 ']'
+ '[' '' == 3 ']'
+ '[' -n /opt/hadoop ']'
+ '[' -z '/opt/hadoop/etc/hadoop:/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/common/*:/opt/hadoop/share/hadoop/hdfs:/opt/hadoop/share/hadoop/hdfs/lib/*:/opt/hadoop/share/hadoop/hdfs/*:/opt/hadoop/share/hadoop/yarn:/opt/hadoop/share/hadoop/yarn/lib/*:/opt/hadoop/share/hadoop/yarn/*:/opt/hadoop/share/hadoop/mapreduce/lib/*:/opt/hadoop/share/hadoop/mapreduce/*:/contrib/capacity-scheduler/*.jar:/opt/hadoop/share/hadoop/tools/lib/*' ']'
+ '[' -z ']'
+ case "$1" in
+ echo 'Non-spark-on-k8s command provided, proceeding in pass-through mode...'
Non-spark-on-k8s command provided, proceeding in pass-through mode...
+ CMD=("$@")
+ exec /usr/bin/tini -s -- /bin/bash
[jboss@9777580591d0 work-dir]$
[jboss@9777580591d0 work-dir]$ pwd
/opt/spark/work-dir
[jboss@9777580591d0 work-dir]$ ls
[jboss@9777580591d0 work-dir]$ cd ..
[jboss@9777580591d0 spark]$ ls
bin  conf  data  examples  jars  kubernetes  LICENSE  licenses	NOTICE	python	R  README.md  RELEASE  sbin  work-dir  yarn
[jboss@9777580591d0 spark]$ cd bin
[jboss@9777580591d0 bin]$ ls
beeline		      find-spark-home	   load-spark-env.sh  pyspark.cmd      spark-class	 sparkR       spark-shell	spark-sql	spark-submit
beeline.cmd	      find-spark-home.cmd  pyspark	      run-example      spark-class2.cmd  sparkR2.cmd  spark-shell2.cmd	spark-sql2.cmd	spark-submit2.cmd
docker-image-tool.sh  load-spark-env.cmd   pyspark2.cmd       run-example.cmd  spark-class.cmd	 sparkR.cmd   spark-shell.cmd	spark-sql.cmd	spark-submit.cmd
[jboss@9777580591d0 bin]$ ./spark-submit -version
Error: Unrecognized option: -version

Usage: spark-submit [options] <app jar | python file | R file> [app arguments]
Usage: spark-submit --kill [submission ID] --master [spark://...]
Usage: spark-submit --status [submission ID] --master [spark://...]
Usage: spark-submit run-example [options] example-class [example args]

Options:
  --master MASTER_URL         spark://host:port, mesos://host:port, yarn,
                              k8s://https://host:port, or local (Default: local[*]).
  --deploy-mode DEPLOY_MODE   Whether to launch the driver program locally ("client") or
                              on one of the worker machines inside the cluster ("cluster")
                              (Default: client).
  --class CLASS_NAME          Your application's main class (for Java / Scala apps).
  --name NAME                 A name of your application.
  --jars JARS                 Comma-separated list of jars to include on the driver
                              and executor classpaths.
  --packages                  Comma-separated list of maven coordinates of jars to include
                              on the driver and executor classpaths. Will search the local
                              maven repo, then maven central and any additional remote
                              repositories given by --repositories. The format for the
                              coordinates should be groupId:artifactId:version.
  --exclude-packages          Comma-separated list of groupId:artifactId, to exclude while
                              resolving the dependencies provided in --packages to avoid
                              dependency conflicts.
  --repositories              Comma-separated list of additional remote repositories to
                              search for the maven coordinates given with --packages.
  --py-files PY_FILES         Comma-separated list of .zip, .egg, or .py files to place
                              on the PYTHONPATH for Python apps.
  --files FILES               Comma-separated list of files to be placed in the working
                              directory of each executor. File paths of these files
                              in executors can be accessed via SparkFiles.get(fileName).

  --conf, -c PROP=VALUE       Arbitrary Spark configuration property.
  --properties-file FILE      Path to a file from which to load extra properties. If not
                              specified, this will look for conf/spark-defaults.conf.

  --driver-memory MEM         Memory for driver (e.g. 1000M, 2G) (Default: 1024M).
  --driver-java-options       Extra Java options to pass to the driver.
  --driver-library-path       Extra library path entries to pass to the driver.
  --driver-class-path         Extra class path entries to pass to the driver. Note that
                              jars added with --jars are automatically included in the
                              classpath.

  --executor-memory MEM       Memory per executor (e.g. 1000M, 2G) (Default: 1G).

  --proxy-user NAME           User to impersonate when submitting the application.
                              This argument does not work with --principal / --keytab.

  --help, -h                  Show this help message and exit.
  --verbose, -v               Print additional debug output.
  --version,                  Print the version of current Spark.

 Cluster deploy mode only:
  --driver-cores NUM          Number of cores used by the driver, only in cluster mode
                              (Default: 1).

 Spark standalone or Mesos with cluster deploy mode only:
  --supervise                 If given, restarts the driver on failure.

 Spark standalone, Mesos or K8s with cluster deploy mode only:
  --kill SUBMISSION_ID        If given, kills the driver specified.
  --status SUBMISSION_ID      If given, requests the status of the driver specified.

 Spark standalone, Mesos and Kubernetes only:
  --total-executor-cores NUM  Total cores for all executors.

 Spark standalone, YARN and Kubernetes only:
  --executor-cores NUM        Number of cores used by each executor. (Default: 1 in
                              YARN and K8S modes, or all available cores on the worker
                              in standalone mode).

 Spark on YARN and Kubernetes only:
  --num-executors NUM         Number of executors to launch (Default: 2).
                              If dynamic allocation is enabled, the initial number of
                              executors will be at least NUM.
  --principal PRINCIPAL       Principal to be used to login to KDC.
  --keytab KEYTAB             The full path to the file that contains the keytab for the
                              principal specified above.

 Spark on YARN only:
  --queue QUEUE_NAME          The YARN queue to submit to (Default: "default").
  --archives ARCHIVES         Comma separated list of archives to be extracted into the
                              working directory of each executor.

[jboss@9777580591d0 bin]$ ./spark-submit --version
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.0.1
      /_/

Using Scala version 2.12.10, OpenJDK 64-Bit Server VM, 1.8.0_332
Branch HEAD
Compiled by user ubuntu on 2020-08-28T08:11:27Z
Revision 2b147c4cd50da32fe2b4167f97c8142102a0510d
Url https://gitbox.apache.org/repos/asf/spark.git
Type --help for more information.
[jboss@9777580591d0 bin]$
[jboss@9777580591d0 bin]$ pwd
/opt/spark/bin
[jboss@9777580591d0 bin]$ cd ..
[jboss@9777580591d0 spark]$ ls
bin  conf  data  examples  jars  kubernetes  LICENSE  licenses	NOTICE	python	R  README.md  RELEASE  sbin  work-dir  yarn
[jboss@9777580591d0 spark]$ cd examples/
[jboss@9777580591d0 examples]$ ls
jars  src
[jboss@9777580591d0 examples]$ cd src/
[jboss@9777580591d0 src]$ ;s
bash: syntax error near unexpected token `;'
[jboss@9777580591d0 src]$ ls
main
[jboss@9777580591d0 src]$ cd main/
[jboss@9777580591d0 main]$ ls
java  python  r  resources  scala  scripts
[jboss@9777580591d0 main]$ xd python/
bash: xd: command not found
[jboss@9777580591d0 main]$ ls
java  python  r  resources  scala  scripts
[jboss@9777580591d0 main]$ cd python/
[jboss@9777580591d0 python]$ ls
als.py	avro_inputformat.py  kmeans.py	logistic_regression.py	ml  mllib  pagerank.py	parquet_inputformat.py	pi.py  sort.py	sql  status_api_demo.py  streaming  transitive_closure.py  wordcount.py
[jboss@9777580591d0 python]$ pwd
/opt/spark/examples/src/main/python
[jboss@9777580591d0 python]$ cd /opt/spark
[jboss@9777580591d0 spark]$ ./bin/spark-submit examples/src/main/python/pi.py 10
2022-09-27 17:41:50,674 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
2022-09-27 17:41:52,125 INFO spark.SparkContext: Running Spark version 3.0.1
2022-09-27 17:41:52,234 INFO resource.ResourceUtils: ==============================================================
2022-09-27 17:41:52,238 INFO resource.ResourceUtils: Resources for spark.driver:

2022-09-27 17:41:52,239 INFO resource.ResourceUtils: ==============================================================
2022-09-27 17:41:52,240 INFO spark.SparkContext: Submitted application: PythonPi
2022-09-27 17:41:52,427 INFO spark.SecurityManager: Changing view acls to: jboss
2022-09-27 17:41:52,427 INFO spark.SecurityManager: Changing modify acls to: jboss
2022-09-27 17:41:52,427 INFO spark.SecurityManager: Changing view acls groups to:
2022-09-27 17:41:52,428 INFO spark.SecurityManager: Changing modify acls groups to:
2022-09-27 17:41:52,428 INFO spark.SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(jboss); groups with view permissions: Set(); users  with modify permissions: Set(jboss); groups with modify permissions: Set()
2022-09-27 17:41:53,138 INFO util.Utils: Successfully started service 'sparkDriver' on port 44521.
2022-09-27 17:41:53,215 INFO spark.SparkEnv: Registering MapOutputTracker
2022-09-27 17:41:53,308 INFO spark.SparkEnv: Registering BlockManagerMaster
2022-09-27 17:41:53,379 INFO storage.BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
2022-09-27 17:41:53,380 INFO storage.BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
2022-09-27 17:41:53,391 INFO spark.SparkEnv: Registering BlockManagerMasterHeartbeat
2022-09-27 17:41:53,425 INFO storage.DiskBlockManager: Created local directory at /tmp/blockmgr-cf33d37b-6cee-4cbd-a06a-7c0fabf01c5c
2022-09-27 17:41:53,492 INFO memory.MemoryStore: MemoryStore started with capacity 366.3 MiB
2022-09-27 17:41:53,533 INFO spark.SparkEnv: Registering OutputCommitCoordinator
2022-09-27 17:41:53,781 INFO util.log: Logging initialized @6011ms to org.sparkproject.jetty.util.log.Slf4jLog
2022-09-27 17:41:54,028 INFO server.Server: jetty-9.4.z-SNAPSHOT; built: 2019-04-29T20:42:08.989Z; git: e1bc35120a6617ee3df052294e433f3a25ce7097; jvm 1.8.0_332-b09
2022-09-27 17:41:54,107 INFO server.Server: Started @6340ms
2022-09-27 17:41:54,176 INFO server.AbstractConnector: Started ServerConnector@3f949c61{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
2022-09-27 17:41:54,176 INFO util.Utils: Successfully started service 'SparkUI' on port 4040.
2022-09-27 17:41:54,235 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@3a7e943d{/jobs,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,240 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@2a4f1d54{/jobs/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,240 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@a653483{/jobs/job,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,256 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@339686b1{/jobs/job/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,258 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@59262ba3{/stages,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,259 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@6d0dc504{/stages/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,261 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@68945adf{/stages/stage,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,264 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@383095ac{/stages/stage/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,267 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@ded96f2{/stages/pool,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,342 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@1947cc{/stages/pool/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,344 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@5b0d172{/storage,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,345 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@32580e03{/storage/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,346 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@95bc909{/storage/rdd,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,348 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@2beb260e{/storage/rdd/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,348 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@6bc8448e{/environment,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,350 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@4818002f{/environment/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,352 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@3b87ba20{/executors,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,353 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@540af1e{/executors/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,356 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@255f78e{/executors/threadDump,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,359 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@140f91e{/executors/threadDump/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,385 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@f1f0a6{/static,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,387 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@2d865e24{/,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,390 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@1bc673bc{/api,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,392 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@5323dd68{/jobs/job/kill,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,393 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@2e489998{/stages/stage/kill,null,AVAILABLE,@Spark}
2022-09-27 17:41:54,397 INFO ui.SparkUI: Bound SparkUI to 0.0.0.0, and started at http://9777580591d0:4040
2022-09-27 17:41:54,924 INFO executor.Executor: Starting executor ID driver on host 9777580591d0
2022-09-27 17:41:54,981 INFO util.Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 38207.
2022-09-27 17:41:54,982 INFO netty.NettyBlockTransferService: Server created on 9777580591d0:38207
2022-09-27 17:41:54,986 INFO storage.BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
2022-09-27 17:41:55,014 INFO storage.BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 9777580591d0, 38207, None)
2022-09-27 17:41:55,022 INFO storage.BlockManagerMasterEndpoint: Registering block manager 9777580591d0:38207 with 366.3 MiB RAM, BlockManagerId(driver, 9777580591d0, 38207, None)
2022-09-27 17:41:55,034 INFO storage.BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 9777580591d0, 38207, None)
2022-09-27 17:41:55,039 INFO storage.BlockManager: Initialized BlockManager: BlockManagerId(driver, 9777580591d0, 38207, None)
2022-09-27 17:41:55,492 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@48fd1f57{/metrics/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:56,197 INFO internal.SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir ('file:/opt/spark/spark-warehouse').
2022-09-27 17:41:56,198 INFO internal.SharedState: Warehouse path is 'file:/opt/spark/spark-warehouse'.
2022-09-27 17:41:56,234 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@4ea6bce6{/SQL,null,AVAILABLE,@Spark}
2022-09-27 17:41:56,235 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@57b14478{/SQL/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:56,237 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@55a87762{/SQL/execution,null,AVAILABLE,@Spark}
2022-09-27 17:41:56,238 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@2c51cf0b{/SQL/execution/json,null,AVAILABLE,@Spark}
2022-09-27 17:41:56,263 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@458d3d4c{/static/sql,null,AVAILABLE,@Spark}
2022-09-27 17:41:58,352 INFO spark.SparkContext: Starting job: reduce at /opt/spark/examples/src/main/python/pi.py:44
2022-09-27 17:41:58,385 INFO scheduler.DAGScheduler: Got job 0 (reduce at /opt/spark/examples/src/main/python/pi.py:44) with 10 output partitions
2022-09-27 17:41:58,386 INFO scheduler.DAGScheduler: Final stage: ResultStage 0 (reduce at /opt/spark/examples/src/main/python/pi.py:44)
2022-09-27 17:41:58,387 INFO scheduler.DAGScheduler: Parents of final stage: List()
2022-09-27 17:41:58,391 INFO scheduler.DAGScheduler: Missing parents: List()
2022-09-27 17:41:58,405 INFO scheduler.DAGScheduler: Submitting ResultStage 0 (PythonRDD[1] at reduce at /opt/spark/examples/src/main/python/pi.py:44), which has no missing parents
2022-09-27 17:41:58,537 INFO memory.MemoryStore: Block broadcast_0 stored as values in memory (estimated size 6.3 KiB, free 366.3 MiB)
2022-09-27 17:41:58,820 INFO memory.MemoryStore: Block broadcast_0_piece0 stored as bytes in memory (estimated size 4.0 KiB, free 366.3 MiB)
2022-09-27 17:41:58,825 INFO storage.BlockManagerInfo: Added broadcast_0_piece0 in memory on 9777580591d0:38207 (size: 4.0 KiB, free: 366.3 MiB)
2022-09-27 17:41:58,830 INFO spark.SparkContext: Created broadcast 0 from broadcast at DAGScheduler.scala:1223
2022-09-27 17:41:58,859 INFO scheduler.DAGScheduler: Submitting 10 missing tasks from ResultStage 0 (PythonRDD[1] at reduce at /opt/spark/examples/src/main/python/pi.py:44) (first 15 tasks are for partitions Vector(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
2022-09-27 17:41:58,862 INFO scheduler.TaskSchedulerImpl: Adding task set 0.0 with 10 tasks
2022-09-27 17:41:59,043 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0, 9777580591d0, executor driver, partition 0, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,068 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 0.0 (TID 1, 9777580591d0, executor driver, partition 1, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,070 INFO scheduler.TaskSetManager: Starting task 2.0 in stage 0.0 (TID 2, 9777580591d0, executor driver, partition 2, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,073 INFO scheduler.TaskSetManager: Starting task 3.0 in stage 0.0 (TID 3, 9777580591d0, executor driver, partition 3, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,074 INFO scheduler.TaskSetManager: Starting task 4.0 in stage 0.0 (TID 4, 9777580591d0, executor driver, partition 4, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,076 INFO scheduler.TaskSetManager: Starting task 5.0 in stage 0.0 (TID 5, 9777580591d0, executor driver, partition 5, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:41:59,101 INFO executor.Executor: Running task 4.0 in stage 0.0 (TID 4)
2022-09-27 17:41:59,101 INFO executor.Executor: Running task 2.0 in stage 0.0 (TID 2)
2022-09-27 17:41:59,104 INFO executor.Executor: Running task 3.0 in stage 0.0 (TID 3)
2022-09-27 17:41:59,104 INFO executor.Executor: Running task 0.0 in stage 0.0 (TID 0)
2022-09-27 17:41:59,104 INFO executor.Executor: Running task 1.0 in stage 0.0 (TID 1)
2022-09-27 17:41:59,107 INFO executor.Executor: Running task 5.0 in stage 0.0 (TID 5)
2022-09-27 17:42:00,437 INFO python.PythonRunner: Times: total = 684, boot = 557, init = 21, finish = 106
2022-09-27 17:42:00,465 INFO python.PythonRunner: Times: total = 716, boot = 569, init = 31, finish = 116
2022-09-27 17:42:00,491 INFO python.PythonRunner: Times: total = 736, boot = 543, init = 38, finish = 155
2022-09-27 17:42:00,518 INFO executor.Executor: Finished task 0.0 in stage 0.0 (TID 0). 1552 bytes result sent to driver
2022-09-27 17:42:00,520 INFO executor.Executor: Finished task 5.0 in stage 0.0 (TID 5). 1552 bytes result sent to driver
2022-09-27 17:42:00,525 INFO python.PythonRunner: Times: total = 776, boot = 585, init = 15, finish = 176
2022-09-27 17:42:00,526 INFO executor.Executor: Finished task 3.0 in stage 0.0 (TID 3). 1552 bytes result sent to driver
2022-09-27 17:42:00,532 INFO executor.Executor: Finished task 1.0 in stage 0.0 (TID 1). 1552 bytes result sent to driver
2022-09-27 17:42:00,542 INFO scheduler.TaskSetManager: Starting task 6.0 in stage 0.0 (TID 6, 9777580591d0, executor driver, partition 6, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:42:00,551 INFO executor.Executor: Running task 6.0 in stage 0.0 (TID 6)
2022-09-27 17:42:00,564 INFO scheduler.TaskSetManager: Starting task 7.0 in stage 0.0 (TID 7, 9777580591d0, executor driver, partition 7, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:42:00,572 INFO python.PythonRunner: Times: total = 823, boot = 553, init = 41, finish = 229
2022-09-27 17:42:00,577 INFO executor.Executor: Finished task 2.0 in stage 0.0 (TID 2). 1552 bytes result sent to driver
2022-09-27 17:42:00,582 INFO scheduler.TaskSetManager: Finished task 5.0 in stage 0.0 (TID 5) in 1492 ms on 9777580591d0 (executor driver) (1/10)
2022-09-27 17:42:00,584 INFO executor.Executor: Running task 7.0 in stage 0.0 (TID 7)
2022-09-27 17:42:00,627 INFO python.PythonRunner: Times: total = 876, boot = 586, init = 26, finish = 264
2022-09-27 17:42:00,644 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 1674 ms on 9777580591d0 (executor driver) (2/10)
2022-09-27 17:42:00,652 INFO python.PythonAccumulatorV2: Connected to AccumulatorServer at host: 127.0.0.1 port: 54725
2022-09-27 17:42:00,656 INFO scheduler.TaskSetManager: Starting task 8.0 in stage 0.0 (TID 8, 9777580591d0, executor driver, partition 8, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:42:00,661 INFO executor.Executor: Finished task 4.0 in stage 0.0 (TID 4). 1552 bytes result sent to driver
2022-09-27 17:42:00,663 INFO executor.Executor: Running task 8.0 in stage 0.0 (TID 8)
2022-09-27 17:42:00,666 INFO scheduler.TaskSetManager: Finished task 3.0 in stage 0.0 (TID 3) in 1595 ms on 9777580591d0 (executor driver) (3/10)
2022-09-27 17:42:00,699 INFO scheduler.TaskSetManager: Starting task 9.0 in stage 0.0 (TID 9, 9777580591d0, executor driver, partition 9, PROCESS_LOCAL, 7333 bytes)
2022-09-27 17:42:00,699 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 1634 ms on 9777580591d0 (executor driver) (4/10)
2022-09-27 17:42:00,713 INFO executor.Executor: Running task 9.0 in stage 0.0 (TID 9)
2022-09-27 17:42:00,734 INFO scheduler.TaskSetManager: Finished task 2.0 in stage 0.0 (TID 2) in 1665 ms on 9777580591d0 (executor driver) (5/10)
2022-09-27 17:42:00,736 INFO scheduler.TaskSetManager: Finished task 4.0 in stage 0.0 (TID 4) in 1663 ms on 9777580591d0 (executor driver) (6/10)
2022-09-27 17:42:00,787 INFO python.PythonRunner: Times: total = 229, boot = -109, init = 135, finish = 203
2022-09-27 17:42:00,791 INFO executor.Executor: Finished task 6.0 in stage 0.0 (TID 6). 1509 bytes result sent to driver
2022-09-27 17:42:00,795 INFO scheduler.TaskSetManager: Finished task 6.0 in stage 0.0 (TID 6) in 254 ms on 9777580591d0 (executor driver) (7/10)
2022-09-27 17:42:00,860 INFO python.PythonRunner: Times: total = 187, boot = -169, init = 180, finish = 176
2022-09-27 17:42:00,864 INFO executor.Executor: Finished task 8.0 in stage 0.0 (TID 8). 1509 bytes result sent to driver
2022-09-27 17:42:00,866 INFO scheduler.TaskSetManager: Finished task 8.0 in stage 0.0 (TID 8) in 211 ms on 9777580591d0 (executor driver) (8/10)
2022-09-27 17:42:00,877 INFO python.PythonRunner: Times: total = 280, boot = -119, init = 135, finish = 264
2022-09-27 17:42:00,884 INFO executor.Executor: Finished task 7.0 in stage 0.0 (TID 7). 1509 bytes result sent to driver
2022-09-27 17:42:00,888 INFO scheduler.TaskSetManager: Finished task 7.0 in stage 0.0 (TID 7) in 324 ms on 9777580591d0 (executor driver) (9/10)
2022-09-27 17:42:00,912 INFO python.PythonRunner: Times: total = 183, boot = -188, init = 204, finish = 167
2022-09-27 17:42:00,916 INFO executor.Executor: Finished task 9.0 in stage 0.0 (TID 9). 1509 bytes result sent to driver
2022-09-27 17:42:00,918 INFO scheduler.TaskSetManager: Finished task 9.0 in stage 0.0 (TID 9) in 224 ms on 9777580591d0 (executor driver) (10/10)
2022-09-27 17:42:00,921 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool
2022-09-27 17:42:00,930 INFO scheduler.DAGScheduler: ResultStage 0 (reduce at /opt/spark/examples/src/main/python/pi.py:44) finished in 2.485 s
2022-09-27 17:42:00,943 INFO scheduler.DAGScheduler: Job 0 is finished. Cancelling potential speculative or zombie tasks for this job
2022-09-27 17:42:00,946 INFO scheduler.TaskSchedulerImpl: Killing all running tasks in stage 0: Stage finished
2022-09-27 17:42:00,959 INFO scheduler.DAGScheduler: Job 0 finished: reduce at /opt/spark/examples/src/main/python/pi.py:44, took 2.606524 s
Pi is roughly 3.141452
2022-09-27 17:42:01,014 INFO server.AbstractConnector: Stopped Spark@3f949c61{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
2022-09-27 17:42:01,025 INFO ui.SparkUI: Stopped Spark web UI at http://9777580591d0:4040
2022-09-27 17:42:01,095 INFO spark.MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
2022-09-27 17:42:01,136 INFO memory.MemoryStore: MemoryStore cleared
2022-09-27 17:42:01,137 INFO storage.BlockManager: BlockManager stopped
2022-09-27 17:42:01,156 INFO storage.BlockManagerMaster: BlockManagerMaster stopped
2022-09-27 17:42:01,164 INFO scheduler.OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
2022-09-27 17:42:01,186 INFO spark.SparkContext: Successfully stopped SparkContext
2022-09-27 17:42:01,967 INFO util.ShutdownHookManager: Shutdown hook called
2022-09-27 17:42:01,969 INFO util.ShutdownHookManager: Deleting directory /tmp/spark-2783f477-1fa1-4019-bcda-24fb9c4d9281
2022-09-27 17:42:01,977 INFO util.ShutdownHookManager: Deleting directory /tmp/spark-1debe124-6948-418f-a740-754eed146be9/pyspark-26dc159b-d148-4bcf-b522-66b8edc53f04
2022-09-27 17:42:01,988 INFO util.ShutdownHookManager: Deleting directory /tmp/spark-1debe124-6948-418f-a740-754eed146be9
[jboss@9777580591d0 spark]$ python
Python 3.8.12 (default, Sep 16 2021, 10:46:05)
[GCC 8.5.0 20210514 (Red Hat 8.5.0-3)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
[jboss@9777580591d0 spark]$ pip3 --version
pip 19.3.1 from /usr/lib/python3.8/site-packages/pip (python 3.8)
[jboss@9777580591d0 spark]$
```
```
./bin/spark-submit \
    --master k8s://https://<k8s-apiserver-host>:<k8s-apiserver-port> \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=<spark-image> \
    local:///path/to/examples.jar


./bin/spark-submit \
   --master yarn \
   --deploy-mode cluster \
   wordByExample.py


./bin/spark-submit \
   --master yarn \
   --deploy-mode cluster \
   local:///examples/src/main/python/pi.py 10

```

### Create a real Spark Application

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

### Application level RBAC
_Is this needed?_: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/manifest/spark-application-rbac/spark-application-rbac.yaml

__HelloWorld__
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

__Kafka__

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

__Net spark submit__
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
https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443
--conf spark.kubernetes.authenticate.driver.serviceAccountName=my-release-spark \
Caused by: javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target

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
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
--jars /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar \
--conf spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp \

# Works
```
/bin/spark-submit \
--master k8s://https://api.aws-jb-acm25.dev05.red-chesterfield.com:6443 \
--deploy-mode cluster \
--conf spark.kubernetes.namespace=default \
--conf spark.app.name=spark-hello-jb-rem \
--conf spark.kubernetes.driver.pod.name=spark-hello-jb-rem-driver \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
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
-v local:///opt/spark/work-dir/simpleKafkaConsumer.py
```
# Works
```
./bin/spark-submit \
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