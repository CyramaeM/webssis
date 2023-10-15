import mysql
import mysql.connector as mysql


def database():

    db = mysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="app",
        port = "3330"

    )
    cursor = db.cursor()

    
    create_query_user = """CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        fname VARCHAR(100),
        lname VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(255)
    )"""

    cursor.execute(create_query_user)

    create_query_college = """CREATE TABLE IF NOT EXISTS college(
        collegecode VARCHAR(10) PRIMARY KEY,
        collegename VARCHAR(255)
    )"""

    cursor.execute(create_query_college)

    create_query_course = """CREATE TABLE IF NOT EXISTS course (
        coursecode VARCHAR(255) PRIMARY KEY,
        coursename VARCHAR(255),
        collegecode VARCHAR(10),
        FOREIGN KEY(collegecode) REFERENCES college(collegecode) ON DELETE CASCADE
       
    )"""

    cursor.execute(create_query_course)

    create_query_student = """CREATE TABLE IF NOT EXISTS student(
        stu_id VARCHAR(100) PRIMARY KEY,
        fname VARCHAR(100),
        lname VARCHAR(100),
        gender VARCHAR(10),
        course VARCHAR(100),
        yearlevel VARCHAR (50),
        coursecode VARCHAR(255),
        FOREIGN KEY(coursecode) REFERENCES course(coursecode) ON DELETE CASCADE
    )"""

    cursor.execute(create_query_student)

    
    
    