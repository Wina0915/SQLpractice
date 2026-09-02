import sqlite3

import pandas as pd

conn = sqlite3.connect("database.db")

students = pd.read_csv("csv/students.csv")

students.to_sql("students", conn, if_exists="replace", index=False)

questions = pd.read_csv("csv/questions.csv")

questions.to_sql("questions", conn, if_exists="replace", index=False)

# 現在解いている問題を保存するテーブル
conn.execute("""
CREATE TABLE IF NOT EXISTS current_question (
    user_id TEXT PRIMARY KEY,
    question_id INTEGER
)
""")

conn.commit()

conn.close()