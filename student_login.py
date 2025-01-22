from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from student_dashboard import StudentDashboard
import mysql.connector
import bcrypt


class Student_loginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Login")
        self.setFixedSize(400, 450)

        # Apply a colorful style
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fc;  /* Light blue-gray background */
            }

            QLabel {
                font-size: 18px;
                color: #34495e;  /* Dark slate for labels */
                font-weight: bold;
                margin-bottom: 10px;
            }

            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border-radius: 20px;
                border: 2px solid #3498db;  /* Blue border for inputs */
                background-color: #ffffff;  /* White background */
                color: #2c3e50;  /* Dark text for input */
                margin-bottom: 15px;
            }

            QLineEdit:focus {
                border-color: #1abc9c;  /* Teal border when focused */
                background-color: #e8f8f5;  /* Light teal background */
            }

            QPushButton {
                background-color: #2980b9;  /* Vibrant blue button */
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border: none;
                margin-top: 20px;
            }

            QPushButton:hover {
                background-color: #1abc9c;  /* Teal hover effect */
                color: white;
            }

            QPushButton:pressed {
                background-color: #27ae60;  /* Dark green when pressed */
            }
        """)

        # Center layout
        central_layout = QVBoxLayout(self)
        central_layout.setAlignment(Qt.AlignCenter)

        # Login form layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create UI elements
        self.title_label = QLabel("Welcome to Student Login")
        self.title_label.setStyleSheet("font-size: 22px; color: #2c3e50; font-weight: bold; text-align: center;")
        self.email_label = QLabel("Email:")
        self.password_label = QLabel("Password:")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        self.login_button = QPushButton("Login")

        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Add form layout to the central layout
        central_layout.addLayout(layout)

        # Connect the login button to its action
        self.login_button.clicked.connect(self.login)

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database: {err}")
            return None

    def login(self):
        """Validate credentials."""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please fill in both email and password fields.")
            return

        connection = self.connect_database()
        if not connection:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                # Check password using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    self.dashboard_window = StudentDashboard(user)
                    self.dashboard_window.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            else:
                QMessageBox.warning(self, "Login Failed", "Email not found.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {err}")
        finally:
            connection.close()


if __name__ == "__main__":
    app = QApplication([])
    login_window = StudentLoginScreen()
    login_window.show()
    app.exec_()
