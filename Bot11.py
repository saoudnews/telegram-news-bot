from flask import Flask, request
import requests
import os

app = Flask(__name__)

# إعداد التوكن
TOKEN = os.environ.get("TELEGRAM_TOKEN")
BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_news(query):
    return f"📰 هذه آخر الأخبار حول: {query}"

def send_message(chat_id, text):
    url = f"{BASE_TELEGRAM_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        message = data.get("message", {})
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if not text:
            send_message(chat_id, "أرسل اسم دولة مثل غزة أو لبنان 📩")
        else:
            news = get_news(text)
            send_message(chat_id, news)

    except Exception as e:
        print("Error:", e)

    return "OK"

@app.route("/setwebhook")
def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    url = f"{BASE_TELEGRAM_URL}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    return response.text

@app.route("/")
def home():
    return "✅ البوت يعمل بنجاح!"

if __name__ == "__main__":
    app.run(debug=True)