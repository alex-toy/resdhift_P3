import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']
DWH_ROLE_ARN = config.get("DWH","DWH_ROLE_ARN")


# STAGING TABLES INSERTION

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


# QUERY LISTS

copy_table_queries = [staging_events_copy, staging_songs_copy]

