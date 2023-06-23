import threading
import datetime
import time
import pyttsx3
import pymysql

# Establish a database connection
conn = pymysql.connect(host='database-1.cpwdrdfsy4f3.eu-north-1.rds.amazonaws.com', user='admin', password='Abcd1234', database='taskreminder')

# Create an empty set to store the announced tasks
announced_tasks = set()

# Function to announce tasks in a loop
def announce_tasks():

    #while True:
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
        print(task_time)

        # Compare the task date and time with the current date and time
        if task_date == current_date and task_time == current_time.time():
            print("ggh")
            task_id = row_data[0]
            task_text = row_data[1]
            modified_task = task_text.replace('I', 'You')  # Modify the task text
            print(modified_task)

            # Check if the task has already been announced
            if task_id not in announced_tasks:
                announcement = "{} at {}".format(modified_task, "now")  # Create the announcement text
                print(announcement)
                speak_text(announcement)  # Speak the announcement
                announced_tasks.add(task_id)  # Add the task to the announced tasks set

    # Wait for a certain duration before checking again (e.g., 1 minute)
    #time.sleep(60)

# Function to speak the provided text using text-to-speech
def speak_text(text):

    player = pyttsx3.init()
    voices = player.getProperty('voices')
    player.setProperty('voices', voices[1].id)
    player.say(text)
    player.runAndWait()

# Start the task announcement thread
#task_announcement_thread = threading.Thread(target=announce_tasks)
#task_announcement_thread.start()

# Main server loop
while True:
    announce_tasks()  # Check and announce tasks
    time.sleep(60)  # Wait for a certain duration before checking again (e.g., 1 minute)
