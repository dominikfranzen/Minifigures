import auth
import database_handling as db
from datetime import datetime

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
            print(minifigure_price_item)
    return minifigure_prices_list

def fetch_and_save_minifigure_prices(category_number):
    minifigure_list = db.get_minifigures_of_category(category_number)
    for minifigure in minifigure_list:
        minifigure_prices = generate_minifigure_pricelist(minifigure)
        db.save_minifigure_prices(minifigure_prices)