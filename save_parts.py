import auth
import database_handling as dbh
import json
import sqlalchemy as db

with open('db_secrets.json', 'r') as json_data:
    db_secrets = json.load(json_data)
    db_user = db_secrets["db_user"]
    db_password = db_secrets["db_password"]
    db_url = db_secrets["db_url"]
    db_ports = db_secrets["db_ports"]
    db_name = db_secrets["db_name"]    

engine = db.create_engine('mysql+pymysql://'+db_user+':'+db_password+'@'+db_url+':'+db_ports+'/'+db_name)
metadata = db.MetaData()
minifigure_parts = db.Table('minifigure_parts', metadata, autoload=True, autoload_with=engine)

def get_db_entries():
    db_entries = []
    with engine.connect() as connection:
        query = connection.execute(minifigure_parts.select()).fetchall()
    for item in query:
        minifigure_id = item[1]
        if minifigure_id not in db_entries:
            db_entries.append(minifigure_id)
    return db_entries

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
    minifigure_list = dbh.get_minifigures_of_category(category_number)
    db_entries = get_db_entries()
    for minifigure in minifigure_list:
        if minifigure not in db_entries:
            parts_list = generate_parts_list(minifigure)
            dbh.save_minifigure_parts(parts_list)