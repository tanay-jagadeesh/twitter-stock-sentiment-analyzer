import sqlite3

conn = sqlite3.connect('news.sentiment.db')

c = conn.cursor()

c.execute("SELECT * FROM articles ")
print(c.fetchone())









conn.commit()

conn.close()