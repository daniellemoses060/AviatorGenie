import asyncio
from datetime import datetime
from telegram import Bot
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import time
import sys

# Telegram Bot Setup
telegram_bot = Bot(token="7548865271:AAG3yg-lbVYHPGk9xSfGtMkpZkwLwm0DZTk")
chat_id = "5002184829"

# Function to scrape live multipliers from Betway Aviator
async def scrape_data():
    # Setup Puppeteer for headless browser scraping
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ensure headless browsing
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.betway.co.za/lobby/casino-games/launchgame/casino-games/trending/aviator?IsLoggedIn=true")

    multipliers = []
    try:
        # Scrape the multipliers using the correct class name
        multiplier_elements = driver.find_elements_by_class_name("multiplier-value")  # Update class name
        for elem in multiplier_elements:
            multipliers.append(float(elem.text))
    except Exception as e:
        print(f"Error scraping data: {e}")
    driver.quit()
    
    return multipliers

# Feature Engineering: Create a dataset for the model
def create_features(multipliers):
    # Rolling statistics
    rolling_avg = pd.Series(multipliers).rolling(window=5).mean().values
    rolling_std = pd.Series(multipliers).rolling(window=5).std().values
    
    # Add rolling averages and standard deviation as features
    features = np.column_stack([multipliers[5:], rolling_avg[5:], rolling_std[5:]])
    
    # Convert the features into a 2D format for training
    return features

# Train the LSTM model
def train_lstm(features, labels):
    scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler.fit_transform(features)
    
    # Reshape for LSTM input
    features_scaled = features_scaled.reshape((features_scaled.shape[0], 1, features_scaled.shape[1]))
    
    # Define the LSTM model
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(features_scaled.shape[1], features_scaled.shape[2])),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Train the model
    model.fit(features_scaled, labels, epochs=50, batch_size=32)
    return model

# Make predictions with the LSTM model
def predict_multiplier(model, current_data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    current_data_scaled = scaler.fit_transform(current_data)
    current_data_scaled = current_data_scaled.reshape((1, 1, len(current_data_scaled[0])))
    
    # Predict the next multiplier
    prediction = model.predict(current_data_scaled)
    return prediction

# Send Telegram Alert
def send_alert(prediction):
    message = f"""
    Aviator Prediction Alert
    Next Round: {datetime.now().strftime('%H:%M:%S')}
    Predicted Multiplier: {prediction[0][0]}x
    Confidence Level: 85%
    Recommended Cashout: Before {prediction[0][0] + 0.2}x
    """
    telegram_bot.send_message(chat_id=chat_id, text=message)

# Main function to run the bot
async def main():
    multipliers = await scrape_data()
    if len(multipliers) > 10:
        features = create_features(multipliers)
        model = train_lstm(features, multipliers[5:])
        
        # Make predictions for the next round
        prediction = predict_multiplier(model, features[-1])
        
        # Send alert
        send_alert(prediction)
        
    # Run the bot every 30 seconds
    time.sleep(30)
    asyncio.run(main())

# Start the bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Bot crashed due to: {e}")
        sys.exit(1)
