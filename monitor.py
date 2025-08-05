import requests
import time
import schedule

# === Cấu hình ===
WEBSITES = [
    "https://nettruyenvia.com/",
    "https://alonhadat.com.vn/"
]
THRESHOLD_SECONDS = 3

# Thông tin Telegram
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def send_telegram(message):
    url = f"https://api.telegram.org/bot8254604373:AAFNVvpyDuzc7-Wee15xV73i-7RfjeqdjPk/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Lỗi gửi telegram: {response.text}")
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start

        if response.status_code != 200:
            send_telegram(f"❌ {url} trả về mã lỗi HTTP {response.status_code}")
        elif elapsed > THRESHOLD_SECONDS:
            send_telegram(f"⚠️ {url} tải chậm: {elapsed:.2f} giây")
        else:
            print(f"✅ {url} OK ({elapsed:.2f}s)")
    except requests.exceptions.RequestException as e:
        send_telegram(f"❌ Không thể truy cập {url}:\n{e}")

def job():
    print("🔍 Kiểm tra website...")
    for site in WEBSITES:
        check_website(site)

schedule.every(5).minutes.do(job)  # Kiểm tra mỗi 5 phút

# Chạy lần đầu
job()

while True:
    schedule.run_pending()
    time.sleep(1)

