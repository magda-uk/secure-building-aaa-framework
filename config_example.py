# config_example.py
# -------------------------------------------------------------------------
# SECURITY NOTE: 
# The actual 'config.py' contains sensitive credentials and is 
# listed in the .gitignore file to prevent it from being pushed to GitHub.
# -------------------------------------------------------------------------

# This is an example template. 
# 1. Create a file named 'config.py' in this directory.
# 2. Copy the variables below and replace them with your local credentials.
## We create a dictionary to store our database connection data-> best practice  


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password_here"
}