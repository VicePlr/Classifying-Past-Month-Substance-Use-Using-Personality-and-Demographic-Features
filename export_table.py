import sqlite3
import pandas as pd
from contextlib import closing

with closing(sqlite3.Connection("database.sqlite3")) as conn:
    df_raw = pd.read_sql_query("SELECT * FROM data_raw", con=conn)
    df_raw.to_csv("tables/raw_data.csv", index=False)
    df_clean = pd.read_sql_query("SELECT * FROM data_clean", con=conn)
    df_clean.to_csv("tables/clean_data.csv", index=False)