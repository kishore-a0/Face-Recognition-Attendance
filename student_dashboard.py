from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QFormLayout,
    QGroupBox, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import mysql.connector


class StudentDashboard(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user  # Store user data
        self.setWindowTitle(f"Dashboard - {self.user['first_name']}")
        self.setGeometry(100, 50, 900, 700)
        self.setStyleSheet("""
            background-color: #f0f4c3; 
            font-family: Arial; 
            font-size: 14px;
        """)

        # Tabbed layout
        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #80cbc4;
                border-radius: 10px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background: #4caf50;
                color: white;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #1b5e20;
                color: white;
            }
        """)
        self.tabs.addTab(self.create_profile_tab(), "Profile")
        self.tabs.addTab(self.create_attendance_tab(), "Attendance")
        self.tabs.addTab(self.create_settings_tab(), "Settings")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def create_profile_tab(self):
        """Create the profile tab."""
        profile_tab = QWidget()
        layout = QVBoxLayout(profile_tab)

        # Profile Card
        profile_card = QGroupBox("Profile")
        profile_card.setStyleSheet("""
            background-color: #ffffff; 
            border: 1px solid #81c784; 
            border-radius: 10px; 
            padding: 20px;
        """)
        card_layout = QHBoxLayout()

        # Profile Picture
        profile_pic = QLabel()
        face_path = self.user.get('face_path', 'default_profile.png')
        pixmap = QPixmap(face_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_pic.setPixmap(pixmap)
        profile_pic.setStyleSheet("""
            border: 3px solid #43a047; 
            border-radius: 75px;
        """)
        card_layout.addWidget(profile_pic)

        # User Info
        user_info_layout = QVBoxLayout()
        user_info_labels = [
            f"Name: {self.user['first_name']} {self.user['last_name']}",
            f"Email: {self.user['email']}",
            f"Class: {self.user['class']}",
            f"Gender: {self.user['gender']}",
            f"DOB: {self.user['dob']}"
        ]
        for text in user_info_labels:
            label = QLabel(text)
            label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            label.setFont(QFont("Arial", 12))
            user_info_layout.addWidget(label)

        card_layout.addLayout(user_info_layout)
        profile_card.setLayout(card_layout)
        layout.addWidget(profile_card)
        return profile_tab

    def create_attendance_tab(self):
        """Create the attendance tab."""
        attendance_tab = QWidget()
        layout = QVBoxLayout(attendance_tab)

        # Attendance Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(3)
        self.attendance_table.setHorizontalHeaderLabels(["Date", "Status", "Remarks"])
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #66bb6a;
            }
            QHeaderView::section {
                background-color: #2e7d32;
                color: white;
                font-weight: bold;
                padding: 4px;
            }
        """)
        layout.addWidget(self.attendance_table)

        # Load attendance data
        self.load_attendance_data()

        return attendance_tab

    def create_settings_tab(self):
        """Create the settings tab."""
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)

        # Settings Info
        settings_info = QLabel("Settings are under development.")
        settings_info.setStyleSheet("color: #455a64; font-style: italic;")
        settings_info.setFont(QFont("Arial", 14))
        layout.addWidget(settings_info)
        return settings_tab

    def load_attendance_data(self):
        """Load attendance data into the table."""
        connection = self.connect_database()
        if not connection:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT date, status, remarks FROM attendance WHERE reg_no = %s ORDER BY date DESC"
            cursor.execute(query, (self.user['reg_no'],))
            records = cursor.fetchall()

            self.attendance_table.setRowCount(len(records))

            for i, record in enumerate(records):
                self.attendance_table.setItem(i, 0, QTableWidgetItem(record['date'].strftime('%Y-%m-%d')))
                self.attendance_table.setItem(i, 1, QTableWidgetItem(record['status']))
                self.attendance_table.setItem(i, 2, QTableWidgetItem(record['remarks'] or "No remarks"))
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not fetch attendance data: {e}")
        finally:
            connection.close()

    def connect_database(self):
        """Connect to the MySQL database."""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            return None
