FROM python:3.8-slim

# Install system dependencies for Chromium and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set up the working directory
WORKDIR /app
COPY . /app

# Run the bot
CMD ["python", "bot.py"]
