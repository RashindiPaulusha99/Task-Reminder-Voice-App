from flask import Flask, request, render_template,jsonify
from flask_cors import CORS, cross_origin
import datetime
import mysql.connector
import datetime
import json

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MYSQL_HOST'] = 'database-1.cpwdrdfsy4f3.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Abcd1234'
app.config['MYSQL_DB'] = 'taskreminder'

# connect mysql database
conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

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

if __name__ == '__main__':
    app.run(debug=True)

