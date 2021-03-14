import configparser
import psycopg2
from sql_queries_tables_insertion import insert_table_queries


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    conn, cur = get_connection()
    insert_tables(cur, conn)
    conn.close()


if __name__ == "__main__":
    main()