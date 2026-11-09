import pandas as pd

file_path = "dataset/bharat_mandi_gujarat_2011_2026.csv"

df = pd.read_csv(file_path)

# Remove completely empty column
df = df.drop(columns=["variety_id"])

# Remove rows with missing dates
df = df.dropna(subset=["date"])

# Remove duplicate rows
df = df.drop_duplicates()
df["max_price_rs_quintal"] = df["max_price_rs_quintal"].fillna(
    df["modal_price_rs_quintal"]
)

# Save cleaned dataset
df.to_csv("dataset/cleaned_mandi_data.csv", index=False)

print("Cleaning completed!")
print("Cleaned dataset shape:", df.shape)
print("Remaining missing values:")
print(df.isnull().sum())
print("\nRow with missing maximum price:")
print(df[df["max_price_rs_quintal"].isnull()])
print("\nTotal unique commodities:")
print(df["commodity"].nunique())

print("\nCommodity names:")
print(df["commodity"].unique())
print("\nTop 15 commodities by record count:")
print(df["commodity"].value_counts().head(15))
selected = ["Tomato", "Onion", "Wheat", "Groundnut", "Cotton"]

print("\nSelected commodity records:")
print(df[df["commodity"].isin(selected)]["commodity"].value_counts())

print("\nDate range for selected commodities:")
print(
    df[df["commodity"].isin(selected)]
    .groupby("commodity")["date"]
    .agg(["min", "max", "count"])
)
print("\nTop 10 markets for Tomato:")
print(
    df[df["commodity"] == "Tomato"]["market"]
    .value_counts()
    .head(10)
)
tomato_dahod = df[
    (df["commodity"] == "Tomato") &
    (df["market"] == "Dahod(Veg. Market) APMC")
]

print("\nDahod Tomato data:")
print("Records:", len(tomato_dahod))
print("Date range:")
print(tomato_dahod["date"].min(), "to", tomato_dahod["date"].max())
print("\nDahod Tomato Price Statistics:")
print(tomato_dahod["modal_price_rs_quintal"].describe())
import matplotlib.pyplot as plt

tomato_dahod["date"] = pd.to_datetime(tomato_dahod["date"])

tomato_dahod = tomato_dahod.sort_values("date")

plt.figure(figsize=(12, 5))
plt.plot(
    tomato_dahod["date"],
    tomato_dahod["modal_price_rs_quintal"]
)

plt.title("Historical Tomato Prices - Dahod APMC")
plt.xlabel("Date")
plt.ylabel("Modal Price (₹/quintal)")
plt.grid(True)
plt.tight_layout()
plt.savefig("dataset/tomato_price_trend.png")
plt.close()
tomato_dahod["month"] = tomato_dahod["date"].dt.month

monthly_prices = tomato_dahod.groupby("month")[
    "modal_price_rs_quintal"
].mean()

print("\nAverage Tomato Price by Month:")
print(monthly_prices)
plt.figure(figsize=(10, 5))

monthly_prices.plot(kind="bar")

plt.title("Average Monthly Tomato Prices - Dahod APMC")
plt.xlabel("Month")
plt.ylabel("Average Price (₹/quintal)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("dataset/monthly_tomato_prices.png")
plt.close()

print("\nMonthly chart saved successfully!")
yearly_monthly = tomato_dahod.pivot_table(
    index=tomato_dahod["date"].dt.year,
    columns=tomato_dahod["date"].dt.month,
    values="modal_price_rs_quintal",
    aggfunc="mean"
)

print("\nYear-wise monthly average prices:")
print(yearly_monthly.tail(5).round(2))