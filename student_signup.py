import os
import cv2
import face_recognition
import bcrypt
import mysql.connector
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QComboBox, QDateEdit, QScrollArea
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class StudentSignup(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 50, 500, 800)
        self.setStyleSheet("background-color: #eef2f3;")

        # Scrollable layout
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)

        # Header
        header = QLabel("Sign Up")
        header.setFont(QFont("Arial", 28, QFont.Bold))
        header.setStyleSheet("color: #4caf50; text-align: center;")
        scroll_layout.addWidget(header, alignment=Qt.AlignCenter)

        # Input fields
        self.first_name_input = self.create_input_field("Enter your first name", scroll_layout)
        self.last_name_input = self.create_input_field("Enter your last name", scroll_layout)
        self.reg_no_input = self.create_input_field("Enter your registration number", scroll_layout)
        self.email_input = self.create_input_field("Enter your email", scroll_layout)
        self.password_input = self.create_input_field("Enter your password", scroll_layout, is_password=True)

        # Dropdowns
        self.class_input = self.create_dropdown(['MCA', 'BCA', 'MTech', 'BTech'], scroll_layout)
        self.gender_input = self.create_dropdown(['Male', 'Female', 'Other'], scroll_layout)

        # Date of Birth Field
        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        self.dob_input.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.dob_input)

        # Additional fields
        self.parent_contact_input = self.create_input_field("Enter parent contact number", scroll_layout)
        self.member_type_input = self.create_dropdown(['Student', 'Faculty', 'Admin'], scroll_layout)

        # Sign Up Button
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet(
            "background-color: #4caf50; color: white; font-size: 16px; padding: 10px; border-radius: 8px;"
        )
        self.signup_button.clicked.connect(self.capture_and_register)
        scroll_layout.addWidget(self.signup_button, alignment=Qt.AlignCenter)

        # Scroll area setup
        scroll_area.setWidget(content_widget)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

    def create_input_field(self, placeholder, layout, is_password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(self.input_style())
        if is_password:
            field.setEchoMode(QLineEdit.Password)
        layout.addWidget(field)
        return field

    def create_dropdown(self, items, layout):
        dropdown = QComboBox()
        dropdown.addItems(items)
        dropdown.setStyleSheet(self.dropdown_style())
        layout.addWidget(dropdown)
        return dropdown

    def input_style(self):
        return (
            "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
            "margin-bottom: 10px;"
        )

    def dropdown_style(self):
        return "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 10px;"

    def capture_and_register(self):
        reg_no = self.reg_no_input.text().strip()
        if not reg_no:
            QMessageBox.warning(self, "Input Error", "Registration number is required.")
            return

        face_path = f"faces/{reg_no}.jpg"
        os.makedirs("faces", exist_ok=True)

        cap = cv2.VideoCapture(0)
        QMessageBox.information(self, "Capture", "Press 's' to capture your face or 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                QMessageBox.critical(self, "Error", "Could not access the camera.")
                return

            cv2.imshow("Capture Face", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                cv2.imwrite(face_path, frame)
                QMessageBox.information(self, "Success", "Face captured successfully!")
                break
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        cap.release()
        cv2.destroyAllWindows()

        if self.is_duplicate_face(face_path):
            QMessageBox.warning(self, "Duplicate Error", "This face is already registered.")
            os.remove(face_path)
            return

        self.register_user(face_path)

    def is_duplicate_face(self, new_face_path):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT face_path FROM users")
            face_paths = cursor.fetchall()

            for (path,) in face_paths:
                if path and os.path.exists(path):
                    known_image = face_recognition.load_image_file(path)
                    new_image = face_recognition.load_image_file(new_face_path)

                    known_encoding = face_recognition.face_encodings(known_image)[0]
                    new_encoding = face_recognition.face_encodings(new_image)[0]

                    results = face_recognition.compare_faces([known_encoding], new_encoding)
                    if results[0]:
                        return True
            return False
        finally:
            cursor.close()
            conn.close()

    def register_user(self, face_path):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        reg_no = self.reg_no_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        student_class = self.class_input.currentText()
        gender = self.gender_input.currentText()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        parent_contact = self.parent_contact_input.text().strip()
        member_type = self.member_type_input.currentText()

        if not first_name or not last_name or not email or not password or not parent_contact:
            QMessageBox.warning(self, "Input Error", "Please fill all the fields.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="attendance_system"
            )
            cursor = conn.cursor()

            query = """INSERT INTO users 
                       (first_name, last_name, reg_no, email, password, class, gender, dob, parent_contact, member_type, face_path)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (
                first_name, last_name, reg_no, email, hashed_password,
                student_class, gender, dob, parent_contact, member_type, face_path
            )
            cursor.execute(query, data)
            conn.commit()

            QMessageBox.information(self, "Success", "User registered successfully!")
            self.redirect_to_login()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def redirect_to_login(self):
        from student_login import login
        self.close()
        self.login_window = login()
        self.login_window.show()
