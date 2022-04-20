import json

with open('clustering/categories.json') as categories:
    minifigure_ids = json.load(categories)[0]['minifigure_ids']
    print(minifigure_ids)