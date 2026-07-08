import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

students = pd.read_csv("csv/students.csv")
students.to_sql("students", conn, if_exists="replace", index=False)

questions = pd.read_csv("csv/questions.csv")
questions.to_sql("questions", conn, if_exists="replace", index=False)

conn.close()