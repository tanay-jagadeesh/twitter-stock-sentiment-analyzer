import sqlite3

conn = sqlite3.connect('news.sentiment.db')

#Create a cursor
c = conn.cursor()

#Create an article table
# language=sql
c.execute("""CREATE TABLE articles (
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
conn.commit()