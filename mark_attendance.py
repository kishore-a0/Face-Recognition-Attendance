import tkinter as tk
from tkinter import messagebox
import mysql.connector
import cv2
import numpy as np
import os


class MarkAttendanceScreen:
    def __init__(self, staff_id):
        self.staff_id = staff_id
        self.root = tk.Toplevel()
        self.root.title("Mark Attendance Screen")
        self.root.geometry("400x300")
        self.root.configure(bg="#e0f7fa")

        self.student_listbox = tk.Listbox(self.root, height=10, width=50)
        self.student_listbox.pack(pady=20)

        self.load_student_list()

        # Button to start face capture
        tk.Button(
            self.root,
            text="Capture Face",
            font=("Arial", 14),
            bg="#8e24aa",
            fg="white",
            command=self.capture_face
        ).pack(pady=20)

    def load_student_list(self):
        """Fetch and display students in the listbox."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT unique_id, name FROM students")
            students = cursor.fetchall()

            for student in students:
                unique_id, name = student
                self.student_listbox.insert(tk.END, f"{name} (ID: {unique_id})")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def capture_face(self):
        """Capture and compare the student's face with the stored data."""
        selected_student = self.student_listbox.get(tk.ACTIVE)
        if not selected_student:
            messagebox.showerror("Selection Error", "Please select a student!")
            return

        unique_id = selected_student.split(" ")[-1][1:-1]  # Extract unique ID
        student_name = selected_student.split(" (")[0]  # Extract student name

        # Check if the student's face is already stored
        if not self.is_face_stored(unique_id):
            messagebox.showerror("Face Not Found", f"No stored face found for {student_name}. Attendance cannot be marked.")
            return

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

                if self.match_face(unique_id, face_resized):
                    messagebox.showinfo("Attendance", f"Student {student_name} recognized!")
                    self.mark_attendance(unique_id)
                    cap.release()
                    cv2.destroyAllWindows()
                    self.root.destroy()  # Close the screen
                    return

            cv2.imshow("Capturing Face", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def is_face_stored(self, unique_id):
        """Check if a face is already stored for the student."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT face_path FROM students WHERE unique_id = %s", (unique_id,))
            result = cursor.fetchone()

            if result and result[0]:  # Check if face_path exists and is not empty
                return os.path.exists(result[0])  # Verify that the file exists on disk
            return False

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False

    def match_face(self, unique_id, captured_face):
        """Compare the captured face with the stored face data."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT face_path FROM students WHERE unique_id = %s", (unique_id,))
            result = cursor.fetchone()

            if result and result[0]:
                stored_face_path = result[0]
                stored_face = cv2.imread(stored_face_path, cv2.IMREAD_GRAYSCALE)
                stored_face_resized = cv2.resize(stored_face, (179, 179))

                distance = np.linalg.norm(captured_face - stored_face_resized)
                return distance < 100  # Smaller distance means a match

            cursor.close()
            conn.close()
            return False

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
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

            messagebox.showinfo("Attendance", "Attendance marked successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


if __name__ == "__main__":
    def test_screen():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        MarkAttendanceScreen(staff_id=1)
        root.mainloop()

    test_screen()
