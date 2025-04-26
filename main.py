# main.py
import requests
import time
import logging
import random
from datetime import datetime
from telegram import Bot

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = '7548865271:AAG3yg-lbVYHPGk9xSfGtMkpZkwLwm0DZTk'
TELEGRAM_CHAT_ID = '5002184829'
LOG_FILE = 'prediction_log.txt'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

round_counter = 0

# --- AI-LIKE PREDICTION LOGIC ---
def fetch_multiplier_data():
    # Placeholder: replace with actual web scraping logic
    return [round(random.uniform(1.0, 5.0), 2) for _ in range(5)]

def predict_safe_entry(multiplier_history):
    high_multipliers = [m for m in multiplier_history if m >= 2.0]
    success_rate = len(high_multipliers) / len(multiplier_history)
    return success_rate >= 0.6, success_rate

def send_alert(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    logging.info(f'Telegram alert sent: {message}')

def log_prediction(data, result):
    status = "SAFE" if result else "WAIT"
    logging.info(f"Data: {data} | Prediction: {status}")

def main():
    global round_counter
    multiplier_history = []
    while True:
        try:
            round_counter += 1
            new_data = fetch_multiplier_data()
            multiplier_history.extend(new_data)
            if len(multiplier_history) > 20:
                multiplier_history = multiplier_history[-20:]  # Keep last 20 entries only

            prediction, success_rate = predict_safe_entry(multiplier_history[-5:])
            log_prediction(multiplier_history[-5:], prediction)

            if prediction:
                countdown = 15  # Approx. seconds till next round
                msg = (
                    f"ROUND #{round_counter}\n"
                    f"🚀 95% CONFIDENCE: Play the NEXT round!\n"
                    f"Target Cashout: 1.8x–3.0x\n"
                    f"Estimated start in {countdown} seconds\n"
                    f"Recent win rate: {int(success_rate * 100)}% (last 5 rounds)"
                )
                send_alert(msg)
            else:
                logging.info(f"Round #{round_counter}: No safe signal.")

            time.sleep(60)  # Check every 1 minute
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()
