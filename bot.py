import time
from scraper import scrape_data
from model import train_models, predict_multiplier
from telegram import send_alert, send_performance_summary

def run_bot():
    while True:
        try:
            # Scrape latest data every 30 seconds
            data = scrape_data()

            # Train models with the new data
            model_1, model_2 = train_models(data)

            # Predict the next round's multiplier using both models
            prediction_1 = predict_multiplier(model_1, data)
            prediction_2 = predict_multiplier(model_2, data)

            # Choose the best prediction (can be based on confidence score or logic)
            best_prediction = max(prediction_1, prediction_2, key=lambda x: x['confidence'])

            # Send Telegram alert
            send_alert(best_prediction)

            # Optionally, send daily/weekly performance summaries
            send_performance_summary()

            # Wait for the next cycle (30 seconds)
            time.sleep(30)

        except Exception as e:
            print(f"Error in bot execution: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying to avoid crash
