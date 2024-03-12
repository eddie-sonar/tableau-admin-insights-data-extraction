import os
import pandas as pd
import time
import sqlite3

# Create database connection
conn = sqlite3.connect("admin_insights.db")

csv_location = "./csv"

print("\n----- Loading to sqlite db -----\n")
for csv in os.listdir(csv_location): 
    csv_file = f"{csv_location}/{csv}"
    df = pd.read_csv(csv_file)
    table_name = "adm_" + csv.removesuffix(".csv").lower()
    print(f"creating {table_name}")

    # start_time = time.time()
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    # end_time = time.time() - start_time
    # print(f"{table_name} took {end_time} seconds")

print("\nAll done!")