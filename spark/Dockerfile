# Note: Spark 3.0.1 supports Python up to 3.8, this will be the installed version

#ARG base_img

#FROM $base_img
FROM quay.io/opendatahub-contrib/pyspark:s3.0.1-h3.3.0_v0.1.0

EXPOSE 8080

ENV PYTHON_VERSION=3.8 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    CNB_STACK_ID=com.redhat.stacks.ubi8-python-38 \
    CNB_USER_ID=1001 \
    CNB_GROUP_ID=0 \
    PIP_NO_CACHE_DIR=off

USER 0

RUN INSTALL_PKGS="python38 python38-devel python38-setuptools python38-pip nss_wrapper \
        httpd httpd-devel mod_ssl mod_auth_gssapi mod_ldap \
        mod_session atlas-devel gcc-gfortran libffi-devel libtool-ltdl enchant" && \
    microdnf -y module enable python38:3.8 httpd:2.4 && \
    microdnf -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    microdnf -y clean all --enablerepo='*' 
    #&& \
    #ln -s /usr/bin/python3 /usr/bin/python

ENV PYTHONPATH ${SPARK_HOME}/python/lib/pyspark.zip:${SPARK_HOME}/python/lib/py4j-*.zip

WORKDIR /opt/spark/jars
COPY spark-sql-kafka-0-10_2.12-3.0.1.jar .
COPY spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar .
COPY commons-pool2-2.6.2.jar .
RUN chmod a+rwx /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar
RUN chmod a+rwx /opt/spark/jars/spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar
RUN chmod a+rwx /opt/spark/jars/commons-pool2-2.6.2.jar

RUN chmod a+rwx /tmp
RUN mkdir -p /opt/spark/.ivy2/cache
RUN chmod a+rwx /opt/spark/.ivy2/cache
RUN mkdir -p /opt/spark/.ivy2/jars
RUN chmod a+rwx /opt/spark/.ivy2/jars

WORKDIR /opt/spark/work-dir

COPY helloworld.py .
COPY simpleKafkaConsumer.py .

ENTRYPOINT [ "/opt/entrypoint.sh" ]

USER 185
