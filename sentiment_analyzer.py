import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from text_processor import remove_url, remove_special_characters, lowercase, remove_whitespace
from match_data import cleaned
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect('news.sentiment.db')

# Load articles
articles_df = pd.read_sql_query("SELECT * FROM articles", conn)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Combine title and description/clean text
articles_df['combined_scores'] = (articles_df['title'].fillna('') + ' ' + articles_df['description'].fillna('')).apply(cleaned)

# Get sentiment scores for text
def get_sentiments(txt):
    scores = analyzer.polarity_scores(txt)
    return scores

# Apply VADER to all articles
articles_df['vader_sentiment'] = articles_df['combined_scores'].apply(get_sentiments)

print(f"Sentiment Scores: {articles_df['vader_sentiment']}")

# Extract individual sentiment scores from dictionary
articles_df['neg'] = articles_df['vader_sentiment'].apply(lambda x: x['neg'])

articles_df['neu'] = articles_df['vader_sentiment'].apply(lambda x: x['neu'])

articles_df['pos'] = articles_df['vader_sentiment'].apply(lambda x: x['pos'])

articles_df['compound'] = articles_df['vader_sentiment'].apply(lambda x: x['compound'])

print(articles_df[['title', 'neg', 'neu', 'pos', 'compound']].head())

# Classify sentiment as bullish/bearish/neutral
def classify_sentiment(compound):
    if compound > 0.05:
        return "bullish"
    elif compound < -0.05:
        return "bearish"
    else:
        return "neutral"

articles_df['classify'] = articles_df['compound'].apply(classify_sentiment)

print(articles_df[['title', 'compound', 'classify']].head(10))

# Calculate overall sentiment metrics
print(f"The average compound score: {articles_df['compound'].agg('mean')}")

total = len(articles_df['classify'])

print(f"The % bullish articles: {(articles_df['classify'] == "bullish").sum() / total}")

print(f"The % bearish articles: {(articles_df['classify'] == "bearish").sum() / total}")

print(f"The % neutral articles: {(articles_df['classify'] == "neutral").sum() / total}")

# Calculate sentiment metrics per stock
print(f"The average compound score for each ticker: {articles_df.groupby('ticker')['compound'].mean()}")

# Extract date from timestamp
articles_df['date'] = articles_df['published_at'].str[:10]

# Calculate average sentiment per ticker per day
daily_sentiment = articles_df.groupby(['ticker','date'])['compound'].mean()

# Calculate sentiment momentum (3-day change)
momentum = daily_sentiment - daily_sentiment.shift(3)

print(momentum)

# Convert Series to DataFrame for merging
momentum_df = momentum.reset_index()

# Merge sentiment momentum with articles
merged_df = articles_df.merge(momentum_df, on=['ticker', 'date'], how='inner')
