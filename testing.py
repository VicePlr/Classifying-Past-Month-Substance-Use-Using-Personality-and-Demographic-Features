import sqlite3
import pandas as pd

conn = sqlite3.connect(r"sqlite3\sqlite.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Age INTEGER
    )
"""
)

data = pd.read_csv(r"data\raw\drug_consumption.data", index_col=False)
print(data)
cursor.execute("""
    INSERT INTO students(Name, Age) VALUES("Hoang Trong Hieu", 19)
"""
)

conn.commit()

cursor.execute("""
    SELECT * FROM students
"""
)

rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
