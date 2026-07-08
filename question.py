import sqlite3

def get_question(level):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT question, reference_sql
        FROM questions
        WHERE level = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, (level,))

    problem = cur.fetchone()

    conn.close()

    if problem is None:
        return None

    question = problem[0]
    reference_sql = problem[1]

    return question, reference_sql