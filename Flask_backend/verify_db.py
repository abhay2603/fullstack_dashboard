import sqlite3
import psycopg2

# PostgreSQL connection details
db_name = 'your_db_name'
user = 'your_user'
password = 'your_password'
host = 'localhost'
port = '5432'

# Connect to the database
conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

# Fetch and print data
cursor.execute('SELECT * FROM sales')
rows = cursor.fetchall()
for row in rows:
    print(row)


conn.close()
