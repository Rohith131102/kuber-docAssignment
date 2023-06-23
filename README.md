# Docker and Kubernets Assignment

## Question

<img width="554" alt="Screenshot 2023-06-22 at 3 19 12 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/9e0408cd-44cc-4a87-847a-735fe81c9135">


### Approach

- The dags folder contains .py files for the dags created in correspondence to question-1.
- The .yaml files contains details of configuration required required for other tasks.

## Docker Task

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

<img width="1434" alt="Screenshot 2023-06-22 at 12 14 14 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/a4c0f992-ea89-4fae-bec5-13930befaa56">

<img width="314" alt="Screenshot 2023-06-22 at 12 14 04 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/12aac2ec-2acd-48c7-b0c4-c36d794891b4">


## Kubernetes Task

Installed minikube to make a kubernetes cluster using the following commands.

```
brew install minikube
minikube start
```

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

<img width="709" alt="Screenshot 2023-06-22 at 2 31 03 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/cac3544b-1063-4380-a660-9c8bc66fb5db">

### DAG

<img width="1439" alt="Screenshot 2023-06-22 at 2 34 03 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/b29f4631-f0cf-4db6-9ed5-6d12db91e360">


<img width="318" alt="Screenshot 2023-06-22 at 2 35 27 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/84d7b661-4d83-44ba-9b24-bbc2e3edee9d">



### Postgres-deployment.yaml

- This .yaml file represents a Kubernetes Deployment resource definition for a PostgreSQL database container. It creates a deployment named "postgres" with a single replica.

- A Deployment in Kubernetes is responsible for managing the lifecycle of a set of pods. In this case, the Deployment ensures that one replica of the PostgreSQL container is running and maintained within the cluster.

- The PostgreSQL container is defined with the image "postgres:latest", which refers to the latest version of the official PostgreSQL Docker image. The container exposes port 5432 for communication.

- The environment variables `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` are set within the container to configure the database. The values for these variables are set to "airflow" in this example.

- The `POSTGRES_PASSWORD` value is obtained from a secret named "postgres-creds". This secret is created separately, and the key named "password" is referenced in the `secretKeyRef` field.
  
Using the postgres-deployment.yaml file the pod containing postgres container was created.
To connect postgres and airflow install the dependencies in postgres container. We need to run below commands to open postgres container terminal.



### Postgres-service.yaml

This .yaml defines a Kubernetes Service named "postgres" that exposes a port for communication with a PostgreSQL database deployment.

A Service in Kubernetes acts as an abstraction layer that enables other pods or services to communicate with it, regardless of their location within the cluster. The Service YAML includes the following specifications:

- `apiVersion: v1`: Specifies the Kubernetes API version used for this resource.
- `kind: Service`: Indicates that this resource is a Service.
- `metadata: name: postgres`: Specifies the name of the Service as "postgres".
- `spec:`: Defines the Service's specifications.
  - `ports:`: Specifies the ports exposed by the Service.
    - `- port: 5432`: Exposes port 5432 for the Service, which is the default port for PostgreSQL database connections.
  - `selector:`: Determines the set of pods targeted by the Service.
    - `deploy: postgres`: Selects pods with the label "deploy" set to "postgres". This label is used to identify the pods associated with the PostgreSQL deployment.

### Airflow-deployment.yaml

This .yaml defines a Kubernetes Deployment for Apache Airflow, version 2.5.0. It creates a single replica of the deployment and includes two containers: one for the Airflow Scheduler and another for the Airflow Webserver. The Scheduler container runs the Airflow scheduler, while the Webserver container runs the Airflow webserver. Both containers are configured to connect to a PostgreSQL database using environment variables. The Webserver container exposes port 8080 for communication.

### Airflow-service.yaml

This .yaml defines a Kubernetes Service called "airflow", as below

- `spec:`: Defines the Service's specifications.
  - `type: LoadBalancer`: Specifies that a cloud provider load balancer should be created to expose the Service externally. This allows external access to the Airflow application.
  - `ports:`: Specifies the ports configuration for the Service.
    - `port: 8080`: Sets the port number as 8080 for the Service. This is the port that will be exposed by the Service.
      - `protocol: TCP`: Specifies that the traffic protocol for this port is TCP.
      - `targetPort: 8080`: Sets the target port as 8080. This indicates that traffic arriving at the Service's port 8080 will be forwarded to the pods associated with the Service, specifically to port 8080 on those pods.
  - `selector:`: Determines the set of pods targeted by the Service.
    - `deploy: airflow`: Selects pods with the label "deploy" set to "airflow". This label is used to identify the pods associated with the Airflow Deployment.
   
### Secrets management using secrets.yaml
In the context of Kubernetes, a secrets.yaml file is a YAML file used to define and manage sensitive information, such as passwords, API keys, or certificates, within a Kubernetes cluster.

The things need to be secured like password are stored in secrets.yaml file by encoding using base64 and these values are further referenced from required value space and mapped them with the orginal values, so as to preseve them, the secrets.yaml is applied by below command.

```
kubectl apply -f secrets.yaml
```

### DAG after adding secrets

<img width="1436" alt="Screenshot 2023-06-23 at 5 43 06 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/fa80a98c-4e2e-455b-bd54-40acd244ffc9">

<img width="364" alt="Screenshot 2023-06-23 at 6 11 22 PM" src="https://github.com/Rohith131102/kuber-docAssignment/assets/123619674/a326e340-b92a-43d1-81a6-2ec3c4993a82">

