import datetime

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

while True:
    # This block code present the menu options to the user and convert their input to lowercase.
    menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
s - statistics
e - exit
: ''').lower()

    if menu == 'r':
        # This block code allow only the admin user to register new users.
        if username == "admin":
            new_username = input("Please enter a new username: ")
            new_password = input("Please create a password: ")
            confirm_password = input("Please confirm your password: ")
            if new_password == confirm_password:
                with open("user.txt", "a") as user_file:
                    user_file.write(f"\n{new_username}, {new_password}")
                print("User has been successfully added.")
            else:
                print("Passwords do not match")
        else:
            print("Only an Admin user can register a new user.")

    elif menu == 'a':
        # This block code gather task details from the user.
        username = input("Enter the username of the person you want to assign the task to: ")
        title = input("Please enter the title of the task: ")
        description = input("Please enter the description of the task: ")
        current_date = datetime.date.today()
        due_date = input("Please enter the due date using this format YYYY/MM/DD: ")
        completed = input("Is the task completed? (Yes/No): ")

        # This block code append the task details to the "tasks.txt" file.
        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"\n{username}, {title}, {description},\
                              {current_date}, {due_date}, {completed}")
            print("New task added successfully.")

    elif menu == 'va':
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

    elif menu == 'vm':
        # This block code display tasks assigned to the current user.
        with open("tasks.txt", "r") as tasks_file:
            for task_lines in tasks_file:
                assigned_task = task_lines.strip().split(", ")
                if assigned_task[0] == username:
                    print(f"Title:          {assigned_task[1]}")
                    print(f"Description:    {assigned_task[2]}")

    elif menu == 's':
        # This block code calculate and display statistics (total tasks and total users).
        with open("user.txt", "r") as user_file:
            all_users = len(user_file.readlines())

        with open("tasks.txt", "r") as tasks_file:
            total_tasks = len(tasks_file.readlines())

        print(f"Total tasks: {total_tasks}")
        print(f"Total users: {all_users}")
    # This block code exits the running code
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    # Display a messege if user does not enter an input from a menu
    else:
        print("You have entered an invalid input. Please try again")