from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlite3 import *

app = Flask(__name__)
api = Api(app)

base = connect('bases.db', check_same_thread=False)
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

class StudentResource(Resource):
    def get(self, roll_number):
        cr.execute("SELECT * FROM students WHERE roll_number=?", (roll_number,))
        student = cr.fetchone()
        if student:
            return {
                'id': student[0],
                'name': student[1],
                'roll_number': student[2],
                'subject1': student[3],
                'subject2': student[4],
                'subject3': student[5],
                'subject4': student[6],
                'subject5': student[7]
            }
        else:
            return {'message': 'Student not found'}, 404

    def post(self, roll_number):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('subject1', type=int, required=True)
        parser.add_argument('subject2', type=int, required=True)
        parser.add_argument('subject3', type=int, required=True)
        parser.add_argument('subject4', type=int, required=True)
        parser.add_argument('subject5', type=int, required=True)
        args = parser.parse_args()

        name = args['name']
        subject1 = args['subject1']
        subject2 = args['subject2']
        subject3 = args['subject3']
        subject4 = args['subject4']
        subject5 = args['subject5']

        try:
            cr.execute('''INSERT INTO students(name, roll_number, subject1, subject2, subject3, subject4, subject5)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, roll_number, subject1, subject2, subject3, subject4, subject5))
            base.commit()
            return {'message': 'Student created successfully'}
        except IntegrityError:
            return {'message': 'Failed to create student. Roll number already exists'}, 400

api.add_resource(StudentResource, '/students/<int:roll_number>')

if __name__ == '__main__':
    app.run(port="5001", debug=True)
