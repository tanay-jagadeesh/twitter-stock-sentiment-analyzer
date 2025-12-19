import sqlite3
import pandas as pd 

conn = sqlite3.connect('news.sentiment.db')
conn2 = sqlite3.connect('stock_value.db')

c = conn.cursor()
c2 = conn2.cursor()

c.execute("SELECT * FROM articles ")
article = c.fetchone()

# The published_at is at index 6
published_at = article[6]
print("Full timestamp:", published_at)

# Extract just the date (first 10 characters)
just_date = published_at[:10]
print("Just the date:", just_date)

c2.execute("SELECT * FROM stock_prices ")
stock_price = c2.fetchone()
just_stock_date = stock_price[1]
print("Stock date: ", just_stock_date)

# Load articles into DataFrame
articles_df = pd.read_sql_query("SELECT * FROM articles", conn)

# Load stock prices into DataFrame  
stocks_df = pd.read_sql_query("SELECT * FROM stock_prices", conn2)

# clean up the dates so they match format
articles_df['date'] = articles_df['published_at'].str[:10]  
stocks_df['date'] = stocks_df['date'].str[:10]  

# Now merge them by ticker AND date
merged_df = articles_df.merge(stocks_df, on=['ticker', 'date'], how='inner')

print(f"Found {len(merged_df)} matches!")
print(merged_df.head())

grouped = merged_df.groupby(['ticker', 'date'])

daily_stats = grouped.agg({
    'article_id': 'count',
    'source': 'nunique',
    'title': lambda x: ' | '.join(x),
    'open': 'first',
    'close': 'first',
    'volume': 'first',
    'price_change_pct': 'first'
})

print("\nDaily stats:")
print(daily_stats.head())

# Rename columns to match master dataset format
daily_stats = daily_stats.rename(columns={
    'article_id': 'article_count',
    'source': 'source_count',
    'title': 'titles_combined',
    'open': 'open_price',
    'close': 'close_price'
})

# Reset index to make ticker and date regular columns
daily_stats = daily_stats.reset_index()

print("\nMaster dataset:")
print(daily_stats.head())

daily_stats['next_day_change'] = (daily_stats.groupby('ticker')['close_price'].shift(-1)- daily_stats['close_price']) / daily_stats['close_price'] * 100

conn.commit()

conn.close()