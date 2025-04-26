import requests

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "7548865271:AAG3yg-lbVYHPGk9xSfGtMkpZkwLwm0DZTk"
TELEGRAM_CHAT_ID = "5002184829"

def send_alert(prediction):
    try:
        message = f"Prediction: {prediction['prediction']}, Confidence: {prediction['confidence'] * 100}%"
        send_telegram_message(message)
    except Exception as e:
        print(f"Error sending alert: {e}")

def send_performance_summary():
    # Placeholder function for sending a performance summary (can be daily/weekly)
    summary = "Performance Summary: ..."
    send_telegram_message(summary)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code}")
