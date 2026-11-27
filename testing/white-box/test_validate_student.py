import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import validate_student


def valid_data():
    return {
        "name": "Ayesha Khan",
        "email": "ayesha.unit@example.com",
        "age": "21",
        "department": "Software Engineering",
        "marks": "80",
        "status": "Active",
    }


def test_name_too_short():
    data = valid_data(); data["name"] = "A"
    ok, result = validate_student(data)
    assert not ok and "at least 2" in result


def test_name_too_long():
    data = valid_data(); data["name"] = "A" * 61
    ok, result = validate_student(data)
    assert not ok and "60 characters" in result


def test_invalid_email():
    data = valid_data(); data["email"] = "bad-email"
    ok, result = validate_student(data)
    assert not ok and "valid email" in result


def test_empty_department():
    data = valid_data(); data["department"] = ""
    ok, result = validate_student(data)
    assert not ok and "Department is required" in result


def test_age_not_integer():
    data = valid_data(); data["age"] = "abc"
    ok, result = validate_student(data)
    assert not ok and "whole number" in result


def test_age_below_range():
    data = valid_data(); data["age"] = "15"
    ok, result = validate_student(data)
    assert not ok and "between 16 and 100" in result


def test_marks_not_numeric():
    data = valid_data(); data["marks"] = "abc"
    ok, result = validate_student(data)
    assert not ok and "must be a number" in result


def test_marks_above_range():
    data = valid_data(); data["marks"] = "101"
    ok, result = validate_student(data)
    assert not ok and "between 0 and 100" in result


def test_invalid_status():
    data = valid_data(); data["status"] = "Pending"
    ok, result = validate_student(data)
    assert not ok and "Status must be" in result


def test_valid_student():
    ok, result = validate_student(valid_data())
    assert ok
    assert result["age"] == 21
    assert result["marks"] == 80.0
    assert result["email"] == "ayesha.unit@example.com"
