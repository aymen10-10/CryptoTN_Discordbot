import json

def load_database():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"sell_offers": [], "buy_offers": []}

def save_database(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)
