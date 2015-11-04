import json
from pymongo import MongoClient

with open('shirt_data.json', 'r') as infile:
    data = json.load(infile)
    client = MongoClient()
    db = client.test
    for line in data:
        try: 
            line = {
                "merchant": line["merchant"], 
                "category": line["category"], 
                "price": line["price"], 
                "description": line["description"], 
                "url": line["url"], 
                "on_sale": line["on_sale"], 
                "part_number": line["part_number"], 
                "brand": line["brand"], 
                "image": line["image"], 
                "name": line["name"] 
            }
        except:
            continue
        db.shirt.insert_one(line)
