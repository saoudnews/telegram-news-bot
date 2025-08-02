import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
KEYWORDS = os.environ.get("KEYWORDS", "").split(",")
LANGUAGE = os.environ.get("LANGUAGE", "ar")
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "default_key")

def get_news():
    return "✅ البوت يعمل بنجاح! (اختبار)"
    
    query = " OR ".join(KEYWORDS)
    params = {
        "q": query,
        "language": LANGUAGE,
        "sortBy": "publishedAt",
        "pageSize": 3,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API, params=params)
    data = response.json()
    
    if "articles" in data:
        articles = data["articles"]
        news_list = [f"- {article['title']}\n{article['url']}" for article in articles]
        return "\n\n".join(news_list)
    else:
        return "لم يتم العثور على أخبار حاليًا."

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
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
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "أهلاً بك! ✅ البوت يعمل الآن ويجهز لك آخر الأخبار.")
        else:
            news = get_news()
            send_message(chat_id, news or "لم يتم العثور على أخبار حالياً.")
    return {"ok": True}

@app.route("/")
def home():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)