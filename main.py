from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
from mark_attendance import MarkAttendanceScreen  # Import the MarkAttendanceScreen class


class HoverButton(QPushButton):
    """Custom QPushButton with hover effects."""
    def __init__(self, text, default_color, hover_color, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.default_color = default_color
        self.hover_color = hover_color
        self.setStyleSheet(self.get_style(self.default_color))

    def enterEvent(self, event):
        """Change background color on hover."""
        self.setStyleSheet(self.get_style(self.hover_color))
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Revert to default background color."""
        self.setStyleSheet(self.get_style(self.default_color))
        super().leaveEvent(event)

    def get_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color}; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 18px;
                font-family: 'Roboto';
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """


class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(200, 100, 900, 650)
        self.setStyleSheet("background-color: #f7f8fc;")  # Light background for clean design

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Initialize pages
        self.initialize_home_page()
        self.initialize_student_page()
        self.initialize_admin_page()

        # Set the main layout
        central_widget.setLayout(main_layout)

    def initialize_home_page(self):
        """Sets up the Home Page."""
        self.home_page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Face Recognition Attendance System")
        header.setFont(QFont("Helvetica Neue", 36, QFont.Bold))
        header.setStyleSheet("""
            color: white;
            background-color: #6200ea;
            padding: 30px;
            text-align: center;
            border-radius: 15px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Subheader
        subheader = QLabel("Enhancing productivity with automated attendance tracking.")
        subheader.setFont(QFont("Roboto", 18))
        subheader.setStyleSheet("color: #424242; margin: 20px 10px; text-align: center;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        # Buttons Layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(20)  # Add spacing between buttons

        buttons_layout.addWidget(self.create_button("Mark Attendance", "#ff9800", "#ffc107", self.mark_attendance), alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.create_button("Student Menu", "#03a9f4", "#29b6f6", lambda: self.show_page(self.student_page)), alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.create_button("Admin Menu", "#4caf50", "#66bb6a", lambda: self.show_page(self.admin_page)), alignment=Qt.AlignCenter)

        layout.addLayout(buttons_layout)

        # Footer
        footer = QLabel("Developed by Kishore")
        footer.setFont(QFont("Roboto", 14))
        footer.setStyleSheet("color: #ff1744; margin-top: 30px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.home_page.setLayout(layout)
        self.stacked_widget.addWidget(self.home_page)

    def initialize_student_page(self):
        """Sets up the Student Page."""
        self.student_page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Student Menu")
        header.setFont(QFont("Helvetica Neue", 30, QFont.Bold))
        header.setStyleSheet("""
            color: white;
            background-color: #009688;
            padding: 25px;
            text-align: center;
            border-radius: 15px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Subheader
        subheader = QLabel("Select an option below:")
        subheader.setFont(QFont("Roboto", 18))
        subheader.setStyleSheet("color: #424242; margin: 15px;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        # Buttons
        layout.addWidget(self.create_button("Student Login", "#009688", "#4db6ac", self.open_student_login), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Back to Home", "#f44336", "#e57373", lambda: self.show_page(self.home_page)), alignment=Qt.AlignCenter)

        self.student_page.setLayout(layout)
        self.stacked_widget.addWidget(self.student_page)

    def initialize_admin_page(self):
        """Sets up the Admin Page."""
        self.admin_page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Admin Menu")
        header.setFont(QFont("Helvetica Neue", 30, QFont.Bold))
        header.setStyleSheet("""
            color: white;
            background-color: #1e88e5;
            padding: 25px;
            text-align: center;
            border-radius: 15px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Subheader
        subheader = QLabel("Select an option below:")
        subheader.setFont(QFont("Roboto", 18))
        subheader.setStyleSheet("color: #424242; margin: 15px;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        # Buttons
        layout.addWidget(self.create_button("Admin Login", "#1e88e5", "#42a5f5", self.open_admin_login), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Admin Signup", "#1e88e5", "#42a5f5", self.open_admin_signup), alignment=Qt.AlignCenter)
        layout.addWidget(
            self.create_button(
                "Back to Home",
                "#f44336",
                "#e57373",
                self.open_admin_signup
            ),
            alignment=Qt.AlignCenter
        )

        self.admin_page.setLayout(layout)
        self.stacked_widget.addWidget(self.admin_page)

    def create_button(self, text, color, hover_color, callback):
        """Creates a colorful button with hover effect."""
        button = HoverButton(text, color, hover_color)
        button.setMinimumWidth(300)
        button.setMaximumWidth(400)
        button.clicked.connect(callback)
        return button

    def show_page(self, page):
        """Displays the specified page."""
        self.stacked_widget.setCurrentWidget(page)

    def open_student_login(self):
        """Redirect to the Student Login page."""
        try:
            from student_login import Student_loginScreen
            self.student_login_screen = Student_loginScreen()
            self.stacked_widget.addWidget(self.student_login_screen)
            self.stacked_widget.setCurrentWidget(self.student_login_screen)
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to load Student Login module.\n{e}")

    def open_admin_login(self):
        """Redirect to the Admin Login page."""
        try:
            from admin_login import Admin_loginScreen
            self.admin_login_screen = Admin_loginScreen()
            self.stacked_widget.addWidget(self.admin_login_screen)
            self.stacked_widget.setCurrentWidget(self.admin_login_screen)
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to load Admin Login module.\n{e}")

    def open_admin_signup(self):
        """Redirect to the Admin Signup page."""
        try:
            from admin_signup import Admin_signupScreen
            self.admin_signup_screen = Admin_signupScreen()
            self.stacked_widget.addWidget(self.admin_signup_screen)
            self.stacked_widget.setCurrentWidget(self.admin_signup_screen)
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to load Admin Signup module.\n{e}")

    def mark_attendance(self):
        """Redirect to the Mark Attendance page."""
        try:
            self.attendance_screen = MarkAttendanceScreen(staff_id=1)
            self.stacked_widget.addWidget(self.attendance_screen)
            self.stacked_widget.setCurrentWidget(self.attendance_screen)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Mark Attendance screen.\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())
