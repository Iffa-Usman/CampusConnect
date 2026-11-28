# Black-Box Test Scenarios

This document describes the scenarios designed for CampusConnect using the six Black-Box Testing techniques required by the assignment.

## 1. Equivalence Partitioning (EP)

Equivalence Partitioning divides input values into valid and invalid classes. Representative values from each class are selected to check the application's response when creating a student record.

| Scenario ID | Input class | Test data | Expected behaviour |
|---|---|---|---|
| EP-01 | Valid student data | Age: 21, marks: 85, valid name, email, and department | Application should accept the student record. |
| EP-02 | Age below valid range | Age: 15 | Application should reject the record and report that age must be between 16 and 100. |
| EP-03 | Marks above valid range | Marks: 105 | Application should reject the record and report that marks must be between 0 and 100. |
| EP-04 | Invalid email format | Email: `not-an-email` | Application should reject the record and display an invalid email message. |

## 2. Boundary Value Analysis (BVA)

Boundary Value Analysis checks values at the edges of valid input ranges and values immediately outside those ranges.

### 2.1 Age boundaries

The application's valid age range is 16 to 100.

| Scenario ID | Age | Position | Expected behaviour |
|---|---:|---|---|
| BVA-01 | 15 | Just below minimum | Reject |
| BVA-02 | 16 | Minimum boundary | Accept |
| BVA-03 | 17 | Just above minimum | Accept |
| BVA-04 | 99 | Just below maximum | Accept |
| BVA-05 | 100 | Maximum boundary | Accept |
| BVA-06 | 101 | Just above maximum | Reject |

### 2.2 Marks boundaries

The application's valid marks range is 0 to 100.

| Scenario ID | Marks | Position | Expected behaviour |
|---|---:|---|---|
| BVA-07 | -0.1 | Just below minimum | Reject |
| BVA-08 | 0 | Minimum boundary | Accept |
| BVA-09 | 0.1 | Just above minimum | Accept |
| BVA-10 | 99.9 | Just below maximum | Accept |
| BVA-11 | 100 | Maximum boundary | Accept |
| BVA-12 | 100.1 | Just above maximum | Reject |

## 3. Decision Table Testing (DT)

Decision Table Testing checks combinations of conditions and the resulting action. For the login feature, the conditions are whether the email is registered and whether the password is correct.

| Rule | Email registered? | Password correct? | Expected result |
|---|---|---|---|
| DT-01 | Yes | Yes | Login should succeed and the dashboard should be displayed. |
| DT-02 | Yes | No | Login should be rejected with an invalid credentials message. |
| DT-03 | No | Not applicable / any value | Login should be rejected with an invalid credentials message. |

## 4. State Transition Testing (ST)

State Transition Testing checks the changes in a student record as operations are performed.

The following record states are used for the test model:

- **Absent:** The student record does not exist.
- **Present:** The student record exists in the application.
- **Updated:** The student record exists with modified information.
- **Deleted:** The record has been removed and is absent from the active student list.

| Scenario ID | Initial state | Action | Expected state | Expected behaviour |
|---|---|---|---|---|
| ST-01 | Absent | Add a valid student | Present | Student should appear in the student list. |
| ST-02 | Present | Edit the student's marks | Updated | The new marks should be saved and displayed. |
| ST-03 | Present / Updated | Delete the student | Deleted | Student should no longer appear in the student list. |
| ST-04 | Deleted | Search for the deleted student | Deleted / absent | No matching student should be returned. |

## 5. Scenario-Based Testing (SBT)

Scenario-Based Testing checks a complete sequence of actions that a user may perform.

**Scenario SBT-01: Manage a student record**

1. Log in to CampusConnect.
2. Add a student using valid information.
3. Search for the newly added student.
4. Open the student's record for editing.
5. Change the student's marks and save the update.
6. Verify that the updated marks are displayed.
7. Delete the student record.
8. Search for the student again and verify that the record is no longer present.

**Expected result:** Each operation should complete successfully, and the student record should reflect the changes made during the workflow.

## 6. Error Guessing (EG)

Error Guessing focuses on inputs and actions that may cause errors based on likely user mistakes or weaknesses in the application.

| Scenario ID | Possible error | Test data / action | Expected behaviour |
|---|---|---|---|
| EG-01 | Invalid email format | Enter `not-an-email` as the student email. | Application should reject the input with a validation message. |
| EG-02 | Invalid numeric range | Enter marks above 100. | Application should reject the value. |
| EG-03 | Duplicate student information | Submit a student record using an email already assigned to another student, if duplicate emails are restricted. | Application should prevent an unintended duplicate or handle it according to its defined rules. |
| EG-04 | Record does not exist | Request or search for a student ID that does not exist. | Application should return an appropriate not-found response or no-results message. |
| EG-05 | Missing required input | Submit the student form with a required field empty. | Application should reject the incomplete submission and indicate the missing information. |


