import streamlit as st
import os
import sqlite3
from ai import get_gemini_response, read_sql_query

# Function to retrieve student data
def get_student_data(portal_id, role):
    conn = sqlite3.connect("output.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if role == "student":
            cursor.execute("SELECT * FROM table1 WHERE portal_id = ?", (portal_id,))
            result = cursor.fetchone()
            if result:
                save_to_result_db([dict(result)], role)
            return result
        else:
            cursor.execute("SELECT * FROM table1")
            result = cursor.fetchall()
            if result:
                save_to_result_db([dict(row) for row in result], role)
            return result
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        conn.close()

# Function to save results to result.db
def save_to_result_db(data, role):
    with sqlite3.connect("result.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS table1 (
                s_no INTEGER PRIMARY KEY,
                portal_id TEXT,
                register_number TEXT,
                name TEXT,
                department TEXT,
                ctps REAL,
                l1___score REAL,
                l2___score REAL,
                l3___score REAL,
                l4___score REAL,
                l5___score REAL,
                pds REAL,
                total_score REAL,
                user_role TEXT
            )
        """)
        cursor.execute("DELETE FROM table1")  # Clear previous data
        for entry in data:
            entry['user_role'] = role
        cursor.executemany("INSERT INTO table1 (s_no, portal_id, register_number, name, department, ctps, l1___score, l2___score, l3___score, l4___score, l5___score, pds, total_score, user_role) VALUES (:s_no, :portal_id, :register_number, :name, :department, :ctps, :l1___score, :l2___score, :l3___score, :l4___score, :l5___score, :pds, :total_score, :user_role)", data)
        conn.commit()

# Streamlit login page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "portal_id" not in st.session_state:
    st.session_state["portal_id"] = None

def login(username, password):
    conn = sqlite3.connect("output.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM USERS WHERE portal_id = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        st.session_state["logged_in"] = True
        st.session_state["role"] = user[0]
        st.session_state["portal_id"] = username
        return True
    return False

if not st.session_state["logged_in"]:
    st.title("Login Page")
    username = st.text_input("Portal ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")
else:
    st.title("Student Dashboard")
    role = st.session_state["role"]
    portal_id = st.session_state["portal_id"]

    student_data = get_student_data(portal_id, role)

    if role == "student":
        st.subheader("Your Data")
        st.write(student_data)
    else:
        st.subheader("All Students Data")
        all_students_data = read_sql_query("SELECT * FROM table1", "result.db")
        st.write(all_students_data)

    question = st.text_input("Enter your question:")
    if st.button("Submit"):
        if question:
            sql_query = get_gemini_response(question)  # Get the SQL query from AI
            st.write("Generated SQL Query:", sql_query)  # Display the SQL query for debugging
            
            # Execute the generated SQL query
            try:
                result = read_sql_query(sql_query, "result.db")
                if result:
                    st.write("Query Result:", result)
                else:
                    st.warning("No results found for the given query.")
            except Exception as e:
                st.error(f"Error executing SQL query: {e}")
        else:
            st.warning("Please enter a question.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.session_state["portal_id"] = None
