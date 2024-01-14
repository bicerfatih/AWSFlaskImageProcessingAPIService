"""
Database Management Module
--------------------------

This module handles all database-related operations for the image processing application. It includes
functions for creating a SQLite database, creating a table for storing image data, and inserting
resized image data into the database.

Functions:
- create_and_populate_db(csv_file, db_name): Creates a database and populates it with data from a CSV file.
"""

import sqlite3
import pandas as pd

def create_and_populate_db(csv_file, db_name='images.db'):
    # Create a new SQLite database
    db_connection = sqlite3.connect(db_name)

    # Create a table for storing image data
    columns = ', '.join([f'col{i} INTEGER' for i in range(1, 151)])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS image_data (
        depth REAL PRIMARY KEY,
        {columns}
    );
    """
    db_connection.execute(create_table_query)

    # Read the resized image data from CSV
    resized_data = pd.read_csv(csv_file)

    # Insert data into the database
    resized_data.to_sql('image_data', db_connection, if_exists='replace', index=False)

    # Close the database connection
    db_connection.close()
