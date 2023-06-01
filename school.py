from flask import *
from sqlite3 import *

app = Flask(__name__)  # initiate flask object

base = connect('bas.db', check_same_thread=False)
base.execute('''CREATE TABLE IF NOT EXISTS students
            (id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            roll_number INTEGER NOT NULL UNIQUE,
            subject1 INTEGER NOT NULL,
            subject2 INTEGER NOT NULL,
            subject3 INTEGER NOT NULL,
            subject4 INTEGER NOT NULL,
            subject5 INTEGER NOT NULL);''')
cr = base.cursor()

# CREATE THE HTML PAGE DIRECT
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        roll = request.form['roll_number']
        cr.execute('''SELECT ROLL_NUMBER FROM students
        WHERE ROLL_NUMBER=?''', (roll,))
        var = cr.fetchone()
        if var:
            return render_template('student_page.html')
        else:
            return render_template('student_creation.html')
    return render_template('student_creation.html')

@app.route('/s', methods=['POST'])
def create_student():
    name = request.form['name']
    roll = request.form['roll_number']
    subject1 = int(request.form['subject1'])
    subject2 = int(request.form['subject2'])
    subject3 = int(request.form['subject3'])
    subject4 = int(request.form['subject4'])
    subject5 = int(request.form['subject5'])

    try:
        cr.execute('''INSERT INTO students(name, roll_number, subject1, subject2, subject3, subject4, subject5)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, roll, subject1, subject2, subject3, subject4, subject5))
        base.commit()
        return render_template('student_successful_msg.html')
    except IntegrityError:
        return render_template('student_failed.html')

if __name__ == '__main__':
    app.run(port="5001", debug=True)
