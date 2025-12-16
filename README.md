# Reddit Sentiment Analyzer for Stock Mentions

## What it does
Scrapes r/wallstreetbets, analyzes sentiment around stocks, correlates with price movements

## Data Science concepts
- Natural Language Processing (NLP)
- Sentiment analysis (VADER or transformers)
- Time series analysis
- Correlation analysis
- Data visualization

## Tech stack
- Python
- Reddit API (PRAW)
- NLTK/TextBlob
- pandas
- Streamlit

## Project phases

### Day 1-2: Set up Reddit scraping
- [ ] Get Reddit API credentials (free)
- [ ] Install PRAW: `pip install praw pandas`
- [ ] Create `reddit_scraper.py`
- [ ] Scrape last 100 posts from r/wallstreetbets
- [ ] Extract: post title, body, score, comments, timestamp
- [ ] Save to CSV
- [ ] Commit to GitHub

## Author
tanay-jagadeesh
