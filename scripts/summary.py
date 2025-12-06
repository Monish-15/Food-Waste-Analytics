from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm

print("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
db = client["food_waste_db"]
collection = db["food_waste_data"]

print("✅ Connected. Aggregating data...")

pipeline = [
    {
        "$addFields": {
            "waste_kg_num": {
                "$convert": {
                    "input": "$waste_kg",
                    "to": "double",
                    "onError": 0,
                    "onNull": 0
                }
            },
            "waste_cost_num": {
                "$convert": {
                    "input": "$waste_cost",
                    "to": "double",
                    "onError": 0,
                    "onNull": 0
                }
            }
        }
    },
    {
        "$group": {
            "_id": {
                "country": "$country",
                "year": "$year",
                "food_category": "$food_category"
            },
            "total_waste_kg": {"$sum": "$waste_kg_num"},
            "total_cost": {"$sum": "$waste_cost_num"},
            "avg_waste_kg": {"$avg": "$waste_kg_num"},
            "records": {"$sum": 1}
        }
    },
    {"$sort": {"_id.country": 1, "_id.year": 1}}
]

# Run aggregation
results = list(collection.aggregate(pipeline, allowDiskUse=True))

# Convert to DataFrame
data = []
for r in tqdm(results, desc="Processing results"):
    entry = {
        "Country": r["_id"]["country"],
        "Year": r["_id"]["year"],
        "Food Category": r["_id"]["food_category"],
        "Total Waste (kg)": round(r["total_waste_kg"], 2),
        "Total Cost (₹)": round(r["total_cost"], 2),
        "Average Waste (kg)": round(r["avg_waste_kg"], 2),
        "Records Count": r["records"]
    }
    data.append(entry)

df = pd.DataFrame(data)
output_path = "../data/summary.csv"
df.to_csv(output_path, index=False)

print(f"\n✅ Summary file saved at: {output_path}")
print(f"📊 {len(df)} grouped records generated.")
