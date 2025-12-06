from pymongo import MongoClient
from tqdm import tqdm

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["food_waste_db"]
collection = db["food_waste_data"]

print("Connected to MongoDB ✅")

cursor = collection.find({}, no_cursor_timeout=True)

updated_count = 0

for doc in tqdm(cursor, desc="Processing records"):
    updates = {}

    # Safely convert waste_kg to float
    try:
        waste_kg = float(doc.get("waste_kg", 0))
    except (ValueError, TypeError):
        waste_kg = 0

    # 1️⃣ Calculate waste cost (example: ₹50/kg)
    if "waste_cost" not in doc:
        updates["waste_cost"] = round(waste_kg * 50, 2)

    # 2️⃣ Add season info based on month
    if "season" not in doc:
        month = doc.get("month", 0)
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Autumn"
        updates["season"] = season

    # 3️⃣ Flag high waste incidents
    if "is_high_waste" not in doc:
        updates["is_high_waste"] = waste_kg > 500

    # 4️⃣ Add normalized waste (0–1 scale)
    if "normalized_waste" not in doc:
        normalized = min(waste_kg / 1000, 1.0)
        updates["normalized_waste"] = round(normalized, 4)

    # Apply updates if any
    if updates:
        collection.update_one({"_id": doc["_id"]}, {"$set": updates})
        updated_count += 1

cursor.close()
print(f"\n✅ Updated {updated_count} documents successfully.")
