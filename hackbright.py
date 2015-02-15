import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")    # creates a connection object that represents the database
    DB = CONN.cursor()                         # a cursor allows use to loop over rows in the query. Can call the execute() method on the cursor object to perform SQL commands

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""   # ? is placeholder b/c we're going to use this query several times to get the details of a diff student
    DB.execute(query, (github,))        # executing the query on the cursor. even though only have 1 value to substitute into query, sqlite3 module demands we pack it into a tuple when we do substitution
    row = DB.fetchone()                 # fetch rows out of the table 1 @ a time; returns a row as a tuple containg the values for each of the columns we selected
    
    print "Student: %s %s, Github account: %s""" % (row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    
    CONN.commit()                                          # commit the data to add it to our db
    print "Successfully added student: %s %s" % (first_name, last_name)

def find_project_by_title(title):
    query = """SELECT description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query,(title,))
    row = DB.fetchone()        # select each row, 1 @ a time. W/o this, query won't run
    
    print """Description: %s, Max Grade: %s""" % (row[0], row[1])

def add_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES  (?,?,?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print """\
    Successfully added project with the following information: 
    Title: %s
    Description %s
    Max Grade: %s """ % (title, description, max_grade)

def find_grade(github, project_title):
    query = """ SELECT s.first_name, s.last_name, g.grade, p.max_grade         # first_name, last_name from Students table, grade from grades table and max_grade from project table
                FROM Sudents AS s
                    LEFT JOIN Grades AS g ON (s.github = g.student_github)
                    JOIN Projects AS p ON (g.project_title = p.title);"""
    DB.execute(query, (first_name, last_name))

def main():
    connect_to_db()
    command = None              # initializing command
    while command != "quit":
 
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_info":
            find_project_by_title(*args)
        elif command == "add_project":
            add_project(*args)

    CONN.close()                        # closes the connection to the database 

if __name__ == "__main__":
    main()


"""
Add a Student - w/ COMMAND - DONE
Query for projects by title - CHECK W/HEATHER
Add a project - DONE
Query for a student's grade given a project
Give a grade to a student
Show all the grades for a student
"""