import os
import psycopg2
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Database connection information
dbname = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")

def print_table(rows, headers):
    if rows:
        print("\n" + "-"*80)
        print(" | ".join(headers))
        print("-"*80)
        for row in rows:
            print(" | ".join(str(col) for col in row))
        print("-"*80)

try:
    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor
    cur = conn.cursor()

    # Get list of tables in the database
    cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\'')
    tables = cur.fetchall()

    # Display the entire Pillcase table
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cur.execute(f'SELECT * FROM "public"."{table_name}"')
        try:
            rows = cur.fetchall()
            headers = [i[0] for i in cur.description]
            print_table(rows, headers)
        except psycopg2.Error as e:
            print("Error fetching data from table:", e)

    # Close cursor and connection
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to the database:", e)