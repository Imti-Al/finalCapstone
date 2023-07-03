# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def read_tasks():
    # Check if tasks.txt file exists, if not create it
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    # Read task data from tasks.txt file
    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split task components and assign them to a dictionary
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

def write_tasks(task_list):
    # Write task data to tasks.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def register_user():
    # Register a new user by providing a username and password.
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
        return

    # Check if the new password and confirmed password are the same. Provide relevant message if not.
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    # If they are the same, add new user to username_password dictionary and write to user.txt file.
    username_password[new_username] = new_password
    with open("user.txt", "a") as user_file:
        user_file.write(f"\n{new_username};{new_password}")
    print("New user added.")

def add_task():
    # Add a new task to the task list
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    write_tasks(task_list)
    print("Task added successfully.")

    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
def display_tasks(tasks):
    for i, t in enumerate(tasks):
        disp_str = f"\nTask {i + 1}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\n{t['description']}\n"
        disp_str += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)

def view_all_tasks():
    display_tasks(task_list)

def view_my_tasks(username):
    user_tasks = [t for t in task_list if t['username'] == username]
    display_tasks(user_tasks)

    task_number = input("Enter the task number to select a specific task (or -1 to return to the main menu): ")
    if task_number == "-1":
        return

    try:
        task_index = int(task_number) - 1
        selected_task = user_tasks[task_index]
    except (ValueError, IndexError):
        print("Invalid task number. Please enter a valid task number.")
        return

    edit_task = input("Do you want to mark this task as complete or edit it? (mark/edit): ")
    if edit_task.lower() == "mark":
        if selected_task['completed']:
            print("Task is already marked as complete.")
        else:
            selected_task['completed'] = True
            write_tasks(task_list)
            print("Task marked as complete.")
    elif edit_task.lower() == "edit":
        if selected_task['completed']:
            print("Task cannot be edited as it is already marked as complete.")
        else:
            new_username = input("Enter a new username (press enter to keep it unchanged): ")
            new_due_date = input("Enter a new due date (YYYY-MM-DD) (press enter to keep it unchanged): ")

            if new_username:
                selected_task['username'] = new_username
            if new_due_date:
                try:
                    selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                except ValueError:
                    print("Invalid datetime format. The due date remains unchanged.")

            write_tasks(task_list)
            print("Task edited successfully.")
    else:
        print("Invalid option. Returning to the main menu.")

'''Function takes 'current_user' parameter. 
    Checks if 'current_user' is not 'admin'.
    If so, prints relevant message and returns early without displaying statistics.'''

'''def display_statistics(current_user):
    if current_user != 'admin':
        print("Only the 'admin' user can view statistics.")
        return

    num_users = len(username_password)
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")'''

def generate_reports():
    # Calculating task statistics.
    total_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < date.today())

    # Calculate percentages.
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Create task report string.
    task_report = f"Task Overview:\n" \
                  f"Total tasks: {total_tasks}\n" \
                  f"Completed tasks: {completed_tasks}\n" \
                  f"Uncompleted tasks: {uncompleted_tasks}\n" \
                  f"Overdue tasks: {overdue_tasks}\n" \
                  f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n" \
                  f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n"

    # Write task report to file.
    with open("task_overview.txt", "w") as task_file:
        task_file.write(task_report)

    # Create user report string.
    user_report = f"User Overview:\n" \
                  f"Total users: {len(username_password)}\n" \
                  f"Total tasks: {total_tasks}\n"

    # Generate user-specific statistics.
    for username in username_password.keys():
        user_tasks = [t for t in task_list if t['username'] == username]
        user_total_tasks = len(user_tasks)
        user_completed_tasks = sum(t['completed'] for t in user_tasks)
        user_uncompleted_tasks = user_total_tasks - user_completed_tasks
        user_overdue_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < date.today())

        # Calculate percentages for the specific users.
        user_task_percentage = (user_total_tasks / total_tasks) * 100
        user_completed_percentage = (user_completed_tasks / user_total_tasks) * 100
        user_uncompleted_percentage = (user_uncompleted_tasks / user_total_tasks) * 100
        user_overdue_percentage = (user_overdue_tasks / user_total_tasks) * 100

        # Append user statistics to the report string.
        user_report += f"\nUser: {username}\n" \
                       f"Total tasks assigned: {user_total_tasks}\n" \
                       f"Percentage of total tasks assigned: {user_task_percentage:.2f}%\n" \
                       f"Percentage of completed tasks: {user_completed_percentage:.2f}%\n" \
                       f"Percentage of tasks to be completed: {user_uncompleted_percentage:.2f}%\n" \
                       f"Percentage of overdue tasks: {user_overdue_percentage:.2f}%\n"

    # Write user report to file.
    with open("user_overview.txt", "w") as user_file:
        user_file.write(user_report)

    print("Reports generated successfully.")

def display_statistics(current_user):
    if current_user != 'admin':
        print("Only the admin user can view statistics.")
        return
    try:
        with open("task_overview.txt", "r") as task_file:
            task_report = task_file.read()
            print("")
            print(task_report)

        with open("user_overview.txt", "r") as user_file:
            user_report = user_file.read()
            print("")
            print(user_report)

    except FileNotFoundError:
        print("Reports not found. Generating reports...")
        generate_reports()
        display_reports()

def login():
    logged_in = False

    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        if curr_user not in username_password:
            print("User does not exist.")
        elif username_password[curr_user] != curr_pass:
            print("Wrong password.")
        else:
            print("Login Successful!")
            logged_in = True

    return curr_user

# Main program execution
username_password = {}

if os.path.exists("user.txt"):
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")
        username_password = dict(user.split(';') for user in user_data if user != "")

task_list = read_tasks()

logged_in_user = login()

while True:
    print()
    menu = input('''Select one of the following options below:
r  - Register a user
a  - Add a task
va - View all tasks
vm - View my tasks
ds - Display statistics
gr - Generate reports
e  - Exit
: ''').lower()

    if menu == 'r':
        register_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all_tasks()
    elif menu == 'vm':
        view_my_tasks(logged_in_user)
    elif menu == 'ds':
        # display_statistics functions is called with logged_in_user passed as argument.
        # ensures that only user 'admin' can view statistics.
        display_statistics(logged_in_user)
    elif menu == 'gr':
        generate_reports()
    elif menu == 'e':
        break
    else:
        print("Invalid option. Please choose again.")