import database_handling as db
import auth
from datetime import datetime, date

parts_list = db.select_parts_to_check()
client = auth.auth_on_bricklink()
capture_week = str(date.today().isocalendar()[0])+str(date.today().isocalendar()[1])

def generate_parts_pricelist(part_id, part_color_id):
    part_prices_list = []
    id = str(capture_week)+part_id+'-'+part_color_id  
    no_parts_in_market_identifier = 0  
    url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?new_or_used=U&color_id='+str(part_color_id)
    response = client.get(url)
    data = response.json()['data']
    if data['total_quantity'] == 0:
        url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?color_id='+str(part_color_id)
        data = response.json()['data']
    if data['total_quantity'] == 0:
        no_parts_in_market_identifier = 1
    part_price_item = generate_parts_price_item(id, part_id, part_color_id, data['min_price'], data['total_quantity'], no_parts_in_market_identifier)
    part_prices_list.append(part_price_item)
    print(part_price_item)
    return part_prices_list

def generate_parts_price_item(id, part_id, part_color_id, unit_price, quantity, no_parts_in_market_identifier):
    part_price_item = {
        'id': id,
        'part_id': part_id,
        'part_color_id': part_color_id,
        'capture_week': capture_week,
        'unit_price': unit_price,
        'quantity': quantity,
        'no_parts_in_market': no_parts_in_market_identifier
        }
    return part_price_item

def fetch_and_save_part_prices():
    for part in parts_list:
        part_id = part.split("-")[0]
        part_color_id = part.split("-")[1]
        db.save_part_prices(generate_parts_pricelist(part_id, part_color_id))