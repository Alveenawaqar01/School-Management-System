import os

import pandas as pd

from app import Admin, Student, Teacher


def load_data(self):
    try:
        # Load students data
        if os.path.exists("data/students.csv") and os.path.getsize("data/students.csv") > 0:
            students_df = pd.read_csv("data/students.csv")
            for _, row in students_df.iterrows():
                student = Student(
                    row['id'], row['name'], row['username'], row['password'],
                    row['grade'], row['parent_name'], row['contact'], row['address'],
                    row['admission_date'], row['fees'], row['image_path']
                )
                if 'fee_history' in row and row['fee_history']:
                    try:
                        student.fee_history = eval(row['fee_history'])
                    except:
                        student.fee_history = []
                self.students[student.id] = student
        
        # Load teachers data
        if os.path.exists("data/teachers.csv") and os.path.getsize("data/teachers.csv") > 0:
            teachers_df = pd.read_csv("data/teachers.csv")
            for _, row in teachers_df.iterrows():
                teacher = Teacher(
                    row['id'], row['name'], row['username'], row['password'],
                    row['subject'], row['qualification'], row['contact'], row['address'],
                    row['join_date'], row['salary']
                )
                if 'salary_history' in row and row['salary_history']:
                    try:
                        teacher.salary_history = eval(row['salary_history'])
                    except:
                        teacher.salary_history = []
                self.teachers[teacher.id] = teacher
        
        # Load admins data
        if os.path.exists("data/admins.csv") and os.path.getsize("data/admins.csv") > 0:
            admins_df = pd.read_csv("data/admins.csv")
            for _, row in admins_df.iterrows():
                admin = Admin(row['id'], row['name'], row['username'], row['password'])
                self.admins[admin.id] = admin
        
        # Load finances data
        if os.path.exists("data/finances.csv") and os.path.getsize("data/finances.csv") > 0:
            finances_df = pd.read_csv("data/finances.csv")
            revenue_df = finances_df[finances_df['type'] == 'revenue']
            expenses_df = finances_df[finances_df['type'] == 'expense']
            
            self.revenue = revenue_df[['date', 'amount', 'description']].to_dict('records')
            self.expenses = expenses_df[['date', 'amount', 'description']].to_dict('records')
            
    except Exception as e:
        print(f"Error loading data: {e}")
        # Continue with empty data structures rather than crashing