from flask import Flask, render_template, request,redirect, url_for,flash
#from flask_mysql_connector import MySQL
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
import mysql.connector
#from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key="BLUE"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "app"
app.config['MYSQL_PORT'] = '3330'

#db = mysql(app)
db_connect = mysql.connector.connect(
        host=app.config['MYSQL_HOST'] ,
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port = app.config['MYSQL_PORT']
    )
cursor = db_connect.cursor(app)

#cursor= mysql.cursor()


    
'''@app.route("/")

def base():
   return render_template("base.html")

@app.route("/sign-in")
def signin():
    return render_template("sign-in.html")
    

    

@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")    
'''

@app.route("/")
def home():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM student")
    student = cursor.fetchall()
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.close()
    return render_template("index.html",student=student,course=course,college=college)

@app.route("/student")
def student():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.close()
    return render_template("student.html",course=course,college=college)

@app.route("/course")
def course():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.close()
    return render_template("course.html",college=college)

@app.route("/college")
def college():
    cursor=db_connect.cursor()
    cursor.close()
    return render_template("college.html")

@app.route("/studentlist")
def studentlist():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM student")
    student = cursor.fetchall()
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.close()
    return render_template("studentlist.html",student=student,course=course,college=college)

@app.route("/courselist")
def courselist():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM student")
    student = cursor.fetchall()
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.close()
    return render_template("courselist.html",student=student,course=course,college=college)

@app.route("/collegelist")
def collegelist():
    cursor=db_connect.cursor()
    cursor.execute("SELECT * FROM student")
    student = cursor.fetchall()
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.execute("SELECT * FROM college")
    college = cursor.fetchall()
    cursor.close()
    return render_template("collegelist.html",student=student,course=course,college=college)

@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        stud_id = request.form['stud_id']
        fname = request.form['fname']
        lname = request.form['lname']
        yearlevel = request.form['yearlevel']
        course = request.form['course']
        gender = request.form['gender']

        # Check if the ID number already exists in the database
        cursor = db_connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM student WHERE stud_id = %s", (stud_id,))
        count = cursor.fetchone()[0]
        cursor.close()

        if count > 0:
            flash('ID number already exists', 'error')
            return redirect(url_for('addstudent'))

        # Insert data into the database
        cursor = db_connect.cursor()
        insert_query = "INSERT INTO student (stud_id, fname, lname, course, gender, yearlevel) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (stud_id, fname, lname, course, gender, yearlevel)

        cursor.execute(insert_query, values)
        db_connect.commit()
        cursor.close()

        # Redirect to a success page or do something else
        return redirect(url_for('studentlist'))

    else:
        # Fetch course data from the database
        cursor = db_connect.cursor()
        cursor.execute("SELECT coursecode, coursename FROM course")
        courses = cursor.fetchall()
        cursor.close()

        return render_template("student.html", courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        # Perform validation here if needed

        cursor = db_connect.cursor()

        # Check if the selected college exists in the 'college' table
        check_college_query = "SELECT collegecode FROM college WHERE collegecode = %s"
        cursor.execute(check_college_query, (college_code,))
        
        # Read and clear any results from the cursor
        cursor.fetchall()

        # If you need to check if a college exists, you can do it here
        if cursor.rowcount == 0:
            # The selected college does not exist; handle the error
            flash("Selected college does not exist. Please choose a valid college.", "error")
        else:
            # If the college exists, proceed with course insertion
            insert_query = "INSERT INTO course (coursecode, coursename, collegecode) VALUES (%s, %s, %s)"
            values = (course_code, course_name, college_code)

            cursor.execute(insert_query, values)
            db_connect.commit()

            flash("Course added successfully!", "success")
            

        cursor.close()

    # Redirect to a specific page (you might want to modify this)
    return redirect(url_for('courselist'))

@app.route('/add college', methods=['GET', 'POST'])
def addcollege():
    if request.method == 'POST':
        # Retrieve form data
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        # Perform validation here
        cursor =db_connect.cursor()

        insert_query = "INSERT INTO college (collegecode, collegename) VALUES (%s, %s)"
        values = (college_code, college_name,)

        cursor.execute(insert_query, values)
        db_connect.commit()
        cursor.close()

        # Redirect to a success page or do something else
        return redirect(url_for('collegelist'))

    # Render the registration form
    return render_template('college.html')

@app.route('/delete_college/<string:id>', methods=['GET'])
def delete_college(id):
    try:
        cursor = db_connect.cursor()
        sql = "DELETE FROM college WHERE collegecode = %s"
        cursor.execute(sql, (id,))
        db_connect.commit()
        cursor.close()
        return redirect(url_for('collegelist'))  # Redirect to the list of colleges
    except Exception as e:
        flash(f"Error deleting college: {str(e)}")
        return redirect(url_for('collegelist'))

        
@app.route('/delete_course/<string:id>', methods=['GET'])
def delete_course(id):
    try:
        cursor = db_connect.cursor()
        sql = "DELETE FROM course WHERE coursecode = %s"
        cursor.execute(sql, (id,))
        db_connect.commit()
        cursor.close()
        return redirect(url_for('courselist'))  # Redirect to the list of courses
    except Exception as e:
        flash(f"Error deleting course: {str(e)}")
        return redirect(url_for('courselist'))

@app.route('/delete_student/<string:id>', methods=['GET'])
def delete_student(id):
    try:
        cursor = db_connect.cursor()
        sql = "DELETE FROM student WHERE stud_id = %s"
        cursor.execute(sql, (id,))
        db_connect.commit()
        cursor.close()
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"Error deleting student: {str(e)}")
        return redirect(url_for('home'))
    
@app.route('/edit_student/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        # Handle the form submission to update the student record
        new_fname = request.form['new_fname']
        new_lname = request.form['new_lname']
        new_course = request.form['new_course']
        new_yearlevel = request.form['new_yearlevel']
        new_gender = request.form['new_gender']

        try:
            cursor = db_connect.cursor()
            sql = "UPDATE student SET fname = %s, lname = %s, course = %s, yearlevel = %s, gender = %s WHERE stud_id = %s"
            cursor.execute(sql, (new_fname, new_lname, new_course, new_yearlevel, new_gender, id))
            db_connect.commit()
            cursor.close()
            flash("Student record updated successfully", "success")
        except Exception as e:
            flash(f"Error updating student record: {str(e)}", "error")
        return redirect(url_for('home'))

    else:
        # Fetch the existing student record based on the given ID
        try:
            cursor = db_connect.cursor()
            cursor.execute("SELECT * FROM student WHERE stud_id = %s", (id,))
            student = cursor.fetchone()
            cursor.execute("SELECT * FROM course")
            course= cursor.fetchall()
            cursor.close()
            if student:
                return render_template("editstudent.html", student=student,course=course)
            else:
                flash("Student not found", "error")
                return redirect(url_for('home'))
        except Exception as e:
            flash(f"Error retrieving student record: {str(e)}", "error")
            return redirect(url_for('home'))

@app.route('/edit_course/<string:id>', methods=['GET', 'POST'])
def edit_course(id):
    if request.method == 'POST':
        # Handle the form submission to update the course
        new_course_name = request.form['new_course_name']
        new_course_code = request.form['new_course_code']  # Add new_course_code

        try:
            cursor = db_connect.cursor()
            sql = "UPDATE course SET coursename = %s, coursecode = %s WHERE coursecode = %s"  # Include coursecode
            cursor.execute(sql, (new_course_name, new_course_code, id))
            db_connect.commit()
            cursor.close()
            flash("Course updated successfully", "success")
        except Exception as e:
            flash(f"Error updating course: {str(e)}", "error")
        return redirect(url_for('courselist'))  # Redirect to courselist

    else:
        # Fetch the existing course based on the given ID
        try:
            cursor = db_connect.cursor()
            cursor.execute("SELECT * FROM course WHERE coursecode = %s", (id,))
            course = cursor.fetchone()
            cursor.close()
            if course:
                return render_template("editcourse.html", course=course)
            else:
                flash("Course not found", "error")
                return redirect(url_for('courselist'))
        except Exception as e:
            flash(f"Error retrieving course: {str(e)}", "error")
            return redirect(url_for('courselist'))



@app.route('/edit_college/<string:id>', methods=['GET', 'POST'])
def edit_college(id):
    if request.method == 'POST':
        # Handle the form submission to update the college
        new_college_name = request.form['new_college_name']
        new_college_code = request.form['new_college_code']

        try:
            cursor = db_connect.cursor()
            sql = "UPDATE college SET collegename = %s, collegecode = %s WHERE collegecode = %s"
            cursor.execute(sql, (new_college_name, new_college_code, id))
            db_connect.commit()
            cursor.close()
            flash("College updated successfully", "success")
        except Exception as e:
            flash(f"Error updating college: {str(e)}", "error")
        return redirect(url_for('collegelist'))

    else:
        # Fetch the existing college based on the given ID
        try:
            cursor = db_connect.cursor()
            cursor.execute("SELECT * FROM college WHERE collegecode = %s", (id,))
            college = cursor.fetchone()
            cursor.close()
            if college:
                return render_template("editcollege.html", college=college)
            else:
                flash("College not found", "error")
                #return redirect(url_for('home'))
        except Exception as e:
            flash(f"Error retrieving college: {str(e)}", "error")
            return redirect(url_for('collegelist'))

