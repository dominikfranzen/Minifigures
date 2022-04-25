import database_handling as db
import auth
from datetime import datetime

parts_list = db.select_parts_to_check()
client = auth.auth_on_bricklink()
capture_date = datetime.now().strftime('%Y-%m-%d')

def generate_parts_pricelist(part_id, part_color_id):    
    url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?new_or_used=U&color_id='+str(part_color_id)
    response = client.get(url)
    price_list = response.json()['data']['price_details']
    part_prices_list = []
    if len(price_list) == 0:
        url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?color_id='+str(part_color_id)
        price_list = response.json()['data']['price_details']
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
        if part_color_id == 0:
            part_color_id = ''
        db.save_part_prices(generate_parts_pricelist(part_id, part_color_id))

#fetch_and_save_part_prices(parts_list)
#fetch_and_save_part_prices(['20482-88', '4599b-7', '4697b-11', '4733-88', '4740-88', '85861-85', '11211-1', '25269-1', '30136-1', '3021-156', '3022-1', '3023-156', '33172-4', '33183-36', '35480-1', '3700-1', '87580-1', '99206-1', '973pb4009c01-5', '68523pb01-85', '973pb4108c01-4', '3626cpb2721-90', '973pb4107c01-88', '3626cpb2718-68', '69539pb01-68', '973pb4105c01-77', '3626c-77', '68615pb01-77', '973pb4104c01-85', '970c00pb1149-88', '973pb4110c01-88', '10301pb05-88', '3626cpb2720-88', '41879-68', '973pb4109c01-1', '87570pb03-2', '973pb4103c01-2', '11090-55', '15395-1', '4070-1', '53451-5', '553c-1', '57900-1', '33183-88', '3626cpb2229-1', '47905-1', 'x164pb21-1', '87610pb09-95', '970c00pb1152-120', '973pb4119c01-120', '970c00pb1151-11', '973pb4118c01-11', '970c04pb12-86', '973pb4120c01-4', '21269-1', '3626cpb2728-90', '970c00pb1153-2', '973pb4121c01-2', '973pb4168c02-11', '973pb4367c01-11', '3626cpb2923-1', '970c00pb1285-86', '973pb4503c01-69', '21566c01pb04-1', '61189pb18-1', '970c00pb1283-1', '973pb4501c01-1', '2524-88', '973pb4255c01-2', '11217pb18-77', '3626cpb2953-28', '970c77pb14-11', '973pb4556c01-77', '28631pb19-77', '3626cpb2983-28', '78643pb02-77', '11217pb17-77', '3626cpb2954-90', '970c00pb1322-77', '973pb4557c01-77', '3021-85', '970c77pb13-11', '973pb4398c01-77', '3626cpb2980-88', '970c00pb1326-120', '973pb4597c01-11', '42861pb04-11', '64567-1', '970c01pb56-11', '973pb4507c01-1', 'bb0673pb03-3', '3626cpb2850-28', '87610pb14-48', '970c77pb12-11', '973pb4396c01-11', '3626cpb2920-90', '78642pb01-4', '970c00pb1281-11', '973pb4499c01-11', '19888pb02-0', '3626cpb2919-88', '973pb4498c01-11', '3626cpb2921-11', '78643pb01-11', '79230-11', '970c00pb1282-11', '973pb4500c01-11', '3626cpb2927-90', '78645pb01-77', '970c00pb1286-77', '973pb4504c01-77', '3626cpb2882-90', '87610pb15-7', '970c85pb29-88', '973pb4438c01-85', '87610pb17-77', '970c86pb38-88', '973pb4679c01-86', '3626cpb2922-88', '970c00pb1284-69', '973pb4502c01-69', '3626cpb2925-88', '3626cpb2926-90', '973pb4437c01-120', '78645pb02-115', '970c00pb1298-120', '973pb4530c01-85', '78643pb03-55', '87610pb16-55', '970c00pb1299-85', '973pb4531c01-85', '99780-85', '99781-3', '25128pb009-5', '3957b-12', '53020-86', '3626cpb2928-28', '973pb4508c01-1', '3626cpb2924-88', '970c00pb1320-1', '973pb4505c01-1', '18674-11', '25893u-11', '30503-1', '32828-11', '35480-85', '58176-11', '60474-85', '87994-85', '92946-85', '93061-11', '970c00pb1348-11', '973pb4656c01-11', '69857-11', '1656-90', '3626cpb3100-90', '970c00pb1341-11', '973pb4646c01-11', '29634-47', '3626cpb3101-90', '970c00pb1343-1', '973pb4645c01-1', '66132pb01-68', '970c00pb1342-1', '973pb4649c01-85', '970c00pb1345-88', '973c94-88', '98120pb02-88', '3626cpb3102-150', '973pb4647c01-69'])
print(generate_parts_pricelist('33648c01pb03', 1))