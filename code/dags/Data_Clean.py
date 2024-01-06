
from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
#Define the dag retried time and number in case of failure
default_args={
    'owner':'Airflow',
    'retries':1,
    'retry_delay':timedelta(minutes=0.5)
}
#Define the print function
def Print():
    print("The table users_count was cleaned")
#Create the dag with the specific schedule
with DAG(
    dag_id='CountCleaner',
    default_args=default_args,
    description='Code cleance one in a hour (at 30 minute) the user_count table',
    start_date=datetime.utcnow()-timedelta(minutes=1),
    schedule_interval='30 * * * *',
    catchup=False
) as dag:
    #Cleans user_count table
    Task1 =PostgresOperator (
        task_id='Clean_data',
        postgres_conn_id='postgres_default',
        sql="""TRUNCATE  users_count;"""
    )
    #Simple print in logs
    Task2 =PythonOperator (
        task_id='Print',
        python_callable=Print
    )
    #The task1 has to be awaited
    Task1 >> Task2
 