import pandas as pd

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_mandi_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Filter Tomato from Dahod APMC
tomato = df[
    (df["commodity"] == "Tomato") &
    (df["market"] == "Dahod(Veg. Market) APMC")
].copy()

# Sort by date
tomato = tomato.sort_values("date")

# Keep required columns
tomato = tomato[["date", "modal_price_rs_quintal"]]

# Save forecasting dataset
tomato.to_csv("dataset/tomato_dahod.csv", index=False)

print("Forecasting dataset prepared!")
print("Total records:", len(tomato))
print("Date range:", tomato["date"].min(), "to", tomato["date"].max())
# Create time-based features
tomato["year"] = tomato["date"].dt.year
tomato["month"] = tomato["date"].dt.month
tomato["day"] = tomato["date"].dt.day
tomato["day_of_week"] = tomato["date"].dt.dayofweek

print("\nFeature preview:")
print(tomato.head())

print("\nDataset columns:")
print(tomato.columns.tolist())
# Create historical price features
tomato["lag_1"] = tomato["modal_price_rs_quintal"].shift(1)
tomato["lag_7"] = tomato["modal_price_rs_quintal"].shift(7)
tomato["lag_30"] = tomato["modal_price_rs_quintal"].shift(30)

print("\nLag feature preview:")
print(tomato.head(10))
# Remove rows with missing lag values
tomato = tomato.dropna()

print("\nFinal forecasting dataset:")
print("Shape:", tomato.shape)
print("\nMissing values:")
print(tomato.isnull().sum())
print("Duplicate dates:", tomato["date"].duplicated().sum())
# Split data chronologically
split_index = int(len(tomato) * 0.8)

train_data = tomato.iloc[:split_index]
test_data = tomato.iloc[split_index:]

print("\nTraining data:", train_data.shape)
print("Testing data:", test_data.shape)

print("Training date range:",
      train_data["date"].min(), "to", train_data["date"].max())

print("Testing date range:",
      test_data["date"].min(), "to", test_data["date"].max())
# Select input features
features = [
    "year",
    "month",
    "day",
    "day_of_week",
    "lag_1",
    "lag_7",
    "lag_30"
]

# Separate features (X) and target (y)
X_train = train_data[features]
y_train = train_data["modal_price_rs_quintal"]

X_test = test_data[features]
y_test = test_data["modal_price_rs_quintal"]

print("\nFeature and target shapes:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

# Initialize the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train the model
model.fit(X_train, y_train)

print("\nRandom Forest model training completed!")
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Predict prices using test data
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation Results")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))
# Baseline evaluation using previous observation
baseline_pred = X_test["lag_1"]

baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
baseline_r2 = r2_score(y_test, baseline_pred)

print("\nBaseline Model Results")
print("MAE:", round(baseline_mae, 2))
print("RMSE:", round(baseline_rmse, 2))
print("R2 Score:", round(baseline_r2, 4))
# Compare model performance

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

plt.plot(
    test_data["date"],
    y_test,
    label="Actual Price"
)

plt.plot(
    test_data["date"],
    baseline_pred,
    label="Baseline Prediction"
)

plt.title("Tomato Price: Actual vs Baseline Prediction")
plt.xlabel("Date")
plt.ylabel("Price (₹ per Quintal)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("dataset/actual_vs_predicted.png")
plt.close()

print("\nComparison graph saved successfully!")
# Feature importance
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance)
from sklearn.ensemble import HistGradientBoostingRegressor

# Initialize Gradient Boosting model
gb_model = HistGradientBoostingRegressor(
    max_iter=200,
    learning_rate=0.05,
    max_leaf_nodes=15,
    random_state=42
)

# Train the model
gb_model.fit(X_train, y_train)

# Predict test prices
gb_pred = gb_model.predict(X_test)

# Evaluate
gb_mae = mean_absolute_error(y_test, gb_pred)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_r2 = r2_score(y_test, gb_pred)

print("\nGradient Boosting Results")
print("MAE:", round(gb_mae, 2))
print("RMSE:", round(gb_rmse, 2))
print("R2 Score:", round(gb_r2, 4))
# Extra Trees model
extra_model = ExtraTreesRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

extra_model.fit(X_train, y_train)

extra_pred = extra_model.predict(X_test)

extra_mae = mean_absolute_error(y_test, extra_pred)
extra_rmse = np.sqrt(mean_squared_error(y_test, extra_pred))
extra_r2 = r2_score(y_test, extra_pred)

print("\nExtra Trees Results")
print("MAE:", round(extra_mae, 2))
print("RMSE:", round(extra_rmse, 2))
print("R2 Score:", round(extra_r2, 4))
# Compare model performance
# Compare all models
results = pd.DataFrame({
    "Model": [
        "Random Forest",
        "Baseline",
        "Gradient Boosting",
        "Extra Trees"
    ],
    "MAE": [
        mae,
        baseline_mae,
        gb_mae,
        extra_mae
    ],
    "RMSE": [
        rmse,
        baseline_rmse,
        gb_rmse,
        extra_rmse
    ],
    "R2 Score": [
        r2,
        baseline_r2,
        gb_r2,
        extra_r2
    ]
})

print("\nFinal Model Comparison:")
print(results)

results.to_csv("dataset/model_comparison.csv", index=False)

import joblib

# Save trained models
joblib.dump(model, "models/random_forest.pkl")
joblib.dump(gb_model, "models/gradient_boosting.pkl")
joblib.dump(extra_model, "models/extra_trees.pkl")

print("\nModels saved successfully!")