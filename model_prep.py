import pandas as pd

df = pd.read_csv('features_scaled.csv')

#defined target variable
df['target'] = df['next_day_change']
