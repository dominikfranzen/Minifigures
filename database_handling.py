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

def insert_to_table(list_of_dicts, tablename):
    if len(list_of_dicts) > 0:
        with engine.connect() as connection:
            if tablename == 'minifigure_parts':
                connection.execute(minifigure_parts.insert(), list_of_dicts)
            elif tablename == 'minifigure_prices':
                connection.execute(minifigure_prices.insert(), list_of_dicts)
            elif tablename == 'part_prices':
                connection.execute(part_prices.insert(), list_of_dicts)

def select_parts_to_check():
    with engine.connect() as connection:
        query = connection.execute(minifigure_parts.select())
        parts_list = []
        for row in query:
            part_id = row[2]
            part_color_id = row[3]
            key = part_id+'-'+part_color_id
            if key in parts_list:
                continue
            else:
                parts_list.append(key)
        return parts_list
