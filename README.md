# JSON Documents Pipeline

# Introduction & Goals
This project combined tools like Jupyter/Pyspark-notebook, bitnami/Kafka image, FastAPI, Asyncio, Aiohttp, MongoDB image, SQLAlchemy, Postgres, Airflow image and the Docker.
Probably all these tools were connected and pulled to the pipeline in the Docker container. After pipeline speed was tested using client script, which simulated the stream of documents and estimated the response time. The maximum pipeline speed is around 20 responses(JSON documents) per second.

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Connection](#connection)
  - [Buffer](#buffer)
  - [Storage](#storage)
- [Pipeline](#pipeline)
- [Additional Tools](#additional-tools)
  - [Authentication](#authentication) 
  - [Airflow](#airflow)
- [Conclusion](#conclusion)
- [LinkedIn Profile](#linkedin-profile)


# The Data Set
The free data set was used from open-source Kaggle about customers and invoices.
The data set had 6 columns and more than 500K rows. The date had an unusual format (%d/%m/%Y %H:%M).\
This format was considered in the API main file. 

# Used Tools
- FastAPI received the data from the simulated user stream. Also, using FastAPI there was built a script of connection to Postgres image and transferring tokens and credentials system. 
- As a buffer, the BitnamiKafka image was used. It provides the distribution of load and message streams.
- MongoDB was used as the main storage of documents. It is the best choice for storing JSON documents. 
- For deployment, Docker was the best solution since it provides an isolated environment and uses only the computer resources\
This feature allows you to run this application on any OS.
- The Python Aiohttp and Asyncio libraries were used for the client stream. A combination of them allows to simulate a stream of requests. 
- For the inner adjustments and document transformation, Apache Spark in Jupiter Notebook was used. This combination can be used as a separate container. Also, Jupiter Notebook can be started on the web. This feature allows us to regulate and modify connections and data transformation code without stopping the container.
- Postgres image was used with Adminer image to provide UI for the database of all registered users.
- An Airflow image was added as the additional tool for analyzation of registered users from Postgres. Airflow contains two scheduled dags. The first one (User_counter) creates a new table "users_count". It counts the number of registered users in the user table and each minute adds data (operation ID, count number, and timestamp). The second dag (CountCleaner) runs each hour and deletes all stored count rows.

## Connection
 The main part of the inner connection was built in the Docker container using Docker ports and network. Probably all the bounds were defined in the docker-compose file.
 For the external connection and client simulation FastAPI, Aiohttp, and Asyncio were used. Client simulation code had two tasks: to send a large number of requests, estimate the number of errors, and sort the invalid JSON requests.\
 From the Spark in the project, I used SparkSession, readStream&writeStream, DataFrame tools, and SQL queries. For document formation, the foreachBatch function was added. For the Postgres connection, SQLAlchemy was used.
 
## Buffer
BitnamiKafka image was used as a buffer. API was set on the producer's side and Spark from the consumer side. In the docker-compose in the environment section were specified external and internal ports for the ability to connect API independently of the container. In other words, we can send Kafka messages from external sources and inside the Docker network.

## Storage
 Mongo and Mongo-express images can work as the NoSQL database and user interface. The client can easily connect to MongoDB using credentials from docker-compose and browser. The Mongo-express can be used to adjust the collections in the database.

# Pipeline
As was mentioned above, the pipeline consists of API, BitnamiKafka, and Spark. The pipeline was pushed to the Docker container. The advantage of this pipeline is that all its components are stored in the container as well as the data processing code can be modified through the API connection to Jupiter Notebook container.

## Authentication
Authentication was created using FastAIP, SQLAlchemy, and Postgres. A client has to provide the username and password as a JSON string. This data will pass through schema and after SQLAlchemy will send it to Postgres. The password is stored in hash form in Postgres for security purposes. Using the same credentials the client can request the token using a separate API URL. Only by providing the token in the header section client can send the documents in the main pipeline. Authentication slows down the velocity of the pipeline by 50 percent.

## Airflow
The docker-compose file base was used from the airflow docker-compose file that the command can create: curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'. As was mentioned above, Airflow in this project stored information about the amount of users that can request a token. For testing purposes, Airflow work was scheduled for each minute activation. 

# Pipeline testing
There was built special Asynchronous_api_client  and api_client scripts for testing purposes. This Asynchronous_api_client has two main features. The first one is the simulation of the loaded stream. The second feature is to estimate the speed and the proper work of the pipeline. We have to consider that the speed depends mostly on the computer resources and system adjustments. In the test of the pipeline, 5000 requests were used. 1254 requests  could not pass since some fields had a None value which was not allowed in the Base model of API (some documents also had other reasons for rejection). To pass 3746 and reject 1254 documents, the pipeline took around 253 seconds. So the speed was around 20 requests per second on the machine with 16Ram and Intel(R) Core(TM) i5-6500 CPU 3.20GHz. All the documents were stored in MongoDB without any losses. 

# Conclusion
This project allowed me to learn the basics of configurations in docker, Api connection, and data transformation. Also, this project estimated the speed of the pipeline, 20 Json documents per second without errors from the pipeline side.

# LinkedIn Profile
- www.linkedin.com/in/arūras
