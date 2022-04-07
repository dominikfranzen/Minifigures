import api_auth
import json

def get_minifigure_parts(category_number):    
    with open('clustering/categories.json') as categories:
        minifigure_ids = json.load(categories)[category_number]['minifigure_ids']
        for element in minifigure_ids:
            print(element)
            print(generate_parts_list(element))
        return minifigure_ids

def generate_parts_list(minifigure_id):
    client = api_auth.auth_on_bricklink()
    url = 'https://api.bricklink.com/api/store/v1/items/minifig/'+minifigure_id+'/subsets?direction=in'
    response = client.get(url)
    parts_json = response.json()['data']
    parts_count = len(parts_json)
    parts_list = []
    for i in range(0,parts_count):
        parts_item_dict = {
            'part_number': parts_json[i]['entries'][0]['item']['no'],
            'part_color': parts_json[i]['entries'][0]['color_id'],
            'qantity': parts_json[i]['entries'][0]['quantity']
        }
        parts_list.append(parts_item_dict)
    return parts_list
    
#print(generate_parts_list(response))
get_minifigure_parts(15)



