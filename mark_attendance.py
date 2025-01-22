import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QListWidget, QMessageBox
import mysql.connector
import cv2
import numpy as np
import os

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

        # Hide the Capture Face button, camera will open automatically
        self.capture_button = QPushButton("Capture Face", self)
        self.capture_button.setStyleSheet(
            "font-size: 14px; color: white; background-color: #3498db; border-radius: 5px; padding: 10px;"
        )
        self.capture_button.setEnabled(False)  # Disable the button
        main_layout.addWidget(self.capture_button)

        # Start capturing face directly when the window is loaded
        self.capture_face()

    def capture_face(self):
        """Capture and compare the face with the stored data."""
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face_region = gray[y:y + h, x:x + w]
                face_resized = cv2.resize(face_region, (179, 179))

                # Compare the captured face with stored faces
                if self.compare_face(face_resized):
                    QMessageBox.information(self, "Attendance", "Face recognized and attendance marked!")
                    cap.release()
                    cv2.destroyAllWindows()
                    self.show_student_dashboard()  # Show the student dashboard
                    self.close()  # Close the current window
                    return

            cv2.imshow("Capturing Face", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

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

            cursor.execute("SELECT unique_id, face_path FROM users")
            users = cursor.fetchall()

            for user in users:
                unique_id, stored_face_path = user
                if stored_face_path and os.path.exists(stored_face_path):
                    stored_face = cv2.imread(stored_face_path, cv2.IMREAD_GRAYSCALE)
                    stored_face_resized = cv2.resize(stored_face, (179, 179))

                    # Compute the Euclidean distance between the captured and stored faces
                    distance = np.linalg.norm(captured_face - stored_face_resized)

                    print(f"Distance for user {unique_id}: {distance}")  # Debugging line

                    # If distance is small, faces match
                    if distance < 100:  # Adjust this value if necessary
                        self.unique_id = unique_id
                        self.mark_attendance(unique_id)
                        return True

            cursor.close()
            conn.close()
            return False

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            return False

    def mark_attendance(self, unique_id):
        """Mark attendance in the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO attendance (student_id, attendance_date) VALUES (%s, CURDATE())", (unique_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Attendance", "Attendance marked successfully!")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def show_student_dashboard(self):
        """Show the student dashboard after attendance is marked."""
        dashboard_window = QWidget(self)
        dashboard_window.setWindowTitle("Student Dashboard")
        dashboard_window.setGeometry(100, 100, 500, 500)

        dashboard_layout = QVBoxLayout(dashboard_window)

        # For demonstration purposes, you can add widgets here
        dashboard_layout.addWidget(QPushButton("Dashboard - Student Information"))

        dashboard_window.setLayout(dashboard_layout)
        dashboard_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkAttendanceScreen(staff_id=1)
    window.show()
    sys.exit(app.exec_())
