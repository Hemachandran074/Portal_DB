import streamlit as st
import os
import sqlite3
from src.logger import logging
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Prompt to sql
prompt=[
       """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - table marks=[STUDENTID, SUBJECT, MARKS,CLASS,DEPARTMENT]
    SECTION.

    Important: 
    1. Do NOT include backticks (```) or the keyword "sql" in the SQL command output.
    2. Just return the plain SQL command without any markdown formatting.

    For example:
    Example 1 - How many entries of records are present? 
    SQL command: SELECT COUNT(*) FROM MARKS;

    Example 2 - Tell me all the students studying in AIML class? 
    SQL command: SELECT * FROM STUDENT WHERE CLASS = 'AIML';

    """


]


def get_gemini_response(question,prompt = prompt):
    logging.info('getting gemini response')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0],question])
    return response.text

#sql to DB

def read_sql_query(sql,db):
    logging.info('reading sql')
    con=sqlite3.connect(db)
    cur=con.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    con.commit()

    for row in rows:
        print(row)
    return rows


