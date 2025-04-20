import json
import os

DATABASE_FILE = "database.json"

def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {"vendeurs": [], "acheteurs": []}
    with open(DATABASE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_database(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
import json

def save_database(database, path="database.json"):
    with open(path, "w") as f:
        json.dump(database, f, indent=4)
