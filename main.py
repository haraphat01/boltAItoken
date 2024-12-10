import asyncio
import random
import time
import os
from twikit import Client
import openai
from dotenv import load_dotenv
import schedule
from datetime import datetime

# Load environment variables
load_dotenv()

# Twitter credentials from .env
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# OpenAI API Key from .env
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Twikit client
client = Client('en-US')

# Function to login to Twitter
async def login():
    await client.login(auth_info_1=TWITTER_USERNAME, auth_info_2=TWITTER_EMAIL, password=TWITTER_PASSWORD)

# Generate meme content using OpenAI model
def generate_meme():
    prompt = "Generate a fun meme-related tweet about BoltAI token and crypto, make it humorous and related to financial success."
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt, 
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Generate financial update using OpenAI model
def generate_financial_update():
    prompt = "Generate a financial update tweet about BoltAI token, focusing on its growth and market potential."
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt, 
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Post tweet function
async def post_tweet(content):
    await client.create_tweet(text=content)
    print(f"Tweet posted: {content}")

# Get trending hashtags and hijack relevant ones
async def hijack_trending():
    trends = await client.get_trends('trending')
    trending_crypto_hashtags = [trend['name'] for trend in trends if 'crypto' in trend['name'].lower()]
    
    if trending_crypto_hashtags:
        chosen_hashtag = random.choice(trending_crypto_hashtags)
        tweet_content = f"Join the #BoltAI revolution with #CryptoMagic! 🚀 #BoltToTheMoon #Crypto {chosen_hashtag}"
        await client.create_tweet(text=tweet_content)
        print(f"Tweet hijacked with trending hashtag: {chosen_hashtag}")

# Generate and post content 6 times a day
async def run_bot():
    await login()

    # Posting routine
    schedule.every(4).hours.do(asyncio.run, post_tweet(generate_meme()))
    schedule.every().day.at("12:00").do(asyncio.run, post_tweet(generate_financial_update()))
    schedule.every().day.at("12:30").do(asyncio.run, hijack_trending())
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
