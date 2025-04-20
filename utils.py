import json
import os

DB_FILE = "database.json"

def load_database():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"vendeurs": [], "acheteurs": []}, f)

    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_offer(offer_type, offer_data):
    data = load_database()
    data[offer_type].append(offer_data)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
