import streamlit as st
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Prompt to sql
prompt=[
       """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name output and has the following columns - table1=[s_no, portal_id, register_number, name, department, ctps, l1___score, l2___score, l3___score, l4___score, l5___score, pds, total_score]

    SECTION.

    Important: 
    1. Do NOT include backticks (```) or the keyword "sql" in the SQL command output.
    2. Just return the plain SQL command without any markdown formatting.

    For example:
    Example 1 - How many entries of records are present? 
    SQL command: SELECT COUNT(*) FROM table1;

    Example 2 - show me student who scored more than 10000 in total_score;
    SQL command: SELECT * FROM table1 WHERE total_score>10000;


    """


]


def get_gemini_response(question,prompt = prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0],question])
    print(response.text)
    return response.text

#sql to DB

def read_sql_query(sql,db):

    con=sqlite3.connect(db)
    cur=con.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    con.commit()

    for row in rows:
        print(row)
    return rows
