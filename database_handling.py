from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Date
import sqlalchemy as db
import json
from datetime import date

capture_week = int(str(date.today().isocalendar()[0])+str(date.today().isocalendar()[1]))

def get_db_url_from_credentials():
    with open('db_secrets.json', 'r') as json_data:
        db_secrets = json.load(json_data)
        db_user = db_secrets["db_user"]
        db_password = db_secrets["db_password"]
        db_url = db_secrets["db_url"]
        db_ports = db_secrets["db_ports"]
        db_name = db_secrets["db_name"]
    db_url = 'mysql+pymysql://'+db_user+':'+db_password+'@'+db_url+':'+db_ports+'/'+db_name
    return db_url

engine = db.create_engine(get_db_url_from_credentials())
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
    Column('capture_week', Integer),
    Column('unit_price', Float),
    Column('quantity', Integer)
)
part_prices = Table(
    'part_prices', meta, 
    Column('id', String(50), primary_key = True ),
    Column('part_id', String(50)),
    Column('part_color_id', String(50)),
    Column('capture_week', Integer),
    Column('unit_price', Float),
    Column('quantity', Integer),
    Column('no_parts_in_market', Integer)
)
meta.create_all(engine)

def get_minifigures_of_category(category_number):
    minifigure_ids_to_request = []
    with open('clustering/categories.json') as categories:
        minifigure_ids = json.load(categories)[category_number]['minifigure_ids']
    with engine.connect() as connection:
        minifigure_prices_checked_this_week = connection.execute(minifigure_prices.select().where(minifigure_prices.columns.capture_week == capture_week)).fetchall()
        already_gathered = []
        for row in minifigure_prices_checked_this_week:
            already_gathered.append(row[1])
    for minifigure in minifigure_ids:
        if minifigure not in already_gathered:
            minifigure_ids_to_request.append(minifigure)
    return minifigure_ids_to_request

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
    gathered_already =['sw1051-0'] #exceptions
    parts_list = []
    with engine.connect() as connection:
        db_parts_checklist = connection.execute(minifigure_parts.select()).fetchall()
        part_prices_checked_this_week = connection.execute(part_prices.select().where(part_prices.columns.capture_week == capture_week)).fetchall()
    for row in part_prices_checked_this_week:
        gathered_already.append(row[1]+"-"+row[2])
    for row in db_parts_checklist:
        part_id = row[2]
        part_color_id = row[3]
        key = part_id+'-'+part_color_id
        if key not in parts_list and key not in gathered_already:
            parts_list.append(key)
    return parts_list