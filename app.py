import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import base64
import os
import uuid
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create directories if they don't exist
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("images"):
    os.makedirs("images")

# Define CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4361ee;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3a0ca3;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .card {
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        background-color: #f8f9fa;
        margin-bottom: 1.5rem;
        border-left: 5px solid #4361ee;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .success-msg {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
        border-left: 5px solid #155724;
    }
    .error-msg {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8d7da;
        color: #721c24;
        margin-bottom: 1rem;
        border-left: 5px solid #721c24;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #0d6efd;
    }
    .metric-card {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.7rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4361ee !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #4361ee;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a0ca3;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 1px solid #ced4da;
    }
    .stDateInput>div>div>div {
        border-radius: 10px;
        border: 1px solid #ced4da;
    }
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
    }
    .stFileUploader>div>div {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    .stSidebar [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    .stSidebar [data-testid="stSidebarNav"] {
        padding-top: 2rem;
    }
    .stSidebar [data-testid="stSidebarNav"] ul {
        padding-left: 0;
    }
    .stSidebar [data-testid="stSidebarNav"] ul li {
        margin-bottom: 0.5rem;
    }
    .stSidebar [data-testid="stSidebarNav"] ul li a {
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stSidebar [data-testid="stSidebarNav"] ul li a:hover {
        background-color: #e9ecef;
    }
    .stSidebar [data-testid="stSidebarNav"] ul li a.active {
        background-color: #4361ee;
        color: white;
    }
    .user-welcome {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .user-welcome h3 {
        margin: 0;
        font-size: 1.2rem;
    }
    .dashboard-card {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-top: 5px solid #4361ee;
    }
    .dashboard-card h4 {
        color: #3a0ca3;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-header img {
        width: 100px;
        margin-bottom: 1rem;
    }
    .login-form {
        margin-bottom: 1.5rem;
    }
    .login-footer {
        text-align: center;
        margin-top: 1.5rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Base class for users
class User:
    def __init__(self, id, name, username, password, role):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

# Student class
class Student(User):
    def __init__(self, id, name, username, password, grade, parent_name, contact, address, admission_date, fees, image_path=None):
        super().__init__(id, name, username, password, "student")
        self.grade = grade
        self.parent_name = parent_name
        self.contact = contact
        self.address = address
        self.admission_date = admission_date
        self.fees = fees
        self.image_path = image_path
        self.fee_history = []
    
    def to_dict(self):
        student_dict = super().to_dict()
        student_dict.update({
            "grade": self.grade,
            "parent_name": self.parent_name,
            "contact": self.contact,
            "address": self.address,
            "admission_date": self.admission_date,
            "fees": self.fees,
            "image_path": self.image_path,
            "fee_history": self.fee_history
        })
        return student_dict
    
    def pay_fees(self, amount, payment_date, payment_method):
        payment = {
            "amount": amount,
            "date": payment_date,
            "method": payment_method,
            "receipt_no": f"FEE-{uuid.uuid4().hex[:8].upper()}"
        }
        self.fee_history.append(payment)
        return payment
    
    def generate_id_card(self):
        # Create a blank image for the ID card
        img = Image.new('RGB', (600, 375), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # Try to load a font, use default if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_medium = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except IOError:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw school name
        d.rectangle([(0, 0), (600, 60)], fill=(67, 97, 238))
        d.text((300, 30), "SCHOOL NAME", fill=(255, 255, 255), font=font_large, anchor="mm")
        
        # Draw student image placeholder or actual image
        if self.image_path and os.path.exists(self.image_path):
            try:
                student_img = Image.open(self.image_path)
                student_img = student_img.resize((150, 150))
                img.paste(student_img, (50, 80))
            except:
                d.rectangle([(50, 80), (200, 230)], outline=(0, 0, 0))
                d.text((125, 155), "PHOTO", fill=(0, 0, 0), font=font_medium, anchor="mm")
        else:
            d.rectangle([(50, 80), (200, 230)], outline=(0, 0, 0))
            d.text((125, 155), "PHOTO", fill=(0, 0, 0), font=font_medium, anchor="mm")
        
        # Draw student details
        d.text((230, 100), f"Name: {self.name}", fill=(0, 0, 0), font=font_medium)
        d.text((230, 130), f"ID: {self.id}", fill=(0, 0, 0), font=font_medium)
        d.text((230, 160), f"Grade: {self.grade}", fill=(0, 0, 0), font=font_medium)
        d.text((230, 190), f"Parent: {self.parent_name}", fill=(0, 0, 0), font=font_small)
        
        # Draw footer
        d.rectangle([(0, 315), (600, 375)], fill=(67, 97, 238))
        d.text((300, 345), "STUDENT ID CARD", fill=(255, 255, 255), font=font_medium, anchor="mm")
        
        # Save the image
        img_path = f"images/id_card_{self.id}.png"
        img.save(img_path)
        return img_path

    def generate_fee_receipt(self, payment):
        # Create a blank image for the receipt
        img = Image.new('RGB', (600, 800), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # Try to load a font, use default if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_medium = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 18)
            font_tiny = ImageFont.truetype("arial.ttf", 14)
        except IOError:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
        
        # Draw header
        d.rectangle([(0, 0), (600, 80)], fill=(67, 97, 238))
        d.text((300, 40), "FEE RECEIPT", fill=(255, 255, 255), font=font_large, anchor="mm")
        
        # Draw receipt details
        d.text((50, 100), "SCHOOL NAME", fill=(0, 0, 0), font=font_medium)
        d.text((50, 130), "Address: 123 School Street, City", fill=(0, 0, 0), font=font_tiny)
        d.text((50, 150), "Phone: 123-456-7890", fill=(0, 0, 0), font=font_tiny)
        
        # Draw line
        d.line([(50, 180), (550, 180)], fill=(0, 0, 0), width=2)
        
        # Draw receipt number and date
        d.text((50, 200), f"Receipt No: {payment['receipt_no']}", fill=(0, 0, 0), font=font_small)
        d.text((50, 230), f"Date: {payment['date']}", fill=(0, 0, 0), font=font_small)
        
        # Draw student details
        d.text((50, 280), "Student Details:", fill=(0, 0, 0), font=font_medium)
        d.text((50, 310), f"Name: {self.name}", fill=(0, 0, 0), font=font_small)
        d.text((50, 340), f"ID: {self.id}", fill=(0, 0, 0), font=font_small)
        d.text((50, 370), f"Grade: {self.grade}", fill=(0, 0, 0), font=font_small)
        
        # Draw payment details
        d.text((50, 420), "Payment Details:", fill=(0, 0, 0), font=font_medium)
        d.text((50, 450), f"Amount Paid: ${payment['amount']}", fill=(0, 0, 0), font=font_small)
        d.text((50, 480), f"Payment Method: {payment['method']}", fill=(0, 0, 0), font=font_small)
        
        # Draw footer
        d.rectangle([(0, 700), (600, 800)], fill=(67, 97, 238))
        d.text((300, 730), "Thank You!", fill=(255, 255, 255), font=font_medium, anchor="mm")
        d.text((300, 770), "This is a computer-generated receipt", fill=(255, 255, 255), font=font_tiny, anchor="mm")
        
        # Save the image
        receipt_path = f"images/receipt_{payment['receipt_no']}.png"
        img.save(receipt_path)
        return receipt_path

# Teacher class
class Teacher(User):
    def __init__(self, id, name, username, password, subject, qualification, contact, address, join_date, salary):
        super().__init__(id, name, username, password, "teacher")
        self.subject = subject
        self.qualification = qualification
        self.contact = contact
        self.address = address
        self.join_date = join_date
        self.salary = salary
        self.salary_history = []
    
    def to_dict(self):
        teacher_dict = super().to_dict()
        teacher_dict.update({
            "subject": self.subject,
            "qualification": self.qualification,
            "contact": self.contact,
            "address": self.address,
            "join_date": self.join_date,
            "salary": self.salary,
            "salary_history": self.salary_history
        })
        return teacher_dict
    
    def pay_salary(self, amount, payment_date):
        payment = {
            "amount": amount,
            "date": payment_date,
            "receipt_no": f"SAL-{uuid.uuid4().hex[:8].upper()}"
        }
        self.salary_history.append(payment)
        return payment

# Admin class
class Admin(User):
    def __init__(self, id, name, username, password):
        super().__init__(id, name, username, password, "admin")

# School Management System class
class SchoolManagementSystem:
    def __init__(self):
        self.students = {}
        self.teachers = {}
        self.admins = {}
        self.revenue = []
        self.expenses = []
        
        # Load data if exists
        self.load_data()
        
        # Create default admin if none exists
        if not self.admins:
            admin = Admin("admin1", "Admin User", "admin", "admin123")
            self.admins[admin.id] = admin
            self.save_data()
    
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
    
    def save_data(self):
        try:
            # Create data directory if it doesn't exist
            if not os.path.exists("data"):
                os.makedirs("data")
                
            # Save students
            students_data = [student.to_dict() for student in self.students.values()]
            pd.DataFrame(students_data).to_csv("data/students.csv", index=False)
            
            # Save teachers
            teachers_data = [teacher.to_dict() for teacher in self.teachers.values()]
            pd.DataFrame(teachers_data).to_csv("data/teachers.csv", index=False)
            
            # Save admins
            admins_data = [admin.to_dict() for admin in self.admins.values()]
            pd.DataFrame(admins_data).to_csv("data/admins.csv", index=False)
            
            # Save finances
            revenue_data = [{"type": "revenue", **item} for item in self.revenue]
            expense_data = [{"type": "expense", **item} for item in self.expenses]
            finances_data = revenue_data + expense_data
            pd.DataFrame(finances_data).to_csv("data/finances.csv", index=False)
            
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def authenticate(self, username, password):
        # Check admins
        for admin in self.admins.values():
            if admin.username == username and admin.password == password:
                return admin
        
        # Check teachers
        for teacher in self.teachers.values():
            if teacher.username == username and teacher.password == password:
                return teacher
        
        # Check students
        for student in self.students.values():
            if student.username == username and student.password == password:
                return student
        
        return None
    
    def add_student(self, name, username, password, grade, parent_name, contact, address, admission_date, fees, image_path=None):
        student_id = f"S{len(self.students) + 1:04d}"
        student = Student(student_id, name, username, password, grade, parent_name, contact, address, admission_date, fees, image_path)
        self.students[student_id] = student
        self.save_data()
        return student
    
    def update_student(self, student_id, **kwargs):
        if student_id in self.students:
            student = self.students[student_id]
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            self.save_data()
            return True
        return False
    
    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
            return True
        return False
    
    def add_teacher(self, name, username, password, subject, qualification, contact, address, join_date, salary):
        teacher_id = f"T{len(self.teachers) + 1:04d}"
        teacher = Teacher(teacher_id, name, username, password, subject, qualification, contact, address, join_date, salary)
        self.teachers[teacher_id] = teacher
        self.save_data()
        return teacher
    
    def update_teacher(self, teacher_id, **kwargs):
        if teacher_id in self.teachers:
            teacher = self.teachers[teacher_id]
            for key, value in kwargs.items():
                if hasattr(teacher, key):
                    setattr(teacher, key, value)
            self.save_data()
            return True
        return False
    
    def delete_teacher(self, teacher_id):
        if teacher_id in self.teachers:
            del self.teachers[teacher_id]
            self.save_data()
            return True
        return False
    
    def record_fee_payment(self, student_id, amount, payment_date, payment_method):
        if student_id in self.students:
            student = self.students[student_id]
            payment = student.pay_fees(amount, payment_date, payment_method)
            
            # Record as revenue
            revenue_entry = {
                "date": payment_date,
                "amount": amount,
                "description": f"Fee payment from {student.name} ({student_id})"
            }
            self.revenue.append(revenue_entry)
            self.save_data()
            
            return payment
        return None
    
    def pay_teacher_salary(self, teacher_id, amount, payment_date):
        if teacher_id in self.teachers:
            teacher = self.teachers[teacher_id]
            payment = teacher.pay_salary(amount, payment_date)
            
            # Record as expense
            expense_entry = {
                "date": payment_date,
                "amount": amount,
                "description": f"Salary payment to {teacher.name} ({teacher_id})"
            }
            self.expenses.append(expense_entry)
            self.save_data()
            
            return payment
        return None
    
    def get_monthly_revenue(self, year, month):
        monthly_revenue = 0
        for entry in self.revenue:
            entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
            if entry_date.year == year and entry_date.month == month:
                monthly_revenue += entry['amount']
        return monthly_revenue
    
    def get_monthly_expenses(self, year, month):
        monthly_expenses = 0
        for entry in self.expenses:
            entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
            if entry_date.year == year and entry_date.month == month:
                monthly_expenses += entry['amount']
        return monthly_expenses
    
    def get_financial_summary(self):
        total_revenue = sum(entry['amount'] for entry in self.revenue)
        total_expenses = sum(entry['amount'] for entry in self.expenses)
        profit = total_revenue - total_expenses
        
        # Get monthly data for the current year
        current_year = datetime.now().year
        monthly_revenue = [0] * 12
        monthly_expenses = [0] * 12
        
        for entry in self.revenue:
            try:
                entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                if entry_date.year == current_year:
                    monthly_revenue[entry_date.month - 1] += entry['amount']
            except:
                pass
        
        for entry in self.expenses:
            try:
                entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                if entry_date.year == current_year:
                    monthly_expenses[entry_date.month - 1] += entry['amount']
            except:
                pass
        
        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "profit": profit,
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": monthly_expenses
        }

# Initialize the school management system
sms = SchoolManagementSystem()

# Function to get image as base64 for display
def get_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Function to display image from path
def display_image(image_path, width=None):
    try:
        image = Image.open(image_path)
        st.image(image, width=width)
    except:
        st.error("Could not display image")

# Login page
def login_page():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        st.markdown("<div class='login-header'>", unsafe_allow_html=True)
        st.markdown("<h1 class='main-header'>School Management System</h1>", unsafe_allow_html=True)
        st.markdown("<p>Welcome back! Please login to your account.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='login-form'>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me")
        
        if st.button("Login", use_container_width=True):
            if username and password:
                user = sms.authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='login-footer'>", unsafe_allow_html=True)
        # st.markdown("Default Admin: username = 'admin', password = 'admin123'", unsafe_allow_html=True) hi
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Admin dashboard
def admin_dashboard():
    # Sidebar menu
    with st.sidebar:
        st.markdown("<div class='user-welcome'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Welcome, {st.session_state.user.name}</h3>", unsafe_allow_html=True)
        st.markdown("<p>Admin Dashboard</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Students", "Teachers", "Finances", "Reports", "Logout"],
            icons=["house", "mortarboard", "person-badge", "cash-coin", "file-earmark-bar-graph", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )
        
        if selected == "Logout":
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if selected == "Dashboard":
        show_admin_dashboard_home()
    elif selected == "Students":
        show_admin_students()
    elif selected == "Teachers":
        show_admin_teachers()
    elif selected == "Finances":
        show_admin_finances()
    elif selected == "Reports":
        show_admin_reports()

# Admin dashboard home
def show_admin_dashboard_home():
    st.markdown("<h1 class='main-header'>Admin Dashboard</h1>", unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Key Metrics</h4>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    financial_summary = sms.get_financial_summary()
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(sms.students)}</div>
            <div class='metric-label'>Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(sms.teachers)}</div>
            <div class='metric-label'>Teachers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>${financial_summary['total_revenue']}</div>
            <div class='metric-label'>Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>${financial_summary['profit']}</div>
            <div class='metric-label'>Net Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Financial charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Monthly Revenue vs Expenses</h4>", unsafe_allow_html=True)
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Create a DataFrame for Plotly
        df = pd.DataFrame({
            'Month': months,
            'Revenue': financial_summary['monthly_revenue'],
            'Expenses': financial_summary['monthly_expenses']
        })
        
        # Melt the DataFrame for easier plotting
        df_melted = pd.melt(df, id_vars=['Month'], value_vars=['Revenue', 'Expenses'], 
                           var_name='Category', value_name='Amount')
        
        # Create the bar chart
        fig = px.bar(df_melted, x='Month', y='Amount', color='Category', barmode='group',
                    color_discrete_map={'Revenue': '#4361ee', 'Expenses': '#ef476f'},
                    title='Monthly Revenue vs Expenses')
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            legend_title='Category',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Revenue Distribution</h4>", unsafe_allow_html=True)
        
        if sms.revenue:
            # Group revenue by source (simplified for demo)
            revenue_sources = {'Fees': 0, 'Other': 0}
            for entry in sms.revenue:
                if 'Fee payment' in entry['description']:
                    revenue_sources['Fees'] += entry['amount']
                else:
                    revenue_sources['Other'] += entry['amount']
            
            # Create a DataFrame for Plotly
            df = pd.DataFrame({
                'Source': list(revenue_sources.keys()),
                'Amount': list(revenue_sources.values())
            })
            
            # Create the pie chart
            fig = px.pie(df, values='Amount', names='Source', 
                        color_discrete_sequence=['#4361ee', '#3a0ca3', '#4cc9f0'],
                        title='Revenue Distribution')
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available to display chart")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent activities
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Recent Activities</h4>", unsafe_allow_html=True)
    
    # Combine and sort recent financial activities
    all_activities = []
    
    for entry in sms.revenue:
        all_activities.append({
            'date': entry['date'],
            'description': entry['description'],
            'amount': f"+${entry['amount']}",
            'type': 'revenue'
        })
    
    for entry in sms.expenses:
        all_activities.append({
            'date': entry['date'],
            'description': entry['description'],
            'amount': f"-${entry['amount']}",
            'type': 'expense'
        })
    
    # Sort by date (most recent first)
    all_activities.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=True)
    
    # Display recent activities
    if all_activities:
        activities_df = pd.DataFrame(all_activities[:10])
        st.dataframe(activities_df, use_container_width=True, height=300)
    else:
        st.info("No recent activities to display")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("© 2023 School Management System. All rights reserved.", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Admin students management
def show_admin_students():
    st.markdown("<h1 class='main-header'>Student Management</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["All Students", "Add Student", "Student Details", "Fee Payment"])
    
    with tabs[0]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>All Students</h4>", unsafe_allow_html=True)
        
        if sms.students:
            students_data = []
            for student in sms.students.values():
                students_data.append({
                    "ID": student.id,
                    "Name": student.name,
                    "Grade": student.grade,
                    "Parent": student.parent_name,
                    "Contact": student.contact,
                    "Fees": f"${student.fees}"
                })
            
            students_df = pd.DataFrame(students_data)
            st.dataframe(students_df, use_container_width=True, height=300)
            
            # Delete student
            st.markdown("<h4>Delete Student</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                student_to_delete = st.selectbox("Select student to delete", 
                                                [f"{s.id} - {s.name}" for s in sms.students.values()],
                                                index=None)
            with col2:
                if student_to_delete and st.button("Delete Student", type="primary"):
                    student_id = student_to_delete.split(" - ")[0]
                    if sms.delete_student(student_id):
                        st.success(f"Student {student_id} deleted successfully")
                        st.rerun()
                    else:
                        st.error("Failed to delete student")
        else:
            st.info("No students registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Add New Student</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name")
            grade = st.selectbox("Grade", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
            parent_name = st.text_input("Parent/Guardian Name")
            contact = st.text_input("Contact Number")
        
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            address = st.text_area("Address")
            fees = st.number_input("Monthly Fees ($)", min_value=0, value=100)
        
        admission_date = st.date_input("Admission Date")
        
        # Upload student photo
        uploaded_file = st.file_uploader("Upload Student Photo", type=["jpg", "jpeg", "png"])
        image_path = None
        
        if uploaded_file is not None:
            # Save the uploaded file
            image_path = f"images/student_{username}_{uuid.uuid4().hex[:8]}.png"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Photo uploaded successfully")
        
        if st.button("Add Student", use_container_width=True):
            if name and username and password and grade and parent_name and contact:
                student = sms.add_student(
                    name, username, password, grade, parent_name, contact,
                    address, admission_date.strftime("%Y-%m-%d"), fees, image_path
                )
                if student:
                    st.success(f"Student added successfully with ID: {student.id}")
                    st.rerun()
                else:
                    st.error("Failed to add student")
            else:
                st.error("Please fill all required fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Student Details</h4>", unsafe_allow_html=True)
        
        if sms.students:
            student_selection = st.selectbox("Select Student", 
                                           [f"{s.id} - {s.name}" for s in sms.students.values()],
                                           index=None)
            
            if student_selection:
                student_id = student_selection.split(" - ")[0]
                student = sms.students.get(student_id)
                
                if student:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if student.image_path and os.path.exists(student.image_path):
                            display_image(student.image_path, width=200)
                        else:
                            st.markdown("No photo available")
                        
                        if st.button("Generate ID Card"):
                            id_card_path = student.generate_id_card()
                            st.success("ID Card generated successfully")
                            display_image(id_card_path)
                            
                            # Download button for ID card
                            with open(id_card_path, "rb") as file:
                                btn = st.download_button(
                                    label="Download ID Card",
                                    data=file,
                                    file_name=f"id_card_{student.id}.png",
                                    mime="image/png"
                                )
                    
                    with col2:
                        st.markdown(f"<h3>{student.name} ({student.id})</h3>", unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Grade:** {student.grade}")
                            st.markdown(f"**Parent/Guardian:** {student.parent_name}")
                            st.markdown(f"**Contact:** {student.contact}")
                        
                        with col2:
                            st.markdown(f"**Address:** {student.address}")
                            st.markdown(f"**Admission Date:** {student.admission_date}")
                            st.markdown(f"**Monthly Fees:** ${student.fees}")
                        
                        # Fee payment history
                        st.markdown("### Fee Payment History")
                        if student.fee_history:
                            fee_history_data = []
                            for payment in student.fee_history:
                                fee_history_data.append({
                                    "Receipt No": payment['receipt_no'],
                                    "Date": payment['date'],
                                    "Amount": f"${payment['amount']}",
                                    "Method": payment['method']
                                })
                            
                            fee_history_df = pd.DataFrame(fee_history_data)
                            st.dataframe(fee_history_df, use_container_width=True)
                        else:
                            st.info("No fee payment history available")
                else:
                    st.error("Student not found")
        else:
            st.info("No students registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Fee Payment</h4>", unsafe_allow_html=True)
        
        if sms.students:
            col1, col2 = st.columns(2)
            
            with col1:
                student_selection = st.selectbox("Select Student for Fee Payment", 
                                               [f"{s.id} - {s.name}" for s in sms.students.values()],
                                               index=None,
                                               key="fee_payment_student")
            
            if student_selection:
                student_id = student_selection.split(" - ")[0]
                student = sms.students.get(student_id)
                
                if student:
                    with col2:
                        st.markdown(f"**Monthly Fee:** ${student.fees}")
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        amount = st.number_input("Payment Amount ($)", min_value=1, value=student.fees)
                    
                    with col2:
                        payment_date = st.date_input("Payment Date")
                    
                    with col3:
                        payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Bank Transfer", "Check"])
                    
                    if st.button("Process Payment", use_container_width=True):
                        payment = sms.record_fee_payment(
                            student_id, amount, payment_date.strftime("%Y-%m-%d"), payment_method
                        )
                        
                        if payment:
                            st.success(f"Payment of ${amount} recorded successfully. Receipt No: {payment['receipt_no']}")
                            
                            # Generate receipt
                            receipt_path = student.generate_fee_receipt(payment)
                            
                            # Display receipt
                            display_image(receipt_path, width=400)
                            
                            # Download button for receipt
                            with open(receipt_path, "rb") as file:
                                btn = st.download_button(
                                    label="Download Receipt",
                                    data=file,
                                    file_name=f"receipt_{payment['receipt_no']}.png",
                                    mime="image/png"
                                )
                        else:
                            st.error("Failed to process payment")
                else:
                    st.error("Student not found")
        else:
            st.info("No students registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Admin teachers management
def show_admin_teachers():
    st.markdown("<h1 class='main-header'>Teacher Management</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["All Teachers", "Add Teacher", "Teacher Details", "Salary Payment"])
    
    with tabs[0]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>All Teachers</h4>", unsafe_allow_html=True)
        
        if sms.teachers:
            teachers_data = []
            for teacher in sms.teachers.values():
                teachers_data.append({
                    "ID": teacher.id,
                    "Name": teacher.name,
                    "Subject": teacher.subject,
                    "Qualification": teacher.qualification,
                    "Contact": teacher.contact,
                    "Salary": f"${teacher.salary}"
                })
            
            teachers_df = pd.DataFrame(teachers_data)
            st.dataframe(teachers_df, use_container_width=True, height=300)
            
            # Delete teacher
            st.markdown("<h4>Delete Teacher</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                teacher_to_delete = st.selectbox("Select teacher to delete", 
                                                [f"{t.id} - {t.name}" for t in sms.teachers.values()],
                                                index=None)
            with col2:
                if teacher_to_delete and st.button("Delete Teacher", type="primary"):
                    teacher_id = teacher_to_delete.split(" - ")[0]
                    if sms.delete_teacher(teacher_id):
                        st.success(f"Teacher {teacher_id} deleted successfully")
                        st.rerun()
                    else:
                        st.error("Failed to delete teacher")
        else:
            st.info("No teachers registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Add New Teacher</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", key="teacher_name")
            subject = st.text_input("Subject")
            qualification = st.text_input("Qualification")
            contact = st.text_input("Contact Number", key="teacher_contact")
        
        with col2:
            username = st.text_input("Username", key="teacher_username")
            password = st.text_input("Password", type="password", key="teacher_password")
            address = st.text_area("Address", key="teacher_address")
            salary = st.number_input("Monthly Salary ($)", min_value=0, value=2000)
        
        join_date = st.date_input("Join Date")
        
        if st.button("Add Teacher", use_container_width=True):
            if name and username and password and subject and qualification and contact:
                teacher = sms.add_teacher(
                    name, username, password, subject, qualification, contact,
                    address, join_date.strftime("%Y-%m-%d"), salary
                )
                if teacher:
                    st.success(f"Teacher added successfully with ID: {teacher.id}")
                    st.rerun()
                else:
                    st.error("Failed to add teacher")
            else:
                st.error("Please fill all required fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Teacher Details</h4>", unsafe_allow_html=True)
        
        if sms.teachers:
            teacher_selection = st.selectbox("Select Teacher", 
                                           [f"{t.id} - {t.name}" for t in sms.teachers.values()],
                                           index=None)
            
            if teacher_selection:
                teacher_id = teacher_selection.split(" - ")[0]
                teacher = sms.teachers.get(teacher_id)
                
                if teacher:
                    st.markdown(f"<h3>{teacher.name} ({teacher.id})</h3>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Subject:** {teacher.subject}")
                        st.markdown(f"**Qualification:** {teacher.qualification}")
                        st.markdown(f"**Contact:** {teacher.contact}")
                    
                    with col2:
                        st.markdown(f"**Address:** {teacher.address}")
                        st.markdown(f"**Join Date:** {teacher.join_date}")
                        st.markdown(f"**Monthly Salary:** ${teacher.salary}")
                    
                    # Salary payment history
                    st.markdown("### Salary Payment History")
                    if teacher.salary_history:
                        salary_history_data = []
                        for payment in teacher.salary_history:
                            salary_history_data.append({
                                "Receipt No": payment['receipt_no'],
                                "Date": payment['date'],
                                "Amount": f"${payment['amount']}"
                            })
                        
                        salary_history_df = pd.DataFrame(salary_history_data)
                        st.dataframe(salary_history_df, use_container_width=True)
                    else:
                        st.info("No salary payment history available")
                else:
                    st.error("Teacher not found")
        else:
            st.info("No teachers registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Salary Payment</h4>", unsafe_allow_html=True)
        
        if sms.teachers:
            col1, col2 = st.columns(2)
            
            with col1:
                teacher_selection = st.selectbox("Select Teacher for Salary Payment", 
                                               [f"{t.id} - {t.name}" for t in sms.teachers.values()],
                                               index=None,
                                               key="salary_payment_teacher")
            
            if teacher_selection:
                teacher_id = teacher_selection.split(" - ")[0]
                teacher = sms.teachers.get(teacher_id)
                
                if teacher:
                    with col2:
                        st.markdown(f"**Monthly Salary:** ${teacher.salary}")
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        amount = st.number_input("Payment Amount ($)", min_value=1, value=teacher.salary)
                    
                    with col2:
                        payment_date = st.date_input("Payment Date", key="salary_payment_date")
                    
                    if st.button("Process Salary Payment", use_container_width=True):
                        payment = sms.pay_teacher_salary(
                            teacher_id, amount, payment_date.strftime("%Y-%m-%d")
                        )
                        
                        if payment:
                            st.success(f"Salary payment of ${amount} recorded successfully. Receipt No: {payment['receipt_no']}")
                        else:
                            st.error("Failed to process salary payment")
                else:
                    st.error("Teacher not found")
        else:
            st.info("No teachers registered yet")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Admin finances management
def show_admin_finances():
    st.markdown("<h1 class='main-header'>Financial Management</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Overview", "Revenue", "Expenses", "Monthly Report"])
    
    with tabs[0]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Financial Overview</h4>", unsafe_allow_html=True)
        
        financial_summary = sms.get_financial_summary()
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>${financial_summary['total_revenue']}</div>
                <div class='metric-label'>Total Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>${financial_summary['total_expenses']}</div>
                <div class='metric-label'>Total Expenses</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>${financial_summary['profit']}</div>
                <div class='metric-label'>Net Profit</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Revenue vs Expenses chart
        st.markdown("<h4>Revenue vs Expenses</h4>", unsafe_allow_html=True)
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Create a DataFrame for Plotly
        df = pd.DataFrame({
            'Month': months,
            'Revenue': financial_summary['monthly_revenue'],
            'Expenses': financial_summary['monthly_expenses']
        })
        
        # Melt the DataFrame for easier plotting
        df_melted = pd.melt(df, id_vars=['Month'], value_vars=['Revenue', 'Expenses'], 
                           var_name='Category', value_name='Amount')
        
        # Create the bar chart
        fig = px.bar(df_melted, x='Month', y='Amount', color='Category', barmode='group',
                    color_discrete_map={'Revenue': '#4361ee', 'Expenses': '#ef476f'},
                    title='Monthly Revenue vs Expenses')
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            legend_title='Category',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Profit/Loss chart
        st.markdown("<h4>Monthly Profit/Loss</h4>", unsafe_allow_html=True)
        
        monthly_profit = [r - e for r, e in zip(financial_summary['monthly_revenue'], financial_summary['monthly_expenses'])]
        
        # Create a DataFrame for Plotly
        df = pd.DataFrame({
            'Month': months,
            'Profit/Loss': monthly_profit
        })
        
        # Create the bar chart
        fig = px.bar(df, x='Month', y='Profit/Loss',
                    color='Profit/Loss', color_continuous_scale=['#ef476f', '#4cc9f0'],
                    title='Monthly Profit/Loss')
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=400
        )
        
        # Add a horizontal line at y=0
        fig.add_shape(
            type='line',
            x0=0,
            y0=0,
            x1=1,
            y1=0,
            xref='paper',
            yref='y',
            line=dict(color='gray', width=1, dash='dash')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Revenue Management</h4>", unsafe_allow_html=True)
        
        # Add new revenue
        st.markdown("<h5>Add New Revenue</h5>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            revenue_amount = st.number_input("Amount ($)", min_value=1, value=100, key="revenue_amount")
        
        with col2:
            revenue_date = st.date_input("Date", key="revenue_date")
        
        with col3:
           revenue_description = st.text_input("Description", key="revenue_description")
        
        # with col3:
        #     revenue_description = st.text_input("Description", key="revenue_description")
        
        if st.button("Add Revenue", use_container_width=True):
            if revenue_amount and revenue_description:
                revenue_entry = {
                    "date": revenue_date.strftime("%Y-%m-%d"),
                    "amount": revenue_amount,
                    "description": revenue_description
                }
                sms.revenue.append(revenue_entry)
                sms.save_data()
                st.success("Revenue added successfully")
                st.rerun()
            else:
                st.error("Please fill all required fields")
        
        # Revenue list
        st.markdown("<h5>Revenue List</h5>", unsafe_allow_html=True)
        
        if sms.revenue:
            revenue_data = []
            for entry in sms.revenue:
                revenue_data.append({
                    "Date": entry['date'],
                    "Amount": f"${entry['amount']}",
                    "Description": entry['description']
                })
            
            revenue_df = pd.DataFrame(revenue_data)
            st.dataframe(revenue_df, use_container_width=True)
        else:
            st.info("No revenue entries available")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Expense Management</h4>", unsafe_allow_html=True)
        
        # Add new expense
        st.markdown("<h5>Add New Expense</h5>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            expense_amount = st.number_input("Amount ($)", min_value=1, value=100, key="expense_amount")
        
        with col2:
            expense_date = st.date_input("Date", key="expense_date")
        
        with col3:
            expense_description = st.text_input("Description", key="expense_description")
        
        if st.button("Add Expense", use_container_width=True):
            if expense_amount and expense_description:
                expense_entry = {
                    "date": expense_date.strftime("%Y-%m-%d"),
                    "amount": expense_amount,
                    "description": expense_description
                }
                sms.expenses.append(expense_entry)
                sms.save_data()
                st.success("Expense added successfully")
                st.rerun()
            else:
                st.error("Please fill all required fields")
        
        # Expense list
        st.markdown("<h5>Expense List</h5>", unsafe_allow_html=True)
        
        if sms.expenses:
            expense_data = []
            for entry in sms.expenses:
                expense_data.append({
                    "Date": entry['date'],
                    "Amount": f"${entry['amount']}",
                    "Description": entry['description']
                })
            
            expense_df = pd.DataFrame(expense_data)
            st.dataframe(expense_df, use_container_width=True)
        else:
            st.info("No expense entries available")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Monthly Financial Report</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_year = st.selectbox("Year", list(range(datetime.now().year, datetime.now().year - 5, -1)))
        
        with col2:
            report_month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: datetime(2000, x, 1).strftime("%B"))
        
        if st.button("Generate Report", use_container_width=True):
            # Calculate monthly revenue
            monthly_revenue = 0
            revenue_items = []
            
            for entry in sms.revenue:
                try:
                    entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if entry_date.year == report_year and entry_date.month == report_month:
                        monthly_revenue += entry['amount']
                        revenue_items.append(entry)
                except:
                    pass
            
            # Calculate monthly expenses
            monthly_expenses = 0
            expense_items = []
            
            for entry in sms.expenses:
                try:
                    entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if entry_date.year == report_year and entry_date.month == report_month:
                        monthly_expenses += entry['amount']
                        expense_items.append(entry)
                except:
                    pass
            
            # Display report
            month_name = datetime(report_year, report_month, 1).strftime("%B")
            st.markdown(f"<h4>Financial Report for {month_name} {report_year}</h4>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${monthly_revenue}</div>
                    <div class='metric-label'>Total Revenue</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${monthly_expenses}</div>
                    <div class='metric-label'>Total Expenses</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                profit = monthly_revenue - monthly_expenses
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${profit}</div>
                    <div class='metric-label'>Net Profit</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Revenue breakdown
            st.markdown("<h5>Revenue Breakdown</h5>", unsafe_allow_html=True)
            
            if revenue_items:
                revenue_data = []
                for entry in revenue_items:
                    revenue_data.append({
                        "Date": entry['date'],
                        "Amount": f"${entry['amount']}",
                        "Description": entry['description']
                    })
                
                revenue_df = pd.DataFrame(revenue_data)
                st.dataframe(revenue_df, use_container_width=True)
            else:
                st.info("No revenue entries for this month")
            
            # Expense breakdown
            st.markdown("<h5>Expense Breakdown</h5>", unsafe_allow_html=True)
            
            if expense_items:
                expense_data = []
                for entry in expense_items:
                    expense_data.append({
                        "Date": entry['date'],
                        "Amount": f"${entry['amount']}",
                        "Description": entry['description']
                    })
                
                expense_df = pd.DataFrame(expense_data)
                st.dataframe(expense_df, use_container_width=True)
            else:
                st.info("No expense entries for this month")
            
            # Generate PDF report
            st.markdown("<h5>Export Report</h5>", unsafe_allow_html=True)
            
            if st.button("Export as PDF"):
                st.info("PDF export functionality would be implemented here in a real application")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Admin reports
def show_admin_reports():
    st.markdown("<h1 class='main-header'>Reports</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    report_type = st.selectbox("Select Report Type", [
        "Student List", "Teacher List", "Fee Collection", "Salary Payment", "Financial Summary"
    ])
    
    if report_type == "Student List":
        st.markdown("<h4>Student List Report</h4>", unsafe_allow_html=True)
        
        if sms.students:
            students_data = []
            for student in sms.students.values():
                students_data.append({
                    "ID": student.id,
                    "Name": student.name,
                    "Grade": student.grade,
                    "Parent": student.parent_name,
                    "Contact": student.contact,
                    "Admission Date": student.admission_date,
                    "Fees": f"${student.fees}"
                })
            
            students_df = pd.DataFrame(students_data)
            st.dataframe(students_df, use_container_width=True)
            
            # Filter options
            st.markdown("<h5>Filter Options</h5>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                grade_filter = st.multiselect("Filter by Grade", 
                                             sorted(list(set(s.grade for s in sms.students.values()))))
            
            with col2:
                name_filter = st.text_input("Search by Name")
            
            # Apply filters
            filtered_data = students_data
            
            if grade_filter:
                filtered_data = [s for s in filtered_data if s["Grade"] in grade_filter]
            
            if name_filter:
                filtered_data = [s for s in filtered_data if name_filter.lower() in s["Name"].lower()]
            
            if filtered_data != students_data:
                st.markdown("<h5>Filtered Results</h5>", unsafe_allow_html=True)
                filtered_df = pd.DataFrame(filtered_data)
                st.dataframe(filtered_df, use_container_width=True)
            
            # Export options
            st.markdown("<h5>Export Options</h5>", unsafe_allow_html=True)
            
            if st.button("Export as CSV"):
                csv = pd.DataFrame(filtered_data).to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="student_list_report.csv",
                    mime="text/csv"
                )
        else:
            st.info("No students registered yet")
    
    elif report_type == "Teacher List":
        st.markdown("<h4>Teacher List Report</h4>", unsafe_allow_html=True)
        
        if sms.teachers:
            teachers_data = []
            for teacher in sms.teachers.values():
                teachers_data.append({
                    "ID": teacher.id,
                    "Name": teacher.name,
                    "Subject": teacher.subject,
                    "Qualification": teacher.qualification,
                    "Contact": teacher.contact,
                    "Join Date": teacher.join_date,
                    "Salary": f"${teacher.salary}"
                })
            
            teachers_df = pd.DataFrame(teachers_data)
            st.dataframe(teachers_df, use_container_width=True)
            
            # Filter options
            st.markdown("<h5>Filter Options</h5>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                subject_filter = st.multiselect("Filter by Subject", 
                                               sorted(list(set(t.subject for t in sms.teachers.values()))))
            
            with col2:
                name_filter = st.text_input("Search by Name", key="teacher_name_filter")
            
            # Apply filters
            filtered_data = teachers_data
            
            if subject_filter:
                filtered_data = [t for t in filtered_data if t["Subject"] in subject_filter]
            
            if name_filter:
                filtered_data = [t for t in filtered_data if name_filter.lower() in t["Name"].lower()]
            
            if filtered_data != teachers_data:
                st.markdown("<h5>Filtered Results</h5>", unsafe_allow_html=True)
                filtered_df = pd.DataFrame(filtered_data)
                st.dataframe(filtered_df, use_container_width=True)
            
            # Export options
            st.markdown("<h5>Export Options</h5>", unsafe_allow_html=True)
            
            if st.button("Export as CSV", key="export_teacher_csv"):
                csv = pd.DataFrame(filtered_data).to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="teacher_list_report.csv",
                    mime="text/csv"
                )
        else:
            st.info("No teachers registered yet")
    
    elif report_type == "Fee Collection":
        st.markdown("<h4>Fee Collection Report</h4>", unsafe_allow_html=True)
        
        # Date range selection
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().replace(day=1))
        
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
        
        if st.button("Generate Report", key="fee_collection_report"):
            # Collect fee payment data
            fee_data = []
            
            for student in sms.students.values():
                for payment in student.fee_history:
                    payment_date = datetime.strptime(payment['date'], "%Y-%m-%d")
                    if start_date <= payment_date.date() <= end_date:
                        fee_data.append({
                            "Receipt No": payment['receipt_no'],
                            "Date": payment['date'],
                            "Student ID": student.id,
                            "Student Name": student.name,
                            "Grade": student.grade,
                            "Amount": payment['amount'],
                            "Payment Method": payment['method']
                        })
            
            if fee_data:
                # Display summary
                total_collected = sum(payment['Amount'] for payment in fee_data)
                payment_count = len(fee_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>${total_collected}</div>
                        <div class='metric-label'>Total Collected</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{payment_count}</div>
                        <div class='metric-label'>Number of Payments</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display detailed report
                st.markdown("<h5>Fee Collection Details</h5>", unsafe_allow_html=True)
                
                fee_df = pd.DataFrame(fee_data)
                st.dataframe(fee_df, use_container_width=True)
                
                # Export options
                st.markdown("<h5>Export Options</h5>", unsafe_allow_html=True)
                
                if st.button("Export as CSV", key="export_fee_csv"):
                    csv = pd.DataFrame(fee_data).to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="fee_collection_report.csv",
                        mime="text/csv"
                    )
            else:
                st.info("No fee payments found in the selected date range")
    
    elif report_type == "Salary Payment":
        st.markdown("<h4>Salary Payment Report</h4>", unsafe_allow_html=True)
        
        # Date range selection
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().replace(day=1), key="salary_start_date")
        
        with col2:
            end_date = st.date_input("End Date", value=datetime.now(), key="salary_end_date")
        
        if st.button("Generate Report", key="salary_payment_report"):
            # Collect salary payment data
            salary_data = []
            
            for teacher in sms.teachers.values():
                for payment in teacher.salary_history:
                    payment_date = datetime.strptime(payment['date'], "%Y-%m-%d")
                    if start_date <= payment_date.date() <= end_date:
                        salary_data.append({
                            "Receipt No": payment['receipt_no'],
                            "Date": payment['date'],
                            "Teacher ID": teacher.id,
                            "Teacher Name": teacher.name,
                            "Subject": teacher.subject,
                            "Amount": payment['amount']
                        })
            
            if salary_data:
                # Display summary
                total_paid = sum(payment['Amount'] for payment in salary_data)
                payment_count = len(salary_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>${total_paid}</div>
                        <div class='metric-label'>Total Paid</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-value'>{payment_count}</div>
                        <div class='metric-label'>Number of Payments</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display detailed report
                st.markdown("<h5>Salary Payment Details</h5>", unsafe_allow_html=True)
                
                salary_df = pd.DataFrame(salary_data)
                st.dataframe(salary_df, use_container_width=True)
                
                # Export options
                st.markdown("<h5>Export Options</h5>", unsafe_allow_html=True)
                
                if st.button("Export as CSV", key="export_salary_csv"):
                    csv = pd.DataFrame(salary_data).to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="salary_payment_report.csv",
                        mime="text/csv"
                    )
            else:
                st.info("No salary payments found in the selected date range")
    
    elif report_type == "Financial Summary":
        st.markdown("<h4>Financial Summary Report</h4>", unsafe_allow_html=True)
        
        # Year selection
        report_year = st.selectbox("Select Year", list(range(datetime.now().year, datetime.now().year - 5, -1)), key="financial_year")
        
        if st.button("Generate Report", key="financial_summary_report"):
            # Calculate monthly data
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            monthly_revenue = [0] * 12
            monthly_expenses = [0] * 12
            
            # Calculate revenue
            for entry in sms.revenue:
                try:
                    entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if entry_date.year == report_year:
                        monthly_revenue[entry_date.month - 1] += entry['amount']
                except:
                    pass
            
            # Calculate expenses
            for entry in sms.expenses:
                try:
                    entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if entry_date.year == report_year:
                        monthly_expenses[entry_date.month - 1] += entry['amount']
                except:
                    pass
            
            # Calculate profit
            monthly_profit = [r - e for r, e in zip(monthly_revenue, monthly_expenses)]
            
            # Create summary data
            summary_data = []
            for i in range(12):
                summary_data.append({
                    "Month": months[i],
                    "Revenue": monthly_revenue[i],
                    "Expenses": monthly_expenses[i],
                    "Profit/Loss": monthly_profit[i]
                })
            
            # Display summary
            total_revenue = sum(monthly_revenue)
            total_expenses = sum(monthly_expenses)
            total_profit = sum(monthly_profit)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${total_revenue}</div>
                    <div class='metric-label'>Total Revenue</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${total_expenses}</div>
                    <div class='metric-label'>Total Expenses</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>${total_profit}</div>
                    <div class='metric-label'>Net Profit</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display monthly breakdown
            st.markdown("<h5>Monthly Breakdown</h5>", unsafe_allow_html=True)
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
            
            # Display charts
            st.markdown("<h5>Revenue vs Expenses Chart</h5>", unsafe_allow_html=True)
            
            # Create a DataFrame for Plotly
            df = pd.DataFrame({
                'Month': months,
                'Revenue': monthly_revenue,
                'Expenses': monthly_expenses
            })
            
            # Melt the DataFrame for easier plotting
            df_melted = pd.melt(df, id_vars=['Month'], value_vars=['Revenue', 'Expenses'], 
                               var_name='Category', value_name='Amount')
            
            # Create the bar chart
            fig = px.bar(df_melted, x='Month', y='Amount', color='Category', barmode='group',
                        color_discrete_map={'Revenue': '#4361ee', 'Expenses': '#ef476f'},
                        title=f'Monthly Revenue vs Expenses for {report_year}')
            
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                legend_title='Category',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Profit/Loss chart
            st.markdown("<h5>Monthly Profit/Loss Chart</h5>", unsafe_allow_html=True)
            
            # Create a DataFrame for Plotly
            df = pd.DataFrame({
                'Month': months,
                'Profit/Loss': monthly_profit
            })
            
            # Create the bar chart
            fig = px.bar(df, x='Month', y='Profit/Loss',
                        color='Profit/Loss', color_continuous_scale=['#ef476f', '#4cc9f0'],
                        title=f'Monthly Profit/Loss for {report_year}')
            
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            
            # Add a horizontal line at y=0
            fig.add_shape(
                type='line',
                x0=0,
                y0=0,
                x1=1,
                y1=0,
                xref='paper',
                yref='y',
                line=dict(color='gray', width=1, dash='dash')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Export options
            st.markdown("<h5>Export Options</h5>", unsafe_allow_html=True)
            
            if st.button("Export as CSV", key="export_financial_csv"):
                csv = pd.DataFrame(summary_data).to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"financial_summary_{report_year}.csv",
                    mime="text/csv"
                )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Teacher dashboard
def teacher_dashboard():
    # Sidebar menu
    with st.sidebar:
        st.markdown("<div class='user-welcome'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Welcome, {st.session_state.user.name}</h3>", unsafe_allow_html=True)
        st.markdown("<p>Teacher Dashboard</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Profile", "Salary History", "Logout"],
            icons=["person", "cash-coin", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )
        
        if selected == "Logout":
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if selected == "Profile":
        show_teacher_profile()
    elif selected == "Salary History":
        show_teacher_salary_history()

# Teacher profile
def show_teacher_profile():
    teacher = st.session_state.user
    
    st.markdown("<h1 class='main-header'>Teacher Profile</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{teacher.name}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>ID:</strong> {teacher.id}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Subject:</strong> {teacher.subject}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Qualification:</strong> {teacher.qualification}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Contact Information</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Contact:</strong> {teacher.contact}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Address:</strong> {teacher.address}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Join Date:</strong> {teacher.join_date}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Update profile
    st.markdown("<h4>Update Profile</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        contact = st.text_input("Contact Number", value=teacher.contact)
    
    with col2:
        address = st.text_area("Address", value=teacher.address)
    
    if st.button("Update Profile", use_container_width=True):
        if sms.update_teacher(teacher.id, contact=contact, address=address):
            st.session_state.user.contact = contact
            st.session_state.user.address = address
            st.success("Profile updated successfully")
        else:
            st.error("Failed to update profile")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Teacher salary history
def show_teacher_salary_history():
    teacher = st.session_state.user
    
    st.markdown("<h1 class='main-header'>Salary History</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Monthly Salary:</strong> ${teacher.salary}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if teacher.salary_history:
        salary_data = []
        for payment in teacher.salary_history:
            salary_data.append({
                "Receipt No": payment['receipt_no'],
                "Date": payment['date'],
                "Amount": f"${payment['amount']}"
            })
        
        salary_df = pd.DataFrame(salary_data)
        st.dataframe(salary_df, use_container_width=True)
        
        # Salary chart
        st.markdown("<h4>Salary Payment Chart</h4>", unsafe_allow_html=True)
        
        # Group by month
        payment_by_month = {}
        
        for payment in teacher.salary_history:
            try:
                payment_date = datetime.strptime(payment['date'], "%Y-%m-%d")
                month_key = f"{payment_date.year}-{payment_date.month:02d}"
                
                if month_key in payment_by_month:
                    payment_by_month[month_key] += payment['amount']
                else:
                    payment_by_month[month_key] = payment['amount']
            except:
                pass
        
        if payment_by_month:
            # Sort by month
            sorted_months = sorted(payment_by_month.keys())
            amounts = [payment_by_month[month] for month in sorted_months]
            
            # Format month labels
            month_labels = []
            for month_key in sorted_months:
                year, month = month_key.split('-')
                month_name = datetime(int(year), int(month), 1).strftime("%b %Y")
                month_labels.append(month_name)
            
            # Create a DataFrame for Plotly
            df = pd.DataFrame({
                'Month': month_labels,
                'Amount': amounts
            })
            
            # Create the bar chart
            fig = px.bar(df, x='Month', y='Amount',
                        color_discrete_sequence=['#4361ee'],
                        title='Monthly Salary Payments')
            
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to display chart")
    else:
        st.info("No salary payment history available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Student dashboard
def student_dashboard():
    # Sidebar menu
    with st.sidebar:
        st.markdown("<div class='user-welcome'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Welcome, {st.session_state.user.name}</h3>", unsafe_allow_html=True)
        st.markdown("<p>Student Dashboard</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Profile", "Fee History", "ID Card", "Logout"],
            icons=["person", "cash-coin", "card-heading", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )
        
        if selected == "Logout":
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if selected == "Profile":
        show_student_profile()
    elif selected == "Fee History":
        show_student_fee_history()
    elif selected == "ID Card":
        show_student_id_card()

# Student profile
def show_student_profile():
    student = st.session_state.user
    
    st.markdown("<h1 class='main-header'>Student Profile</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if student.image_path and os.path.exists(student.image_path):
            display_image(student.image_path, width=200)
        else:
            st.markdown("No photo available")
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{student.name}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<p><strong>ID:</strong> {student.id}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Grade:</strong> {student.grade}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Parent/Guardian:</strong> {student.parent_name}</p>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<p><strong>Contact:</strong> {student.contact}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Address:</strong> {student.address}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Admission Date:</strong> {student.admission_date}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Update profile
    st.markdown("<h4>Update Profile</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        contact = st.text_input("Contact Number", value=student.contact)
    
    with col2:
        address = st.text_area("Address", value=student.address)
    
    # Upload new photo
    uploaded_file = st.file_uploader("Upload New Photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        image_path = f"images/student_{student.username}_{uuid.uuid4().hex[:8]}.png"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Photo uploaded successfully")
    else:
        image_path = student.image_path
    
    if st.button("Update Profile", use_container_width=True):
        if sms.update_student(student.id, contact=contact, address=address, image_path=image_path):
            st.session_state.user.contact = contact
            st.session_state.user.address = address
            st.session_state.user.image_path = image_path
            st.success("Profile updated successfully")
        else:
            st.error("Failed to update profile")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Student fee history
def show_student_fee_history():
    student = st.session_state.user
    
    st.markdown("<h1 class='main-header'>Fee History</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Monthly Fee:</strong> ${student.fees}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if student.fee_history:
        fee_data = []
        for payment in student.fee_history:
            fee_data.append({
                "Receipt No": payment['receipt_no'],
                "Date": payment['date'],
                "Amount": f"${payment['amount']}",
                "Method": payment['method']
            })
        
        fee_df = pd.DataFrame(fee_data)
        st.dataframe(fee_df, use_container_width=True)
        
        # View receipt
        st.markdown("<h4>View Receipt</h4>", unsafe_allow_html=True)
        receipt_selection = st.selectbox("Select Receipt to View", 
                                       [f"{p['receipt_no']} - {p['date']}" for p in student.fee_history],
                                       index=None)
        
        if receipt_selection:
            receipt_no = receipt_selection.split(" - ")[0]
            
            # Find the payment
            selected_payment = None
            for payment in student.fee_history:
                if payment['receipt_no'] == receipt_no:
                    selected_payment = payment
                    break
            
            if selected_payment:
                # Generate receipt
                receipt_path = student.generate_fee_receipt(selected_payment)
                
                # Display receipt
                display_image(receipt_path, width=400)
                
                # Download button for receipt
                with open(receipt_path, "rb") as file:
                    btn = st.download_button(
                        label="Download Receipt",
                        data=file,
                        file_name=f"receipt_{receipt_no}.png",
                        mime="image/png"
                    )
    else:
        st.info("No fee payment history available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Student ID card
def show_student_id_card():
    student = st.session_state.user
    
    st.markdown("<h1 class='main-header'>Student ID Card</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    # Generate ID card
    id_card_path = student.generate_id_card()
    
    # Display ID card
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    display_image(id_card_path, width=400)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download button for ID card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with open(id_card_path, "rb") as file:
            btn = st.download_button(
                label="Download ID Card",
                data=file,
                file_name=f"id_card_{student.id}.png",
                mime="image/png",
                use_container_width=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main app
def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check login status
    if not st.session_state.logged_in:
        login_page()
    else:
        # Show dashboard based on user role
        if st.session_state.user.role == "admin":
            admin_dashboard()
        elif st.session_state.user.role == "teacher":
            teacher_dashboard()
        elif st.session_state.user.role == "student":
            student_dashboard()
        else:
            st.error("Invalid user role")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()