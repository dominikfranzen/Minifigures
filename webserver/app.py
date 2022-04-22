from flask import Flask, render_template
import sqlalchemy as db
import json

with open('../db_secrets.json', 'r') as json_data:
    db_secrets = json.load(json_data)
    db_user = db_secrets["db_user"]
    db_password = db_secrets["db_password"]
    db_url = db_secrets["db_url"]
    db_ports = db_secrets["db_ports"]
    db_name = db_secrets["db_name"]

engine = db.create_engine('mysql+pymysql://'+db_user+':'+db_password+'@'+db_url+':'+db_ports+'/'+db_name)
metadata = db.MetaData()
profit_center = db.Table('profit_center', metadata, autoload=True, autoload_with=engine)

app = Flask(__name__)

@app.route('/')
def index():
    with engine.connect() as connection:
        query = connection.execute(profit_center.select()).fetchall()

    return render_template('index.html', minifigures=query)
app.run(host="0.0.0.0", port=80)
