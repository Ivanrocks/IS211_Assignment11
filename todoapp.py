import os
import sqlite3
import dbutility
from flask import request, redirect, url_for, flash
from flask import Flask, render_template
import re

def is_email(email):
    """
    Validates if the provided email address matches the standard email format.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_priority(priority):
    """
    Validates if the provided priority is one of the accepted values: 'low', 'medium', or 'high'.

    Args:
        priority (str): The priority level to be validated.

    Returns:
        bool: True if the priority is valid, False otherwise.
    """
    return priority.lower() in ["low", "medium", "high"]

def connect_to_db():
    """
    Establishes a connection to the 'TODO.db' SQLite database. If the database
    file does not exist, it will be created. Returns a cursor object for executing SQL commands.

    Returns:
        sqlite3.Cursor: Cursor object to interact with the database.
    """
    # Create or connect to the TODO.db database
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()
    return cursor

# Initialize the Flask web application
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte secret key for session management

@app.route('/')
def index():
    """
    Renders the home page of the application. It fetches all tasks from the database and displays them.

    Returns:
        str: The rendered HTML template for the home page with task data.
    """
    tasks = dbutility.fetch_all()  # Fetch all tasks from the database using dbutility
    return render_template('index.html', tasks=tasks)

@app.route('/clear')
def clear_data():
    """
    Clears all tasks from the database by calling the delete_all function from dbutility.

    Returns:
        Response: Redirects to the index page after clearing the data.
    """
    dbutility.delete_all()  # Clears all tasks from the database
    return redirect(url_for('index'))  # Redirect to the home page after clearing

@app.route('/save')
def save():
    """
    Saves all tasks from the database to a text file 'TODO.txt'. Each task is written on a new line with its data separated by commas.
    If any task is missing data, it will be skipped.

    Returns:
        Response: Redirects to the index page with a success or error message.
    """
    try:
        with open('TODO.txt', 'w') as f:
            tasks = dbutility.fetch_all()  # Fetch all tasks from the database
            for task in tasks:
                try:
                    if task and len(task) >= 4:  # Ensure the task has the expected structure
                        # Write task data to file
                        f.write(
                            str(task[0]) + "," +
                            task[1] + "," +
                            task[2] + "," +
                            task[3] + "\n"
                        )
                    else:
                        print(f"Skipping invalid task: {task}")
                except Exception as e:
                    print(f"Error writing task {task}: {e}")

        # Flash success message for saving tasks
        flash("Your tasks have been saved successfully!", "success")

    except Exception as e:
        # Flash error message if there is an issue with file operations
        flash(f"Error saving tasks: {e}", "error")

    return redirect(url_for('index'))  # Redirect back to the homepage

@app.route('/submit', methods=['GET', 'POST'])
def submit_form():
    """
    Renders a form to submit a new task. It validates the task name, email, and priority before adding the task to the database.

    If the form is submitted (POST request):
        - It validates the email and priority fields.
        - If valid, it inserts the new task into the database.
        - Redirects to the home page.

    If the form is accessed via GET request, it simply renders the form for input.

    Returns:
        str: Rendered HTML template for the form (if GET) or redirects to the homepage (if POST).
    """
    if request.method == "POST":
        addTODO = True
        taskName = request.form.get('taskName')
        email = request.form.get('email')
        priority = request.form.get('priority')

        # Validate email and priority
        if is_email(email) is False:
            addTODO = False
        if is_valid_priority(priority) is False:
            addTODO = False

        # If the form data is valid, add the task to the database
        if addTODO:
            dbutility.insert_data(taskName, email, priority)

        return redirect(url_for('index'))  # Redirect to the homepage

    if request.method == "GET":
        return render_template('submit_form.html')  # Render the task submission form

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Deletes a task by its ID from the database. It also flashes a success message after deletion.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        Response: Redirects to the index page after deleting the task, with a success message.
    """
    dbutility.delete_task_by_id(task_id)  # Delete the task by ID
    # Flash success message for deletion
    flash("Your task has been deleted successfully!", "success")
    return redirect(url_for('index'))  # Redirect back to the task list

if __name__ == "__main__":
    """
    Entry point of the application. This block runs the Flask web application after setting up the database.
    - Creates the database and loads data from 'TODO.txt' into the database.
    """
    file_path = "TODO.txt"
    dbutility.create_database()  # Create the database and tables
    dbutility.load_data_from_file(file_path)  # Load tasks from 'TODO.txt' file into the database

    app.run()  # Start the Flask application
