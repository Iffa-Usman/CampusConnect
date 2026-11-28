# Task 1: Test Scenarios and Black-Box Testing

## 1. Introduction

For this assignment, we selected **CampusConnect**, a Student Management System, as the application for testing.

CampusConnect is a web-based application developed using Python and Flask. It allows users to register and log in, view a dashboard, and manage student records.

The purpose of this task is to evaluate the application's externally observable behaviour using different inputs and user actions. The test cases are designed without relying on the application's internal code structure.

## 2. Main Features of the Application

The application provides the following features:

1. **User Registration:** Allows a new user to create an account.
2. **Login:** Allows a registered user to access the application.
3. **Dashboard:** Displays student records and provides access to student management functions.
4. **Add Student:** Allows a student record to be created using details such as name, email, age, department, marks, and status.
5. **View Students:** Displays the student records stored in the application.
6. **Search Students:** Allows users to search for student records.
7. **Edit Student:** Allows an existing student record to be updated.
8. **Delete Student:** Allows a student record to be removed.
9. **Student REST API:** Provides endpoints for retrieving and managing student records.

## 3. Selected Features for Testing

The selected features were chosen because they accept user input, change or retrieve application data, and produce results that can be observed.

- **Student creation and validation:** Checks whether valid student information is accepted and invalid information is rejected.
- **Student search:** Checks whether a student can be found and how the application responds when no matching student is found.
- **Student editing and deletion:** Checks whether changes to existing records are saved and whether deleted records are removed.
- **Login:** Checks the response to different combinations of registered email addresses and passwords.

## 4. Black-Box Testing Techniques

We apply all six techniques required by the assignment:

### 4.1 Equivalence Partitioning

This technique divides input data into valid and invalid groups. Representative values are selected from these groups. We apply it to student age, marks, and email values.

### 4.2 Boundary Value Analysis

This technique checks values at and around the limits of an allowed range. We apply it to the age range of 16–100 and the marks range of 0–100.

### 4.3 Decision Table Testing

This technique checks combinations of conditions and their expected outcomes. We apply it to login by considering whether an email is registered and whether the password is correct.

### 4.4 State Transition Testing

This technique checks how the application behaves when an entity moves from one state to another. We apply it to a student record as it is created, updated, and deleted, and verify whether the corresponding operations are reflected in the application.

### 4.5 Scenario-Based Testing

This technique tests a complete sequence of actions that a user may perform. We use a student-management workflow that includes adding a student, searching for the student, editing the record, and deleting it.

### 4.6 Error Guessing

This technique uses likely error situations to identify problems. We consider cases such as invalid input formats, missing required data, duplicate student information, and requests for student records that do not exist. These cases will be checked against the application's actual responses.

## 5. Organization of Task 1

This folder contains the following documentation:

- **README.md:** Introduces CampusConnect, describes its main features, and explains the six testing techniques.
- **test_scenarios.md:** Describes the scenarios designed for each of the six techniques.
- **test_cases.md:** Lists the test cases, input data, expected results, actual results, status, decision table, and test-case derivation.

The automated Python tests for selected EP, BVA, and Decision Table cases are maintained separately in the project's `testing/black-box/` directory.

## 6. Conclusion

Black-Box Testing is used to evaluate CampusConnect through inputs, user actions, and observable outputs. The six required techniques provide different ways to examine input validation, boundary conditions, combinations of conditions, record-state changes, complete user workflows, and possible error situations.

The test cases and their execution results will be used to assess whether the selected application features behave as expected.
