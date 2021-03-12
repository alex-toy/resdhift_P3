import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, copy_table_queries, staging_events_copy


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT               = config.get("DWH","DWH_PORT")
    DWH_DB                 = config.get("DWH","DWH_DB")
    DWH_ENDPOINT           = config.get("DWH","DWH_ENDPOINT")

    conn_string = f"host={DWH_ENDPOINT} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
    #conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()