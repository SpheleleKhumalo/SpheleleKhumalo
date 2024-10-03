import sqlite3
import json
import xml.etree.ElementTree as et

try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()


def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False


# store data on a json file
def store_data_as_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Store data on an xml file
def store_data_as_xml(data, filename):
    root = et.SubElement("data")
    for row in data:
        entry = et.SubElement(root, "entry")
        for i, field in enumerate(row):
            et.SubElement(entry, f"field{i}").text = str(field)
    tree = et.ElementTree(root)
    tree.write(filename)


def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
            elif ext == 'json':
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")


usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        sql_query = (f"SELECT c.course_name 
                     FROM Course c 
                     INNER JOIN StudentCourse sc ON c.course_code = sc.course_code 
                     WHERE sc.student_id = {student_id}")
        cur.execute(sql_query)
        subjects = cur.fetchall()
        print(f"Subjects for student {student_id}:")
        for subject in subjects:
            print(subject[0])
        offer_to_store(subjects)

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        sql_query = (f"SELECT a.street, a.city 
                     FROM Address a 
                     INNER JOIN Student s ON a.address_id = s.address_id 
                     WHERE s.first_name = %s AND s.last_name = %s") 
        cur.execute(sql_query, (firstname, surname))
        address = cur.fetchall()
        print(f"Address for {firstname} {surname}")
        print(address[0][0], address[0][1])
        offer_to_store(address)
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        sql_query = (f"SELECT r.review_text, r.completeness, r.efficiency, r.style, r.documentation 
                     FROM Review r 
                     INNER JOIN StudentCourse sc ON r.student_id = sc.student_id 
                     WHERE sc.student_id = {student_id}")
        cur.execute(sql_query)
        reviews = cur.fetchall()
        print(f"Reviews for student {student_id}")
        for review in reviews:
            print(f"Scores: {review[:4]}")
            print(f"Review text: {review[4]}")
        offer_to_store(reviews)
    
    elif command == 'lc':# list all courses taken by teacher_id
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        sql_query = (f"SELECT c.course_name 
                     FROM Course c 
                     INNER JOIN Teacher t ON c.teacher_id = t.teacher_id 
                     WHERE t.teacher_id = {teacher_id}")
        cur.execute(sql_query)
        courses = cur.fetchall()
        print(f"Courses tought by teacher {teacher_id}")
        for course in courses:
            print(course[0])
        offer_to_store(courses)
    
    elif command == 'lnc':# list all students who haven't completed their course
        sql_query = '''
        SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name 
        FROM Student s 
        LEFT OUTER JOIN StudentCourse sc ON s.student_id = sc.student_id 
        WHERE sc.is_complete = 0'''
        cur.execute(sql_query) 
        incomplete_students = cur.fetchall()
        print("Students who are yet to complete their course.")
        for student in incomplete_students:
            print(student)
        offer_to_store(incomplete_students)
        
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
        sql_query = '''
        SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name, sc.marks 
        FROM Student s 
        INNER JOIN StudentCourse sc ON s.student_id = sc.student_id 
        WHERE sc.marks <=30 AND sc.is_complete = 1'''
        cur.execute(sql_query)
        low_marks_students = cur.fetchall()
        print("Students with low marks:")
        for student in low_marks_students:
            print(student)
        offer_to_store(low_marks_students)
    
    elif command == 'e':# list address by name and surname
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")
    

    
