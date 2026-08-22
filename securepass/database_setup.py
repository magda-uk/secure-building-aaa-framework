import mysql.connector
from db_utils import get_connection # We bring factory connection


def setup_database():
    # Sets up the db and create the tables
    try:
        # First step is to connect to your MySQL Server. 
        conn = get_connection()  
        cursor = conn.cursor() # Create your cursor object to execute SQL commands

        # Create the DB if it's not already there
        cursor.execute("CREATE DATABASE IF NOT EXISTS secure_pass_db")
        cursor.execute("USE secure_pass_db") # Start using the DB we just created

        print ("Database secure_pass has been created ✅")

        # Defining our tables in a dictionary to keep things organized
        tables ={
            "employees": """ CREATE TABLE IF NOT EXISTS employees(
                                badge_id VARCHAR(10) PRIMARY KEY,
                                first_name VARCHAR(50) NOT NULL,
                                last_name VARCHAR(50) NOT NULL,
                                security_level INT NOT NULL,
                                cantine_access VARCHAR(20) DEFAULT 'PENDING')""",
            
            "areas": """ CREATE TABLE IF NOT EXISTS areas(
                            area_name VARCHAR(50) PRIMARY KEY,
                            required_level INT NOT NULL)""",

            "access_logs": """ CREATE TABLE IF NOT EXISTS access_logs(
                                  log_id INT AUTO_INCREMENT PRIMARY KEY,
                                  badge_id VARCHAR(10),
                                  access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                  area_requested VARCHAR(50),
                                  access_result VARCHAR(50),
                                  FOREIGN KEY (badge_id) REFERENCES employees(badge_id),
                                  FOREIGN KEY (area_requested) REFERENCES areas(area_name)
                                  )"""
           
                 }
        # Loop through dictionary to create each table
        for name, query in tables.items():
            cursor.execute(query)
            print (f"Table {name} has been created ✅")
            
        # Save all the changes we just made
        conn.commit()

        # Clean up: close the cursor and the connection
        cursor.close()
        conn.close()
    
    except mysql.connector.Error as err:
        # If anything breaks (like a wrong password), show us the error
        print(f"Something went wrong: {err}")

# This ensures that setup_database() only triggers if we run this script directly, 
# and not if we import it from somewhere else.   
if __name__ == "__main__":
    setup_database()