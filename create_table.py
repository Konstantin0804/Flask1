import os
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))

def create_connection(path):
   try:
       print("Connection to SQLite DB successful")
       return sqlite3.connect(path)
   except Error as e:
       print(f"The error '{e}' occurred")


def execute_query(connection, query):
   cursor = connection.cursor()
   try:
       cursor.executescript(query)
       connection.commit()
       print("Query executed successfully")
   except Error as e:
       print(f"The error '{e}' occurred")

create_quote_table = """
CREATE TABLE IF NOT EXISTS quotes (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 author TEXT NOT NULL,
 quote TEXT NOT NULL
);
"""

def main():
    path = os.path.join(base_dir, "db.sqlite")
    connect = create_connection(path)
    execute_query(connect, create_quote_table)


if __name__ == "__main__":
    main()