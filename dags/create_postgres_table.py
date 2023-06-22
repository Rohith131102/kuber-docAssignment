from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(dag_id='time_task', start_date=datetime(2022, 1, 1), 
        schedule_interval='@daily',  catchup=False) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS myTime_assignment (
                curr_time TIMESTAMP
            );
        '''
    )
    
    insert_value = PostgresOperator(
        task_id = 'insert_value',
        postgres_conn_id='postgres',
        sql = '''
                INSERT INTO myTime_assignment VALUES (CURRENT_TIMESTAMP);   
        '''
    )
    
    create_table >> insert_value
    
