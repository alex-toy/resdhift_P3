#from sql_queries import create_table_queries, drop_table_queries
from settings import get_connection


conn, cur = get_connection()
cur.execute("SELECT * FROM staging_events LIMIT 5;")
conn.close()
