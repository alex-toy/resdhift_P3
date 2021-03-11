import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']


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
    songplay_id SERIAL PRIMARY KEY, 
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

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    song_id text PRIMARY KEY, 
    title text NOT NULL, 
    artist_id text, 
    year int, 
    duration numeric
);
""")

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id SERIAL PRIMARY KEY, 
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

staging_events_copyold = ("""
COPY staging_events 
FROM {}
CREDENTIALS {}
COMPUPDATE OFF region 'us-west-2'
format as json {};
""").format(LOG_DATA,'aws_iam_role='+IAM_ROLE,LOG_JSONPATH)


table = "part"
DWH_ROLE_ARN="arn:aws:iam::850736946254:role/dwhRole"
staging_events_copy = """
copy {} from 's3://awssampledbuswest2/ssbgz/{}' 
credentials 'aws_iam_role={}'
gzip region 'us-west-2';
""".format(table,table, DWH_ROLE_ARN)


staging_songs_copy = ("""
COPY staging_songs 
FROM {}
CREDENTIALS aws_iam_role={}
COMPUPDATE OFF region 'us-west-2'
FORMAT AS JSON 'auto';
""").format(SONG_DATA, IAM_ROLE)


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO NOTHING;
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
