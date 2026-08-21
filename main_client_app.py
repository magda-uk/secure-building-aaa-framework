"""
SECURE-PASS SYSTEM - MAIN CLIENT APPLICATION
--------------------------------------------
Purpose: Provides a centralized interface to manage building security operations, 
         including identity verification, zone access control, and incident reporting.
         
Core Functions:
    - [Authentication]: Identity verification via Badge ID.
    - [Authorization]: Real-time clearance checks for restricted building zones.
    - [Accounting]: Automated audit logs and manual security alert reporting.

Student: Magdalena Dominguez | Version: 1.1 - Building Management Edition
"""
# ---------------------------------------------------------------------------------
import requests
from colorama import Back, Fore, Style, init
init(autoreset=True)
import utils
BASE_URL = "http://127.0.0.1:5000"

# Areas of the building 
menu_map = {
    "1": "Main Office",
    "2": "Cantine",
    "3": "Development Lab",
    "4": "Server Room",
    "5": "Cyber Operations Vault"}
#-------------------------------------------------------------------------------------
def run():
    print("="*35)
    print(Fore.MAGENTA + Style.BRIGHT+"  WELCOME TO SECUREPASS BUILDING   ")
    print( "="*35 )
    try:
        while True:
            print("Please,swipe your card to get identified")
            print(Fore.GREEN + "Demo badge_ids: B01-B10")
            badge_id = input("Enter demo badge_id: :  ").upper() .strip()
            
            # Step 1: Authentication (GET) Calling the API to check if the badge exists
            auth_response = requests.get(f"{BASE_URL}/auth/{badge_id}")

            if auth_response.status_code == 200:
                data = auth_response.json()
                print(Back.GREEN + Fore.BLACK + "Authentication successful")
                print(f"\nGood morning👋 {data.get('first_name')} {data.get('last_name')}")
                break
            else:
                print (Fore.RED +"Invalid Badge")
                print("❌ Please try again.")
        
        # Step 2: Mandatory Security Update (PATCH)
        # Simulation of a protocol where users must update their cantine access before entering
        if data.get('cantine_access') == 'PENDING':
            print(Fore.YELLOW + Style.BRIGHT+ "\n🛡️ SECURITY UPDATE 🛡️") 
            print("All staff must update their Cantine Access Pass before proceeding.")
            input( "Press any key to update your pass:  ")
            # Calling the Patch endpoint to update the cantine_access column
            patch_response = requests.patch(f"{BASE_URL}/update_access/{badge_id}")
            if patch_response.status_code == 200:
                data = patch_response.json()
                print(Fore.MAGENTA + "Success")
                print(Fore.GREEN +"Your badge has been updated with cantine permissions ☕") 
        else:    # if cantine pass has been recorded already
            print(Fore.YELLOW +"SECURITY CHECK: Cantine acces_permit " )
            print(Fore.GREEN + "[✓] Up to date") 
            # Skip straight to the floor selection menu

        # ==========================================================
        # MAIN MENU: SECUREPASS INTERFACE
        # ==========================================================
        # Step 3: Area Selection Menu (Authorization & Accounting)

        while True:  
                print("\n" + "="*35)
                print(Fore.BLUE + "--- BUILDING ACCESS MENU ---")
                print("="*35)
                print("1. ENTER BUILDING (Elevator)")
                print("2. REPORT SECURITY INCIDENT")
                print("3. VIEW YOUR SECURITY HISTORY")
                print("4. EXIT")

                choice = input ("\nSelect an option (1-4): ")

                if choice == "1":
                # 3.1 Submenu: The Elevator"
                    print(Fore.MAGENTA +"\n------- ELEVATOR: SELECT FLOOR ---------")
                    print(Fore.BLUE +"\n1. Main Office | 2. Cantine | 3. Development Lab \n4. Server Room | 5. Cyber Operations Vault")
                    floor_choice = input("\nSelect destination floor: ")
                    area_requested = menu_map.get(floor_choice)
                    
                    if area_requested:
                    # Authorization :Calling the API to check user security_levels 
                    # NOTE: The API logs this automatically (Invisible Accounting)
                        access_response= requests.get(f"{BASE_URL}/authorize/{badge_id}/{area_requested}")

                        status = access_response.status_code
                        
                        if status == 200:
                            # Acces permitted 
                            result_to_log = "GRANTED"
                            print(Back.GREEN + Fore.BLACK + "Authorization successful ")

                        elif status == 403:
                            # Badge valid but not enough security_leves
                            result_to_log = "DENIED"
                            print(Fore.RED +"ACCES DENIED: Insufficient security level.")

                        elif status == 404:
                            # Other errors 404 (Badge not found) or 500 (Server/ DB error)
                            result_to_log = "ERROR"
                            result_to_log = "ERROR"
                            print(Fore.YELLOW + " [?] Area or Badge not found in database. ")

                        else:
                            result_to_log = "ERROR"
                            print(Fore.RED + f" [X] System Error (Code {status}): Please contact security. ")
                        
                        log_payload = {
                            "badge_id": badge_id,
                            "area_requested": area_requested,
                            "access_result": result_to_log
                        }
                        # We send a POST to /log_access every time an attempt is made.
                        requests.post(f"{BASE_URL}/log_access", json=log_payload)
                    else:
                        print (Fore.RED +"Invalid floor selection. ")
        
                elif choice == "2":
                    print(Fore.MAGENTA +"\n--- REGISTER SECURITY ISSUE ---")
                    # Show building map first
                    for floor_num, area_name in menu_map.items():
                        print(f"{floor_num}. {area_name}")

                    area_choice = input(Fore.MAGENTA +"\nSelect area where issue was found (1-5): "+ Style.RESET_ALL)
                    area= menu_map.get(area_choice)
                    
                    if area:
                        description= input(Fore.MAGENTA +"Describe the problem briefly: "+ Style.RESET_ALL)
                        # I use the helper function that I tested
                        if not utils.is_valid_description(description):
                            print(Fore.YELLOW + "Error: Description must be at least 5 characters long.")
                        else:
                            issue_payload = {
                                "badge_id": badge_id,
                                "area_requested": area,
                                "alert_description": description
                            }
                            # only if description is valid we post the alert.
                            post_res = requests.post(f"{BASE_URL}/security_alert", json=issue_payload)

                            if post_res.status_code == 201:
                                print(Fore.GREEN+ "Security report submitted successfully.")
                            elif post_res.status_code == 400:
                                # Handling the list of errors from the API
                                api_errors = post_res.json().get('errors', [])
                                print(Fore.RED +"Report Rejected:")
                                for error in api_errors:
                                    print(f"  - {error}")
                            else:
                                print(Fore.YELLOW +"⚠️ A server error occurred.")
                    else:
                        print(Fore.RED + "Invalid area selection.")

                elif choice == "3":
                    # History (GET) request to the API recent access logs
                    hist_res = requests.get(f"{BASE_URL}/history/{badge_id}")

                    if hist_res.status_code == 200:
                        print(Fore.BLACK + Back.GREEN +"Accountability succesful")

                        # Store the results send into a variable
                        logs = hist_res.json() 
                        denied_count = 0

                        # Iterate through the access logs one by one
                        # Display and analyse the results
                        for entry in logs:
                            print(f"\n[{entry['access_time']}]")
                            print(f"[{entry['area_requested']}: {entry['access_result']}")

                            # increment the counter if the acces was denied
                            if entry['access_result'] == "DENIED":
                                denied_count += 1
                        
                        # Final security summary report
                        print("-" * 40)
                        if denied_count > 0:
                            print(Fore.YELLOW + f"WARNING: {denied_count} access attempts were DENIED.")
                        else:
                            print(Fore.GREEN + " No security issues found in your history.")

                    # Identity unknown or no history records
                    elif hist_res.status_code == 404:
                        print(Fore.RED + f" {hist_res.json().get('error', 'No history found')}")

                    else:
                        # Fail server or connection errors
                        print(Fore.RED + "An error occurred while fetching history.")

                elif choice == "4":
                    print(Fore.MAGENTA + Style.BRIGHT+ "See you soon")
                    print(Fore.MAGENTA + Style.BRIGHT+ "Have a lovely day")
                    print ("    ")
                                        
                    break

    except requests.exceptions.ConnectionError:
        print(Fore.RED +"SYSTEM ERROR :Could not connect to the server")
        print(Fore.YELLOW +"Ensure the flask_app is running")

# Main Entry Point
if __name__ == "__main__":
    run()