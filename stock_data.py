import pandas as pd
import sqlite3
import yfinance as yf
from news_headline_scraper import ticker_symbols 

conn = sqlite3.connect('stock_value.db')

c = conn.cursor()

start_date = '2024-01-01'
end_date = '2025-01-01'

def stock_prices():
    for ticker in ticker_symbols:
        ticker = yf.Ticker(ticker)
        data = yf.download(ticker, start = start_date, end = end_date, interval = '1d')
stock_prices()

c.execute("""CREATE TABLE IF NOT EXISTS stock_prices (
    ticker TEXT,
    date TEXT,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume INTEGER,
    price_change_pct REAL
          )      
""")


conn.commit()
conn.close()