import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from src.logger import logging

from ai import get_gemini_response, read_sql_query

# Connect to database
conn = sqlite3.connect('student.db')
c = conn.cursor()

# Database functions
def login(username, password):
    logging.info('Login initiated')
    c.execute('SELECT role FROM users WHERE username=? AND password=?', (username, password))
    role = c.fetchone()
    if role:
        return role[0]
    return None

def get_student_data(student_id):
    logging.info('Logged in as student')
    c.execute('SELECT * FROM marks WHERE student_id=?', (student_id,))
    return pd.DataFrame(c.fetchall(), columns=["ID", "Student ID", "Subject", "Marks", "Class", "Department"])

def get_class_data(class_name):
    logging.info('Logged in as staff')
    c.execute('SELECT * FROM marks WHERE class=?', (class_name,))
    return pd.DataFrame(c.fetchall(), columns=["ID", "Student ID", "Subject", "Marks", "Class", "Department"])

def get_department_data(department_name):
    logging.info('Logged in as HOD')
    c.execute('SELECT * FROM marks WHERE department=?', (department_name,))
    return pd.DataFrame(c.fetchall(), columns=["ID", "Student ID", "Subject", "Marks", "Class", "Department"])

def get_all_data():
    logging.info('Logged in as Principal')
    c.execute('SELECT * FROM marks')
    return pd.DataFrame(c.fetchall(), columns=["ID", "Student ID", "Subject", "Marks", "Class", "Department"])

# Streamlit App
st.title("Portal Dashboard")

# Initialize session state for login status and role if not already set
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None

# Login page
if not st.session_state["logged_in"]:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login(username, password)
        if role:
            st.session_state["logged_in"] = True
            st.session_state["role"] = role
            st.success(f"Logged in as {role}")
        else:
            st.error("Invalid credentials")

# Main dashboard page after login
if st.session_state["logged_in"]:
    role = st.session_state["role"]
    st.header(f"Welcome, {role}")

    if role == 'Student':
        student_data = get_student_data(student_id=1)  # Example student ID
        st.write("Your Marks")
        st.dataframe(student_data)
        fig = px.pie(student_data, names='Subject', values='Marks', title='Marks Distribution')
        st.plotly_chart(fig)
    
    elif role == 'Staff':
        class_data = get_class_data(class_name='CTPS')  # Example class
        st.write("Class Marks")
        st.dataframe(class_data)
        fig = px.bar(class_data, x='Student ID', y='Marks', color='Subject', title='Class Marks Distribution')
        st.plotly_chart(fig)
    
    elif role == 'HOD':
        dept_data = get_department_data(department_name='AIML')  # Example department
        st.write("Department Marks")
        st.dataframe(dept_data)
        fig = px.line(dept_data, x='Student ID', y='Marks', color='Subject', title='Department Marks Over Time')
        st.plotly_chart(fig)
    
    elif role == 'Principal':
        all_data = get_all_data()
        st.write("All Marks")
        st.dataframe(all_data)
        fig = px.histogram(all_data, x='Marks', color='Class', title='Overall Marks Distribution')
        st.plotly_chart(fig)
    
    # Question input section for logged-in users
    question = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    if submit:
        response = get_gemini_response(question)
        st.subheader("The Response is")
        
        response1 = read_sql_query(response, "student.db")
        for row in response1:
            st.header(row)
