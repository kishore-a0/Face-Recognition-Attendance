from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import mysql.connector
from student_signup import StudentSignup  # Import the StudentSignup class


class AdminDashboard(QMainWindow):
    def __init__(self, staff_id, staff_name):
        super().__init__()

        # Admin Details
        self.staff_id = staff_id
        self.staff_name = staff_name

        # Window Settings
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #f1f8e9;")

        # Main Layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Welcome to the Admin Dashboard")
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #1b5e20; margin: 20px;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Admin Info Section
        admin_info_layout = QVBoxLayout()
        admin_info_layout.setContentsMargins(20, 10, 20, 10)

        admin_pic = QLabel()
        admin_pic.setPixmap(QPixmap("admin_icon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        admin_pic.setAlignment(Qt.AlignCenter)

        admin_info_label = QLabel(f"Admin Name: {self.staff_name}\nAdmin ID: {self.staff_id}")
        admin_info_label.setFont(QFont("Arial", 16))
        admin_info_label.setStyleSheet("color: #004d40; padding: 10px;")
        admin_info_label.setAlignment(Qt.AlignCenter)

        admin_info_layout.addWidget(admin_pic)
        admin_info_layout.addWidget(admin_info_label)
        layout.addLayout(admin_info_layout)

        # Buttons
        buttons_layout = QVBoxLayout()
        buttons = [
            ("Add Student", "#1e88e5", self.open_student_signup),
            ("View Attendance Requests", "#8e24aa", self.view_attendance_requests),
            ("Logout", "#d32f2f", self.logout),
        ]

        for text, color, callback in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14, QFont.Bold))
            button.setStyleSheet(f"""
                background-color: {color};
                color: white;
                border-radius: 15px;
                padding: 15px;
                margin: 10px 50px;
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(callback)
            buttons_layout.addWidget(button)

        layout.addLayout(buttons_layout)

        # Footer
        footer_label = QLabel("© 2025 Admin Management System")
        footer_label.setFont(QFont("Arial", 12))
        footer_label.setStyleSheet("color: #757575; margin: 20px;")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_student_signup(self):
        """Open the Student Signup window."""
        try:
            self.student_signup_window = StudentSignup()
            self.student_signup_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Student Signup: {str(e)}")

    def view_attendance_requests(self):
        """Fetch and display attendance requests from the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute(
                "SELECT review_id, reg_no, date, status FROM admin_review WHERE status = 'Pending'"
            )
            requests = cursor.fetchall()

            if not requests:
                QMessageBox.information(self, "No Requests", "No pending attendance requests.")
                return

            # Create a new window to display requests
            request_window = QMainWindow(self)
            request_window.setWindowTitle("Attendance Requests")
            request_window.setGeometry(100, 100, 600, 400)
            request_window.setStyleSheet("background-color: #ffffff;")

            central_widget = QWidget()
            layout = QVBoxLayout()

            header_label = QLabel("Pending Attendance Requests")
            header_label.setFont(QFont("Arial", 16))
            header_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(header_label)

            # Create a table to display requests
            table = QTableWidget(len(requests), 5)  # Added extra column for actions
            table.setHorizontalHeaderLabels(["Review ID", "Reg No", "Date", "Status", "Action"])

            for row, (review_id, reg_no, date, status) in enumerate(requests):
                table.setItem(row, 0, QTableWidgetItem(str(review_id)))
                table.setItem(row, 1, QTableWidgetItem(reg_no))
                table.setItem(row, 2, QTableWidgetItem(str(date)))
                table.setItem(row, 3, QTableWidgetItem(status))

                # Create action buttons for Approve and Reject
                button_layout = QHBoxLayout()

                approve_button = QPushButton("Approve")
                approve_button.setStyleSheet("background-color: #43a047; color: white;")
                approve_button.clicked.connect(lambda _, rid=review_id: self.update_request(rid, "Present"))

                reject_button = QPushButton("Reject")
                reject_button.setStyleSheet("background-color: #e53935; color: white;")
                reject_button.clicked.connect(lambda _, rid=review_id: self.update_request(rid, "Absent"))

                button_layout.addWidget(approve_button)
                button_layout.addWidget(reject_button)

                action_widget = QWidget()
                action_widget.setLayout(button_layout)
                table.setCellWidget(row, 4, action_widget)

            layout.addWidget(table)
            central_widget.setLayout(layout)
            request_window.setCentralWidget(central_widget)
            request_window.show()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def update_request(self, review_id, decision):
        """Update attendance request status in the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE admin_review SET status = 'Reviewed', decision = %s WHERE review_id = %s",
                (decision, review_id)
            )
            conn.commit()

            QMessageBox.information(self, "Success", f"Attendance marked as {decision}.")
            cursor.close()
            conn.close()

            self.view_attendance_requests()  # Refresh the requests view

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def logout(self):
        """Handle logout process."""
        confirm = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dashboard = AdminDashboard(staff_id="A12345", staff_name="John Doe")
    dashboard.show()
    sys.exit(app.exec_())
