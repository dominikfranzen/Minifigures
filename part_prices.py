import database_handling as db
import auth
from datetime import datetime

parts_list = db.select_parts_to_check()
client = auth.auth_on_bricklink()
capture_date = datetime.now().strftime('%Y-%m-%d')

def generate_parts_pricelist(part_id, part_color_id):    
    url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?new_or_used=U&color_id='+str(part_color_id)+'&region=europe'
    response = client.get(url)
    price_list = response.json()['data']['price_detail']
    part_prices_list = []
    if len(price_list) == 0:
        url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?color_id='+str(part_color_id)+'region=europe'
        price_list = response.json()['data']['price_detail']
    if len(price_list) == 0:
        id = str(capture_date)+part_id+'-'+part_color_id+'-'+'1'
        part_price_item = generate_parts_price_item(id, part_id, part_color_id, 0, 0, 1)
        part_prices_list.append(part_price_item)

    for item in range(0, len(price_list)):
        entry = price_list[item]
        id = str(capture_date)+part_id+'-'+part_color_id+'-'+str(item)
        if entry['shipping_available'] == True:    
            unit_price = entry['unit_price']
            quantity = entry['quantity']
            no_parts_in_market_identifier = 0
        else:
            unit_price = 0
            quantity = 0
            no_parts_in_market_identifier = 1
        part_price_item = generate_parts_price_item(id, part_id, part_color_id, unit_price, quantity,no_parts_in_market_identifier)
        part_prices_list.append(part_price_item)
        print(part_price_item)
    return part_prices_list

def generate_parts_price_item(id, part_id, part_color_id, unit_price, quantity, no_parts_in_market_identifier):
    part_price_item = {
        'id': id,
        'part_id': part_id,
        'part_color_id': part_color_id,
        'capture_date': capture_date,
        'unit_price': unit_price,
        'quantity': quantity,
        'no_parts_in_market': no_parts_in_market_identifier
        }
    return part_price_item

def fetch_and_save_part_prices(parts_list):
    for part in parts_list:
        part_id = part.split("-")[0]
        part_color_id = part.split("-")[1]
        db.insert_to_table(generate_parts_pricelist(part_id, part_color_id), 'part_prices')

fetch_and_save_part_prices(parts_list)