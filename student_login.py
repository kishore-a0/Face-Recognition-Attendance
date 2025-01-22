import mysql.connector
from mysql.connector import Error
from bcrypt import checkpw
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from student_dashboard import StudentDashboard  # Import the StudentDashboard class

class Student_loginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Login")
        self.setStyleSheet("background-color: #f5f5f5;")
        layout = QVBoxLayout()

        # Header
        header = QLabel("Student Login")
        header.setFont(QFont("Helvetica Neue", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #4caf50;")
        layout.addWidget(header)

        # Username (email or registration number)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your email or registration number")
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px;")
        login_button.clicked.connect(self.authenticate_user)
        layout.addWidget(login_button)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',         # Update with your MySQL username
                password='',         # Update with your MySQL password
                database='attendance_system'
            )
            return connection
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database:\n{e}")
            return None

    def authenticate_user(self):
        """Authenticate the user credentials."""
        email_or_regno = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not email_or_regno or not password:
            QMessageBox.warning(self, "Error", "Email/Registration number and password cannot be empty!")
            return

        connection = self.connect_database()
        if not connection:
            return  # Exit if the database connection fails

        try:
            cursor = connection.cursor(dictionary=True)
            # Query modified to use `users` table (search by either reg_no or email)
            query = "SELECT * FROM users WHERE reg_no = %s OR email = %s"
            cursor.execute(query, (email_or_regno, email_or_regno))  # Passing email or reg_no twice
            user = cursor.fetchone()

            if user:
                hashed_password = user["password"]
                if checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    # If login is successful, create and show the dashboard
                    self.show_dashboard(user)
                else:
                    QMessageBox.critical(self, "Error", "Invalid credentials!")
            else:
                QMessageBox.critical(self, "Error", "Invalid credentials!")
        except Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred:\n{e}")
        finally:
            connection.close()

    def show_dashboard(self, user):
        """Show the student dashboard after successful login."""
        unique_id = user["unique_id"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        reg_no = user["reg_no"]
        student_class = user["class"]
        gender = user["gender"]
        dob = user["dob"]
        parent_contact = user["parent_contact"]
        member_type = user["member_type"]
        face_path = user["face_path"]

        # Create an instance of the StudentDashboard
        dashboard = StudentDashboard(
            unique_id, first_name, last_name, reg_no, student_class, gender, dob, parent_contact, member_type, face_path)

        # Show the student dashboard
        dashboard.show()

        # Close the login screen
        self.close()

    def go_back(self):
        """Go back to the main page."""
        parent = self.parent()
        if parent and hasattr(parent, 'show_page'):
            parent.show_page(parent.home_page)
        else:
            self.close()
