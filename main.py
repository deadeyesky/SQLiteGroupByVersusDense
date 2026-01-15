import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Department (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary INTEGER NOT NULL,
    departmentId INTEGER,
    FOREIGN KEY (departmentId) REFERENCES Department(id)
);
""")

# Insert departments
departments = [
    (1, "IT"),
    (2, "Sales"),
    (3, "HR"),
    (4, "Finance"),
    (5, "Marketing")
]

cursor.executemany(
    "INSERT OR REPLACE INTO Department (id, name) VALUES (?, ?);",
    departments
)

# Generate employees
first_names = [
    "Joe", "Jim", "Henry", "Sam", "Max", "Amy", "John", "Pam",
    "Alex", "Sara", "Mike", "Linda", "Chris", "Anna", "Tom"
]

employees = []
num_employees = 500

for emp_id in range(1, num_employees + 1):
    name = random.choice(first_names) + "_" + str(emp_id)
    department_id = random.randint(1, len(departments))

    # Salary ranges by department
    if department_id == 1:        # IT
        salary = random.randint(70000, 150000)
    elif department_id == 2:      # Sales
        salary = random.randint(50000, 120000)
    elif department_id == 3:      # HR
        salary = random.randint(40000, 90000)
    elif department_id == 4:      # Finance
        salary = random.randint(60000, 140000)
    else:                         # Marketing
        salary = random.randint(45000, 100000)

    employees.append((emp_id, name, salary, department_id))

cursor.executemany(
    "INSERT OR REPLACE INTO Employee (id, name, salary, departmentId) VALUES (?, ?, ?, ?);",
    employees
)

# Commit and close
conn.commit()
conn.close()

print(f"Database created with {num_employees} employees.")

