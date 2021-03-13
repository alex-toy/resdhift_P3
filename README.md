# Data Engineering project 3 - Data Warehouse with AWS Redshift

By Alessio Rea

==============================

You need to have Python 3.6.3 installed for this project

# General explanation

## 1. Purpose of the project

The purpose of the project is to build an ETL pipeline that extracts data from S3, stages it in Redshift, and transforms data into a set of dimensional tables for analysis,and insights in what songs users are listening to. Data is modelled according to a star schema with fact and dimension tables for easy and fast analysis. Redshift gives the opportunity to execute SQL statements that create the analytics tables from these staging tables.



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

    ├── README.md               <- The top-level README for users and developers using this project.
    ├── create_tables.py        <- Python script allowing to create database, create / drop tables with appropriate schema
    ├── etl.ipynb               <- Notebook for step by step testing
    ├── requirements.txt        <- install psycopg2 for local use
    ├── sql_queries.py          <- SQL queries
    ├── test.ipynb              <- unitary tests for creation, deletion, insertion steps
    ├── etl.py                  <- Python script allowing to create tables based on json files
    ├── stack.yml               <- Docker container for postgres image
    ├── data_querying.ipynb     <- Notebook for querying the star model
    ├── data                    <- json files containing data




# Getting started

## 1. Clone this repository

```
$ git clone <this_project>
$ cd <this_project>
```

## 2. Install requirements

```
$ pip install -r requirements.txt
```
--------


