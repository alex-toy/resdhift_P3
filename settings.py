import configparser
import psycopg2

config_file = "path/to/dwh.cfg"


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


def set_config_file(config_file, DWH_ENDPOINT, DWH_ROLE_ARN) :
    lines = []
    with open(config_file, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines) :
            if line.startswith('DWH_ENDPOINT') :
                lines[index] = f"DWH_ENDPOINT={DWH_ENDPOINT}\n"

            if line.startswith('DWH_ROLE_ARN') :
                lines[index] = f"DWH_ROLE_ARN={DWH_ROLE_ARN}"

    with open(config_file, 'w') as f:
        f.writelines(lines)




if __name__ == "__main__":

    DWH_ENDPOINT = 'khjgupimghjtestDWH_ENDPOINT'
    DWH_ROLE_ARN = 'temklkjôi$p`jokstDWH_ROLE_ARN'

    set_config_file(config_file, DWH_ENDPOINT, DWH_ROLE_ARN)