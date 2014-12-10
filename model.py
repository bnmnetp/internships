from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os.path

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{0}/test.db'.format(os.path.abspath(os.path.dirname(__file__)))
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    grad_year =  db.Column(db.Integer)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    
    def __init__(self,student_id, grad_year, fname, lname):
        """docstring for __init__"""
        self.student_id = student_id
        self.grad_year = grad_year
        self.first_name = fname
        self.last_name = lname



class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    addr_number = db.Column(db.Integer)
    street = db.Column(db.String)
    city = db.Column(db.String)
    db.latitude = db.Column(db.Float)
    db.longitude = db.Column(db.Float)
    students = db.relationship('Internship',backref='course')
    
    def __init__(self,name):
        self.name = name

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))    
    start_date = db.Column(db.Date)
    contact_name = db.Column(db.String)
    contact_email = db.Column(db.String)
    description = db.Column(db.String)
    student = db.relationship('Student',backref='student_internships')
    
    def __init__(self):
        pass

    
@app.route('/initdb')
def initdb():
    db.create_all()
    return os.path.abspath(os.path.dirname(__file__))
    
if __name__ == '__main__':
    app.run()
    
# conn = sqlite3.connect("internapp.db")
#
# curs = conn.cursor()
#
# curs.execute('''drop table student''')
# curs.execute('''create table student (
#                 student_id int primary key,
#                 grad_year int,
#                 first_name text,
#                 last_name text,
#                 major text,
#                 luther_user text );''' )
#
# curs.execute('''insert into student values (123,1986,'brad','miller','CS','millbr02')''')
# curs.execute('''insert into student values (456,2012,'jane','miller','CS','millja03')''')
# curs.execute('''insert into student values (789,2015,'john','smith','MUS','smitjo12')''')
# curs.execute('''insert into student values (321,2014,'libby','larson','CS','larsli02')''')
# curs.execute('''insert into student values (654,2000,'arsene','wenger','PE','wengar01')''')
# conn.commit()
#
#
# rows = curs.execute('''select first_name,grad_year from student where major='CS' or major='PE' order by grad_year desc''')
#
# for row in rows:
#     print(row)
