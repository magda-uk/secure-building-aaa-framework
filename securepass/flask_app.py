"""
FLASK API: Cybersecurity Access Control System (AAA Framework)
------------------------------------------------------------
Authentication: Badge validation.
Authorization: Security level verification & Permission updates.
Accounting: Non-repudiation logging for every transaction.
"""
# ---------------------------------------
# Step 1. Bringing the tools
# ---------------------------------------
from flask import Flask, jsonify, request
import db_utils
from utils import (is_valid_format_badge, is_valid_description, AccessAttempt) 
# Helper functions and class for validation and structured logs.


# Step 2. Creating the app
# --------------------------------------
app= Flask(__name__)

# Step 3. Setting the address
# --------------------------------------
# Basic route
@app.route('/')
def home():
   return jsonify({ 
      "message": "The security server is active. Welcome!",
        "api_version": "1.0",
        "framework": "AAA (Authentication, Authorization, Accounting)",
        "endpoints": {
            "Identity_Services": {
                "Verify_Badge": "/auth/<badge_id> (GET)"
            },
            "Access_Control": {
                "Check_Permission": "/authorize/<badge_id>/<area_requested> (GET)",
                "Compliance_Update": "/update_access/<badge_id> (PATCH)"
            },
            "Audit_&_Reporting": {
                "Automated_Log": "/log_access (POST)",
                "Security_Report": "/security_alert (POST)",
                "Access_History": "/history/<badge_id> (GET)"
            }
                       }  
   })  

# Step 4. Setting endpoints
# -----------------------------------------

# ===========================================
# 4.1. AUTHENTICATION (Identity Verification)
# ===========================================

@app.route('/auth/<string:badge_id>', methods=["GET"])
def authenticate(badge_id):
    # Identity Check.
    
    # Validates the format of the badge_id
    if not is_valid_format_badge(badge_id):
        return jsonify({"error": "Invalid badge format. Expected 'B' + 2 digits"}), 400
    
    # Validates if the provided badge exists in the trusted database.
    employee= db_utils.db_query_check_badge(badge_id)
    if employee:
        # 200 OK: badge found
        return jsonify(employee), 200
    else:
        # 404 Not found
        return jsonify({"error": "Access Denied: Badge unknown"}), 404

# ============================================
# 4.2. AUTHORIZATION (Access Rights & Compliance)
# =============================================
    
    # Mandatory Step    
    # Here we verify if the badge has permit to the Cantine 
    # (authorized or pending) and prompt user to update it

@app.route('/update_access/<string:badge_id>', methods=['PATCH'])
def update_cantine(badge_id): 
    # Compliance update: If the user has a pending access to the cantine, we can update it to authorized.   
    result= db_utils.db_query_update_cantine(badge_id)
    if result:
        updated_employee = db_utils.db_query_check_badge(badge_id)
        return jsonify(updated_employee), 200
    else:
        return jsonify({"error": "Update failed"}), 500
    

@app.route('/authorize/<string:badge_id>/<string:area_requested>', methods=['GET'])
def authorize_access(badge_id, area_requested):
    try:

        area_clean = str(area_requested).strip()
        # Permission Check.
        # Compares user security level against the area's clearance requirements..
        is_allowed = db_utils.db_query_verify_access(badge_id, area_clean)

        if is_allowed is True:
            return jsonify({"result": "GRANTED"}), 200
        
        elif is_allowed is False:
            return jsonify({"result": "DENIED"}), 403  
        
        else:
            # allowed is None (area not found)
            return jsonify({"error": "Area not found in database"}), 404  
        
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
# ==========================================
# 4.3. ACCOUNTING (Audit Trail & History)
# ==========================================

# Non-repudation principle
# Mandatory and automatic step. 
# Not included in the user menu. 
# We log every atempt access in the building-> Ensures permanent audit trail.
 
@app.route('/log_access', methods=['POST'])
def access_attempt():
    # Rejects the request if is not labeled as JSON
    if not request.is_json:
        return jsonify({"error": "INVALID_CONTENT_TYPE"}), 415
    
    # Capture the JSON payload sent by the client application
    # Parse the request body into a python dictionary
    user_interaction= request.get_json()
   
    # checking the json is not empty
    if not user_interaction:
        return jsonify({"error": "No data provided"}), 400
    
    # ckeck if the data has the required fields
    required_fields = ['badge_id', 'area_requested', 'access_result']
    if not all(field in user_interaction for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # DATA INTEGRITY: Validate badge format before database insertion
    if not is_valid_format_badge(user_interaction['badge_id']):
        return jsonify({"error": "Invalid badge format "}), 400

    # Create an AccessAttempt object to structure and sanitize the data before logging
    attempt = AccessAttempt(
        user_interaction['badge_id'],
        user_interaction['area_requested'],
        user_interaction['access_result']  )

    try:
        db_utils.db_insert_access_attempt(
           attempt.badge_id,
           attempt.area,
           attempt.result
        )
        # Return a confirmation response to the client with a 201 (Created) status code
        return jsonify({"status": "Accesss attempt logged succesfully 👀 ✅"}), 201
    
    except Exception as e:
        # if the DB fails, connection, integrity..   
        return jsonify({"error": "Internal server error saving to database"}),500
#--------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
# Manual security reporting. Uses a list of errors for payload validation.  
@app.route('/security_alert', methods=['POST'])
def report_issue():
    data = request.get_json()
    # Initial safety check to prevent crashes if JSON is missing
    if not data:
        return jsonify({"errors": ["No data provided"]}), 400

    badge_id = data.get('badge_id', '')
    description = data.get('alert_description', '')
    area = data.get('area_requested', '')

    errors = []

    # Validation: Badge ID
    if not data.get('badge_id'):
        errors.append("Badge ID is required to identify the reporter")

    elif not is_valid_format_badge(badge_id): # Helper function : validates format
        errors.append("Invalid Badge ID format (Must be BXX)")
    
    # Validation: Area
    if not data.get('area_requested'):
        errors.append("The area is required")

    # Validation: Length   
    if not is_valid_description(description):  # Helper function 
        errors.append("Alert description is too short (minimum 5 characters)")
    elif len(description) > 50:   # Length Limitation (Anti-DoS)
        errors.append("Description is too long (max 50 characters).")

    # If the list has any errors, we stop and return them
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    # Call db_utils function
    # We send the CLEAN description to the DB
    success = db_utils.db_register_security_issue(
        data['badge_id'], 
        data['area_requested'], 
        description 
    )

    if success:
        return jsonify({"status": "success", "message": "Report filed successfully"}), 201
    
    return jsonify({"status": "error", "errors": ["Database failure"]}), 500
#--------------------------------------------------------------------------------------------------------------

# History retrieval
# The user can choose to go over their past access.
@app.route('/history/<string:badge_id>', methods=['GET'])
def get_history(badge_id):
   # Validate: check format
   if not is_valid_format_badge(badge_id):
        return jsonify({"error": "Invalid format. Expected 'B' + 2 digits"}), 400
   
   # Does this user even exist in our system?
   employee = db_utils.db_query_check_badge(badge_id)
   if not employee:
      return jsonify({"error": "Identity unknown. Cannot retrieve history for non-existent user."}), 404
   
   # Fetch existing records from the DB based on the badge_id
   logs= db_utils.db_query_history(badge_id)
    # It might be no recordings on the table logs for this badge_id 
   if not logs:
        return jsonify({"message": f"No access history found for badge {badge_id}"}), 200

   # Send the database results back to the client in JSON format
   return jsonify(logs), 200

     
# Step 5. Starting the server
# ------------------------------------------
if __name__ == "__main__" :
    app.run(debug=True, port=5000)

