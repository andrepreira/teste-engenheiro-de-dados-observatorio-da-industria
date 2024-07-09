#!/bin/bash

source .datapipeline/bin/activate

export AIRFLOW_HOME=$(pwd)/airflow

airflow db init ; airflow webserver ; airflow scheduler

echo "acesse o webserver em http://localhost:1100"