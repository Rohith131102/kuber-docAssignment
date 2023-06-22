# Peer Learning's Document

## Aswat's Approach:

### Docker task: 
- He containerized Airflow and its components by creating Docker containers. 
- To ensure the installation of psycopg2 in all the containers, he utilized a Dockerfile. 
- Within the Docker containers, he developed a DAG (Directed Acyclic Graph) that consisted of two tasks: Task 1 involved creating a table to store the execution date, while Task 2 involved inserting data into the table. He successfully extracted the execution date using kwargs.

### Kubernetes task:
- He opted to use the Postgres helm chart from the Bitnami repository. 
- By installing the Postgres container using the helm chart, he was able to set the password as "postgres".
- In the Postgres container, he built Python and installed Airflow, specifically version 2.5.0 with Postgres support. 
- To establish the Postgres container as Airflow's database, he initialized it accordingly. 
- He ensured the connection between Airflow and Postgres by setting the environment variable AIRFLOW__DATABASE__SQL_ALCHEMY_CONN to the Postgres connection string. 
- Within the Postgres container, he initialized Airflow's database using the relevant command.
- For the deployment and service of Airflow, he created an Airflow deployment and service, utilizing the Postgres service.
- By applying the Airflow deployment and service configuration from the airflow.yaml file, he effectively managed Airflow's setup.
- Finally, he added the DAG file to the Airflow scheduler, completing the Kubernetes assignment.



## Praneeth's Review

### Docker task
- He created a dag with two tasks in Python language, which consists of tasks of the
name -

  a. Create_table - creating the table
  
  b. Insert_into_table - Inserting the data into a table
  
  c. Query_task - Querying a table, which validates the entries.
  
- A connection was established to the database for airflow.
- compiled all the necessary services into a docker-compose file.
- He launched the airflow container by using the docker-compose command.
- He established and verified a connection to Postgres.


### Kubernetes task
- He created a custom docker image for Postgres with airflow installed in it.
- Pushed the Postgres image and the custom airflow image in docker hub for public access.
- Installed minikube to make a Kubernetes cluster.
- Created the Postgres-deployment.yaml file which contains the pod containing Postgres container.
- Created a service of type clusterIP by running postgres-service.yaml to give access to postgres pods inside the cluster.
- Created persistent volumes dags-storage.yaml to mount the dags folder inside the airflow container to the local directory.
- Created a service of type load balancer by running airflow-service.yaml to access airflow webserver from the local system.
- Accessed the airflow webserver by running the command minikube service airflow
