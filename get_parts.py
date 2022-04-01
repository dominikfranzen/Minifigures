import auth
import json

def get_minifigure_id():    
    with open('clustering/categories.json') as categories:
        minifigure_id = json.load(categories)[18]['minifigure_ids'][1]
        return minifigure_id

client = auth.auth_on_bricklink()
url = 'https://api.bricklink.com/api/store/v1/items/minifig/'+get_minifigure_id()+'/subsets?direction=in'
response = client.get(url)

parts_list = []
json_data = response.json()['data'][0]['entries'][0]['item']
#aktueller Stand: Der command eine Zeile weiter oben gibt das Dict des ersten Teils aus der API aus.
print(json_data)