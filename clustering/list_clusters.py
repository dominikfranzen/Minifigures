import json

with open('categories.json') as json_file:
    minifigure_categories = json.load(json_file)
    counter = 0
for item in minifigure_categories:
    category_id = item['category_id']
    first_minifig_in_cat = item['minifigure_ids'][0]
    nbr_of_minifigures = len(item['minifigure_ids'])
    print(str(counter)+"-"+str(category_id)+"-"+first_minifig_in_cat+"-"+str(nbr_of_minifigures))
    counter += 1 