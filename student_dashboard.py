from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, 
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import mysql.connector

class StudentDashboard(QMainWindow):
    def __init__(self, unique_id, name, reg_no, student_class, gender, dob):
        super().__init__()
        self.unique_id = unique_id
        self.name = name
        self.reg_no = reg_no
        self.student_class = student_class
        self.gender = gender
        self.dob = dob

        self.setWindowTitle("Student Dashboard")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #e0f7fa;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel(f"Welcome, {self.name}!")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setStyleSheet("color: #00796b;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Information Section
        info_labels = [
            f"Registration Number: {self.reg_no}",
            f"Class: {self.student_class}",
            f"Gender: {self.gender}",
            f"Date of Birth: {self.dob}"
        ]

        for info in info_labels:
            label = QLabel(info)
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #424242;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        # Attendance Table Section
        attendance_label = QLabel("Attendance Records")
        attendance_label.setFont(QFont("Arial", 16, QFont.Bold))
        attendance_label.setStyleSheet("color: #00796b;")
        attendance_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(attendance_label)

        self.attendance_table = QTableWidget()
        self.attendance_table.setRowCount(0)  # Start with no data
        self.attendance_table.setColumnCount(4)  # Columns: Date, Status, Subject, Remarks
        self.attendance_table.setHorizontalHeaderLabels(["Date", "Status", "Subject", "Remarks"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setStyleSheet("background-color: white; border: 1px solid #b0bec5;")
        layout.addWidget(self.attendance_table)

        # Load Attendance Data
        self.load_attendance_data()

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Arial", 14))
        logout_button.setStyleSheet("""background-color: #1e88e5; color: white; border-radius: 10px; padding: 10px;""")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_attendance_data(self):
        """Load attendance data for the student from the database."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',         # Replace with your DB credentials
                password='',         # Replace with your DB password
                database='attendance_system'
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT date, status, subject, remarks FROM attendance WHERE student_id = %s"
            cursor.execute(query, (self.unique_id,))
            attendance_data = cursor.fetchall()

            self.attendance_table.setRowCount(len(attendance_data))
            for row, record in enumerate(attendance_data):
                self.attendance_table.setItem(row, 0, QTableWidgetItem(record["date"]))
                self.attendance_table.setItem(row, 1, QTableWidgetItem(record["status"]))
                self.attendance_table.setItem(row, 2, QTableWidgetItem(record["subject"]))
                self.attendance_table.setItem(row, 3, QTableWidgetItem(record["remarks"]))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load attendance data:\n{e}")
        finally:
            if connection:
                connection.close()

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            QMessageBox.information(self, "Logged Out", "You have been logged out.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Test Data
    unique_id = 1  # Replace with the student's unique ID from your database
    name = "Kishore"
    reg_no = "REG202301"
    student_class = "MCA - Year 2"
    gender = "Male"
    dob = "01/01/2000"

    dashboard = StudentDashboard(unique_id, name, reg_no, student_class, gender, dob)
    dashboard.show()
    sys.exit(app.exec_())
