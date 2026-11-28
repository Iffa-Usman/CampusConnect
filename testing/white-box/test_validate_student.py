"""
White-box tests for validate_student() in application-campusconnect/app.py

Technique : Basis Path Testing
CFG       : 23 nodes + Exit, 12 decision nodes, V(G) = 13
Each test below drives exactly one independent path (P1..P13) from the CFG.
Extra tests (P7b, P10b) exercise the TypeError side of the except clauses.
"""
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[2] / "application-campusconnect"
sys.path.insert(0, str(APP_DIR))

from app import validate_student  # noqa: E402


def valid_data(**overrides):
    """A baseline input that follows path P1; tests change one field only."""
    data = {
        "name": "Ayesha Khan",
        "email": "ayesha@example.com",
        "age": "21",
        "department": "Software Engineering",
        "marks": "80",
        "status": "Active",
    }
    data.update(overrides)
    return data


# P1: 1-2-4-6-7-9-11-13-14-16-18-19-21-23-Exit
def test_p1_valid_student():
    ok, result = validate_student(valid_data(name="  Ayesha Khan ", email=" AYESHA@Example.com "))
    assert ok is True
    assert result == {
        "name": "Ayesha Khan", "email": "ayesha@example.com", "age": 21,
        "department": "Software Engineering", "marks": 80.0, "status": "Active",
    }


# P2: 1-2-3-Exit
def test_p2_name_too_short():
    ok, msg = validate_student(valid_data(name="A"))
    assert (ok, msg) == (False, "Name must contain at least 2 characters.")


# P3: 1-2-4-5-Exit
def test_p3_name_too_long():
    ok, msg = validate_student(valid_data(name="A" * 61))
    assert (ok, msg) == (False, "Name must not exceed 60 characters.")


# P4: 1-2-4-6-8-Exit   ('@' missing)
def test_p4_email_missing_at_symbol():
    ok, msg = validate_student(valid_data(email="ayesha.example.com"))
    assert (ok, msg) == (False, "Enter a valid email address.")


# P5: 1-2-4-6-7-8-Exit   ('@' present, no '.' in domain)
def test_p5_email_domain_without_dot():
    ok, msg = validate_student(valid_data(email="ayesha@example"))
    assert (ok, msg) == (False, "Enter a valid email address.")


# P6: 1-2-4-6-7-9-10-Exit
def test_p6_department_empty():
    ok, msg = validate_student(valid_data(department="   "))
    assert (ok, msg) == (False, "Department is required.")


# P7: ...9-11-12-Exit   (ValueError)
def test_p7_age_not_a_number():
    ok, msg = validate_student(valid_data(age="abc"))
    assert (ok, msg) == (False, "Age must be a whole number.")


# P7b: same path, TypeError branch of the except clause
def test_p7b_age_missing():
    data = valid_data()
    del data["age"]
    ok, msg = validate_student(data)
    assert (ok, msg) == (False, "Age must be a whole number.")


# P8: ...11-13-15-Exit   (age < 16)
def test_p8_age_below_minimum():
    ok, msg = validate_student(valid_data(age="15"))
    assert (ok, msg) == (False, "Age must be between 16 and 100.")


# P9: ...13-14-15-Exit   (age > 100)
def test_p9_age_above_maximum():
    ok, msg = validate_student(valid_data(age="101"))
    assert (ok, msg) == (False, "Age must be between 16 and 100.")


# P10: ...14-16-17-Exit   (ValueError)
def test_p10_marks_not_a_number():
    ok, msg = validate_student(valid_data(marks="abc"))
    assert (ok, msg) == (False, "Marks must be a number.")


# P10b: same path, TypeError branch of the except clause
def test_p10b_marks_missing():
    data = valid_data()
    del data["marks"]
    ok, msg = validate_student(data)
    assert (ok, msg) == (False, "Marks must be a number.")


# P11: ...16-18-20-Exit   (marks < 0)
def test_p11_marks_below_zero():
    ok, msg = validate_student(valid_data(marks="-1"))
    assert (ok, msg) == (False, "Marks must be between 0 and 100.")


# P12: ...18-19-20-Exit   (marks > 100)
def test_p12_marks_above_hundred():
    ok, msg = validate_student(valid_data(marks="100.5"))
    assert (ok, msg) == (False, "Marks must be between 0 and 100.")


# P13: ...19-21-22-Exit
def test_p13_invalid_status():
    ok, msg = validate_student(valid_data(status="Pending"))
    assert (ok, msg) == (False, "Status must be Active or Inactive.")
