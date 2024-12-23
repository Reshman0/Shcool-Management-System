from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# PostgreSQL connection
def reset_connection():
    global conn
    try:
        conn.close()
    except psycopg2.Error:
        pass
    conn = psycopg2.connect(
        host="localhost",
        database="school_db",
        user="postgres",
        password="31"  # PostgreSQL password
    )

conn = psycopg2.connect(
    host="localhost",
    database="school_db",
    user="postgres",
    password="31"
)

@app.route('/')
def home():
    return render_template('index.html')

# Students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        cur.close()
        return render_template('students.html', students=students)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            data = request.form
            cur = conn.cursor()
            cur.execute("SELECT roll_no FROM student WHERE roll_no LIKE 'ROLL_%' ORDER BY LENGTH(roll_no) DESC, roll_no DESC LIMIT 1")
            max_roll_no = cur.fetchone()
            if max_roll_no and max_roll_no[0]:
                max_roll_number = int(max_roll_no[0].split('_')[1])
                new_roll_no = f"ROLL_{max_roll_number + 1}"
            else:
                new_roll_no = "ROLL_201"

            cur.execute(
                "INSERT INTO student (name, roll_no, section, class_id, photo) VALUES (%s, %s, %s, %s, %s)",
                (data['name'], new_roll_no, data['section'], data['class_id'], data['photo'])
            )
            conn.commit()
            cur.close()
            return "Student added successfully! <a href='/students'>Back to Students</a>"
        except psycopg2.Error as e:
            conn.rollback()
            return f"An error occurred: {e}"

    try:
        cur = conn.cursor()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        sections = ['A', 'B', 'C', 'D']  # Fixed section list
        cur.close()
        return render_template('add_student.html', classes=classes, sections=sections)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    try:
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute(
                "UPDATE student SET name = %s, roll_no = %s, section = %s, class_id = %s, photo = %s WHERE student_id = %s",
                (data['name'], data['roll_no'], data['section'], data['class_id'], data['photo'], student_id)
            )
            conn.commit()
            cur.close()
            return "Student updated successfully! <a href='/students'>Back to Students</a>"

        cur.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        student = cur.fetchone()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        sections = ['A', 'B', 'C', 'D']
        cur.close()
        return render_template('edit_student.html', student=student, classes=classes, sections=sections)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM class_student WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        conn.commit()
        cur.close()
        return "Student deleted successfully! <a href='/students'>Back to Students</a>"
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

# Teachers
@app.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM teacher")
        teachers = cur.fetchall()
        cur.close()
        return render_template('teachers.html', teachers=teachers)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        try:
            data = request.form
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO teacher (name, subject_id, class_id, photo) VALUES (%s, %s, %s, %s)",
                (data['name'], data['subject_id'], data['class_id'], data['photo'])
            )
            conn.commit()
            cur.close()
            return "Teacher added successfully! <a href='/teachers'>Back to Teachers</a>"
        except psycopg2.Error as e:
            conn.rollback()
            return f"An error occurred: {e}"

    try:
        cur = conn.cursor()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        cur.execute("SELECT subject_id, name FROM subject")
        subjects = cur.fetchall()
        cur.close()
        return render_template('add_teacher.html', classes=classes, subjects=subjects)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    try:
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute(
                "UPDATE teacher SET name = %s, subject_id = %s, class_id = %s, photo = %s WHERE teacher_id = %s",
                (data['name'], data['subject_id'], data['class_id'], data['photo'], teacher_id)
            )
            conn.commit()
            cur.close()
            return "Teacher updated successfully! <a href='/teachers'>Back to Teachers</a>"

        cur.execute("SELECT * FROM teacher WHERE teacher_id = %s", (teacher_id,))
        teacher = cur.fetchone()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        cur.execute("SELECT subject_id, name FROM subject")
        subjects = cur.fetchall()
        cur.close()
        return render_template('edit_teacher.html', teacher=teacher, classes=classes, subjects=subjects)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/delete_teacher/<int:teacher_id>', methods=['GET'])
def delete_teacher(teacher_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM teacher WHERE teacher_id = %s", (teacher_id,))
        conn.commit()
        cur.close()
        return "Teacher deleted successfully! <a href='/teachers'>Back to Teachers</a>"
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

# Classes
@app.route('/classes', methods=['GET'])
def get_classes():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM class")
        classes = cur.fetchall()
        cur.close()
        return render_template('classes.html', classes=classes)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        try:
            data = request.form
            cur = conn.cursor()
            cur.execute("INSERT INTO class (class_name) VALUES (%s)", (data['class_name'],))
            conn.commit()
            cur.close()
            return "Class added successfully! <a href='/classes'>Back to Classes</a>"
        except psycopg2.Error as e:
            conn.rollback()
            return f"An error occurred: {e}"
    return render_template('add_class.html')

@app.route('/edit_class/<int:class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    try:
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE class SET class_name = %s WHERE class_id = %s", (data['class_name'], class_id))
            conn.commit()
            cur.close()
            return "Class updated successfully! <a href='/classes'>Back to Classes</a>"

        cur.execute("SELECT * FROM class WHERE class_id = %s", (class_id,))
        class_data = cur.fetchone()
        cur.close()
        return render_template('edit_class.html', class_data=class_data)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/delete_class/<int:class_id>', methods=['GET'])
def delete_class(class_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM class WHERE class_id = %s", (class_id,))
        conn.commit()
        cur.close()
        return "Class deleted successfully! <a href='/classes'>Back to Classes</a>"
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

# Subjects
@app.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM subject")
        subjects = cur.fetchall()
        cur.close()
        return render_template('subjects.html', subjects=subjects)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        try:
            data = request.form
            cur = conn.cursor()
            cur.execute("INSERT INTO subject (name, class_id) VALUES (%s, %s)", (data['name'], data['class_id']))
            conn.commit()
            cur.close()
            return "Subject added successfully! <a href='/subjects'>Back to Subjects</a>"
        except psycopg2.Error as e:
            conn.rollback()
            return f"An error occurred: {e}"

    try:
        cur = conn.cursor()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        cur.close()
        return render_template('add_subject.html', classes=classes)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    try:
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute(
                "UPDATE subject SET name = %s, class_id = %s, teacher_id = %s WHERE subject_id = %s",
                (data['name'], data['class_id'], data['teacher_id'], subject_id)
            )
            conn.commit()
            cur.close()
            return "Subject updated successfully! <a href='/subjects'>Back to Subjects</a>"

        # Mevcut subject bilgilerini al
        cur.execute("SELECT * FROM subject WHERE subject_id = %s", (subject_id,))
        subject = cur.fetchone()

        # Sınıf bilgilerini al
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()

        # Öğretmen bilgilerini al
        cur.execute("SELECT teacher_id, name FROM teacher")
        teachers = cur.fetchall()

        cur.close()
        return render_template('edit_subject.html', subject=subject, classes=classes, teachers=teachers)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"


@app.route('/delete_subject/<int:subject_id>', methods=['GET'])
def delete_subject(subject_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM subject WHERE subject_id = %s", (subject_id,))
        conn.commit()
        cur.close()
        return "Subject deleted successfully! <a href='/subjects'>Back to Subjects</a>"
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

# Rooms
@app.route('/rooms', methods=['GET'])
def get_rooms():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT room.room_id, room.room_number, room.capacity, class.class_name
            FROM room
            LEFT JOIN class ON room.assigned_class = class.class_id
        """)
        rooms = cur.fetchall()
        cur.close()
        return render_template('rooms.html', rooms=rooms)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        try:
            data = request.form
            cur = conn.cursor()
            cur.execute("INSERT INTO room (room_number, capacity, assigned_class) VALUES (%s, %s, %s)", 
                        (data['room_number'], data['capacity'], data['assigned_class']))
            conn.commit()
            cur.close()
            return "Room added successfully! <a href='/rooms'>Back to Rooms</a>"
        except psycopg2.Error as e:
            conn.rollback()
            return f"An error occurred: {e}"

    try:
        cur = conn.cursor()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        cur.close()
        return render_template('add_room.html', classes=classes)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    try:
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute(
                "UPDATE room SET room_number = %s, capacity = %s, assigned_class = %s WHERE room_id = %s",
                (data['room_number'], data['capacity'], data['assigned_class'], room_id)
            )
            conn.commit()
            cur.close()
            return "Room updated successfully! <a href='/rooms'>Back to Rooms</a>"

        cur.execute("SELECT * FROM room WHERE room_id = %s", (room_id,))
        room = cur.fetchone()
        cur.execute("SELECT class_id, class_name FROM class")
        classes = cur.fetchall()
        cur.close()
        return render_template('edit_room.html', room=room, classes=classes)
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

@app.route('/delete_room/<int:room_id>', methods=['GET'])
def delete_room(room_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM room WHERE room_id = %s", (room_id,))
        conn.commit()
        cur.close()
        return "Room deleted successfully! <a href='/rooms'>Back to Rooms</a>"
    except psycopg2.Error as e:
        conn.rollback()
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
