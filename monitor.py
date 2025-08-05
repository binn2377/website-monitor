import requests
import time
import schedule

# === Cấu hình ===
WEBSITES = [
    "https://alonhadat.com.vn/",
    "https://nettruyenvia.com/"
]
THRESHOLD_SECONDS = 3  # Giới hạn tối đa (giây)

# Thông tin Telegram
BOT_TOKEN = '8254604373:AAFNVvpyDuzc7-Wee15xV73i-7RfjeqdjPk'
CHAT_ID = '7136615819'

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start

        if response.status_code != 200:
            send_telegram(f"❌ {url} lỗi HTTP {response.status_code}")
        elif elapsed > THRESHOLD_SECONDS:
            send_telegram(f"⚠️ {url} chậm ({elapsed:.2f}s)")
        else:
            print(f"✅ {url} OK ({elapsed:.2f}s)")
    except Exception as e:
        send_telegram(f"❌ Không truy cập được {url}: {e}")

def job():
    print("🔍 Đang kiểm tra website...")
    for site in WEBSITES:
        check_website(site)

schedule.every(0.5).minutes.do(job)
job()

while True:
    schedule.run_pending()
    time.sleep(1)

