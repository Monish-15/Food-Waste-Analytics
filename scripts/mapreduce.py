# scripts/mapreduce_jobs.py
from pymongo import MongoClient
import os
import json

MONGO_URI = "mongodb://localhost:27017/"
DB = "foodDB"
COL = "waste"

client = MongoClient(MONGO_URI)
db = client[DB]
coll = db[COL]

def total_waste_by_country(output_collection="total_waste_country"):
    map_func = """
    function() {
        var c = this.country || this.location || "Unknown";
        var w = parseFloat(this.waste_tonnes) || 0;
        emit(c, w);
    }
    """
    reduce_func = """
    function(key, values) {
        return Array.sum(values);
    }
    """
    coll.map_reduce(map_func, reduce_func, output_collection)
    print("MapReduce written to", output_collection)

def waste_by_year(output_collection="waste_by_year"):
    map_func = """
    function() {
        var y = this.year || (this.date ? this.date.substring(0,4) : "Unknown");
        var w = parseFloat(this.waste_tonnes) || 0;
        emit(y, w);
    }
    """
    reduce_func = "function(k, vals){ return Array.sum(vals); }"
    coll.map_reduce(map_func, reduce_func, output_collection)
    print("MapReduce written to", output_collection)

def top_wasted_items(output_collection="top_wasted_items"):
    map_func = """
    function() {
        var item = this.item || this.product || "Unknown";
        var w = parseFloat(this.waste_tonnes) || 0;
        emit(item.toLowerCase(), w);
    }
    """
    reduce_func = "function(k, vals){ return Array.sum(vals); }"
    coll.map_reduce(map_func, reduce_func, output_collection)
    print("MapReduce written to", output_collection)

if __name__ == "__main__":
    total_waste_by_country()
    waste_by_year()
    top_wasted_items()
