import database_handling as db
import auth

part_id = '970c11'
part_color_id = 5

client = auth.auth_on_bricklink()
url = 'https://api.bricklink.com/api/store/v1/items/part/'+part_id+'/price?new_or_used=U&color_id='+str(part_color_id)
response = client.get(url)
price_list = response.json()['data']
#function to safe price details to db to be written
print(price_list)

