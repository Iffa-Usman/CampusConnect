# Black-Box Test Cases

This document presents the test cases designed for CampusConnect using the six required Black-Box Testing techniques.

## 1. Test Case Table

| Test Case ID | Technique | Feature | Input / Test Data | Expected Result |
|---|---|---|---|---|
| EP-01 | Equivalence Partitioning | Add Student API | Age: 21, marks: 85, valid name, email, and department | Student should be created successfully. |
| EP-02 | Equivalence Partitioning | Add Student API | Age: 15, marks: 85 | Request should be rejected; age must be 16–100. |
| EP-03 | Equivalence Partitioning | Add Student API | Age: 21, marks: 105 | Request should be rejected; marks must be 0–100. |
| EP-04 | Equivalence Partitioning | Add Student API | Email: `not-an-email` | Request should be rejected with an invalid email message. |
| BVA-01 | Boundary Value Analysis | Add Student API | Age: 15 | Request should be rejected. |
| BVA-02 | Boundary Value Analysis | Add Student API | Age: 16 | Request should be accepted. |
| BVA-03 | Boundary Value Analysis | Add Student API | Age: 17 | Request should be accepted. |
| BVA-04 | Boundary Value Analysis | Add Student API | Age: 99 | Request should be accepted. |
| BVA-05 | Boundary Value Analysis | Add Student API | Age: 100 | Request should be accepted. |
| BVA-06 | Boundary Value Analysis | Add Student API | Age: 101 | Request should be rejected. |
| BVA-07 | Boundary Value Analysis | Add Student API | Marks: -0.1 | Request should be rejected. |
| BVA-08 | Boundary Value Analysis | Add Student API | Marks: 0 | Request should be accepted. |
| BVA-09 | Boundary Value Analysis | Add Student API | Marks: 0.1 | Request should be accepted. |
| BVA-10 | Boundary Value Analysis | Add Student API | Marks: 99.9 | Request should be accepted. |
| BVA-11 | Boundary Value Analysis | Add Student API | Marks: 100 | Request should be accepted. |
| BVA-12 | Boundary Value Analysis | Add Student API | Marks: 100.1 | Request should be rejected. |
| DT-01 | Decision Table Testing | Login | Registered email and correct password | Login should succeed and dashboard should be displayed. |
| DT-02 | Decision Table Testing | Login | Registered email and incorrect password | Login should be rejected. |
| DT-03 | Decision Table Testing | Login | Unregistered email and any password | Login should be rejected. |
| ST-01 | State Transition Testing | Student record | Add a valid student record | Record should move from absent to present. |
| ST-02 | State Transition Testing | Student record | Edit the marks of an existing student | Updated marks should be saved and displayed. |
| ST-03 | State Transition Testing | Student record | Delete an existing student | Record should be removed from the student list. |
| ST-04 | State Transition Testing | Student search | Search for a student after deletion | Deleted student should not be found. |
| SBT-01 | Scenario-Based Testing | Student management workflow | Log in, add a student, search, edit, verify update, delete, and search again | All operations should complete in the correct order and produce the expected results. |
| EG-01 | Error Guessing | Add Student API | Invalid email: `not-an-email` | Application should reject the invalid email. |
| EG-02 | Error Guessing | Add Student API | Marks: 105 | Application should reject marks outside the allowed range. |
| EG-03 | Error Guessing | Add Student API | Submit a record with an email already used by another student, if duplicates are restricted | Application should handle duplicate data according to its defined rules. |
| EG-04 | Error Guessing | Student API / Search | Request or search for a non-existent student ID | Application should return an appropriate not-found response or no-results message. |
| EG-05 | Error Guessing | Add Student | Leave a required field empty | Application should reject the incomplete submission and identify the missing information. |

## 2. Decision Table

The following decision table represents the login conditions and expected outcomes.

| Rule | Email registered? | Password correct? | Expected Result |
|---|---|---|---|
| R1 | Yes | Yes | Accept login and display dashboard |
| R2 | Yes | No | Reject login |
| R3 | No | Not applicable / any value | Reject login |

## 3. State Transition Model

The student record is tested through the following lifecycle:

```text
Absent
  |
  | Add student
  v
Present
  |
  | Edit student details
  v
Updated
  |
  | Delete student
  v
Deleted / Absent
```

The search operation is also used to verify whether a record is present or absent after each relevant transition.

## 4. Test Case Derivation

The test cases were derived from the application's features and input validation rules.

- **Equivalence Partitioning:** Representative values were selected from valid and invalid classes for age, marks, and email.
- **Boundary Value Analysis:** Values at and immediately around the age range (16–100) and marks range (0–100) were selected.
- **Decision Table Testing:** Combinations of registered email and password correctness were used to test login behaviour.
- **State Transition Testing:** The student record was followed through creation, update, and deletion.
- **Scenario-Based Testing:** A complete student-management workflow was designed to represent a typical user interaction.
- **Error Guessing:** Likely user mistakes and unusual inputs were selected, including invalid email, out-of-range marks, duplicate information, missing fields, and non-existent records.

## 5. Summary

A total of 29 test cases have been designed across all six Black-Box Testing techniques: 4 Equivalence Partitioning cases, 12 Boundary Value Analysis cases, 3 Decision Table cases, 4 State Transition cases, 1 Scenario-Based case, and 5 Error Guessing cases.
