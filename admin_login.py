from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector
import bcrypt
from admin_dashboard import AdminDashboard  # Import your admin dashboard

class Admin_loginScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Admin Login")
        self.setGeometry(400, 150, 500, 400)
        self.setStyleSheet("background-color: #e0f7fa;")

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("Admin Login")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #00796b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username Field
        self.username_entry = self.create_input_field("Enter Email")  # Changed to email for admin login
        layout.addWidget(self.username_entry)

        # Password Field
        self.password_entry = self.create_input_field("Enter Password", is_password=True)
        layout.addWidget(self.password_entry)

        # Login Button
        login_button = QPushButton("Login")
        login_button.setFont(QFont("Arial", 14, QFont.Bold))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #8e24aa; 
                color: white; 
                border-radius: 10px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ab47bc;
            }
        """)
        login_button.clicked.connect(self.login)  # Connect to login method
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

    def create_input_field(self, placeholder, is_password=False):
        """Creates an input field with placeholder text."""
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        entry.setFont(QFont("Arial", 14))
        entry.setStyleSheet("""
            QLineEdit {
                border: 2px solid #b0bec5;
                border-radius: 10px;
                padding: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #1e88e5;
            }
        """)
        if is_password:
            entry.setEchoMode(QLineEdit.Password)
        return entry

    def login(self):
        """Handles the login logic."""
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if not username or not password:
            QMessageBox.critical(self, "Error", "Both username and password are required!")
            return

        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",  # Default XAMPP MySQL host
                user="root",       # MySQL username
                password="",       # MySQL password (empty in XAMPP)
                database="attendance_system"  # The database you created
            )
            cursor = conn.cursor()

            # Query to check for the admin's credentials
            cursor.execute("""SELECT admin_id, admin_name, password FROM admins WHERE email = %s""", (username,))
            result = cursor.fetchone()

            if result:
                admin_id, admin_name, stored_password = result

                # Check if the entered password matches the stored password
                if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                    QMessageBox.information(self, "Login Successful", f"Welcome, {admin_name}!")

                    # Open the admin dashboard and pass the admin data
                    self.dashboard = AdminDashboard(admin_id, admin_name)
                    self.dashboard.show()

                    # Optionally reset fields after successful login:
                    self.username_entry.clear()
                    self.password_entry.clear()

                    self.hide()  # Hide the login window

                else:
                    QMessageBox.critical(self, "Error", "Invalid password. Please try again.")
            else:
                QMessageBox.critical(self, "Error", "Invalid email. Please try again.")

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


# Run the application
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AdminLoginScreen()
    window.show()
    sys.exit(app.exec_())
