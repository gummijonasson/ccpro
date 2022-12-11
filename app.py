from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gudmundurmj:gudmundur@localhost/project_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@pdb.cdxlgoybrmsi.us-east-1.rds.amazonaws.com/project_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"

db = SQLAlchemy(app)

class Student(db.Model):
    auto_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    uni = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique = True)

    def __init__(self, uni, first_name, last_name, email):
        self.uni = uni
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

@app.route("/")
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add/', methods =['POST'])
def insert_book():
    if request.method == "POST":
        student = Student(
            uni = request.form.get('uni'),
            first_name = request.form.get('first_name'),
            last_name = request.form.get('last_name'),
            email = request.form.get('email')
        )
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Student.query.get(request.form.get('auto_id'))

        my_data.uni = request.form['uni']
        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.email = request.form['email']

        db.session.commit()
        flash("Student is updated")
        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(auto_id):
    my_data = Student.query.get(auto_id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student is deleted")
    return redirect(url_for('index'))


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0')
    #host='0.0.0.0'