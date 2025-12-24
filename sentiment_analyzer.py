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

#created histogram for sentiment distribution visualization
plt.hist(articles_df['compound'])
plt.xlabel('Compound Sentiment Score')
plt.ylabel('Number of Articles')
plt.title('Distribution of Sentiment Scores')
plt.show()

daily_stats = pd.read_csv('daily_stats.csv')

# Merge sentiment with price data
sentiment_df = daily_sentiment.reset_index()
combined = daily_stats.merge(sentiment_df, on=['ticker', 'date'])

# Filter for AAPL only
aapl = combined[combined['ticker'] == 'AAPL']

# Plot
plt.plot(aapl['date'], aapl['compound'], label='Sentiment')
plt.plot(aapl['date'], aapl['close_price'], label='Price')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Sentiment vs. Price for AAPL')
plt.legend()
plt.show()

volatility = articles_df.groupby('ticker')['compound'].std()

print(f"The stocks with the most volatility are {volatility.sort(ascending = False)}")

# Calculating correlations

# Sort by ticker and date to ensure proper order
daily_stats = daily_stats.sort_values(['ticker', 'date'])

# Calculate next day price change (as percentage)
daily_stats['next_day_change'] = daily_stats.groupby('ticker')['close_price'].pct_change().shift(-1)

# Count articles per day
article_volume = articles_df.groupby(['ticker', 'date']).size().reset_index(name='article_count')

# Merge them together
combined_data = daily_stats.merge(article_volume, on=['ticker', 'date'], how='left')
combined_data['article_count'] = combined_data['article_count'].fillna(0)

# Calculate correlation between article volume and next-day price change
correlation = combined_data['article_count'].corr(combined_data['next_day_change'])
print(f"Correlation between article volume and next-day price change: {correlation}")

# 2. Sentiment score to next-day price change
# Get average daily sentiment per ticker
daily_sentiment_avg = articles_df.groupby(['ticker', 'date'])['compound'].mean().reset_index(name='avg_sentiment')

# Merge with combined_data
combined_data = combined_data.merge(daily_sentiment_avg, on=['ticker', 'date'], how='left')

# Calculate correlation
sentiment_corr = combined_data['avg_sentiment'].corr(combined_data['next_day_change'])
print(f"Correlation between sentiment score and next-day price change: {sentiment_corr}")

# 3. Bullish % to price movement
# Count bullish articles per day
bullish_counts = articles_df[articles_df['classify'] == 'bullish'].groupby(['ticker', 'date']).size().reset_index(name='bullish_count')

# Merge with combined_data to get total article count
combined_data = combined_data.merge(bullish_counts, on=['ticker', 'date'], how='left')
combined_data['bullish_count'] = combined_data['bullish_count'].fillna(0)

# Calculate bullish percentage
combined_data['bullish_pct'] = (combined_data['bullish_count'] / combined_data['article_count']).fillna(0)

# Calculate correlation
bullish_corr = combined_data['bullish_pct'].corr(combined_data['next_day_change'])
print(f"Correlation between bullish % and next-day price change: {bullish_corr}")