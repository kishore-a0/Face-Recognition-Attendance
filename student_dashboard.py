from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout, QGroupBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import mysql.connector
from datetime import datetime

class StudentDashboard(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user  # Store the user data

        # Window setup
        self.setWindowTitle(f"Dashboard - {self.user['first_name']}")
        self.setGeometry(100, 50, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial, sans-serif;")

        # Main layout
        layout = QVBoxLayout(self)

        # Welcome header
        header = QLabel(f"Welcome, {self.user['first_name']} {self.user['last_name']}")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #4caf50; text-align: center;")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        # Student Information
        self.student_info_group = self.create_student_info_group()
        layout.addWidget(self.student_info_group)

        # Mark Attendance Button
        self.mark_attendance_button = QPushButton("Mark Attendance")
        self.mark_attendance_button.setStyleSheet(self.button_style())
        self.mark_attendance_button.clicked.connect(self.mark_attendance)
        layout.addWidget(self.mark_attendance_button, alignment=Qt.AlignCenter)

        # Attendance Button
        self.attendance_button = QPushButton("View Attendance")
        self.attendance_button.setStyleSheet(self.button_style())
        self.attendance_button.clicked.connect(self.view_attendance)
        layout.addWidget(self.attendance_button, alignment=Qt.AlignCenter)

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet(self.button_style())
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(layout)

    def button_style(self):
        """Button hover effects and style"""
        return (
            "background-color: #4caf50; color: white; font-size: 16px; padding: 10px; border-radius: 8px; margin-top: 20px;"
        )

    def create_student_info_group(self):
        """Create a group box with student info."""
        group_box = QGroupBox("Student Information")
        group_box.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 20px;")

        # Form layout for displaying student information
        form_layout = QFormLayout()

        name_label = QLabel(f"Name: {self.user['first_name']} {self.user['last_name']}")
        email_label = QLabel(f"Email: {self.user['email']}")

        # Check if the 'course' key exists
        course_label = QLabel(f"Course: {self.user.get('course', 'N/A')}")  # Fallback if 'course' key is missing

        form_layout.addRow(name_label)
        form_layout.addRow(email_label)
        form_layout.addRow(course_label)

        group_box.setLayout(form_layout)
        return group_box

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',      # Change this to your MySQL username
                password='',      # Change this to your MySQL password
                database='attendance_system'  # Change this to your database name
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database: {err}")
            return None

    def mark_attendance(self):
        """Mark the attendance of the student as present or absent."""
        connection = self.connect_database()
        if not connection:
            return  # Exit if the database connection fails

        try:
            cursor = connection.cursor()

            # Get today's date
            today_date = datetime.today().strftime('%Y-%m-%d')

            # Check if attendance is already marked for today
            query = "SELECT * FROM attendance WHERE student_id = %s AND date = %s"
            cursor.execute(query, (self.user['id'], today_date))
            existing_attendance = cursor.fetchone()

            if existing_attendance:
                QMessageBox.information(self, "Attendance", "Attendance already marked for today.")
            else:
                # If not marked, prompt the user for their status
                reply = QMessageBox.question(self, "Mark Attendance", "Mark yourself as Present or Absent?", 
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                # If "Yes" is clicked, mark as present; if "No" clicked, mark as absent
                status = "Present" if reply == QMessageBox.Yes else "Absent"

                # Insert the attendance record into the database
                insert_query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (self.user['id'], today_date, status))
                connection.commit()

                QMessageBox.information(self, "Attendance", f"Marked as {status} for today.")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while marking attendance: {e}")
        finally:
            connection.close()
    
    def view_attendance(self):
        """Fetch and display attendance from the database."""
        connection = self.connect_database()
        if not connection:
            return  # Exit if the database connection fails

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM attendance WHERE student_id = %s"
            cursor.execute(query, (self.user['id'],))
            attendance_data = cursor.fetchall()

            if attendance_data:
                self.show_attendance(attendance_data)
            else:
                QMessageBox.information(self, "Attendance", "No attendance data found.")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while fetching attendance data: {e}")
        finally:
            connection.close()

    def show_attendance(self, attendance_data):
        """Show the attendance data in a table."""
        table_window = QWidget()
        table_layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Date", "Status", "Remarks"])
        table.setRowCount(len(attendance_data))

        # Fill table with attendance data
        for row, data in enumerate(attendance_data):
            table.setItem(row, 0, QTableWidgetItem(data['date']))
            table.setItem(row, 1, QTableWidgetItem(data['status']))
            table.setItem(row, 2, QTableWidgetItem(data['remarks']))

        table.setStyleSheet("QTableWidget {border: 1px solid #ccc; border-radius: 5px;}")
        table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #4caf50; color: white;}")

        table_layout.addWidget(table)
        table_window.setLayout(table_layout)
        table_window.setWindowTitle("Attendance Records")
        table_window.setGeometry(100, 50, 600, 400)
        table_window.show()

    def logout(self):
        """Logout the user and return to the login window."""
        self.close()  # Close the dashboard
        from student_login import StudentLoginScreen  # Import the login screen here
        self.login_window = StudentLoginScreen()  # Open the login window again
        self.login_window.show()
