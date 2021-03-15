# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"



# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    "artist" TEXT,
    "auth" TEXT,
    "firstName" TEXT,
    "gender" CHAR,
    "itemInSession" INTEGER,
    "lastName" TEXT,
    "length" DOUBLE PRECISION,
    "level" TEXT,
    "location" TEXT,
    "method" TEXT,
    "page" TEXT,
    "registration" DOUBLE PRECISION,
    "sessionId" INTEGER,
    "song" TEXT,
    "status" INTEGER,
    "ts" BIGINT,
    "userAgent" TEXT,
    "userId" TEXT
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    "song_id" BIGINT IDENTITY(1,1), 
    "num_songs" INTEGER,
    "artist_id" TEXT,
    "artist_latitude" TEXT,
    "artist_longitude" TEXT,
    "artist_location" TEXT,
    "artist_name" TEXT,
    "title" TEXT,
    "duration" DOUBLE PRECISION,
    "year" INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id BIGINT IDENTITY(1,1), 
    start_time date NOT NULL, 
    user_id text NOT NULL, 
    level text, 
    song_id text, 
    artist_id text, 
    session_id text, 
    location text, 
    user_agent text
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id text PRIMARY KEY, 
    first_name text NOT NULL, 
    last_name text NOT NULL, 
    gender text, 
    level text
);
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id text PRIMARY KEY, 
    title text NOT NULL, 
    artist_id text, 
    year int, 
    duration numeric
);
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id text PRIMARY KEY, 
    name text NOT NULL, 
    location text, 
    latitude text, 
    longitude text
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time date PRIMARY KEY, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
);
""")



# QUERY LISTS

create_table_queries = [
    staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create,
    artist_table_create, time_table_create
]

drop_table_queries = [
    staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop,
    artist_table_drop, time_table_drop
]

