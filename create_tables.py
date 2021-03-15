import configparser
import psycopg2
from sql_queries_creation import create_table_queries, drop_table_queries
from settings import config_file, get_connection

def drop_tables(cur, conn):
    """
    Utility function that drop tables in redshift cluster.

    Parameters
    ----------
    cur : cursor for psycopg2.connect object
    conn : psycopg2.connect object

    Returns
    -------
    No return.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Utility function that creates tables in redshift cluster.

    Parameters
    ----------
    cur : cursor for psycopg2.connect object
    conn : psycopg2.connect object

    Returns
    -------
    No return.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        



if __name__ == "__main__":
    conn, cur = get_connection()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()