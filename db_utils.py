"""
Description:
    Contains all database logic, including SQL queries.
    Connection management using Context Managers (with).
    Helper function get_connection().
    
Principles:
    - Exception Handling: Specific capture of MySQL errors.
    - Resource Safety: Automatic closing of connections and cursors.
    - Non-repudiation: Mandatory logging of every access attempt.

Core Functions:
    - db_query_check_badge: Authenticates employees.
    - db_query_update_cantine: Updates employee cantine status to AUTHORIZED
    - db_query_verify_access: Authorizes entry based on security levels.
    - db_insert_access_attempt: Logs all entry attempts.
    - db_register_security_issue: Wrapper Function to Records manual security alerts.
    - db_query_history: Retrieves the last 3 denied access attempts.
"""
#===========================================================================================================

import mysql.connector
from config import db_config # Credentials for the DB connection(stored in .gitignore)

# We create a connection Factory
# If db_name is provided, it connects directly to that schema.
# If not, it connects to the server (useful for setup)
def get_connection(db_name=None):  
    temp_config = db_config.copy()
    # Create a local copy to keep the original db_config immutable
    if db_name:
        temp_config['database'] = db_name

    return mysql.connector.connect(**temp_config)

# ========================================================
#  ✅ AUTHENTICATION
# =======================================================
def db_query_check_badge(badge_id):
 try:
    with get_connection(db_name="secure_pass_db") as conn: 
        with conn.cursor (dictionary=True) as cursor:
            
            query = """
                SELECT e.first_name, e.last_name, e.cantine_access 
                FROM employees e 
                WHERE e.badge_id = %s
                """
            cursor.execute(query, (badge_id,))
            return cursor.fetchone()
           
 except Exception as e:
        print(f"Error authentication: {e}")
        return None
# =======================================================
#   ✅  AUTHORIZATION
# =======================================================
# Flips everyone's canteen access to 'AUTHORIZED'. 
# Mandatory security checkpoint before they can enter the building.

def db_query_update_cantine(badge_id ):
    conn = None
    try:
        with get_connection(db_name="secure_pass_db") as conn:
            with conn.cursor(dictionary=True) as cursor:
                 query = "UPDATE employees SET cantine_access = 'AUTHORIZED' WHERE badge_id = %s"
                 cursor.execute(query, (badge_id,)) # Tuple with one element needs a comma
                 conn.commit() # Save changes to the DB
                 return True           
    except Exception as e:
        if conn and conn.is_connected():
            print("🔄 Running Rollback...")
            conn.rollback() # In case of error, we rollback any changes to maintain data integrity
        print(f"Error updating DB: {e}")
        return False       

def db_query_verify_access(badge_id, area_requested):
# Compares employee security level against the area.
    try:
        with get_connection(db_name="secure_pass_db") as conn: 
            with conn.cursor(dictionary=True) as cursor:
                query= """
                    SELECT e.security_level, a.required_level
                    FROM employees e
                    CROSS JOIN areas a
                    WHERE badge_id = %s 
                    AND LOWER(a.area_name) = LOWER(%s)
                """
        
                cursor.execute (query, (badge_id, area_requested))
                result = cursor.fetchone()

                if result:
                    return result['security_level'] >= result['required_level']
                return False # If no result, no access
 
    except Exception as e:
        print(f"Error: verification error  {e}")
        return False
   
# =======================================================
#     ✅ ACCOUNTABILITY
# =======================================================
# Non-repudation principle
# Mandatory step. Not included in the user menu. 
# We log every access,regardless of the result.

def db_insert_access_attempt(badge_id, area_requested, access_result):
    conn = None
    try:
        with get_connection(db_name="secure_pass_db") as conn: 
            with conn.cursor(dictionary=True) as cursor:
                query = "INSERT INTO access_logs (badge_id, area_requested, access_result) VALUES (%s, %s, %s)"
                cursor.execute(query, (badge_id, area_requested,access_result))
                conn.commit()
                print(f" {cursor.rowcount} log entries created ✅")
                return True
        
    except Exception as e:
        print(f"Database Log: {e}")
        try:
            if conn and conn.is_connected():
                conn.rollback()
                print ("🔄 Rollback executed successfully.")
        except:
            pass # if the rollback fails we ignore it.
        return False

# ✅ User can report a security issue.
def db_register_security_issue(badge_id, area_requested, issue_desc):
    clean_desc = issue_desc.lower()
    # Format the description to distinguish it from system logs
    formatted_report = f"ALERT: {clean_desc}"
    return db_insert_access_attempt(badge_id, area_requested, formatted_report)
    # Reuses/Wraps db_insert_access_attempt to save a manual report.


# ✅History: shows the last access atemmps. Highlights the denied ones.
def db_query_history(badge_id):
    try:
        with get_connection(db_name="secure_pass_db") as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """ 
                    SELECT area_requested, access_result, access_time
                    FROM access_logs 
                    WHERE badge_id = %s 
                    ORDER BY access_time DESC 
                    LIMIT 3
                    """
                cursor.execute(query,(badge_id,))
                return cursor.fetchall()
            
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

if __name__ == "__main__":
    pass


    