import pandas as pd

df = pd.read_csv('features_scaled.csv')
print(df.columns)

#defined target variable
df['target'] = df['next_day_change']

#creating feature matrix X
#starting by dropping columns that are not needed for the prediction

matrix_x = df.drop(columns = ['ticker', 'date', 'date_dt', 'target', 'next_day_change'])

matrix_y = df['target']

#splitting data
#train 70%, validation 15% and then test 15% (old, middle, new)

n = len(df)

train_end = int(n * 0.70)

val_end = int(n * 0.85) #NOTE: where it ends/automatically goes to test end

#first 70%
X_train = matrix_x[:train_end]

#next 15%
X_val = matrix_x[train_end:val_end]

#final 15%
X_test = matrix_x[val_end:]

#first 70%
Y_train = matrix_y[:train_end]

#next 15%
Y_val = matrix_y[train_end:val_end]

#final 15%
Y_test = matrix_y[val_end:]

# Save train/val/test sets
X_train.to_csv('X_train.csv', index=False)
X_val.to_csv('X_val.csv', index=False)
X_test.to_csv('X_test.csv', index=False)

Y_train.to_csv('y_train.csv', index=False)
Y_val.to_csv('y_val.csv', index=False)
Y_test.to_csv('y_test.csv', index=False)

print(f"Saved train/val/test splits:")
print(f"Train: {len(X_train)} rows")
print(f"Val: {len(X_val)} rows")
print(f"Test: {len(X_test)} rows")
