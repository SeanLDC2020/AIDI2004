import os
from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "mysql+pymysql://root:@localhost:3308/student_records"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Student = Base.classes.students

# class Student(db.Model):
#     student_id = db.Column(db.String(32), primary_key=True)
#     first_name = db.Column(db.String(32))
#     last_name = db.Column(db.String(32))
#     dob = db.Column(db.Date())
#     amount_due = db.Column(db.Float())

#     def __repr__(self):
#         return "<ID: {}>".format(self.student_id)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.form:
        student = Student(
            student_id=request.form.get("student_id"),
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            dob=request.form.get("dob"),
            amount_due=request.form.get("amount_due"))
        db.session.add(student)
        db.session.commit()
        
    students = db.session.query(Student).all()
    return render_template("home.html", students=students)

@app.route("/update", methods=["POST"])
def update():
    student = db.session.query(Student).filter_by(student_id=request.form.get("student_id")).first()
    student.first_name=request.form.get("first_name")
    student.last_name=request.form.get("last_name")
    student.dob=request.form.get("dob")
    student.amount_due=request.form.get("amount_due")
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    student = db.session.query(Student).filter_by(student_id=request.form.get("student_id")).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)