from sqlalchemy import text
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
metadata = db.MetaData()
connection = engine.connect()
part_prices = db.Table('part_prices', metadata, autoload=True, autoload_with=engine)
minifigure_prices = db.Table('minifigure_prices', metadata, autoload=True, autoload_with=engine)
minifigure_parts = db.Table('minifigure_parts', metadata, autoload=True, autoload_with=engine)

def calculate_profits():
    with open("profit-calculation.sql", "r") as sql_file:
        data = sql_file.read().replace("\n", " ").split(";")
        for item in data:
            if item.strip():
                query = text(item)
                result = connection.execute(query)