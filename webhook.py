from flask import Flask, request, jsonify

from current_question import save_question, get_question_id, delete_question
from question import get_question, get_reference_sql
from judge import judge

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    req = request.get_json()
    print(req)

    # DialogflowからIntent名を取得
    intent = req["queryResult"]["intent"]["displayName"]

    print("===== DEBUG =====")
    print("intent:", intent)
    print("queryText:", req["queryResult"]["queryText"])
    print("=================")

    # ユーザーを識別するID
    user_id = req["session"]

    # ------------------------
    # 初級
    # ------------------------
    if intent == "quiz_1":

        question_id, question, _ = get_question(1)

        save_question(user_id, question_id)

        response_text = (
            "【初級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

        return jsonify({
            "fulfillmentText": response_text,
            "outputContexts": [
                {
                    "name": req["session"] + "/contexts/sql_quiz",
                    "lifespanCount": 5,
                    "parameters": {
                        "question_id": question_id
                    }
                }
            ]
        })

    # ------------------------
    # 中級
    # ------------------------
    elif intent == "quiz_2":

        question_id, question, _ = get_question(2)

        save_question(user_id, question_id)

        response_text = (
            "【中級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

        return jsonify({
            "fulfillmentText": response_text,
            "outputContexts": [
                {
                    "name": req["session"] + "/contexts/sql_quiz",
                    "lifespanCount": 5,
                    "parameters": {
                        "question_id": question_id
                    }
                }
            ]
        })

    # ------------------------
    # 上級
    # ------------------------
    elif intent == "quiz_3":

        question_id, question, _ = get_question(3)

        save_question(user_id, question_id)

        response_text = (
            "【上級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

        return jsonify({
            "fulfillmentText": response_text,
            "outputContexts": [
                {
                    "name": req["session"] + "/contexts/sql_quiz",
                    "lifespanCount": 5,
                    "parameters": {
                        "question_id": question_id
                    }
                }
            ]
        })

    # ------------------------
    # SQL回答
    # ------------------------
    elif intent == "quiz_answer":

        # ユーザーが入力したSQL
        user_sql = req["queryResult"]["queryText"]

        # SQLiteから現在の問題IDを取得
        question_id = get_question_id(user_id)

        if question_id is None:

            response_text = (
                "問題が見つかりません。\n"
                "もう一度レベルを選択してください。"
            )

            return jsonify({
                "fulfillmentText": response_text
            })

        # 正解SQLを取得
        reference_sql = get_reference_sql(question_id)

        if reference_sql is None:

            response_text = "問題データが見つかりません。"

            return jsonify({
                "fulfillmentText": response_text
            })

        # SQLを判定
        correct, message = judge(user_sql, reference_sql)

        if correct:

            response_text = (
                "🎉 正解！\n\n"
                + message
            )

        else:

            response_text = (
                "❌ 不正解\n\n"
                + message
                + "\n\n【正解SQL】\n"
                + reference_sql
            )

        # 回答済みなので現在の問題を削除
        delete_question(user_id)

        return jsonify({
            "fulfillmentText": response_text
        })

    # ------------------------
    # その他
    # ------------------------
    else:

        return jsonify({
            "fulfillmentText": "対応していない操作です。"
        })


if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )   
