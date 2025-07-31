
import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
KEYWORDS = os.environ.get("KEYWORDS", "").split(",")
LANGUAGE = os.environ.get("LANGUAGE", "ar")
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "demo"  # يجب استبداله بمفتاح فعلي إذا أردت مصادر واقعية

def get_news():
    query = " OR ".join(KEYWORDS)
    params = {
        "q": query,
        "language": "en",
        "pageSize": 5,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    r = requests.get(NEWS_API, params=params)
    articles = r.json().get("articles", [])
    results = []
    for art in articles:
        title = art.get("title")
        url = art.get("url")
        results.append(f"• {title}\n{url}")
    return "\n\n".join(results) if results else "لا توجد أخبار جديدة."

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route("/setwebhook")
def set_webhook():
    url = request.url_root + TELEGRAM_TOKEN
    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    response = requests.post(webhook_url, data={"url": url})
    return response.json()

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = get_news()
    send_message(chat_id, text)
    return {"ok": True}

@app.route("/")
def home():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
