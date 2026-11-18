
import os
import json
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import dialogflow_v2 as dialogflow


app = Flask(__name__)
CORS(app)

# Renderに登録したSecret File
CREDENTIALS_PATH = "/etc/secrets/dialogflow-key.json"

# 認証情報を読み込む
with open(CREDENTIALS_PATH, "r", encoding="utf-8") as file:
    credentials_data = json.load(file)

# Google CloudのプロジェクトIDを取得
PROJECT_ID = credentials_data["project_id"]

# Google Cloud認証情報を設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Oshikatsu Chat API is running!"
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or not data.get("message"):
        return jsonify({
            "error": "メッセージがありません"
        }), 400

    message = data["message"].strip()

    if not message:
        return jsonify({
            "error": "メッセージがありません"
        }), 400

    # 同じ会話では同じsession_idを使用する
    session_id = data.get("sessionId") or str(uuid.uuid4())

    try:
        # Dialogflowクライアントを作成
        session_client = dialogflow.SessionsClient()

        # Dialogflowのセッションを指定
        session = session_client.session_path(
            PROJECT_ID,
            session_id
        )

        # テキスト入力を作成
        text_input = dialogflow.TextInput(
            text=message,
            language_code="ja"
        )

        query_input = dialogflow.QueryInput(
            text=text_input
        )

        # Dialogflowに問い合わせる
        response = session_client.detect_intent(
            request={
                "session": session,
                "query_input": query_input
            }
        )

        # Dialogflowからの回答を取得
        reply = response.query_result.fulfillment_text

        return jsonify({
            "reply": reply,
            "sessionId": session_id
        })

    except Exception as e:
        app.logger.exception("Dialogflow connection error")

        return jsonify({
            "error": "チャットの処理中にエラーが発生したよ。"
        }), 500


if __name__ == "__main__":
    app.run()
