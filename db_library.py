import mysql.connector
from config import db_config

"""
TASK: CREATE_LIBRARY_SYSTEM 
- Make database library_db
- Create tables for authors, books, borrowers and book_loans
"""

def create_library_system():
    try:
        db = mysql.connector.connect(**db_config) # First step is to connect to your MySQL Server
        cursor= db.cursor() # Create your cursor object to make queries

        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        cursor.execute("USE library_db")

        print ("Database library_db is done!")

        tables ={
            "authors": """ CREATE TABLE IF NOT EXISTS authors (
                                author_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR (255) NOT NULL)""",
            
            "books": """CREATE TABLE IF NOT EXISTS books (
                           book_id INT AUTO_INCREMENT PRIMARY KEY,
                           title VARCHAR(255) NOT NULL,
                           author_name VARCHAR(255),
                           pub_year INT,
                           genre VARCHAR(100),
                           available BOOLEAN DEFAULT TRUE
                       )""",

            "borrowers": """
                       CREATE TABLE IF NOT EXISTS borrowers (
                           borrower_id INT AUTO_INCREMENT PRIMARY KEY,
                           name VARCHAR(255) NOT NULL
                       )""",

            "book_loans": """
                       CREATE TABLE IF NOT EXISTS book_loans (
                           loan_id INT AUTO_INCREMENT PRIMARY KEY,
                           book_id INT,
                           borrower_id INT
                       )"""

        }

         # loops around the dictionary of dictionaries, and executes the value (aka the query)
        for name, query in tables.items():
           cursor.execute(query) # executing queries one by one, in a loop
           print (f"Table {name} has been created")

        db.commit() # commit the changes
        cursor.close() # close the cursor
        db.close() # close the connection to the SQL server

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")

if __name__ == "__main__":
    create_library_system()

        

