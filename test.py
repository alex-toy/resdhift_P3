from settings import get_connection


conn, cur = get_connection()


query = """
SELECT songplays.start_time, songplays.level, songplays.location, title as songname, name as artist, first_name as userName, time.hour
FROM songplays
JOIN songs ON (songplays.song_id = songs.song_id)
JOIN artists ON (songplays.artist_id = artists.artist_id)
JOIN users ON (songplays.user_id = users.user_id)
JOIN time ON (songplays.start_time = time.start_time)
WHERE title = 'Setanta matins'
AND name = 'Elena'
LIMIT 10;
"""
cur.execute(query)



query = """
SELECT songplays.start_time, songplays.level, songplays.location, title as songname
FROM songplays
JOIN songs ON (songplays.song_id = songs.song_id)
JOIN artists ON (songplays.artist_id = artists.artist_id)
JOIN users ON (songplays.user_id = users.user_id)
JOIN time ON (songplays.start_time = time.start_time)
LIMIT 15;
"""
cur.execute(query)


conn.close()
