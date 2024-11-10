import sqlite3
def create_database():
    # Create or connect to the pets.db database
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS todolist;
    ''')
    # Create the person table
    cursor.execute('''
    CREATE TABLE todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        email TEXT,
        priority TEXT
    );
    ''')

    connection.commit()
    connection.close()

def insert_data(taskName, email, priority):
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()
    task = (
        taskName,
        email,
        priority
    )
    cursor.execute('INSERT INTO todolist (task_name, email, priority) VALUES (?, ?, ?);', task)
    print("Data inserted successfully")
    connection.commit()
    connection.close()

def fetch_all():
    print("Fetching Data")
    connection = sqlite3.connect('TODO.db')

    tasks = connection.execute(
        'SELECT * FROM todolist;'
    ).fetchall()
    return tasks

def delete_all():
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM todolist;')
    connection.commit()
    connection.close()

def load_data_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.readlines()  # Reads each line into a list
        # Process data as needed
        if data:
            print("Loading Data")
        for line in data:
            try:
                task = line.split(",")
                insert_data(task[1], task[2], task[3])
            except IndexError:
                print("Skipping Line. Out of range.")
        print("Data loaded successfully")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")

    except IOError:
        print(f"Error: An error occurred while reading the file '{file_name}'.")


def delete_task_by_id(task_id):
    connection = sqlite3.connect('TODO.db')
    cursor = connection.cursor()
    print("Deleting task with ID: " + str(task_id))
    try:
        cursor.execute("DELETE FROM todoList WHERE id = ?", (task_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting task: {e}")
    finally:
        connection.close()
