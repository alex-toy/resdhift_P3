# FINAL TABLES INSERTION

songplay_table_insert = ("""
INSERT INTO songplays (user_id, level, session_id, location, user_agent, song_id, artist_id, start_time)
SELECT user_id, level, session_id, location, user_agent, song_id, artist_id, TO_CHAR(ts, 'MON-DD-YYYY HH12:MIPM')
FROM staging_events
JOIN staging_songs ON (staging_events.song = staging_songs.title AND staging_events.artist = staging_songs.artist_name);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT user_id, first_name, last_name, gender, level
FROM staging_events
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, year, duration, artist_id)
SELECT song_id, title, year, cast(duration as float), artist_id 
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs
ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT TO_CHAR(ts, 'MON-DD-YYYY HH12:MIPM'), EXTRACT(hour from ts), EXTRACT(day from ts), EXTRACT(week from ts), EXTRACT(month from ts), EXTRACT(year from ts), EXTRACT(weekday from ts)
FROM staging_events
""")


# QUERY LISTS

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
