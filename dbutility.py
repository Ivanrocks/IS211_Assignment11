import sqlite3


def create_database():
    """
    Creates a SQLite database named 'TODO.db' and sets up a 'todolist' table.

    The 'todolist' table has the following columns:
    - id (INTEGER): The primary key, auto-incremented.
    - task_name (TEXT): Name of the task.
    - email (TEXT): Email associated with the task.
    - priority (TEXT): Priority level of the task (Low, Medium, High).

    If the 'todolist' table already exists, it is dropped and recreated to ensure a fresh setup.
    """
    # Create or connect to the TODO.db database
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()

    # Drop the existing todolist table if it exists
    cursor.execute('''DROP TABLE IF EXISTS todolist;''')

    # Create the todolist table with appropriate columns
    cursor.execute('''
    CREATE TABLE todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        email TEXT,
        priority TEXT
    );
    ''')

    # Commit changes and close the connection
    connection.commit()
    connection.close()


def insert_data(taskName, email, priority):
    """
    Inserts a new task into the 'todolist' table.

    Args:
    - taskName (str): The name of the task.
    - email (str): The email associated with the task.
    - priority (str): The priority of the task (Low, Medium, High).

    This function inserts the provided data into the 'todolist' table and commits the changes.
    """
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()

    # Prepare the data for insertion
    task = (
        taskName,
        email,
        priority
    )

    # Insert the task into the todolist table
    cursor.execute('INSERT INTO todolist (task_name, email, priority) VALUES (?, ?, ?);', task)
    print("Data inserted successfully")

    # Commit changes and close the connection
    connection.commit()
    connection.close()


def fetch_all():
    """
    Fetches all tasks from the 'todolist' table.

    Returns:
    - list: A list of tuples containing all rows from the 'todolist' table.

    Each tuple represents a task, with the columns: id, task_name, email, and priority.
    """
    print("Fetching Data")
    connection = sqlite3.connect('TODO.db')

    # Execute the SELECT query and fetch all rows
    tasks = connection.execute(
        'SELECT * FROM todolist;'
    ).fetchall()

    # Return the fetched tasks
    return tasks


def delete_all():
    """
    Deletes all tasks from the 'todolist' table.

    This function executes a DELETE statement to remove all entries from the 'todolist' table.
    """
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()

    # Delete all tasks from the table
    cursor.execute('DELETE FROM todolist;')

    # Commit changes and close the connection
    connection.commit()
    connection.close()


def load_data_from_file(file_name):
    """
    Loads task data from a file and inserts it into the 'todolist' table.

    Args:
    - file_name (str): The path to the file containing task data.

    The file should contain tasks in the format:
    task_name,email,priority (one task per line).

    Each line is split by commas, and the data is inserted into the database.
    If any line is improperly formatted (e.g., missing fields), it is skipped.
    """
    try:
        with open(file_name, 'r') as file:
            data = file.readlines()  # Reads each line into a list

        # Process data as needed
        if data:
            print("Loading Data")

        for line in data:
            try:
                task = line.split(",")  # Split the line into components
                insert_data(task[0], task[1], task[2])  # Insert data into the database
            except IndexError:
                print("Skipping Line. Out of range.")

        print("Data loaded successfully")

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except IOError:
        print(f"Error: An error occurred while reading the file '{file_name}'.")


def delete_task_by_id(task_id):
    """
    Deletes a task from the 'todolist' table by its ID.

    Args:
    - task_id (int): The ID of the task to delete.

    This function uses a DELETE statement to remove the task with the given ID from the 'todolist' table.
    If an error occurs during deletion, it is caught and printed.
    """
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()

    print("Deleting task with ID: " + str(task_id))

    try:
        # Execute the DELETE statement using the task_id as a parameter
        cursor.execute("DELETE FROM todolist WHERE id = ?", (task_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting task: {e}")
    finally:
        # Close the connection after the operation
        connection.close()
