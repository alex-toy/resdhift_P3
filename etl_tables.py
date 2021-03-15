import configparser
import psycopg2
from sql_queries_tables_insertion import insert_table_queries
from settings import config_file, get_connection


def insert_tables(cur, conn):
    """
    Utility function that inserts data from Staging tables into fact and dimension tables in redshift cluster.

    Parameters
    ----------
    cur : cursor for psycopg2.connect object
    conn : psycopg2.connect object

    Returns
    -------
    No return.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()



if __name__ == "__main__":
    conn, cur = get_connection()
    insert_tables(cur, conn)
    conn.close()