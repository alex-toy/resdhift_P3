import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries




query = ("""
SELECT * FROM staging_events LIMIT 5;
""")

config = configparser.ConfigParser()
config.read('dwh.cfg')

conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
cur = conn.cursor()
cur.execute(query)