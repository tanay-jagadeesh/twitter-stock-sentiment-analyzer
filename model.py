import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, root_mean_squared_error, r2_score, mean_absolute_error

# Load train/val/test sets
X_train = pd.read_csv('X_train.csv')
X_val = pd.read_csv('X_val.csv')
X_test = pd.read_csv('X_test.csv')

y_train = pd.read_csv('y_train.csv')
y_val = pd.read_csv('y_val.csv')
y_test = pd.read_csv('y_test.csv')

#created model
reg_model = LinearRegression()

#trained model
reg_model.fit(X_train, y_train)

#predictions
reg_model_predictions = reg_model.predict(X_val)

# Decision Tree Model
dt_model = DecisionTreeRegressor()
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_val)

# Random Forest Model
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_val)

#Mean Squared Error for Lin Reg
lr_mse = mean_squared_error(y_val, reg_model_predictions)
print(f"Linear Regression MSE: {lr_mse}")

#Mean Squared Error for decision tree
dt_mse = mean_squared_error(y_val, dt_predictions)
print(f"Decision Tree MSE: {dt_mse}")

#Mean Squared Error for random forest
rf_mse = mean_squared_error(y_val, rf_predictions)
print(f"Random Forest MSE: {rf_mse}")

#Root Mean Squared Error for Lin Reg
lr_rmse = root_mean_squared_error(y_val, reg_model_predictions)
print(f"Linear Regression RMSE: {lr_rmse}")

#Root Mean Squared Error for decision tree
dt_rmse = root_mean_squared_error(y_val, dt_predictions)
print(f"Decision Tree RMSE: {dt_rmse}")

#Root Mean Squared Error for random forest
rf_rmse = root_mean_squared_error(y_val, rf_predictions)
print(f"Random Forest RMSE: {rf_rmse}")

#R² Score for Lin Reg
lr_r2 = r2_score(y_val, reg_model_predictions)
print(f"Linear Regression R²: {lr_r2}")

#R² Score for decision tree
dt_r2 = r2_score(y_val, dt_predictions)
print(f"Decision Tree R²: {dt_r2}")

#R² Score for random forest
rf_r2 = r2_score(y_val, rf_predictions)
print(f"Random Forest R²: {rf_r2}")

#MAE for Lin Reg
lr_mae = mean_absolute_error(y_val, reg_model_predictions)
print(f"Linear Regression MAE: {lr_mae}")

#MAE for decision tree
dt_mae = mean_absolute_error(y_val, dt_predictions)
print(f"Decision Tree MAE: {dt_mae}")

#MAE for random forest
rf_mae = mean_absolute_error(y_val, rf_predictions)
print(f"Random Forest MAE: {rf_mae}")

# comparing models and seeing which performed well
comparison_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Decision Tree', 'Random Forest'],
    'MSE': [lr_mse, dt_mse, rf_mse],
    'RMSE': [lr_rmse, dt_rmse, rf_rmse],
    'R²': [lr_r2, dt_r2, rf_r2],
    'MAE': [lr_mae, dt_mae, rf_mae]
})

# searching best model
print("\nBest Models by Metric:")
print(f"  Lowest MSE: {comparison_df.loc[comparison_df['MSE'].idxmin(), 'Model']}")
print(f"  Lowest RMSE: {comparison_df.loc[comparison_df['RMSE'].idxmin(), 'Model']}")
print(f"  Highest R²: {comparison_df.loc[comparison_df['R²'].idxmax(), 'Model']}")
print(f"  Lowest MAE: {comparison_df.loc[comparison_df['MAE'].idxmin(), 'Model']}")

# saved results to csv file
comparison_df.to_csv('model_comparison.csv', index=False)


