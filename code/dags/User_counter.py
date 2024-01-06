from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
#Define the dag retried time and number in case of failure
default_args={
    'owner':'Airflow',
    'retries':1,
    'retry_delay':timedelta(minutes=0.5)
}
#Define the current time  function
def time():
    time=datetime.utcnow()
    time=time.strftime("%Y-%m-%d %H:%M:%S")
    return time
#Create the dag with the specific schedule
with DAG(
    dag_id='User_counter',
    default_args=default_args,
    description='Counts each minute the number of users in Postgres users table and stor the result in users_count table',
    start_date=datetime.utcnow()-timedelta(minutes=1),
    schedule_interval='* * * * *',
    catchup=False
) as dag:
    # The first task creates the table (if that does not exist) in the database which was configured in the postgres_default connection
    Task1 =PostgresOperator (
        task_id='PostgresTable',
        postgres_conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS users_count (
            count_id SERIAL PRIMARY KEY,
            count INTEGER NOT NULL,
            date VARCHAR NOT NULL);"""
    )
    #Counts all users in the users table and stores the time of operation, the ID of operation, and count result created by task 1 table.
    Task2 =PostgresOperator (
        task_id='Insert',
        postgres_conn_id='postgres_default',
        sql="""INSERT INTO users_count (count, date) 
        VALUES ((select count(id) from users) , %(date)s );""",
        parameters={ "date": time() }
    )
   #The task1 has to be awaited
    Task1 >> Task2
 