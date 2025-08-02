import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
KEYWORDS = os.environ.get("KEYWORDS", "").split(",")
LANGUAGE = os.environ.get("LANGUAGE", "ar")
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "demo")

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
        return "لم يتم العثور على أخبار حالياً."

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = get_news()
        send_message(chat_id, text)
    return "OK"

@app.route("/setwebhook")
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    webhook_url = f"https://{request.host}/webhook"
    response = requests.post(url, data={"url": webhook_url})
    if response.status_code == 200:
        return "✅ تم ربط البوت بنجاح!"
    else:
        return f"❌ فشل الربط: {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))