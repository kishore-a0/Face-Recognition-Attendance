from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from student_dashboard import StudentDashboard
import mysql.connector
import bcrypt

class Student_loginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Login")
        
        # Setup the login UI elements
        layout = QVBoxLayout(self)

        self.email_label = QLabel("Email:")
        self.password_label = QLabel("Password:")
        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")

        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.login)

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host='localhost',     # MySQL host
                user='root',          # MySQL username
                password='',          # MySQL password
                database='attendance_system'  # Database name
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database: {err}")
            return None

    def login(self):
        """Validate credentials against the database."""
        email = self.email_input.text()
        password = self.password_input.text()

        # Validate if fields are empty
        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
            return
        
        connection = self.connect_database()
        if not connection:
            return  # Exit if database connection fails
        
        try:
            cursor = connection.cursor(dictionary=True)

            # Query to check the email
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                # Check if password matches (using bcrypt to compare hashed passwords)
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    # If password matches, open the dashboard window
                    self.dashboard_window = StudentDashboard(user)
                    self.dashboard_window.show()
                    self.close()  # Close the login window
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email address.")
        
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"An error occurred while checking credentials: {err}")
        finally:
            connection.close()


if __name__ == "__main__":
    app = QApplication([])
    login_window = StudentLoginScreen()
    login_window.show()
    app.exec_()
