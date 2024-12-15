# Test Automation for Wiley Online Library

This project contains automated tests for the Wiley Online Library using Playwright and Pytest. The tests are designed to verify the functionality of the website, including login options, search functionality, and dropdown menus.

## Dependencies

Before running the tests, you need to install the following dependencies:

- **pytest**: A testing framework for Python.
- **playwright**: A library to automate browsers.

## Setup Instructions

### Install Python Dependencies

Ensure that you have Python 3.7 or higher installed. You can install the required dependencies using `pip`:

```bash
pip install pytest playwright
```
## About the files

- **test_functions.py**
  - Contains all the test functions that can run at once.

- **test_login_options.py**
  - Contains test 01 separately.
 
- **test_search.py**
  - Contains test 02 separately.
 
- **test_agriculture.py**
  - Contains test 03 separately.
 

## **Test 01: Login Options Verification**
- **Objective:** 
  - Validate the visibility of "Login / Register" options.
- **Steps:**
  1. Navigate to the Wiley homepage.
  2. Click the "Login / Register" link.
  3. Verify the dropdown menu appears.
  4. Check the visibility of the following options:
     - Individual login
     - Institutional login
     - Register
- **Outcome:** 
  - All three options should be visible.

---

## **Test 02: Search Functionality**
- **Objective:** 
  - Validate the search functionality while bypassing CAPTCHA.
 
  *NOTE: Here, I am directly using the search URL because performing the search through the search bar triggers a 'Verify you are a human' CAPTCHA. To bypass this, I have opted for the approach detailed below.*

- **Steps:**
  1. Navigate directly to the search results page for the term "Quality Engineering."
  2. Verify the presence of search results.
  3. Check that each result contains the terms "Quality" and "Engineering" (case-insensitive).
- **Outcome:** 
  - The search results should display entries relevant to "Quality Engineering."

---

## **Test 03: Agriculture Dropdown**
- **Objective:** 
  - Validate the functionality of the "Agriculture, Aquaculture & Food Science" dropdown.
- **Steps:**
  1. Navigate to the Wiley homepage.
  2. Click the "Agriculture, Aquaculture & Food Science" link to open the dropdown.
  3. Verify the dropdown menu appears and its content is visible.
  4. Click the "Agriculture" option and ensure navigation to the correct page.
- **Outcome:** 
  - The dropdown should function correctly, and navigation to the "Agriculture" page should succeed.

---

### **General Notes:**
- Each test includes:
  - Proper error handling to log issues.
  - Clear assertions to validate expected outcomes.
  - Detailed comments for maintainability and clarity.



# **How to Run the Tests**

## **To Run All Test Cases at Once**

Open your terminal and type the following command:

```bash
pytest -s test_functions.py

```

*Note: The -s flag is used to display print statements in the console output for better debugging.*


## **To run each test case separately**

### Test 01
```bash
pytest -s test_login_options.py
```

### Test 02
```bash
pytest -s test_search.py
```

### Test 03
```bash
pytest -s test_agriculture.py
```
