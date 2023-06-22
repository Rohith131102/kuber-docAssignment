from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Create a DAG with the specified DAG ID, start date, and schedule interval
with DAG(dag_id='time_task', start_date=datetime(2022, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    # Task to create the table if it doesn't exist
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS myTime_assignment (
                curr_time TIMESTAMP
            );
        '''
    )
    
    # Task to insert a value into the table with the current timestamp
    insert_value = PostgresOperator(
        task_id='insert_value',
        postgres_conn_id='postgres',
        sql='''
            INSERT INTO myTime_assignment VALUES (CURRENT_TIMESTAMP);   
        '''
    )
    
    # Set task dependencies
    create_table >> insert_value

    
