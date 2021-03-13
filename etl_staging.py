import configparser
import psycopg2
from sql_queries_staging_insertion import copy_table_queries
from sql_queries_tables_insertion import insert_table_queries
from settings import config_file, get_connection


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    #config = configparser.ConfigParser()
    #config.read(config_file)
    #DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    #DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    #DWH_PORT               = config.get("DWH","DWH_PORT")
    #DWH_DB                 = config.get("DWH","DWH_DB")
    #DWH_ENDPOINT           = config.get("DWH","DWH_ENDPOINT")

    #conn_string = f"host={DWH_ENDPOINT} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
    #conn = psycopg2.connect(conn_string)
    #cur = conn.cursor()

    conn, cur = get_connection()
    
    load_staging_tables(cur, conn)
    conn.close()


if __name__ == "__main__":
    main()