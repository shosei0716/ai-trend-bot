"""LINE Bot Webhook - Vercel Serverless Function (Flask WSGI)

Vercel Python Runtime は api/ 配下の Flask app を WSGI として自動認識する。
変数名 `app` をモジュールレベルでエクスポートすること。
"""

import os

import requests as http_requests
from flask import Flask, abort, jsonify, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ---------- 環境変数 ----------
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")

GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/"
    "shosei0716/ai-trend-bot/main/output/today_post.txt"
)

# ---------- Flask app（Vercel が WSGI として検出） ----------
app = Flask(__name__)

# ---------- LINE SDK ----------
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)


# ---------- GitHub から投稿データ取得 ----------
def fetch_today_post() -> str:
    """GitHubから today_post.txt を取得する。"""
    try:
        resp = http_requests.get(GITHUB_RAW_URL, timeout=10)
        resp.raise_for_status()
        return resp.text.strip()
    except http_requests.RequestException:
        return "投稿データの取得に失敗しました。しばらく後にお試しください。"


# ---------- Webhook エンドポイント ----------
@app.route("/api/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception:
        abort(500)

    return jsonify({"status": "ok"}), 200


# ---------- LINE メッセージハンドラ ----------
@webhook_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    user_text = event.message.text.strip()

    if user_text == "AI":
        reply_text = fetch_today_post()
    else:
        reply_text = "「AI」と送ってください"

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )
