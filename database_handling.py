from sqlalchemy import Table, Column, Integer, String, MetaData
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
connection = engine.connect()
meta = MetaData()

minifigure_parts = Table(
    'minifigure_parts', meta, 
    Column('key', String(50), primary_key = True ),
    Column('minifigure_id', String(50)),
    Column('part_id', String(50)),
    Column('part_color', String(50)),
    Column('part_quantity', String(50))
)
meta.create_all(engine)

conn = engine.connect()
ins = minifigure_parts.insert().values(key = 'alp0011346565', minifigure_id= 'alp001')
result = conn.execute(ins)