import datetime
import os

# Initialize an empty dictionary to store login details.
login_details = {}

# This block code read user data from the "user.txt" file and populate the login_details dictionary.
with open("user.txt", "r") as user_file:
    for user_line in user_file:
        username, password = user_line.strip().split(", ")
        login_details[username] = password

while True:
    # This block code prompt the user for their username and password.
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    # This block code check if the entered username and password match the stored login details.
    if login_details.get(username) == password:
        print(f"Welcome, {username}")
        break
    else:
        print("Invalid login credentials. Please try again.")


def reg_user(login_details):
    new_username = input("Please enter a new username: ")
    # Check if the username already exists.
    if new_username in login_details:
        print("This username already exists.")
        return reg_user(login_details)
    
    new_password = input("Please create a password: ")
    confirm_password = input("Please confirm your password: ")
    if new_password == confirm_password:
        with open("user.txt", "a") as user_file:
            user_file.write(f"\n{new_username}, {new_password}")
        # Update the login_details dictionary
        login_details[new_password] = new_password
        print("User has been successfully added.")
    else:
        print("Passwords do not match. Please try again.")
        return reg_user(login_details)


from datetime import date


def add_task():
    # Add a new task to the selected user
    username = input("Enter the username of the person you want to assign the task to: ")
    title = input("Please enter the title of the task: ")
    description = input("Please enter the description of the task: ")
    current_date = date.today()
    due_date = input("Please enter the due date using this format YYYY/MM/DD: ")
    completed = input("Is the task completed? (Yes/No): ")

    with open("tasks.txt", "a") as tasks_file:
        tasks_file.write(f"\n{username}, {title}, {description},\
                              {current_date}, {due_date}, {completed}")
        print("New task added successfully.") 
        

def view_all():
    # This block code display all tasks from the "tasks.txt" file.
    with open("tasks.txt", "r") as tasks_file:
        for task_lines in tasks_file:
            username, title, description, assigned_date, due_date,\
                      completed = task_lines.strip().split(", ")
            print(f"Task:           {title}")
            print(f"Assigned to:    {username}")
            print(f"Date Assigned:  {assigned_date}")
            print(f"Due date:       {due_date}")
            print(f"Task Complete?  {completed}")
            print(f"Description:    {description}")


def view_my_tasks(username):
    # Read tasks from the file.
    tasks = []
    with open("tasks.txt", "r") as tasks_file:
        tasks = [task_line.strip().split(", ") for task_line in tasks_file]

    # Filter tasks for the given username
    user_tasks = [task for task in tasks if task[0] == username]
    for index, task in enumerate(user_tasks, start=1):
        print(f"{index}. Task: {task[1]} - Due Date: {task[4]} - Completed: {task[5]}")

    # Ask user to select a task.
    task_number = int(input("Enter the number of the task you want to select or -1 to return to main menu"))
    if task_number == -1:
        return
    elif 1 <= task_number <= len(user_tasks):
        selected_task = user_tasks[task_number - 1]
        action = input("Enter c to mark as complete or e to edit task: ").lower()
        if action == 'c':
            # Mark task as completed
            selected_task[5] = "Yes"
            update_tasks_file(tasks)
            print("Task marked as completed.")
        elif action == 'e' and selected_task[5] == "No":
            # Edit task details
            new_username = input("Enter new username for the task: ")
            new_due_date = input("Enter new due date for the task YYYY/MM/DD: ")
            selected_task[0] = new_username
            selected_task[4] = new_due_date
            update_tasks_file(tasks)
            print("Task updated.")
        else:
            print("Invalid input or task already completed.")
    else:
        print("Invalid task number.")


def update_tasks_file(tasks):
    # Write updated tasks back to the file
    with open("tasks.txt", "w") as tasks_file:
        for task in tasks:
            tasks_file.write(", ".join(task) + "\n")


from datetime import datetime


def date_format(date_sting):
    # Convert date string to datetime object
    for format in ("%Y-%m-%d", "%d %b %Y"):
        try:
            return datetime.strptime(date_sting, format)
        except ValueError:
            continue
    raise ValueError(f"{date_sting} does not match the expected format")


def generate_reports():
    # Read tasks and calculate statistics
    with open("tasks.txt", "r") as tasks_file:
        tasks = [task.strip().split(", ") for task in tasks_file]
        total_tasks = len(tasks)
        completed_task = sum(1 for task in tasks if task[5] == "Yes")
        uncompleted_tasks = total_tasks - completed_task
        overdue_tasks = sum(
            1 for task in tasks if task[5] == "No" and date_format(task[4]) < datetime.now())
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Write on task_overview.txt
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(f"Total tasks: {total_tasks}\n")
        task_overview.write(f"Completed tasks: {completed_task}\n")
        task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview.write(f"Incomplete percentage: {incomplete_percentage:.2f}%\n")
        task_overview.write(f"Overdue percentage: {overdue_percentage:.2f}%")

    # Read users and calculate statistics
    with open("user.txt", "r") as user_file:
        users = [user.strip().split(", ") for user in user_file]
        total_users = len(users)

    # Write on user_overview.txt
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(f"Total users: {total_users}\n")
        user_overview.write(f"Total tasks: {total_tasks}\n")

        for user in users:
            user_tasks = sum(1 for task in tasks if task[0] == user[0])
            completed_user_tasks = sum(
                1 for task in tasks if task[0] == user[0] and task[5] == "Yes")
            incomplete_user_task = user_tasks - completed_user_tasks
            overdue_user_tasks = sum(
                1 for task in tasks if task[0] == user[0] and task[5] == "No" and date_format(task[4]) < datetime.now())
            user_overview.write(f"\nUser: {user[0]}\n")
            user_overview.write(f"Assigned tasks: {user_tasks}\n")
            user_overview.write(
                f"Completed tasks: {completed_user_tasks} ({(completed_user_tasks / total_tasks) * 100:.2f}%)\n")
            user_overview.write(
                f"Incomplete tasks: {incomplete_user_task} ({(incomplete_user_task / total_tasks) * 100:.2f}%)\n")
            user_overview.write(
                f"Overdue tasks: {overdue_user_tasks} ({(overdue_user_tasks / total_tasks) * 100:.2f}%)\n")
            
    print("Reports generated successfully.")


def display_statistics():
    # Check if report files exist and generate them if they do not.
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    # Read and display task overview
    with open("task_overview.txt", "r") as task_overview:
        print("\nTask Overview:")
        print(task_overview.read())

    # Read and display user overview
    with open("user_overview.txt", "r") as user_overview:
        print("\nUser Overview:")
        print(user_overview.read())


while True:
    # This block code present the menu options to the user and convert their input to lowercase.
    menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr = generate reports
ds - statistics
e - exit
: ''').lower()
    # Call functions based on user selection from menu.
    if menu == 'r':
        reg_user(login_details)
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_my_tasks(username)
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds' and username == "admin":
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have entered an invalid input. Please try again")
