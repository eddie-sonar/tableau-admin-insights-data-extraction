# THIS SCRIPT DOESNT WORK

import os
import pandas as pd
import sqlalchemy
import time

def get_rs_connection() -> str:
    """
    Returns a sqlalchemy connection string pointing to our Redshift Data Warehouse.

    The format of the URL generally follows RFC-1738, with some exceptions, including
    that, underscores, not dashes or periods, are accepted within the “scheme” portion.
    URLs typically include username, password, hostname, and database name fields, as well
    as optional keyword arguments for additional configuration.

    Environment
    ----------
    To avoid exposure of credentials, the following environment variables are needed:

    OP_ID_RS: ID of the item in 1Password that stores the warehouse password.
    RS_USER: Username of the user to connect to the warehouse

    The typical form of a database URL is:

    ```
      dialect+driver://username:password@host:port/database
    ```

    Returns:
    ----------
        str: SQLAlchemy connection string
    """

    RS_USER = os.getenv("DBT_ENV_RS_USER")
    RS_PWD = os.getenv("DBT_ENV_SECRET_RS_PASSWORD")

    PORT = 5439
    URL = "redshift.sonardata.io"

    connection_string = (
        "postgresql://{user}:{password}@{url}:{port}/sonarsource".format(
            user=RS_USER, password=RS_PWD, port=PORT, url=URL
        )
    )

    return connection_string

# Connect to Redshift
connection_string = get_rs_connection()

# Create database connection
engine = sqlalchemy.create_engine(connection_string)
conn = engine.raw_connection()
schema = 'dbt_ewang'

csv_location = "./csv"

for csv in os.listdir(csv_location): 
    csv_file = f"{csv_location}/{csv}"
    df = pd.read_csv(csv_file)
    table_name = "adm_" + csv.removesuffix(".csv").lower()
    print(f"uploading {csv_file} to {schema}.{table_name}")

    start_time = time.time()
    df.to_sql(table_name, engine, schema, index=False, if_exists='replace')
    end_time = time.time() - start_time
    print(f"{schema}.{table_name} took {end_time} seconds")
