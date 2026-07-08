import sqlite3

def get_question(level):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, question, reference_sql
        FROM questions
        WHERE level = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, (level,))

    problem = cur.fetchone()

    conn.close()


    question_id = problem[0]
    question = problem[1]
    reference_sql = problem[2]

    return question_id, question, reference_sql

def get_reference_sql(question_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT reference_sql
    FROM questions
    WHERE id = ?
    """, (question_id,))

    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]

    return None