import json
import os

DATABASE_FILE = "database.json"

def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {"vendeurs": [], "acheteurs": [], "transactions": []}
    
    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_database(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
