import mysql.connector
from mysql.connector import Error


def get_connection():
    """Helper function to get a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # MySQL host (typically localhost for XAMPP/WAMP)
            user="root",       # MySQL username (default for XAMPP/WAMP)
            password="",       # MySQL password (empty by default for XAMPP)
            database="attendance_system"  # Replace with your actual database name
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def close_connection(connection, cursor):
    """Helper function to close the database connection and cursor."""
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except Error as e:
        print(f"Error closing connection: {e}")


def get_attendance(student_id):
    """Fetch attendance records for a given student."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM attendance WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            records = cursor.fetchall()  # Fetch all records
            return records
        else:
            return None
    except Error as e:
        print(f"Error fetching attendance: {e}")
        return None
    finally:
        close_connection(connection, cursor)


def insert_attendance(student_id, student_name, date, status):
    """Insert an attendance record for a student."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO attendance (student_id, student_name, date, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (student_id, student_name, date, status))
            connection.commit()
            print(f"Attendance for {student_name} on {date} marked as {status}.")
    except Error as e:
        print(f"Error inserting attendance: {e}")
    finally:
        close_connection(connection, cursor)


def update_attendance(student_id, date, new_status):
    """Update attendance record for a student on a given date."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE attendance SET status = %s WHERE student_id = %s AND date = %s"
            cursor.execute(query, (new_status, student_id, date))
            connection.commit()
            print(f"Attendance for student ID {student_id} on {date} updated to {new_status}.")
    except Error as e:
        print(f"Error updating attendance: {e}")
    finally:
        close_connection(connection, cursor)


def delete_attendance(student_id, date):
    """Delete an attendance record for a student on a given date."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM attendance WHERE student_id = %s AND date = %s"
            cursor.execute(query, (student_id, date))
            connection.commit()
            print(f"Attendance record for student ID {student_id} on {date} deleted.")
    except Error as e:
        print(f"Error deleting attendance: {e}")
    finally:
        close_connection(connection, cursor)
