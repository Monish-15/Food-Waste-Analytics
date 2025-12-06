import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# File paths
summary_path = Path("../data/summary.csv")

print("📊 Loading data...")
df = pd.read_csv(summary_path)
print(f"✅ Loaded {len(df)} records from summary.csv")

# Set style
sns.set(style="whitegrid", palette="Set2")

# --- 1️⃣ Top 10 Countries by Total Waste ---
plt.figure(figsize=(10, 6))
top_countries = df.groupby("_id.country")["total_waste_kg"].sum().nlargest(10)
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top 10 Countries by Total Food Waste (kg)")
plt.xlabel("Total Waste (kg)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("../results/top_countries.png")
plt.show()

# --- 2️⃣ Average Waste per Category ---
plt.figure(figsize=(10, 6))
avg_cat = df.groupby("_id.food_category")["avg_waste_kg"].mean().sort_values(ascending=False)
sns.barplot(x=avg_cat.values, y=avg_cat.index)
plt.title("Average Food Waste by Category (kg)")
plt.xlabel("Average Waste (kg)")
plt.ylabel("Food Category")
plt.tight_layout()
plt.savefig("../results/avg_waste_by_category.png")
plt.show()

# --- 3️⃣ Yearly Waste Trend (All Countries) ---
plt.figure(figsize=(10, 6))
trend = df.groupby("_id.year")["total_waste_kg"].sum().reset_index()
sns.lineplot(data=trend, x="_id.year", y="total_waste_kg", marker="o")
plt.title("Yearly Food Waste Trend (Global)")
plt.xlabel("Year")
plt.ylabel("Total Waste (kg)")
plt.tight_layout()
plt.savefig("../results/yearly_trend.png")
plt.show()

print("✅ All visualizations generated successfully in ../results/")
