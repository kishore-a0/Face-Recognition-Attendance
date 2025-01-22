import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import bcrypt

class Admin_signupScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Signup")
        self.setGeometry(300, 100, 600, 400)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Admin Signup")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0d47a1;")
        layout.addWidget(title)

        # Signup Form
        form_layout = QFormLayout()

        # Name input field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addRow("Name:", self.name_input)

        # Email input field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addRow("Email:", self.email_input)

        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addRow("Password:", self.password_input)

        # Confirm Password input field
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

        # Add form layout to main layout
        layout.addLayout(form_layout)

        # Buttons layout for Sign Up and Back to Home
        buttons_layout = QHBoxLayout()

        # Sign Up Button
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        signup_button.clicked.connect(self.signup)
        buttons_layout.addWidget(signup_button)

        # Back Button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        back_button.clicked.connect(self.back_to_home)
        buttons_layout.addWidget(back_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the signup screen
        self.setLayout(layout)

    def signup(self):
        """Handles admin signup logic and inserts data into the database."""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        # Validation checks
        if not name or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Password Error", "Passwords do not match!")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Establish database connection
            conn = mysql.connector.connect(
                host="localhost",  # Database host
                user="root",       # Database user
                password="",       # Database password
                database="attendance_system"  # Database name
            )

            cursor = conn.cursor()

            # Check if the email already exists
            cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                QMessageBox.warning(self, "Email Exists", "An account with this email already exists.")
                return

            # Query to insert new user into the database
            query = """INSERT INTO admins (admin_name, email, password)
                       VALUES (%s, %s, %s)"""
            data = (name, email, hashed_password)

            cursor.execute(query, data)
            conn.commit()

            QMessageBox.information(self, "Success", "Signup successful! You can now log in.")
            
            # Clear input fields after successful signup
            self.name_input.clear()
            self.email_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def back_to_home(self):
        """Handles going back to the home page."""
        self.close()
        # Add logic here to show home page or navigate as needed
        # If you have a parent window, you can call parent.show() to go back.
        # For example: self.parent().show_home_page()

