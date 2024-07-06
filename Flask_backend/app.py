from platform import node
from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine
import logging

app = Flask(__name__)

# PostgreSQL connection details
db_name = 'sales_db'
user = 'postgres'
password = 'Geu260318'
host = 'localhost'
port = '5432'
# database = 'your_database'

DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'

#Function to read Postgresql data
def read_postgresql_data():
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.read_sql('SELECT * FROM sales', con=engine)
        return df
    except Exception as e:
        logging.error(f"Error while reading data from PostgreSQL: {e}")
        # return jsonify({"error": str(e)}), 500
        return None

# Function to read Excel data
def read_excel_data():
    try:
        df = pd.read_excel('Abuja_Branch.xlsx')
        return df
    except Exception as e:
        logging.error(f"Error while reading data from Excel: {e}")
        return None

# Endpoint for sales data filtering
@app.route('/api/sales', methods=['GET'])
def get_sales_data():
    source = request.args.get('source', 'sql')  # Default to 'excel' if not provided
    df = None
    
    if source == 'excel':
        df = read_excel_data()
    elif source == 'sql':
        df = read_postgresql_data()
    
    if df is None:
        return jsonify({"error": "Failed to load data."}), 500

    try:
        # Filtering parameters
        gender = request.args.get('Gender')
        branch = request.args.get('Branch')
        city = request.args.get('City')

        if gender:
            df = df[df['Gender'] == gender]
        if branch:
            df = df[df['Branch'] == branch]
        if city:
            df = df[df['City'] == city]

        
        # Check if df is a pandas DataFrame
        if isinstance(df, pd.DataFrame):
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({"error": "Data is not in the expected format."}), 500
        # return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)





































    # from flask import Flask, jsonify, request
# import pandas as pd
# from sqlalchemy import create_engine
# import logging
# import psycopg2



# app = Flask(__name__)

# # PostgreSQL connection details
# db_name = 'your_db_name'
# user = 'your_user'
# password = 'your_password'
# host = 'localhost'
# port = '5432'


# # Excel data reading
# def read_excel_data():
#     try:
#         df = pd.read_excel('Abuja_Branch.xlsx')
#         return df
#     except Exception as e:
#         logging.error(f"Error while reading data from excel: {e}")
#         # return jsonify({"error": str(e)}), 500
#         return None

# # # SQL data reading
# def read_sql_data():
#     try:
#         engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
#         df = pd.read_sql('SELECT * FROM sales', con=engine)
#         return df
#     except Exception as e:
#         logging.error(f"Error while reading data from PostgreSQL: {e}")
#         return None

# # Endpoint for Excel data
# @app.route('/api/xlsx', methods=['GET'])
# def get_excel_data():
#     df = read_excel_data()
#     return jsonify(df.to_dict(orient='records'))


# # Endpoint for SQL data
# @app.route('/api/sql', methods=['GET'])
# def get_sql_data():
#     df = read_sql_data()
#     return jsonify(df.to_dict(orient='records'))


# # Endpoint for sales data filtering
# @app.route('/api/sales', methods=['GET'])
# def get_sales_data():
#     source = request.args.get('excel')
#     try:
#         if source == 'excel':
#             df = read_excel_data()
        
#         # Filtering parameters
#         Gender = request.args.get('Gender')
#         Branch = request.args.get('Branch')
#         City = request.args.get('City')

#         if Gender:
#             df = df[df['Gender'] == Gender]
#         if Branch:
#             df = df[df['Branch'] == Branch]
#         if City:
#             df = df[df['City'] == City]

#         return jsonify(df.to_dict(orient='records'))

#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
