import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "instance" / "campusconnect.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            department TEXT NOT NULL,
            marks REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
                CHECK(status IN ('Active', 'Inactive'))
        );
        """)
        count = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        if count == 0:
            db.executemany(
                """INSERT INTO students(name,email,age,department,marks,status)
                   VALUES(?,?,?,?,?,?)""",
                [
                    ("Ayesha Khan", "ayesha@example.com", 21, "Software Engineering", 88.5, "Active"),
                    ("Hamza Ali", "hamza@example.com", 22, "Computer Science", 76.0, "Active"),
                    ("Sara Ahmed", "sara@example.com", 20, "Information Technology", 91.0, "Inactive"),
                ],
            )

def validate_student(data):
    """Validation function deliberately includes branches for white-box testing."""
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    department = (data.get("department") or "").strip()
    age_raw = data.get("age")
    marks_raw = data.get("marks")
    status = (data.get("status") or "Active").strip()

    if len(name) < 2:
        return False, "Name must contain at least 2 characters."
    if len(name) > 60:
        return False, "Name must not exceed 60 characters."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Enter a valid email address."
    if not department:
        return False, "Department is required."
    try:
        age = int(age_raw)
    except (TypeError, ValueError):
        return False, "Age must be a whole number."
    if age < 16 or age > 100:
        return False, "Age must be between 16 and 100."
    try:
        marks = float(marks_raw)
    except (TypeError, ValueError):
        return False, "Marks must be a number."
    if marks < 0 or marks > 100:
        return False, "Marks must be between 0 and 100."
    if status not in ("Active", "Inactive"):
        return False, "Status must be Active or Inactive."
    return True, {
        "name": name, "email": email, "age": age,
        "department": department, "marks": marks, "status": status
    }

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access the dashboard.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
app.config["JSON_SORT_KEYS"] = False

@app.context_processor
def inject_user():
    return {"logged_in": "user_id" in session, "current_user": session.get("user_name")}

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if len(name) < 2:
            flash("Name must contain at least 2 characters.", "danger")
        elif "@" not in email:
            flash("Enter a valid email address.", "danger")
        elif len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
        else:
            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
                        (name, email, generate_password_hash(password, method="pbkdf2:sha256")),
                    )
                flash("Account created. You can now log in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An account with this email already exists.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    q = (request.args.get("q") or "").strip()
    with get_db() as db:
        if q:
            students = db.execute(
                """SELECT * FROM students
                   WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
                   ORDER BY id DESC""", (f"%{q}%", f"%{q}%", f"%{q}%")
            ).fetchall()
        else:
            students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        stats = {
            "total": db.execute("SELECT COUNT(*) FROM students").fetchone()[0],
            "active": db.execute("SELECT COUNT(*) FROM students WHERE status='Active'").fetchone()[0],
            "inactive": db.execute("SELECT COUNT(*) FROM students WHERE status='Inactive'").fetchone()[0],
        }
    return render_template("dashboard.html", students=students, stats=stats, q=q)

@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        valid, result = validate_student(request.form)
        if not valid:
            flash(result, "danger")
        else:
            try:
                with get_db() as db:
                    db.execute(
                        """INSERT INTO students(name,email,age,department,marks,status)
                           VALUES(:name,:email,:age,:department,:marks,:status)""", result
                    )
                flash("Student added successfully.", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("A student with this email already exists.", "danger")
    return render_template("student_form.html", student=None, page_title="Add Student")

@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    with get_db() as db:
        student = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        valid, result = validate_student(request.form)
        if not valid:
            flash(result, "danger")
        else:
            try:
                with get_db() as db:
                    db.execute(
                        """UPDATE students SET name=:name,email=:email,age=:age,
                           department=:department,marks=:marks,status=:status WHERE id=:id""",
                        {**result, "id": student_id},
                    )
                flash("Student updated successfully.", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("Another student already uses this email.", "danger")
    return render_template("student_form.html", student=student, page_title="Edit Student")

@app.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    with get_db() as db:
        cursor = db.execute("DELETE FROM students WHERE id=?", (student_id,))
    if cursor.rowcount:
        flash("Student deleted successfully.", "success")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for("dashboard"))

# JSON API endpoints for Postman. Intended for local coursework testing.
@app.route("/api/students", methods=["GET", "POST"])
def api_students():
    if request.method == "GET":
        q = (request.args.get("q") or "").strip()
        with get_db() as db:
            rows = db.execute(
                """SELECT * FROM students WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
                   ORDER BY id""", (f"%{q}%", f"%{q}%", f"%{q}%")
            ).fetchall()
        return jsonify([dict(row) for row in rows]), 200

    data = request.get_json(silent=True) or {}
    valid, result = validate_student(data)
    if not valid:
        return jsonify({"error": result}), 400
    try:
        with get_db() as db:
            cur = db.execute(
                """INSERT INTO students(name,email,age,department,marks,status)
                   VALUES(:name,:email,:age,:department,:marks,:status)""", result
            )
            new_id = cur.lastrowid
            row = db.execute("SELECT * FROM students WHERE id=?", (new_id,)).fetchone()
        return jsonify(dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists."}), 409

@app.route("/api/students/<int:student_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def api_student_detail(student_id):
    with get_db() as db:
        existing = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if existing is None:
        return jsonify({"error": "Student not found."}), 404

    if request.method == "GET":
        return jsonify(dict(existing)), 200
    if request.method == "DELETE":
        with get_db() as db:
            db.execute("DELETE FROM students WHERE id=?", (student_id,))
        return jsonify({"message": "Student deleted."}), 200

    data = request.get_json(silent=True) or {}
    merged = dict(existing)
    merged.update(data)
    valid, result = validate_student(merged)
    if not valid:
        return jsonify({"error": result}), 400
    try:
        with get_db() as db:
            db.execute(
                """UPDATE students SET name=:name,email=:email,age=:age,
                   department=:department,marks=:marks,status=:status WHERE id=:id""",
                {**result, "id": student_id},
            )
            row = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        return jsonify(dict(row)), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Another student already uses this email."}), 409

@app.route("/health")
def health():
    return jsonify({"status": "success", "message": "CampusConnect API is running."}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
