# Secure Building Access Control API (AAA Framework)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](#)
[![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20REST%20API-lightgrey.svg)](#)
[![Security Standard](https://img.shields.io/badge/Security-AAA%20Triad%20%7C%20PoLP-green.svg)](#)
[![Testing](https://img.shields.io/badge/Tests-Unit%20%26%20Security%20Validation-success.svg)](#)

A backend RESTful application and simulation client implementing physical security access controls based on the **AAA (Authentication, Authorization, and Accounting)** cybersecurity model. 

The architecture enforces strict identity verification, role-based permission tiers, input sanitization, and immutable audit logging for security compliance.

---

## 1. Cybersecurity Architecture: The AAA Model
### Core Security Pillars:

1. **Authentication ("Who are you?"):**
   * Verifies badge credentials against database records upon entry.
   * **Security Objective:** Mitigate identity spoofing by restricting interactions to registered entities.

2. **Authorization ("What are you permitted to do?"):**
   * Compares employee security clearance against room access tiers (e.g., *Server Room* vs. *Main Office*).
   * Supports dynamic permission synchronization (`PATCH` endpoints for temporary clearance updates).
   * **Security Objective:** Enforce the **Principle of Least Privilege (PoLP)**, preventing unauthorized lateral movement across facility zones.

3. **Accounting ("What actions were taken?"):**
   * Automatically records every interaction (`GRANTED`, `DENIED`, manual alerts) via dedicated API audit routes (`POST /access_logs`).
   * Provides log querying endpoints (`GET /access_logs`) for incident response teams and forensic triage.
   * **Security Objective:** Ensure non-repudiation and maintain audit trails for security investigations.

## 📁 2. Repository Structure

```text
secure-building-aaa-framework/
├── flask_app.py         # API Entry Point (Routes & Business Logic)
├── main_client_app.py   # User Interface (Building Turnstile Simulation)
├── db_utils.py          # Database Layer (SQL Queries & Connection)
├── db_seed.py           # Data Seeding (Initial Records)
├── database_setup.py    # DB Initialization (Tables & Schema Creation)
├── utils.py             # OOP Models (AccessAttempt class & Sanitization)
├── security_test.py     # Automated Testing (Validation of security logic)
├── config_example.py    # Credentials Template (Ignored by Git)
└── requirements.txt     # Project Dependencies

```

## 3. Getting Started & Installation
### Prerequisites:  

* Python 3.10+

* MySQL Server (or compatible relational database)

### Setup Instructions
 1. Clone the repository:
 ```bash
 git clone https://github.com/magda-uk/secure-building-aaa-framework.git

cd secure-building-aaa-framework
```
2. Install dependencies:

```Bash
pip install -r requirements.txt
```
3. Configure Database Credentials:
Copy the example configuration and set your environment parameters:

```Bash
cp config_example.py config.py
```
4. Initialise and Seed Database:

```Bash
python database_setup.py
python db_seed.py
```




## 4. Running the Application 

1. Start the API server: 
```Bash
python flask_app.py
```
2. Launch the Turnstile Client (in a separate terminal): 
``` bash 
main_client_app.py.
```
## 5. Security Validation & Testing Workflow
### Follow this sequence to evaluate the security controls:

* **Step 1: Identity Authentication**

    Authenticate using employee badge ID B01. The API verifies the record against the datastore.

* **Step 2: Dynamic Clearance Update**

    Request updated zone permissions (triggers a PATCH request to sync access levels).

* **Step 3: Access Control Enforcement**

    Attempt entry into a high-security zone (e.g., Server Room). The policy engine blocks unauthorized entry (403 Forbidden / DENIED).

* **Step 4: Input Sanitization & Incident Logging**

    File a manual security report (e.g., "Gate Left Open"). Notice strings are normalized and sanitized before storage in the audit trail.

### To run automated security tests:
```bash
python security_test.py
```
