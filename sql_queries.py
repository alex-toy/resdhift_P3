import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']
DWH_ROLE_ARN = config.get("DWH","DWH_ROLE_ARN")


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
    "songplay_id" BIGINT IDENTITY(1,1), 
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


# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events 
    FROM '{}'
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    FORMAT AS json '{}';
""").format(LOG_DATA, DWH_ROLE_ARN, LOG_JSONPATH)


staging_songs_copy = ("""
    COPY staging_songs 
    FROM '{}'
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    FORMAT AS json '{}';
""").format(SONG_DATA, DWH_ROLE_ARN, LOG_JSONPATH)


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (user_id, level, session_id, location, user_agent, song_id, artist_id, start_time)
SELECT user_id, level, session_id, location, user_agent, song_id, artist_id, ts
FROM staging_events
JOIN staging_songs ON (staging_events.song = staging_songs.song AND staging_events.artist = staging_songs.artist);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT user_id, first_name, last_name, gender, level
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, year, duration, artist_id)
SELECT song_id, title, year, cast(duration as float), artist_id 
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING;
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

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
