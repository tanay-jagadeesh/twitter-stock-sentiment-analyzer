# News Sentiment Analyzer for Stock Mentions
# Day 1: Set up News API
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import config 

response = requests.get(f"https://newsapi.org/v2/everything?q=Apple&apiKey={config.API_KEY}")

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")

print(response.json())
