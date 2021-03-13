config_file = '/Users/alexei/dwh.cfg'


def get_connection() :
    config = configparser.ConfigParser()
    config.read(config_file)
    DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT               = config.get("DWH","DWH_PORT")
    DWH_DB                 = config.get("DWH","DWH_DB")
    DWH_ENDPOINT           = config.get("DWH","DWH_ENDPOINT")

    conn_string = f"host={DWH_ENDPOINT} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    return conn, cur