# Data Engineering project 3 - Data Warehouse with AWS Redshift

By Alessio Rea

==============================

You need to have Python 3.8.5 installed for this project

# General explanation

## 1. Purpose of the project

The purpose of the project is to build an ETL pipeline that extracts data from S3, stages it in Redshift, and transforms data into a set of dimensional tables for analysis and insights in what songs users are listening to. Data is modelled according to a star schema with fact and dimension tables for fast and easy analysis. Redshift gives the opportunity to execute SQL statements that create the analytics tables from these staging tables.



## 2. Database schema design and ETL pipeline

In this project, initial dataset comes from two json files :

- First : Song Dataset
    
    Here are filepaths to two files that could be found in such a dataset :

    ```
    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json
    ```

    Here is an example of what a single song file may looks like :

    ```
    {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
    ```

    Those files contain the following features : 'artist_id', 'artist_latitude', 'artist_location', 'artist_longitude', 'artist_name', 'duration', 'num_songs', 'song_id', 'title', 'year'

- Second : Log Dataset
    
    Here are filepaths to two files that could be found in such a dataset :

    ```
    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json
    ```
    
    Those files contain the following features : 'artist', 'auth', 'firstName', 'gender', 'itemInSession', 'lastName',
       'length', 'level', 'location', 'method', 'page', 'registration',
       'sessionId', 'song', 'status', 'ts', 'userAgent', 'userId'


Here is how the data is modelled according to a star schema :

- Fact table : table songplays containing the following features : songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

- Dimension tables : 

    - users - users in the app. Features : user_id, first_name, last_name, gender, level
    - songs - songs in music database. Features : song_id, title, artist_id, year, duration
    - artists - artists in music database. Features : artist_id, name, location, latitude, longitude
    - time - timestamps of records in songplays broken down into specific units. Features : start_time, hour, day, week, month, year, weekday


## 3. Example queries and results for song play analysis

Once the data has been ETLed, you are free to take full benefit from the power of star modelling and make business driven queries like :

    - Which song has been played by user 'Lily' on a paid level?
    - When did user 'Lily' play song from artist 'Elena'?



# Project Organization 
----------------------

    ????????? README.md                           <- The top-level README for users and developers using this project.
    ????????? create_tables.py                    <- Python script allowing to create database, create / drop tables with appropriate schema.
    ????????? IaC1.py                             <- Creates new iam role, attaches policy AmazonS3ReadOnlyAccess to it and finally creates new cluster programmatically.
    ????????? IaC2.py                             <- Open an incoming TCP port to access the cluster endpoint.
    ????????? etl_staging.ipynb                   <- Loads staging tables from S3 into cluster.
    ????????? etl_tables.ipynb                    <- Creates facts and dimension tables.
    ????????? requirements.txt                    <- install psycopg2 for local use
    ????????? sql_queries_creation.py             <- SQL queries for creation of tables
    ????????? sql_queries_staging_insertion.py    <- SQL queries for insertion of data into staging tables.
    ????????? sql_queries_tables_insertion.py     <- SQL queries for insertion of data into fact and dimension tables.
    ????????? test.ipynb                          <- Unitary tests for creation, deletion, insertion steps
    ????????? release_resources.py                <- Automatically release all resources created on Redshift.
    ????????? settings.py                         <- Useful functions for project.
    ????????? get_files_from_S3.py                <- Download files form S3 to have a look at internal structure.
    ????????? dwh.cfg                             <- Config file containing credentials. Hide it!!




# Getting started

## 1. Clone this repository

```
$ git clone <this_project>
$ cd <this_project>
```

## 2. Install requirements

I suggest you create a python virtual environment for this project : <https://docs.python.org/3/tutorial/venv.html>

I had a problem installing psycopg2. The following lines did the trick though :

```
- export LDFLAGS="-L/usr/local/opt/openssl/lib"
- export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

```
$ pip install -r requirements.txt
```

--------


## 2. Configuration of project

You need to have an AWS account to run the complete analysis. You also need to create a user that has AmazonRedshiftFullAccess as well as AmazonS3ReadOnlyAccess policies. Make sure to keep its KEY and SECRET credentials in a safe place.

1. Copy the *dwh.cfg* into a safe place.
2. Fill in all fields except *LOG_DATA*, *LOG_JSONPATH*, *SONG_DATA* which are already filled and *DWH_ENDPOINT*, *DWH_ROLE_ARN* which will be automatically filled for you. 
3. In file *settings.py*, give the path to *dwh.cfg* to variable *config_file*.
4. Run *IaC_1.py* and wait untill you see the cluster available in your console.
4. Run *IaC_2.py*.
5. Run *create_tables.py* and check that all tables are created in the redshift query editor.
6. Run *etl_staging.py*, then *etl_tables.py*. In the query editor, run queries to ensure that tables *staging_events* and *staging_songs* and other fact and dimension tables are properly populated.
7. Fill free to write queries in *test.py* to analyse the data.
8. Once done, don't forget to *release_resources.py* !!!!


--------


