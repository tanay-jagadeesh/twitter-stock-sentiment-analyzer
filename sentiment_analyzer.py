import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from text_processor import remove_url, remove_special_characters, lowercase, remove_whitespace

# Connect to database
conn = sqlite3.connect('news.sentiment.db')

# Load articles
articles_df = pd.read_sql_query("SELECT * FROM articles", conn)


