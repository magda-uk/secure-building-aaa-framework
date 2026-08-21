import mysql.connector
from db_utils import get_connection # We bring factory connection

## Populating employees table with pioneer data 
print  ("🌱  Populating tables with some data...")
      
def seed_tables():
    # We use tuples to represent individual rows because they are immutable.
    tech_women = [
            ('B01', 'Ada', 'Lovelace', 3),      # First computer algorithm
            ('B02', 'Grace', 'Hopper', 4),      # First compiler/COBOL
            ('B03', 'Hedy', 'Lamarr', 4),       # Frequency-hopping/Wi-Fi
            ('B04', 'Annie', 'Easley', 2),      # NASA rocket scientist
            ('B05', 'Mary', 'Wilkes', 2),       # First home PC user/dev
            ('B06', 'Adele', 'Goldberg', 2),    # GUI interfaces pioneer
            ('B07', 'Radia', 'Perlman', 3),     # STP protocol (Mother of Internet)
            ('B08', 'Katherine', 'Johnson', 1), # Apollo trajectories
            ('B09', 'Margaret', 'Hamilton', 1), # Apollo flight software lead
            ('B10', 'Elizabeth', 'Holberton', 1)# ENIAC programmer
            ]
    try:
        conn = get_connection(db_name="secure_pass_db")
        cursor = conn.cursor()
    

        # Use 'INSERT IGNORE' to avoid errors if the data already exists
        insert_query = """
                    INSERT IGNORE INTO employees (badge_id, first_name, last_name, security_level) 
                    VALUES (%s, %s, %s, %s)"""
            # Use %s as a placeholder to safely inject values into the SQL query.
                
        # Execute the query, passing the data as a separate tuple.
        # We use executemany() to perform a 'bulk insert'.
        cursor.executemany(insert_query, tech_women)

        # cursor.rowcount to verify the number of successfully inserted rows.
        print(f" {cursor.rowcount} trailblazers added to employees✅")


        print("🌱 Seeding areas and security rules...")
        building_areas = [
                    ('Main Office', 1),
                    ('Cantine', 1),
                    ('Development Lab', 2),
                    ('Server Room', 3),
                    ('Cyber Operations Vault', 4)
                ]
        area_query = "INSERT IGNORE INTO areas (area_name, required_level) VALUES (%s, %s)"
        cursor.executemany(area_query, building_areas)
        print(f"{cursor.rowcount} areas defined with security levels ✅")

            
        print("🌱  Seeding access logs ...")
        mock_logs = [
                ('B01', '2026-05-05 08:30:15', 'Main Office', 'GRANTED'),
                ('B10', '2026-05-05 09:12:44', 'Cantine', 'DENIED'),
                ('B02', '2026-05-05 10:05:02', 'Cyber Operations Vault', 'GRANTED'),
                ('B04', '2026-05-05 11:20:30', 'Cantine', 'DENIED'),
                ('B07', '2026-05-05 13:45:12', 'Server Room', 'GRANTED'),
                ('B05', '2026-05-05 14:10:00', 'Development Lab', 'GRANTED'),
                ('B09', '2026-05-05 15:30:55', 'Server Room', 'DENIED'),
                ('B03', '2026-05-05 16:45:21', 'Main Office', "ALERT: <'Broken Window'>"),
                ('B06', '2026-05-05 17:10:08', 'Development Lab', 'GRANTED'),
                ('B08', '2026-05-05 18:00:00', 'Cyber Operations Vault', 'DENIED'),
                ('B01', '2026-05-05 19:15:00', 'Server Room', 'GRANTED'),
                ('B02', '2026-05-05 20:00:00', 'Main Office', 'ALERT: person tailgating'),
                ('B10', '2026-05-05 21:30:00', 'Development Lab', 'DENIED')
            ]
        
        log_query = """
                   INSERT IGNORE INTO access_logs (badge_id, access_time, area_requested, access_result) 
                   VALUES (%s, %s, %s, %s) 
                   """
            
        # Instead of manually looping through the list, executemany() 
        # automatically maps each tuple in the list to the SQL placeholders.   

        cursor.executemany(log_query, mock_logs)
        print(f" {cursor.rowcount} log entries created ✅")

        
        # 🔄 RESET FINAL: Sincro
        # Reset everyone to 'PENDING' right before committing.
        # This ensures a clean initial state for the demo, even if data already existed.
        cursor.execute("UPDATE employees SET cantine_access = 'PENDING'")

        print("🔄 All employees have PENDING cantine_access for testing purposes")
        
        
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
    seed_tables()

