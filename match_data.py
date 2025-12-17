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

# See what you got
print(f"Found {len(merged_df)} matches!")
print(merged_df.head())







conn.commit()

conn.close()