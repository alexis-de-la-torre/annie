from datetime import timedelta
import json

from airflow import DAG

from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

with DAG(
    'nfl-schedules',
    default_args={
        'depends_on_past': False,
        'email': ['alexiscedros@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(10),
    catchup=True,
    tags=['example'],
) as dag:
    date = '{{ execution_date }}'
    bucket = Variable.get("bucket")

    t1 = SimpleHttpOperator(
        http_conn_id='painter_schedules',
        task_id='painter',
        endpoint='schedules',
        data=json.dumps({"date": date}),
        headers={"Content-Type": "application/json"},
        dag=dag,
    )

    print("Buckettttttt")
    print(bucket)

    t1