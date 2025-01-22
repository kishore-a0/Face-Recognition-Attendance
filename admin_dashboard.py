from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from student_signup import StudentSignup  # Import your StudentSignup class


class AdminDashboard(QMainWindow):
    def __init__(self, staff_id, staff_name):
        super().__init__()

        # Staff Details
        self.staff_id = staff_id
        self.staff_name = staff_name

        # Window Settings
        self.setWindowTitle("Staff Dashboard")
        self.setGeometry(200, 100, 600, 400)
        self.setStyleSheet("background-color: #e0f7fa;")

        # Main Layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Welcome to the Admin Dashboard")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setStyleSheet("color: #00796b;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Staff Details
        details = [
            f"Name: {self.staff_name}",
            f"Staff ID: {self.staff_id}",
        ]
        for detail in details:
            label = QLabel(detail)
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #424242;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        # Buttons
        buttons = [
            ("Add Staff & Student Attendance", "#8e24aa", "#b39ddb", self.open_student_signup),
            ("Logout", "#1e88e5", "#64b5f6", self.logout),
        ]

        for text, color, hover_color, callback in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(f"""
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 10px;
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(callback)
            layout.addWidget(button, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_student_signup(self):
        """Open the student signup window."""
        try:
            self.hide()  # Hide the current dashboard window
            self.student_signup_window = StudentSignup()  # Create an instance of StudentSignup
            self.student_signup_window.show()

            # Ensure we handle what happens when the signup window closes
            self.student_signup_window.destroyed.connect(self.show)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def logout(self):
        """Handle logout process."""
        confirm = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()  # Close the dashboard window
            
            # Open the staff login screen after logout
            self.open_login_screen()

    def open_login_screen(self):
        """Open the staff login screen."""
        from staff_login import StaffLoginScreen  # Import the login screen
        login_window = StaffLoginScreen()
        login_window.show()  # Show the login screen


if __name__ == "__main__":
    import sys

    # Example Staff Data
    staff_id = "S12345"
    staff_name = "John Doe"

    app = QApplication(sys.argv)
    dashboard = StaffDashboard(staff_id, staff_name)
    dashboard.show()
    sys.exit(app.exec_())
