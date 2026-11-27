# CampusConnect – Student Management System

A Flask + SQLite web application prepared for the SE3002 Software Quality Engineering practical assignment.

## Features
- User registration, login and logout
- Student create, read, update and delete (CRUD)
- Search students by name, email or department
- Student status (Active / Inactive)
- Input validation and duplicate-email handling
- JSON REST API for Postman testing
- Health-check endpoint

## Requirements
- Python 3.9+
- pip

## Setup (macOS / Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The SQLite database is created automatically at `instance/campusconnect.db` on first run. Three sample student records are inserted automatically.

## Demo account
1. Open `/register` and create your own account.
2. Log in using that account.
3. The sample student records are already available on the dashboard.

## API endpoints

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/students` | List/search students (`?q=term`) |
| POST | `/api/students` | Create a student |
| GET | `/api/students/<id>` | Get one student |
| PUT | `/api/students/<id>` | Replace/update a student |
| PATCH | `/api/students/<id>` | Update supplied fields |
| DELETE | `/api/students/<id>` | Delete a student |

### Example POST body

```json
{
  "name": "Noor Fatima",
  "email": "noor@example.com",
  "age": 21,
  "department": "Software Engineering",
  "marks": 87.5,
  "status": "Active"
}
```

Expected successful creation status: `201 Created`.

## Validation rules
- Name: 2–60 characters
- Email: must have a basic valid email format and be unique
- Age: integer from 16 to 100 inclusive
- Department: required
- Marks: numeric from 0 to 100 inclusive
- Status: `Active` or `Inactive`

## Notes for coursework
- `validate_student()` in `app.py` is a suitable function for Control Flow Graph and cyclomatic-complexity analysis.
- The API endpoints are intentionally available without authentication to make local Postman testing straightforward.
- Run only on localhost or an environment you are authorised to test. The built-in Flask development server and default secret key are for coursework development only, not production deployment.
- Do not expose this app publicly with `debug=True`.
