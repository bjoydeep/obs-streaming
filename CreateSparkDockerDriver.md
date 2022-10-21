## Building the Docker Driver for Spark

This docker driver container can be used no matter which way Spark job is launched:
- through Spark Operator
- or from Spark running locally on the laptop

We are using ` quay.io/opendatahub-contrib/pyspark:s3.0.1-h3.3.0_v0.1.0` image from Red Hat Open Data Hub (ODH) project.  The spark installed in Google Operator was `Version 3.1.1`. ODH had versions of Spark Driver `Version 3.0.1` and `Version 3.3` and nothing in between. So we chose an image `Version 3.0.1` assuming it Spark Submit from Spark 3.1.1 will be able to handle driver with `Version 3.0.1`.  We could also have used the one provided by Spark itself in which case we would have got `Version 3.1.1` - just did not try.

The docker image is available for free download at `quay.io/bjoydeep/pyspark:latest`.


#### Testing the Docker Driver manually

You  can download the image from quay.io and test it. Else, you can locally build [it](spark/Dockerfile):
```
cd spark
docker build -t pyspark .
```
And then test it - 
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
[jboss@9777580591d0 src]$ ls
main
[jboss@9777580591d0 src]$ cd main/
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
