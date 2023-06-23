from flask import Flask, request, render_template,jsonify
from flask_cors import CORS, cross_origin
import datetime
import mysql.connector
import datetime
import json
import pyttsx3
import threading
import pymysql
import time

#import task_announcer

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MYSQL_HOST'] = 'database-1.cpwdrdfsy4f3.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Abcd1234'
app.config['MYSQL_DB'] = 'taskreminder'

# Establish a database connection
conn = pymysql.connect(host='database-1.cpwdrdfsy4f3.eu-north-1.rds.amazonaws.com', user='admin', password='Abcd1234', database='taskreminder')

# connect index file
@app.route('/')
def index():
    return render_template('index.html')

# handle user registration
@app.route('/register/save', methods=['POST'])
@cross_origin()
def register_data():
    if request.method == 'POST':
        firstname = request.json['firstName']
        lastname = request.json['lastName']
        email = request.json['email']
        password = request.json['password']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO login (firstName ,lastName , email , password ) VALUES (%s, %s, %s, %s)', (firstname, lastname, email, password))
        conn.commit()
        return jsonify({'status': 200})

# handle user login
@app.route('/login', methods=['POST'])
@cross_origin()    
def login():
    
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        if email and password:
            cursor = conn.cursor()
            query = 'SELECT * FROM login WHERE email=%s AND password=%s'
            values = (email,password)
            cursor.execute(query, values)
            response = cursor.fetchone()

            if response:
                # User is successfully logged in
                return jsonify({'status': 200, 'message': 'Successfully logged in'})
            else:
                # Invalid email or password
                return jsonify({'status': 401, 'message': 'Invalid email or password'})
        else:
            # Missing email or password
            return jsonify({'status': 400, 'message': 'Email or password is missing'})

# handle save tasks
@app.route('/task/save', methods=['POST'])
@cross_origin()
def save_tasks():
    if request.method == 'POST':
        date = request.json['date']
        time = request.json['time']
        task = request.json['task']
        status = request.json['status']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO todo (task,task_date ,time,task_status) VALUES (%s, %s, %s, %s)', (task, date, time,status))
        conn.commit()

        return jsonify({'status': 200})

# handle update tasks
@app.route('/task/update', methods=['PUT'])
@cross_origin()
def update_data():
    if request.method == 'PUT':
        id = request.json['id']
        date = request.json['date']
        time = request.json['time']
        task = request.json['task']
        status = request.json['status']

        cursor = conn.cursor()
        query = 'UPDATE todo SET task_date=%s, time=%s, task=%s, task_status=%s WHERE tId=%s'
        values = (date, time, task,status, id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'status': 200})

# handle get all tasks
@app.route('/get/todos', methods=['GET'])
@cross_origin()
def get_all_data():
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todo ORDER BY task_date DESC')
        rows = cursor.fetchall()

        # Convert the date strings back to datetime.date objects
        formatted_rows = []
        for row in rows:
            row_data = list(row)  # Convert the tuple to a list
            row_data[2] = row_data[2].strftime('%Y-%m-%d')  # Format the date as 'YYYY-MM-DD'

            total_seconds = row_data[3].seconds
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_obj = datetime.time(hours, minutes, seconds)
            row_data[3] = str(time_obj)  # Convert time object to string

            dictionary = {
                'tId':  row_data[0],
                'task': row_data[1],
                'date': row_data[2],
                'time': row_data[3],
                'status': row_data[4]
            }

            formatted_rows.append(dictionary)

        return jsonify({'status': 200, 'data': formatted_rows})

# handle get tasks by date
@app.route('/get/todos/bydate', methods=['GET'])
@cross_origin()
def get_all_data_by_date():

    if request.method == 'GET':
        task_date = request.args.get('task_date')

        if task_date:
            cursor = conn.cursor()
            query = 'SELECT * FROM todo WHERE task_date = %s'
            values = (task_date,)
            cursor.execute(query, values)
            rows = cursor.fetchall()

            # Convert the date strings back to datetime.date objects
            formatted_rows = []
            for row in rows:
                row_data = list(row)  # Convert the tuple to a list
                row_data[2] = row_data[2].strftime('%Y-%m-%d')  # Format the date as 'YYYY-MM-DD'

                total_seconds = row_data[3].seconds
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_obj = datetime.time(hours, minutes, seconds)
                row_data[3] = str(time_obj)  # Convert time object to string

                dictionary = {
                    'tId':  row_data[0],
                    'task': row_data[1],
                    'date': row_data[2],
                    'time': row_data[3],
                    'status': row_data[4]
                }

                formatted_rows.append(dictionary)

        return jsonify({'status': 200, 'data': formatted_rows})

# handle delete task
@app.route('/task/delete', methods=['DELETE'])
@cross_origin()
def delete_data():
    if request.method == 'DELETE':
        id = request.json.get('id')
        if id:
            cursor = conn.cursor()
            query = 'DELETE FROM todo WHERE tId = %s'
            values = (id,)
            cursor.execute(query, values)
            conn.commit()
            return jsonify({'status': 200, 'message': 'Successfully Deleted!'})
        else:
            return jsonify({'status': 400, 'message': 'No ID provided'})

# Create an empty set to store the announced tasks
announced_tasks = set()

# Main server loop
@app.route('/task_announcer', methods=['GET'])
@cross_origin()
def announce_tasks():

    # Capture the current date and time
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().replace(microsecond=0, second=0)

    # Query the database for tasks
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todo ORDER BY task_date DESC')
    rows = cursor.fetchall()

    # Iterate over the rows from the database
    for row in rows:
        row_data = list(row)  # Convert the tuple to a list
        task_date = row_data[2]  # Date from the database
        task_time = row_data[3]  # Time from the database

        # Compare the task date and time with the current date and time
        if task_date == current_date:
            task_id = row_data[0]
            task_text = row_data[1]
            modified_task = task_text.replace('I', 'You')  # Modify the task text
            print(modified_task)

            # Check if the task has already been announced
            if task_id not in announced_tasks:
                announcement = "{} at {}".format(modified_task, "now")  # Create the announcement text
                #speak_text(announcement)  # Speak the announcement
                announced_tasks.add(task_id)  # Add the task to the announced tasks set

                return jsonify({'status': 200, 'data': announcement})

    return jsonify({'status': 400, 'data': 'No new tasks to announce'})

# Function to speak the provided text using text-to-speech
def speak_text(text):

    player = pyttsx3.init()
    voices = player.getProperty('voices')
    player.setProperty('voices', voices[1].id)
    player.say(text)
    player.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)

