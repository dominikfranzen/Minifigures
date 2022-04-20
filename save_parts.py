import auth
import database_handling as db

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

def fetch_and_save_minifigure_parts(category_number):
    minifigure_list = db.get_minifigures_of_category(category_number)
    for minifigure in minifigure_list:
        parts_list = generate_parts_list(minifigure)
        db.save_minifigure_parts(parts_list)