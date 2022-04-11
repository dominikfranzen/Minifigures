import auth
import json
import database_handling as udb
from datetime import datetime
import db_secrets

def save_to_db(category_number, identifier):
    db_secrets.get_db_secrets()
    if identifier == 'minifigure_parts' or identifier == 'minifigure_prices':   
        with open('clustering/categories.json') as categories:
            minifigure_ids = json.load(categories)[category_number]['minifigure_ids']
            for element in minifigure_ids:
                if identifier == 'minifigure_parts':
                    udb.insert_to_table(generate_parts_list(element), identifier)
                else:
                    udb.insert_to_table(generate_minifigure_pricelist(element), identifier)
    else:
        print('No valid identifier')


def generate_parts_list(minifigure_id):
    client = auth.auth_on_bricklink()
    url = 'https://api.bricklink.com/api/store/v1/items/minifig/'+minifigure_id+'/subsets?direction=in'
    response = client.get(url)
    parts_json = response.json()['data']
    parts_count = len(parts_json)
    parts_list = []
    for i in range(0,parts_count):
        if len(parts_json) == 0:
            continue
        else:
            entry = parts_json[i]['entries'][0]
            parts_item_dict = {
                'minifigure_id': minifigure_id,
                'part_id': entry['item']['no'],
                'part_color': entry['color_id'],
                'part_quantity': entry['quantity'],
                'key': minifigure_id+entry['item']['no']+str(entry['color_id'])
            }
            parts_list.append(parts_item_dict)
            print(parts_item_dict)
    return parts_list


def generate_minifigure_pricelist(minifigure_id):
    client = auth.auth_on_bricklink()
    url = 'https://api.bricklink.com/api/store/v1/items/minifig/'+minifigure_id+'/price?new_or_used=U'
    response = client.get(url)
    price_list = response.json()['data']['price_detail']
    capture_date = datetime.now().strftime('%Y-%m-%d')
    minifigure_prices_list = []
    for item in range(0, len(price_list)):
        entry = price_list[item]
        if entry['shipping_available'] == True:
            minifigure_price_item = {
                'id': str(capture_date)+minifigure_id+str(item),
                'minifigure_id': minifigure_id,
                'capture_date': capture_date,
                'unit_price': entry['unit_price'],
                'quantity': entry['quantity']
            }
            minifigure_prices_list.append(minifigure_price_item)
            
    return minifigure_prices_list

#save_to_db(0, 'minifigure_parts')
#save_to_db(0, 'minifigure_prices')
