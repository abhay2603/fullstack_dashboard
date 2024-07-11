import pandas as pd
from sqlalchemy import create_engine

# Load Excel data
df = pd.read_excel('Abuja_Branch.xlsx')

# PostgreSQL connection details
db_name = 'your_db_name'
user = 'your_user'
password = 'your_password'
host = 'localhost'  # or your PostgreSQL server address
port = '5432'  # default port for PostgreSQL

# Create the PostgreSQL engine
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')

# Create table and insert data
df.to_sql('sales', engine, if_exists='replace', index=False)

print("Data has been inserted into PostgreSQL.")



# import pandas as pd
# import sqlite3

# # Load Excel data
# df = pd.read_excel('Abuja_Branch.xlsx')

# # Connect to SQLite database
# conn = sqlite3.connect('sales.db')

# # Create table
# conn.execute('''
# CREATE TABLE IF NOT EXISTS sales (
#     InvoiceID TEXT,
#     Branch TEXT,
#     City TEXT,
#     CustomerType TEXT,
#     Gender TEXT,
#     ProductLine TEXT,
#     UnitPrice REAL,
#     Quantity INTEGER,
#     Tax REAL,
#     Total REAL,
#     Date TEXT,
#     Time TEXT,
#     Payment TEXT,
#     COGS REAL,
#     GrossMarginPercentage REAL,
#     GrossIncome REAL,
#     Rating REAL
# )
# ''')

# # Insert data into the table
# df.to_sql('sales', conn, if_exists='replace', index=False)

# # Commit and close connection
# conn.commit()
# conn.close()


# import sqlite3
# import pandas as pd

# # Connect to SQLite database (creates the database if it doesn't exist)
# conn = sqlite3.connect('sales.db')
# cursor = conn.cursor()

# # Create sales table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS sales (
#     id INTEGER PRIMARY KEY,
#     date TEXT,
#     product TEXT,
#     revenue REAL
# )
# ''')

# # Read the new excel data
# df = pd.read_excel('supermarkt_sales.xlsx')

# # Insert data into the sales table
# for index, row in df.iterrows():
#     cursor.execute('''
#     INSERT INTO sales (date, product, revenue) VALUES (?, ?, ?)
#     ''', (row['Date'], row['Product'], row['Revenue']))

# # Commit and close connection
# conn.commit()
# conn.close()

# print("Database created and populated successfully.")


# import sqlite3

# # Connect to SQLite database (creates the database if it doesn't exist)
# conn = sqlite3.connect('sales.db')
# cursor = conn.cursor()

# # Create sales table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS sales (
#     id INTEGER PRIMARY KEY,
#     date TEXT,
#     product TEXT,
#     region TEXT,
#     sales INTEGER
# )
# ''')

# # Insert sample data
# cursor.executemany('''
# INSERT INTO sales (date, product, region, sales) VALUES (?, ?, ?, ?)
# ''', [
#     ('2023-01-01', 'A', 'North', 100),
#     ('2023-01-02', 'B', 'South', 200),
#     ('2023-01-03', 'C', 'East', 150),
#     ('2023-01-04', 'D', 'West', 250)
# ])

# # Commit and close connection
# conn.commit()
# conn.close()

# print("Database created and populated successfully.")

