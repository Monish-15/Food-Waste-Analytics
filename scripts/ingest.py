# scripts/ingest.py
import pandas as pd
import json
import os
from tqdm import tqdm
import subprocess

DATA_CSV = os.path.join("..", "data", "food_waste.csv")
OUT_JSON = os.path.join("..", "data", "food_waste.json")

def csv_to_jsonlines(csv_path=DATA_CSV, out_path=OUT_JSON):
    df = pd.read_csv(csv_path, low_memory=False)
    # Optional: normalize column names
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in df.fillna("").to_dict(orient="records"):
            f.write(json.dumps(rec, default=str) + "\n")
    print(f"Wrote {out_path}")

def mongo_import(db="foodDB", collection="waste", json_path=OUT_JSON):
    # mongoimport expects either --jsonArray or newline-delimited JSON. We use newline-delimited.
    cmd = [
        "mongoimport",
        "--db", db,
        "--collection", collection,
        "--file", json_path,
        "--jsonArray", "--drop"
    ]
    # If file is newline-delimited rather than a single array, remove --jsonArray flag. Adjust accordingly.
    # Here we assume JSON array; if newline-n, remove the --jsonArray option.
    # For safety, try with jsonArray; if it fails comment the flag out.
    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

if __name__ == "__main__":
    csv_to_jsonlines()
    print("Now import using mongoimport CLI (or uncomment call below to call it from Python).")
    # mongo_import()
from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["food_waste_db"]
collection = db["food_waste_data"]

# Read JSON objects line by line
with open("../data/food_waste.json", "r") as f:
    lines = f.readlines()

for line in lines:
    try:
        record = json.loads(line.strip())
        collection.insert_one(record)
    except json.JSONDecodeError:
        continue

print(f"✅ Inserted {len(lines)} records into MongoDB (line-by-line import).")
