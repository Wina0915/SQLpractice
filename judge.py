import sqlite3


def judge(user_sql, reference_sql, db_name="database.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    try:
        # ユーザーSQL
        cur.execute(user_sql)
        user_result = cur.fetchall()

    except Exception as e:
        conn.close()
        return False, f"あなたのSQLでエラーが発生しました。\n{e}"

    try:
        # 正解SQL
        cur.execute(reference_sql)
        correct_result = cur.fetchall()

    except Exception as e:
        conn.close()
        return False, f"問題データのSQLにエラーがあります。\n{e}"

    conn.close()

    # 順番は無視して比較
    if sorted(user_result) == sorted(correct_result):
        return True, "正解！"

    return False, "結果が異なります。"