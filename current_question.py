import sqlite3


def save_question(user_id, question_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO current_question
    (user_id, question_id)
    VALUES (?, ?)
    """, (user_id, question_id))

    conn.commit()
    conn.close()

def get_question_id(user_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT question_id
    FROM current_question
    WHERE user_id = ?
    """, (user_id,))

    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

def delete_question(user_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    DELETE
    FROM current_question
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()