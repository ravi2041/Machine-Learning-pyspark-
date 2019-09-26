#!/bin/bash

usage() {
  cat << EOF
[`basename $0`]
USAGE: `basename $0` [-h]
       `basename $0` [-e executors] [-c cores] [-w worker memory] [-m master memory] [-n name]
OPTIONS:
  -h  usage
  -e  number of executors (default: 2)
  -c  number of cores per executor (default: 1)
  -w  worker memory (default: 1)
  -m  master memory (default: 1) 
  -n  application name (default: USERNAME)
EOF
}

EXECUTOR_INSTANCES=2
EXECUTOR_CORES=1
WORKER_MEMORY=1
MASTER_MEMORY=1
APPLICATION_NAME=${USER%@*}

while getopts ":he:c:w:m:n:" OPTION
do
  case $OPTION in
    h)  usage
        exit 0
        ;;
    e)  EXECUTOR_INSTANCES=$OPTARG
        ;;
    c)  EXECUTOR_CORES=$OPTARG
        ;;
    w)  WORKER_MEMORY=$OPTARG
        ;;
    m)  MASTER_MEMORY=$OPTARG
        ;;
    n)  APPLICATION_NAME=$OPTARG
        ;;
    :)  echo "`basename $0`: $OPTARG requires an argument to be provided"
        echo "See '`basename $0` -h' for usage details"
        exit 1
        ;;
    ?)  echo "`basename $0`: $OPTARG invalid"
        echo "See '`basename $0` -h' for usage details"
        exit 1
        ;;
  esac
done

CORES=$((EXECUTOR_INSTANCES * EXECUTOR_CORES))
PARTITIONS=$(($CORES * 2))
PORT=$((4000 + $((RANDOM % 999))))

DERBY_SYSTEM_HOME=/tmp/$USER/pyspark/$APPLICATION_NAME

rm -rf $DERBY_SYSTEM_HOME
mkdir -p $DERBY_SYSTEM_HOME

export PYSPARK_DRIVER_PYTHON=ipython

pyspark \
  --master spark://node0:7077 \
  --jars /opt/spark/jars/hadoop-auth-2.7.3.jar \
  --conf spark.driver.extraJavaOptions="-Dderby.system.home=$DERBY_SYSTEM_HOME" \
  --conf spark.dynamicAllocation.enabled=false \
  --conf spark.executor.instances=$EXECUTOR_INSTANCES \
  --conf spark.executor.cores=$EXECUTOR_CORES \
  --conf spark.cores.max=$CORES \
  --conf spark.executor.memory=${WORKER_MEMORY}g \
  --conf spark.driver.memory=${MASTER_MEMORY}g \
  --conf spark.driver.maxResultSize=0 \
  --conf spark.sql.shuffle.partitions=$PARTITIONS \
  --conf spark.ui.port=$PORT \
  --name "$APPLICATION_NAME"
