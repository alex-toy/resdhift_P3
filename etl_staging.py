import configparser
import psycopg2
from sql_queries_staging_insertion import copy_table_queries
from settings import config_file, get_connection


def load_staging_tables(cur, conn):
    """
    Utility function that loads data from S3 into staging tables in redshift cluster.

    Parameters
    ----------
    cur : cursor for psycopg2.connect object
    conn : psycopg2.connect object

    Returns
    -------
    No return.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()



if __name__ == "__main__":
    conn, cur = get_connection()
    
    load_staging_tables(cur, conn)
    conn.close()