from flask import Flask, render_template, request, session
from flask_wtf import Form
import flask_wtf
from wtforms.widgets import HiddenInput
from wtforms.ext.sqlalchemy.orm import model_form
from flask.ext.sqlalchemy import SQLAlchemy
import os.path

app = Flask(__name__)
app.debug = True
app.secret_key = 'luthercollege'
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
    state = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    students = db.relationship('Internship',backref='company')
    
    def __init__(self,name='test'):
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
    db.drop_all()
    db.create_all()
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/newcompany', methods=('POST','GET'))
def newcompany():
    MyForm = model_form(Company,base_class=Form,
                 db_session=db.session,
                 field_args={'longitude': {'widget': HiddenInput()},
                             'latitude': {'widget': HiddenInput()}}
                 )
    form = MyForm()
    if form.validate_on_submit():
        c = Company()
        form.populate_obj(c)
        # todo: obtain latitude longitude information
        # see: geolocation-python 0.1.3
        db.session.add(c)
        db.session.commit()
        return "success"
    else:
        return render_template('newcompany.html',form=form)
    
if __name__ == '__main__':
    app.run()

