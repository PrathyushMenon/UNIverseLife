# UNIverseLife

UNIverseLife is a Flask-based web application designed to manage student marks, achievements, and to-do tasks. It includes user registration, authentication, and secure password storage.

## Features

- User Registration and Authentication
- Add and View Student Marks
- View Specific Subject Marks for Students
- Delete Student Marks
- View Achievements
- To-Do List Management

## Setup Instructions

### Prerequisites

- Python 3.x
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/PrathyushMenon/UNIverseLife.git
    cd UNIverseLife
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:

    ```bash
    flask shell
    from app import db
    db.create_all()
    exit()
    ```

5. **Run the application**:

    ```bash
    flask run
    ```

## Application Structure

- `app.py`: The main application file containing all routes and logic.
- `templates/`: Folder containing HTML templates for different pages.
- `static/`: Folder for static files like CSS and JavaScript.

## Endpoints

### User Authentication

- **Register**: `/register`
- **Login**: `/login`
- **Logout**: `/logout`

### Marks Management

- **Home**: `/`
- **Index**: `/index`
- **Add Marks**: `/marks`
- **View Marks**: `/view_marks`
- **View Subject Marks**: `/subject_marks/<int:student_id>/<string:subject>`
- **Delete Marks**: `/delete_marks/<int:student_id>`

### Achievements

- **Achievements**: `/achievements`

### To-Do List

- **To-Do List**: `/todo`
- **Delete Task**: `/delete_task/<int:task_id>`

## Usage

### User Registration

1. Navigate to the registration page at `/register`.
2. Enter a unique username and password to register.

### User Login

1. Navigate to the login page at `/login`.
2. Enter your registered username and password to log in.

### Add Student Marks

1. Navigate to the marks page at `/marks`.
2. Fill in the student name and their marks in various subjects.
3. Submit the form to add the marks.

### View Student Marks

1. Navigate to the view marks page at `/view_marks` to see all students' marks.
2. Use `/subject_marks/<int:student_id>/<string:subject>` to view marks for a specific subject.

### Delete Student Marks

1. Use `/delete_marks/<int:student_id>` to delete marks for a specific student.

### View Achievements

1. Navigate to the achievements page at `/achievements` to see the list of achievements.

### To-Do List Management

1. Navigate to the to-do list page at `/todo`.
2. Add a task by filling in the form.
3. View all tasks on the same page.
4. Delete a task by using the delete task endpoint.

## Security

- Passwords are hashed using `werkzeug.security.generate_password_hash` before storing in the database.
- Flask-Login is used for user session management.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Flask-SQLAlchemy: [https://flask-sqlalchemy.palletsprojects.com/](https://flask-sqlalchemy.palletsprojects.com/)
- Flask-Login: [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)
