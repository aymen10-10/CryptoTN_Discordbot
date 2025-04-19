import json
import os
import random
import string

def load_database():
    if not os.path.exists("database.json"):
        with open("database.json", "w") as f:
            json.dump({"vendeurs": [], "acheteurs": [], "transactions": {}}, f)
    with open("database.json", "r") as f:
        return json.load(f)

def save_database(db):
    with open("database.json", "w") as f:
        json.dump(db, f, indent=4)

def generate_transaction_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
