import pendulum

import requests
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from airflow.decorators import dag
from airflow.operators.python import PythonOperator

TIMEMOUT_IN_SECONDS = 120

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["observatorio@sistemafiea.com.br"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": pendulum.duration(minutes=5),
}


@dag(
    default_args=default_args,
    description="",
    schedule=None,
    start_date=pendulum.datetime(2024, 3, 22, tz="America/Sao_Paulo"),
    catchup=False,
)

def extract_data():
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/1839/periodos/2022/variaveis/630?localidades=N1[all]"
    response = requests.request("GET", url=url, timeout=TIMEMOUT_IN_SECONDS)
    response.raise_for_status()
    response_json = response.json()
    return response_json

extract_data_task = PythonOperator(
    task_id = "extract_data",
    python_callable=extract_data,
    dag=dag,
)

def transform_data_into_spark_df(data):
    if not data:
        raise Exception("data not found!")
    print(data)

fetch_json_task = PythonOperator(
    task_id = "transform_data_into_spark_df",
    python_callable=transform_data_into_spark_df,
    dag=dag,

)

# def pesquisa_industrial_anual_empresas():
#     import os

#     from airflow.providers.papermill.operators.papermill import PapermillOperator

#     PapermillOperator(
#         task_id="workspace",
#         input_nb=os.path.join(
#             os.getcwd(),
#             "dags",
#             "{{ dag.dag_id }}",
#             "notebooks",
#             "workspace.ipynb",
#         ),
#         output_nb="/opt/airflow/dags/resultado/{{ dag.dag_id }}_{{ task.task_id }}_{{ ds }}.ipynb",
#     )

# pesquisa_industrial_anual_empresas()


extract_data >> transform_data_into_spark_df