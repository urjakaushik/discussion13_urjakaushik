import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS Employee
                   (employee_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    hire_date TEXT,
                    job_id INTEGER,
                    salary INTEGER);''')
    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU

    for employee in file_data:
        cur.execute("INSERT INTO Employee (employee_id, first_name, last_name, hire_date, job_id, salary) VALUES (?, ?, ?, ?, ?, ?);",
                    (employee["employee_id"], employee["first_name"], employee["last_name"], employee["hire_date"], employee["job_id"], employee["salary"]))

    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute("SELECT job_id, hire_date FROM Employee;")
    results = cur.fetchall()
    return results

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute('''SELECT e.employee_id, e.salary
                   FROM Employee e JOIN
                        (SELECT job_id, AVG(salary) AS avg_salary
                         FROM Employee
                         GROUP BY job_id
                         HAVING AVG(salary) > 8000) j
                   ON e.job_id = j.job_id
                   WHERE e.salary < j.avg_salary;''')
    results = cur.fetchall()
    return results

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    cur.execute('''SELECT job_id, AVG(salary)
                   FROM Employee
                   GROUP BY job_id;''')
    results = cur.fetchall()

    job_ids = [r[0] for r in results]
    salaries = [r[1] for r in results]

    plt.bar(job_ids, salaries)
    plt.xlabel("Job ID")
    plt.ylabel("Average Salary")
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

