import sqlite3
import pandas as pd


#Loading CSV file into a pandas DF
df = pd.read_csv('news_data.csv')

#Cleaning Data
df.columns = df.columns.str.strip()

conn = sqlite3.connect('news.sentiment.db')

#Create a cursor
c = conn.cursor()

#Create an article table
# language=sql
c.execute("""CREATE TABLE IF NOT EXISTS articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    title TEXT,
    description TEXT,
    content TEXT,
    source TEXT,
    published_at TEXT,
    url TEXT UNIQUE,
    author TEXT
)""")

#create a stocks table
c.execute("""CREATE TABLE IF NOT EXISTS stocks (
    ticker TEXT PRIMARY KEY,
    company_name TEXT  
)  
""")

def insert_article(ticker, title, description, content, source, published_at, url, author):
    c.execute("INSERT INTO articles(ticker, title, description, content, source, published_at, url, author) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
              (ticker, title, description, content, source, published_at, url, author))

def query_article(ticker, from_date, to_date):
    c.execute("SELECT * FROM articles WHERE ticker = ? AND published_at <= ? AND published_at >= ?",
    (ticker, from_date, to_date))
    return c.fetchall()

conn.commit()

for i, row in df.iterrows():
    try:
        insert_article(row['ticker'], row['title'], row['description'], row['content'], str(row['source']), row['publishedAt'], row['url'], row['author'])
    except sqlite3.IntegrityError:
        print(f"Skipping duplicate article: {row['url']}")
        continue

conn.commit()
conn.close()