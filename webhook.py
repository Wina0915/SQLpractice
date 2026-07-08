from flask import Flask, request, jsonify

from current_question import save_question
from question import get_question, get_reference_sql
from judge import judge

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    req = request.get_json()
    print(req)

    # DialogflowからIntent名を取得
    intent = req["queryResult"]["intent"]["displayName"]

    response_text = ""

    if intent == "quiz_1":

        question_id, question, _ = get_question(1)

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

    elif intent == "quiz_2":

        question_id, question, _ = get_question(2)

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

    elif intent == "quiz_3":

        question_id, question, _ = get_question(3)

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
    elif intent == "quiz_answer":

        # ユーザーが入力したSQL
        user_sql = req["queryResult"]["queryText"]

        # Contextから問題ID取得
        question_id = None

        for context in req["queryResult"]["outputContexts"]:

            if context["name"].endswith("/contexts/sql_quiz"):

                question_id = context["parameters"]["question_id"]
                break

        if question_id is None:

            response_text = "問題が見つかりません。もう一度レベルを選択してください。"

        else:

            reference_sql = get_reference_sql(question_id)

            correct, message = judge(user_sql, reference_sql)

            if correct:

                response_text = "🎉 正解！\n\n" + message

            else:

                response_text = (
                    "❌ 不正解\n\n"
                    + message
                    + "\n\n【正解SQL】\n"
                    + reference_sql
                )
    else:

        response_text = "対応していない操作です。"


    return jsonify({
        "fulfillmentText": response_text,
        "outputContexts": [
            {
                "name":
                    req["session"] +
                    "/contexts/sql_quiz",

                "lifespanCount": 5,

                "parameters": {
                    "question_id": question_id,
                    "level": 1
                }
            }
        ]
    })


if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )