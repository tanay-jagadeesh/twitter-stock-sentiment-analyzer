import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

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
mean_squared_error(y_val, reg_model_predictions)

#Mean Squared Error for decision tree
mean_squared_error(y_val, dt_predictions)


