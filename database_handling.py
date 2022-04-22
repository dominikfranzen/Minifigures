from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Date
import sqlalchemy as db
import json

with open('db_secrets.json', 'r') as json_data:
    db_secrets = json.load(json_data)
    db_user = db_secrets["db_user"]
    db_password = db_secrets["db_password"]
    db_url = db_secrets["db_url"]
    db_ports = db_secrets["db_ports"]
    db_name = db_secrets["db_name"]

engine = db.create_engine('mysql+pymysql://'+db_user+':'+db_password+'@'+db_url+':'+db_ports+'/'+db_name)
meta = MetaData()

minifigure_parts = Table(
    'minifigure_parts', meta, 
    Column('key', String(50), primary_key = True ),
    Column('minifigure_id', String(50)),
    Column('part_id', String(50)),
    Column('part_color', String(50)),
    Column('part_quantity', String(50))
)
minifigure_prices = Table(
    'minifigure_prices', meta, 
    Column('id', String(50), primary_key = True ),
    Column('minifigure_id', String(50)),
    Column('capture_date', Date),
    Column('unit_price', Float),
    Column('quantity', Integer)
)
part_prices = Table(
    'part_prices', meta, 
    Column('id', String(50), primary_key = True ),
    Column('part_id', String(50)),
    Column('part_color_id', String(50)),
    Column('capture_date', Date),
    Column('unit_price', Float),
    Column('quantity', Integer),
    Column('no_parts_in_market', Integer)
)
meta.create_all(engine)

def get_minifigures_of_category(category_number):
    with open('clustering/categories.json') as categories:
        minifigure_ids = json.load(categories)[category_number]['minifigure_ids']
    return minifigure_ids

def save_minifigure_parts(parts_list):
    if len(parts_list) == 0:
        return
    with engine.connect() as connection:
        connection.execute(minifigure_parts.insert(), parts_list)

def save_minifigure_prices(minifigure_pricelist):
    if len(minifigure_pricelist) == 0:
        return
    with engine.connect() as connection:
            connection.execute(minifigure_prices.insert(), minifigure_pricelist)

def save_part_prices(part_pricelist):
    if len(part_pricelist) == 0:
        return
    with engine.connect() as connection:
            connection.execute(part_prices.insert(), part_pricelist)

def select_parts_to_check():
    with engine.connect() as connection:
        query = connection.execute(minifigure_parts.select())
        parts_list = []
        for row in query:
            part_id = row[2]
            part_color_id = row[3]
            key = part_id+'-'+part_color_id
            if key not in parts_list:
                parts_list.append(key)
        return parts_list