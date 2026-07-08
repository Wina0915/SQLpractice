from flask import Flask, request, jsonify

from question import get_question

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    req = request.get_json()

    # DialogflowからIntent名を取得
    intent = req["queryResult"]["intent"]["displayName"]

    response_text = ""

    if intent == "quiz_1":

        question, reference_sql = get_question(1)

        response_text = (
            "【初級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

    elif intent == "quiz_2":

        question, reference_sql = get_question(2)

        response_text = (
            "【中級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

    elif intent == "quiz_3":

        question, reference_sql = get_question(3)

        response_text = (
            "【上級問題】\n"
            + question
            + "\n\nSQLを入力してください。"
        )

    else:

        response_text = "対応していない操作です。"


    return jsonify({
        "fulfillmentText": response_text
    })


if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )