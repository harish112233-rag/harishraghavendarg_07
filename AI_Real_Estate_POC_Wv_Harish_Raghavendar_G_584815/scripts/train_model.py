import os
import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

os.makedirs("../output", exist_ok=True)

df = pd.read_csv("../dataset/ultimate_housing_dataset.csv")

df = pd.get_dummies(df, drop_first=True)

X = df.drop("price", axis=1)
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=18,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\n========== MODEL EVALUATION ==========")
print(f"MAE       : {mae:.2f}")
print(f"RMSE      : {rmse:.2f}")
print(f"R2 Score  : {r2:.4f}")

with open("../output/model_metrics.txt", "w") as f:
    f.write("========== MODEL EVALUATION ==========\n")
    f.write(f"MAE       : {mae:.2f}\n")
    f.write(f"RMSE      : {rmse:.2f}\n")
    f.write(f"R2 Score  : {r2:.4f}\n")

pickle.dump(
    model,
    open("../output/house_price_model.pkl", "wb")
)

print("\nModel saved successfully.")
