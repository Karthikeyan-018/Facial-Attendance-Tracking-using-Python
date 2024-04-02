import cv2
from flask import Flask, request, render_template, redirect, url_for
from datetime import date, datetime
import numpy as np
import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# Paths
attendance_file = f'Attendance/Attendance-{date.today().strftime("%m_%d_%y")}.csv'

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# If these directories don't exist, create them
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{date.today().strftime("%m_%d_%y")}.csv' not in os.listdir('Attendance'):
    with open(attendance_file, 'w') as f:
        f.write('Name,Roll,Time')

# Utility functions
def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    try:
        if img.shape != (0, 0, 0):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_points = face_detector.detectMultiScale(gray, 1.3, 5)
            return face_points
        else:
            return []
    except:
        return []

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def add_attendance(name):
    if name is not None:
        username = name.split('_')[0]
        userid = name.split('_')[1]
        current_time = datetime.now().strftime("%H:%M:%S")

        df = pd.read_csv(attendance_file)
        if int(userid) not in list(df['Roll']):
            with open(attendance_file, 'a') as f:
                f.write(f'\n{username},{userid},{current_time}')
            # Add attendance to Firestore
            db.collection('attendance').add({
                'name': username,
                'roll': int(userid),
                'time': current_time
            })
        else:
            message = f"{username} with ID {userid} is already marked present."
            return message

def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')

def getallusers():
    userlist = os.listdir('static/faces')
    names = []
    rolls = []
    l = len(userlist)

    for i in userlist:
        name, roll = i.split('_')
        names.append(name)
        rolls.append(roll)

    return userlist, names, rolls, l

def extract_attendance():
    df = pd.read_csv(attendance_file)
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

# Routes
@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/home')
def home():
    names, rolls, times, l = extract_attendance()
    message = request.args.get('message')
    duplicate_message = add_attendance(request.args.get('duplicate_user'))
    return render_template('home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(),
                           message=message, duplicate_message=duplicate_message)

@app.route('/student')
def student():
    names, rolls, times, l = extract_attendance()
    message = request.args.get('message')
    duplicate_message = add_attendance(request.args.get('duplicate_user'))
    return render_template('student.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(),
                           message=message, duplicate_message=duplicate_message)

@app.route('/start', methods=['GET'])
def start():
    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return redirect(url_for('home', message='There is no trained model in the static folder. Please add a new face to continue.'))

    ret = True
    cap = cv2.VideoCapture(0)
    while ret:
        ret, frame = cap.read()
        if len(extract_faces(frame)) > 0:
            (x, y, w, h) = extract_faces(frame)[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            message = add_attendance(identified_person)
            if message is not None:
                cap.release()
                cv2.destroyAllWindows()
                return redirect(url_for('home', message='Attendance already taken for this user.'))
            cv2.putText(frame, f'{identified_person}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2,
                        cv2.LINE_AA)
        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for('home', message='Attendance taken successfully'))

@app.route('/add', methods=['POST'])
def add_user():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    userimagefolder = 'static/faces/' + newusername + '_' + str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/50', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2,
                        cv2.LINE_AA)
            if j % 10 == 0:
                name = newusername + '_' + str(i) + '.jpg'
                cv2.imwrite(userimagefolder + '/' + name, frame[y:y + h, x:x + w])
                i += 1
            j += 1
        if j == 500:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    # Store user information in Firebase Firestore
    try:
        db.collection('users').add({
            'name': newusername,
            'roll': int(newuserid),
            'image_folder': userimagefolder
        })
    except Exception as e:
        return redirect(url_for('home', message='Error occurred while adding user to Firestore.'))

    print('Training Model')
    train_model()
    return redirect(url_for('home', message='New user added successfully'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Create user with email and password
            user = auth.create_user(email=email, password=password)
            # Redirect to login page after signup
            return redirect(url_for('login'))
        except Exception as e:
            return "Error: " + str(e)
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Get the selected role from the form
        try:
            # Sign in with email and password
            user = auth.get_user_by_email(email)
            # Redirect to home page or student page based on the selected role
            if role == 'teacher':
                return redirect(url_for('home'))
            elif role == 'student':
                return redirect(url_for('student'))
        except Exception as e:
            return "Error: " + str(e)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
