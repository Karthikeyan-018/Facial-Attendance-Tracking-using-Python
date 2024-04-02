# Attendance Management System using Facial Recognition

This project is a Flask-based web application designed for managing attendance using facial recognition technology. It allows users to register their faces and subsequently mark their attendance by simply appearing in front of a webcam.

## Features

- **User Registration:** Users can sign up and register their faces along with their names and roll numbers.
- **Facial Recognition:** The system detects faces using OpenCV's Haar cascade classifier and recognizes registered users using a K-Nearest Neighbors classifier.
- **Attendance Tracking:** Attendance is marked automatically upon recognition of registered faces and recorded in a CSV file and Firestore database.
- **User Roles:** Supports different user roles (teacher and student) for login and access control.
- **Firebase Integration:** Utilizes Firebase Authentication for user authentication and Firestore for storing user data and attendance records.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/attendance-management-system.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Firebase:
   - Create a project on Firebase console.
   - Generate and download a service account key JSON file.
   - Place the JSON file in the project directory and update the `serviceAccountKey.json` path in `app.py`.

4. Set up the Face Recognition Model:
   - Train the face recognition model by capturing and adding faces of users.
   - Run `python app.py` and navigate to `/signup` to register faces.

5. Run the application:

    ```bash
    python app.py
    ```

6. Access the application via web browser at `http://localhost:5000`.

## Usage

- Sign up as a teacher to manage attendance or as a student to view attendance.
- Teachers can start marking attendance by clicking on the "Start Attendance" button.
- Students can view their attendance records on the dashboard.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).