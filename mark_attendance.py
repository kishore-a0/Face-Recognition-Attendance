import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QVBoxLayout, QPushButton
import mysql.connector
import cv2
import numpy as np
import os
import time


class MarkAttendanceScreen(QMainWindow):
    def __init__(self, staff_id):
        super().__init__()

        self.staff_id = staff_id
        self.setWindowTitle("Mark Attendance Screen")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #2c3e50;")  # Dark background color

        # Main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # Title label
        self.title_label = QPushButton("Mark Attendance", self)
        self.title_label.setStyleSheet("font-size: 20px; color: white; background-color: #2c3e50;")
        self.title_label.setEnabled(False)
        main_layout.addWidget(self.title_label)

        # Start capturing face directly
        self.capture_face()

    def capture_face(self):
        """Capture and compare the face with the stored data."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.critical(self, "Error", "Camera not accessible!")
            return

        face_recognized = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face_region = gray[y:y + h, x:x + w]
                    face_resized = cv2.resize(face_region, (179, 179))

                    # Pause for 3 seconds to ensure stability
                    time.sleep(3)

                    if self.compare_face(face_resized):
                        QMessageBox.information(self, "Attendance", "Face recognized! Attendance marked successfully.")
                        face_recognized = True
                        break

            if face_recognized:
                break

            cv2.imshow("Capturing Face", frame)

            # Break the loop if user presses 'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        if not face_recognized:
            QMessageBox.warning(self, "Face Not Detected", "Face not detected! Attendance sent to admin for review.")
            self.send_to_admin_review()

    def compare_face(self, captured_face):
        """Compare the captured face with stored face data in the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT reg_no, face_path FROM users")
            users = cursor.fetchall()

            for user in users:
                reg_no, stored_face_path = user
                if stored_face_path and os.path.exists(stored_face_path):
                    stored_face = cv2.imread(stored_face_path, cv2.IMREAD_GRAYSCALE)
                    stored_face_resized = cv2.resize(stored_face, (179, 179))

                    distance = np.linalg.norm(captured_face - stored_face_resized)

                    if distance < 100:  # Adjust this threshold
                        if self.check_attendance(reg_no):
                            QMessageBox.information(self, "Attendance", "Attendance already marked for today!")
                            return False
                        self.mark_attendance(reg_no, is_present=True)
                        return True

            cursor.close()
            conn.close()

            return False

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            return False

    def check_attendance(self, reg_no):
        """Check if attendance is already marked for the student today."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM attendance WHERE reg_no = %s AND date = CURDATE()",
                (reg_no,)
            )
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return True

            cursor.close()
            conn.close()
            return False

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            return False

    def mark_attendance(self, reg_no, is_present):
        """Mark attendance in the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            if is_present:
                cursor.execute(
                    "INSERT INTO attendance (reg_no, date, status) VALUES (%s, CURDATE(), 'Present')",
                    (reg_no,)
                )
                QMessageBox.information(self, "Attendance", "Attendance marked as Present!")
            conn.commit()
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def send_to_admin_review(self):
        """Send the student ID to admin for review."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO admin_review (staff_id, date, status, reviewed) VALUES (%s, CURDATE(), 'Pending', 0)",
                (self.staff_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Admin Review", "Your attendance has been sent for admin review.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkAttendanceScreen(staff_id=1)
    window.show()
    sys.exit(app.exec_())
