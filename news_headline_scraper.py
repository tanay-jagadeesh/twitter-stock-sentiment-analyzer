# News Sentiment Analyzer for Stock Mentions
# Day 1: Set up News API
import pandas as pd
from datetime import datetime
import requests
import config 

response = requests.get(f"https://newsapi.org/v2/everything?q=Apple&pageSize=20&apiKey={config.API_KEY}")

# Error Handling to see if it prints json
try:
    response.raise_for_status()
    print(response.json())
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")

"""Extracts News from Api"""
def extract_news():
    article_list = []
    for article in response.json()['articles']:
        data = {
            "source": article['source'],
            "title": article['title'],
            "author": article['author'],
            "description": article['description'],
            "url": article['url'],
            "publishedAt": article['publishedAt'],
            "content": article['content']
        }
        article_list.append(data)
    df = pd.DataFrame(article_list)
    df.to_csv('news_data.csv')
    return article_list

extract_news()

stocks_in_demand = ["AAPL", "GOOGL", "MSFT", "TSLA", "META", "NVDA", "AMZN", "JPM", "BAC", "GS", "V", "WMT", "JNJ", "UNH", "DIS"]

ticker_symbols = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "MSFT": "Microsoft",
    "TSLA": "Tesla",
    "META": "Meta OR Facebook",
    "NVDA": "Nvidia",
    "AMZN": "Amazon",
    "JPM": "JPMorgan OR JP Morgan",
    "BAC": "Bank of America",
    "GS": "Goldman Sachs",
    "V": "Visa",
    "WMT": "Walmart",
    "JNJ": "Johnson & Johnson",
    "UNH": "UnitedHealth OR United Health",
    "DIS": "Disney"
}
