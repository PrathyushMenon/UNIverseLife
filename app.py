from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from flask import jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)   
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_BINDS'] = {
    'marks': 'sqlite:///marks.db',
    'todo': 'sqlite:///todo.db'
}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# appa = Flask(__name__)
# appa.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# appa.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# appa.secret_key = 'your_secret_key_here'
# db1 = SQLAlchemy(appa)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def create_user():
    existing_user = User.query.filter_by(username='adm').first()
    if not existing_user:
        hashed_password = generate_password_hash('pass')
        new_user = User(username='adm', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

class StudentMarks(db.Model):
    __bind_key__ = 'marks'  # Bind this model to the 'marks' database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    math = db.Column(db.Float, nullable=False)
    c = db.Column(db.Float, nullable=False)
    esm = db.Column(db.Float, nullable=False)
    dsa = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(10), nullable=False)

# Initialize the database within an application context
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully!')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        login_user(user)  # Log in the user

        flash('Logged in successfully!')
        return redirect(url_for('index'))  # Redirect to 'base' endpoint

    return render_template('login.html')

@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def bas():
    create_user()
    return redirect(url_for('login'))  # Always redirect to login page



@app.route('/marks', methods=['GET', 'POST'])
@login_required
def marks():
    if request.method == 'POST':
        name = request.form['name']
        math = float(request.form['math'])
        c = float(request.form['c'])
        esm = float(request.form['esm'])
        dsa = float(request.form['dsa'])
        total_marks = math + c + esm + dsa
        result = "PASS" if total_marks >= 35 * 4 else "FAIL"

        new_marks = StudentMarks(name=name, math=math, c=c, esm=esm, dsa=dsa, total_marks=total_marks, result=result)
        db.session.add(new_marks)
        db.session.commit()

        flash(f"Marks submitted for {name}: Total Marks = {total_marks}, Result = {result}")
        return redirect(url_for('marks'))

    return render_template('marks.html')

@app.route('/view_marks')
@login_required
def view_marks():
    # Fetch data from the database and pass it to the template
    students = StudentMarks.query.all()
    return render_template('view_marks.html', students=students)

@app.route('/subject_marks/<int:student_id>/<string:subject>')
@login_required
def subject_marks(student_id, subject):
    student = StudentMarks.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'})

    subject_marks = getattr(student, subject, None)
    if subject_marks is None:
        return jsonify({'error': 'Subject not found'})

    return jsonify({'marks': subject_marks})
@app.route('/delete_marks/<int:student_id>', methods=['DELETE'])
@login_required
def delete_marks(student_id):
    student = StudentMarks.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Marks deleted successfully'}), 200


@app.route('/achievements')
@login_required
def achievements():
    achievements = [
        "Increased school-wide average GPA by 0.1", 
        "Achieved a top 10% ranking in the state", 
        "Award-winning Robotics Club/Debate Team",
        "Implemented a successful anti-bullying program"
    ]
    return render_template('achievements.html', achievements=achievements)

class TodoEntry(db.Model):
    __bind_key__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=False)

# Update the todo() function to handle additional task parameters
@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task = request.form['task']
        priority = request.form.get('priority', 0)
        due_date_str = request.form.get('due_date')
        category = request.form.get('category')
        
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        if task:
            new_task = TodoEntry(task=task, priority=priority, due_date=due_date, category=category)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!")
        return redirect(url_for('todo'))

    tasks = TodoEntry.query.all()
    return render_template('todo.html', tasks=tasks)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = TodoEntry.query.get(task_id)
    if not task:
        flash('Task not found!')
        return redirect(url_for('todo'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('todo'))

# class TodoEntry(db1.Model):
#     id = db1.Column(db1.Integer, primary_key=True)
#     place = db1.Column(db1.String(100), nullable=False)
#     date = db1.Column(db1.Date, nullable=False)
#     review = db1.Column(db1.Text, nullable=False)

# @app.route('/todo', methods=['GET', 'POST'])
# def todo():
#     if request.method == 'POST':
#         place = request.form['place']
#         date = request.form['date']
#         review = request.form['review']
#         new_entry = TodoEntry(place=place, date=date, review=review)
#         db.session.add(new_entry)
#         db.session.commit()
#         return redirect(url_for('todo'))

#     entries = TodoEntry.query.all()
#     return render_template('todo.html', entries=entries)

# Wrap db.create_all() in an application context
with app.app_context():
    db.create_all()    

if __name__ == "__main__":
    app.run(debug=True)
