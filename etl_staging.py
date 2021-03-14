import configparser
import psycopg2
from sql_queries_staging_insertion import copy_table_queries
from settings import config_file, get_connection


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    conn, cur = get_connection()
    
    load_staging_tables(cur, conn)
    conn.close()


if __name__ == "__main__":
    main()