import os
import requests
from flask import Flask, request

app = Flask(__name__)

# متغيرات البيئة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# دالة جلب الأخبار
def get_news(query="غزة"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&language=ar&sortBy=publishedAt&pageSize=5"
    response = requests.get(url)
    if response.status_code != 200:
        return "⚠️ حدث خطأ أثناء جلب الأخبار."
    
    articles = response.json().get("articles", [])
    if not articles:
        return "❌ لا توجد أخبار حالياً."

    result = ""
    for article in articles:
        title = article.get("title", "بدون عنوان")
        url = article.get("url", "")
        result += f"📰 {title}\n{url}\n\n"
    return result.strip()

# دالة إرسال رسالة لتليجرام
def send_message(chat_id, text):
    url = f"{BASE_TELEGRAM_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

# نقطة استقبال الرسائل
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        message = data.get("message", {})
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if not text:
            send_message(chat_id, "📩 أرسل كلمة مثل: غزة أو إيران أو لبنان")
        else:
            news = get_news(text)
            send_message(chat_id, news)

    except Exception as e:
        print("Error:", e)
    return "OK"

# نقطة تفعيل Webhook
@app.route("/setwebhook")
def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    url = f"{BASE_TELEGRAM_URL}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    return response.text

# صفحة فحص التشغيل
@app.route("/")
def home():
    return "✅ البوت يعمل بنجاح!"

if __name__ == "__main__":
    app.run(debug=True)