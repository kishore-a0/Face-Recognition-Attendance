from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
from mark_attendance import MarkAttendanceScreen  # Import the MarkAttendanceScreen class


# HoverButton Class (Unchanged)
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
            background-color: {color}; 
            color: white; 
            border-radius: 10px; 
            padding: 10px; 
            font-size: 16px;
        """


class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

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

        header = QLabel("Face Recognition Attendance System")
        header.setFont(QFont("Helvetica Neue", 32, QFont.Bold))
        header.setStyleSheet(""" 
            color: white; 
            background-color: #0d47a1; 
            padding: 20px; 
            text-align: center; 
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        subheader = QLabel("Efficient attendance management with AI-powered face recognition.")
        subheader.setFont(QFont("Roboto", 16))
        subheader.setStyleSheet("color: #424242; margin: 10px;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_button("Student", "#4caf50", "#66bb6a", lambda: self.show_page(self.student_page)))
        buttons_layout.addWidget(self.create_button("Admin", "#7b1fa2", "#9c27b0", lambda: self.show_page(self.admin_page)))

        layout.addLayout(buttons_layout)

        footer = QLabel("Developed by Kishore")
        footer.setFont(QFont("Roboto", 12))
        footer.setStyleSheet("color: red; margin-top: 20px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.home_page.setLayout(layout)
        self.stacked_widget.addWidget(self.home_page)

    def initialize_student_page(self):
        """Sets up the Student Page."""
        self.student_page = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Student Menu")
        header.setFont(QFont("Helvetica Neue", 28, QFont.Bold))
        header.setStyleSheet(""" 
            color: white; 
            background-color: #4caf50; 
            padding: 20px; 
            text-align: center; 
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        subheader = QLabel("Choose an option below:")
        subheader.setFont(QFont("Roboto", 16))
        subheader.setStyleSheet("color: #424242; margin: 10px;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        # Button to open Mark Attendance screen
        layout.addWidget(self.create_button("Mark Attendance", "#4caf50", "#66bb6a", self.mark_attendance), alignment=Qt.AlignCenter)

        layout.addWidget(self.create_button("Student Login", "#4caf50", "#66bb6a", self.open_student_login), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Student Signup", "#4caf50", "#66bb6a", self.open_student_signup), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Back to Home", "#f44336", "#e57373", lambda: self.show_page(self.home_page)), alignment=Qt.AlignCenter)

        self.student_page.setLayout(layout)
        self.stacked_widget.addWidget(self.student_page)

    def initialize_admin_page(self):
        """Sets up the Admin Page."""
        self.admin_page = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Admin Menu")
        header.setFont(QFont("Helvetica Neue", 28, QFont.Bold))
        header.setStyleSheet(""" 
            color: white; 
            background-color: #7b1fa2; 
            padding: 20px; 
            text-align: center; 
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        subheader = QLabel("Choose an option below:")
        subheader.setFont(QFont("Roboto", 16))
        subheader.setStyleSheet("color: #424242; margin: 10px;")
        subheader.setAlignment(Qt.AlignCenter)
        layout.addWidget(subheader)

        layout.addWidget(self.create_button("Admin Login", "#7b1fa2", "#9c27b0", self.open_admin_login), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Admin Signup", "#7b1fa2", "#9c27b0", self.open_admin_signup), alignment=Qt.AlignCenter)
        layout.addWidget(self.create_button("Back to Home", "#f44336", "#e57373", lambda: self.show_page(self.home_page)), alignment=Qt.AlignCenter)

        self.admin_page.setLayout(layout)
        self.stacked_widget.addWidget(self.admin_page)

    def show_page(self, page):
        """Displays the specified page."""
        self.stacked_widget.setCurrentWidget(page)

    def create_button(self, text, color, hover_color, callback):
        """Creates a styled button with a callback."""
        button = HoverButton(text, color, hover_color)
        button.clicked.connect(callback)
        return button

    def open_student_signup(self):
        """Opens the student signup screen."""
        self.open_screen("student_signup", "Student Signup screen not implemented or not found!")

    def open_student_login(self):
        """Opens the student login screen."""
        self.open_screen("student_login", "Student Login screen not implemented or not found!")

    def open_admin_login(self):
        """Opens the admin login screen."""
        self.open_screen("admin_login", "Admin Login screen not implemented or not found!")

    def open_admin_signup(self):
        """Opens the admin signup screen."""
        self.open_screen("admin_signup", "Admin Signup screen not implemented or not found!")

    def open_screen(self, screen_name, error_message):
        """General method to open screens."""
        try:
            # Dynamically import the module for the student or admin screens
            module = __import__(screen_name)

            screen_class_name = f"{screen_name.capitalize()}Screen"  # Generate class name dynamically

            # Make sure the class exists within the module
            screen_class = getattr(module, screen_class_name)

            # Create and add the screen to the stacked widget
            screen = screen_class()
            self.stacked_widget.addWidget(screen)
            self.stacked_widget.setCurrentWidget(screen)
            
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"{error_message}\nError: {e}")
        except AttributeError:
            QMessageBox.critical(self, "Error", f"{error_message}\nClass not found in the module.")

    def mark_attendance(self):
        """Handles the Mark Attendance action by opening the MarkAttendanceScreen."""
        # Create an instance of the MarkAttendanceScreen
        self.attendance_screen = MarkAttendanceScreen(staff_id=1)  # Pass the necessary staff_id or any other data
        
        # Add the MarkAttendanceScreen to the stacked widget
        self.stacked_widget.addWidget(self.attendance_screen)
        
        # Switch to the MarkAttendanceScreen
        self.stacked_widget.setCurrentWidget(self.attendance_screen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())
