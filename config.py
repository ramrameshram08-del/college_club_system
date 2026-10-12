# ====================================================================
# Database Configuration File
# College Club Event Management System
# ====================================================================

# Oracle Database 21c XE Connection Details
DB_CONFIG = {
    "user": "clubadmin",
    "password": "clubpass",
    "dsn": "localhost:1521/XEPDB1"   # Default XE pluggable database
}

# Secret key for Flask session and flash messages
SECRET_KEY = "student_secret_key_college_club_system"
