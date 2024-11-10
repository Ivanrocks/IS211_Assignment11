import os
import sqlite3
import dbutility
from flask import request, redirect, url_for, flash
from flask import Flask, render_template
import re



def is_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_priority(priority):
    return priority.lower() in ["low", "medium", "high"]

def connect_to_db():
    """
        Establishes a connection to the 'pets.db' SQLite database. If the database
        file does not exist, it will be created. Returns a cursor object for executing SQL commands.

        Returns:
            sqlite3.Cursor: Cursor object to interact with the database.
        """
    # Create or connect to the pets.db database
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()
    return cursor

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte secret key

@app.route('/')
def index():
    tasks = dbutility.fetch_all()
    return render_template('index.html', tasks = tasks)

@app.route('/clear')
def clear_data():
    dbutility.delete_all()
    return redirect(url_for('index'))


@app.route('/save')
def save():
    try:
        with open('TODO.txt', 'w') as f:
            tasks = dbutility.fetch_all()
            for task in tasks:
                try:
                    if task and len(task) >= 4:  # Check if the task has the expected structure
                        # Write task to file with a newline after each task
                        f.write(
                            str(task[0]) + "," +
                            task[1] + "," +
                            task[2] + "," +
                            task[3] + "\n"  # Added newline for proper formatting
                        )
                    else:
                        print(f"Skipping invalid task: {task}")
                except Exception as e:
                    print(f"Error writing task {task}: {e}")

        # Flash success message
        flash("Your tasks have been saved successfully!", "success")

    except Exception as e:
        # Flash error message if there's an issue opening or writing the file
        flash(f"Error saving tasks: {e}", "error")

    return redirect(url_for('index'))


@app.route('/submit', methods=['GET', 'POST'])
def submit_form():
    if request.method == "POST":
        addTODO = True
        taskName = request.form.get('taskName')
        email = request.form.get('email')
        priority = request.form.get('priority')

        if is_email(email) is False:
            addTODO = False
        if is_valid_priority(priority) is False:
            addTODO = False

        if addTODO:
            dbutility.insert_data(taskName, email, priority)
        return redirect(url_for('index'))  # Redirects to the homepage ('/')

    if request.method == "GET":
        return render_template('submit_form.html')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Assuming you have a method in dbutility to delete by task ID
    dbutility.delete_task_by_id(task_id)
    # Flash success message
    flash("Your tasks have been deleted successfully!", "success")
    return redirect(url_for('index'))  # Redirect back to the main task list

if __name__ == "__main__":
    file_path = "TODO.txt"
    dbutility.create_database()
    dbutility.load_data_from_file(file_path)

    app.run()