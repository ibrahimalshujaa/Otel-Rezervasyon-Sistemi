# Data Access Layer (DAL)
# Handles database connection and calls stored procedures ONLY.
# Raw SQL execution is strictly forbidden.

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'hotel_reservation_db',
    'charset': 'utf8mb4',
    'use_unicode': True
}

def get_connection():
    """Establish and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise e

def execute_proc(proc_name, params=()):
    """
    Execute a stored procedure and return any result sets.
    Uses cursor.callproc() as per constraints.
    Returns a list of dictionaries for results.
    """
    conn = get_connection()
    # Create cursor with dictionary=True so that results are returned as dicts
    cursor = conn.cursor(dictionary=True)
    results = []
    try:
        # Call the procedure
        cursor.callproc(proc_name, params)
        
        # Read returned result sets (if any)
        for result in cursor.stored_results():
            results.extend(result.fetchall())
            
        conn.commit()
        return results
    except Error as e:
        conn.rollback()
        print(f"Database error executing stored procedure '{proc_name}': {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_proc_non_query(proc_name, params=()):
    """
    Execute a stored procedure that doesn't return result sets 
    but performs mutations (Insert, Update, Delete).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(proc_name, params)
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Database error executing non-query stored procedure '{proc_name}': {e}")
        raise e
    finally:
        cursor.close()
        conn.close()
