import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.makedirs("../output", exist_ok=True)

df = pd.read_csv("../dataset/ultimate_housing_dataset.csv")

print(df.head())

plt.figure(figsize=(12, 8))

sns.heatmap(
    df.select_dtypes(include='number').corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig(
    "../output/heatmap.png",
    bbox_inches="tight"
)

plt.figure(figsize=(10, 6))

sns.scatterplot(
    x=df["area_sqft"],
    y=df["price"],
    hue=df["city"]
)

plt.title("Area vs Price Analysis")

plt.savefig(
    "../output/area_vs_price.png",
    bbox_inches="tight"
)

print("\nEDA Analysis Completed Successfully")
