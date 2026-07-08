import sqlite3
from judge import judge
from question import get_question

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ------------------------
# レベル選択（最初だけ）
# ------------------------
while True:
    level = input(
        "レベルを入力してください（1/2/3 または 初級/中級/上級）："
    ).strip()

    if level in ["1", "初級"]:
        level = 1
        break

    elif level in ["2", "中級"]:
        level = 2
        break

    elif level in ["3", "上級"]:
        level = 3
        break

    else:
        print("レベルは1～3または初級・中級・上級で入力してください。")

# ------------------------
# クイズ開始
# ------------------------
question, reference_sql = get_question(level)

print("\n=== SQLクイズ ===")
print(question)
print()

user_sql = input("SQLを入力してください：\n")

correct, message = judge(user_sql, reference_sql)

print()
print(message)

if not correct:
    print("\n正解SQL")
    print(reference_sql)