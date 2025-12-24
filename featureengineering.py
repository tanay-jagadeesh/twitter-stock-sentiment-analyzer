import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler

print("Loading data...")

# Load articles from database
conn = sqlite3.connect('news.sentiment.db')
articles_df = pd.read_sql_query("SELECT * FROM articles", conn)
conn.close()

# Load daily stats (already has price data and article counts)
daily_stats = pd.read_csv('daily_stats.csv')

# Calculate sentiment scores for each article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from text_processor import remove_url, remove_special_characters, lowercase, remove_whitespace
from match_data import cleaned

analyzer = SentimentIntensityAnalyzer()
articles_df['combined_text'] = (articles_df['title'].fillna('') + ' ' + articles_df['description'].fillna('')).apply(cleaned)
articles_df['vader_sentiment'] = articles_df['combined_text'].apply(lambda x: analyzer.polarity_scores(x))
articles_df['compound'] = articles_df['vader_sentiment'].apply(lambda x: x['compound'])

# Classify sentiment
def classify_sentiment(compound):
    if compound > 0.05:
        return "bullish"
    elif compound < -0.05:
        return "bearish"
    else:
        return "neutral"

articles_df['classify'] = articles_df['compound'].apply(classify_sentiment)
articles_df['date'] = articles_df['published_at'].str[:10]

# Start with daily_stats as our base
features = daily_stats.copy()
features = features.sort_values(['ticker', 'date']).reset_index(drop=True)
