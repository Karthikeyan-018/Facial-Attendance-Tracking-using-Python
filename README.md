Attendance System using Face Recognition and Firebase
Description
This project is a web-based attendance system developed using Flask, OpenCV for face recognition, and Firebase for database management. It allows users to register their faces, take attendance using a webcam, and view attendance records. The system provides separate interfaces for teachers and students, allowing teachers to manage attendance and students to view their attendance status.

Features
User authentication with email and password using Firebase Authentication.
Face registration: Users can register their faces by capturing multiple images through a webcam.
Real-time face recognition: The system identifies registered faces using OpenCV and marks attendance accordingly.
Firebase integration: Attendance records are stored in Firestore, providing a scalable and reliable database solution.
Responsive web interface: The system offers intuitive web pages for both teachers and students.
Setup Instructions
Clone this repository to your local machine.
Install the required dependencies listed in requirements.txt.
Set up a Firebase project and download the service account key JSON file.
Rename the downloaded Firebase service account key JSON file to serviceAccountKey.json and place it in the project directory.
Create a virtual environment (recommended) and activate it.
Run the Flask application by executing python app.py in the terminal.
Access the application through a web browser at http://localhost:5000.
Usage
As a Teacher:
Sign up or log in as a teacher.
Add new students by capturing their faces and providing their names and roll numbers.
Start taking attendance by clicking the "Start" button and allowing the webcam access.
The system will recognize registered faces and mark their attendance automatically.
View attendance records on the home page.
As a Student:
Sign up or log in as a student.
View your attendance records on the student page.
Contributors
Your Name
Karthikeyan V
