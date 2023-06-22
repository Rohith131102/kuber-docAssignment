# Docker and Kubernets Assignment

## Question

<img width="554" alt="Screenshot 2023-06-22 at 3 19 12 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/2f2ec49b-dab9-45ea-903a-909c04c5c079">

### Approach

- The dags folder contains .py files for the dags created in correspondence to question-1.
- The .yaml files contains details of configuration required required for other tasks.

### Docker Task

1. Import the necessary modules and classes:

    ```python
    from airflow import DAG
    from datetime import datetime
    from airflow.providers.postgres.operators.postgres import PostgresOperator
    ```

2. Create a DAG object with the specified parameters:

    ```python
    with DAG(
        dag_id='time_task',
        start_date=datetime(2022, 1, 1),
        schedule_interval='@daily',
        catchup=False
    ) as dag:
    ```

3. Define the task to create the table if it doesn't exist:

    ```python
        create_table = PostgresOperator(
            task_id='create_table',
            postgres_conn_id='postgres',
            sql='''
                CREATE TABLE IF NOT EXISTS myTime_assignment (
                    curr_time TIMESTAMP
                );
            '''
        )
    ```

4. Define the task to insert a value into the table with the current timestamp:

    ```python
        insert_value = PostgresOperator(
            task_id='insert_value',
            postgres_conn_id='postgres',
            sql='''
                INSERT INTO myTime_assignment VALUES (CURRENT_TIMESTAMP);   
            '''
        )
    ```

5. Set the task dependency using the `>>` operator:

    ```python
        create_table >> insert_value
    ```

6. Save the file and run the Airflow scheduler to execute the DAG at the scheduled intervals.

### Explanation

- The DAG is scheduled to run daily starting from January 1, 2022, with no catch-up of missed runs.
- The `create_table` task uses the `PostgresOperator` to execute an SQL statement that creates a table named `myTime_assignment` with a single column called `curr_time` of type `TIMESTAMP`.
- The `insert_value` task uses the `PostgresOperator` to execute an SQL statement that inserts a value with the current timestamp into the `myTime_assignment` table.
- The `create_table` task must complete before the `insert_value` task can start, as specified by the task dependency `create_table >> insert_value`.

#### DAG

<img width="1434" alt="Screenshot 2023-06-22 at 12 14 14 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/2c012a6d-a1a9-4960-b5a3-795a3f713c2a">

<img width="314" alt="Screenshot 2023-06-22 at 12 14 04 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/dca3ab3e-1736-41bf-9868-1e816bdbbb59">

### Kubernetes Task

Installed minikube to make a kubernetes cluster using the following commands.

```
brew install minikube
minikube start
```
Using the postgres-deployment.yaml file the pod containing postgres container was created.
To connect postgres and airflow install the dependencies in postgres container. We need to run below commands to open postgres container terminal.

```
kubectl apply -f postgres-deployment.yaml
minikube ssh
docker exec -it -u root postgres-container-id /bin/bash
```

```
apt-get -y update
apt-get  -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget 
wget https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz
tar -xf Python-3.7.12.tgz
cd /Python-3.7.12
./configure --enable-optimizations
make -j $(nproc)
make altinstall
# STEPS TO INSTALL AIRFLOW VERSION 2.5.0
apt-get install libpq-dev
pip3.7 install "apache-airflow[postgres]==2.5.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@localhost:5432/airflow

airflow db init
airflow users create -u airflow -p airflow -f <fname> -l <lname> -e <mail> -r Admin

```

Then created a service of type clusterIP by running postgres-service.yaml to give access to postgres pods inside the cluster. The following command was used.

```
kubectl apply -f postgres-service.yaml
```

Using the airflow-deployment.yaml file the pod containing airflow container was made. The following command was used,
```
kubectl apply -f airflow-deployment.yaml
```

Creating dags and tasks in airflow scheduler.
```
minikube ssh
# for creating dag
docker exec -it -u root airflow-scheduler-id /bin/bash
cd dags
#installed vim by running these commands
apt-get update
apt install vim
vim time_task.py
# Write same dag file content here
```

airflow is accessible on below url Upon logging in, the dag was visible, then created a postgres connection and then ran my dag, it has been succesfully executed.

<img width="709" alt="Screenshot 2023-06-22 at 2 31 03 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/1710dc40-fd97-4674-9a62-8a271dddad21">

### DAG
<img width="1439" alt="Screenshot 2023-06-22 at 2 34 03 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/8bcbaa11-7b51-4ffd-9c38-4891da2b33d7">

<img width="318" alt="Screenshot 2023-06-22 at 2 35 27 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/e5c8c605-4002-4cc0-960a-fbe59f8d8d34">




