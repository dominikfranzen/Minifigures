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

query = text('\
drop view if exists latest_min_part_prices; \
drop view if exists latest_min_minifigure_prices; \
drop view if exists min_price_overview; \
drop view if exists profit_center; \
 \
create view latest_min_part_prices as \
select part_id, \
       part_color_id, \
       request_date, \
       min(unit_price) as min_part_price, \
       no_parts_in_market \
    from (select part_id, part_color_id, max(capture_date) as request_date, unit_price, no_parts_in_market \
            from part_prices group by part_id, part_color_id) as max_capture_date \
group by part_id, part_color_id; \
 \
create view latest_min_minifigure_prices as \
select minifigure_id, request_date, min(unit_price) as min_minifigure_price \
    from (select minifigure_id, max(capture_date) as request_date, unit_price \
            from minifigure_prices group by minifigure_id) as max_capture_date \
group by minifigure_id; \
 \
create view min_price_overview as \
select minifigure_parts.*, \
       latest_min_part_prices.min_part_price, \
       sum(minifigure_parts.part_quantity*latest_min_part_prices.min_part_price) as min_price_multiple_parts, \
       latest_min_minifigure_prices.min_minifigure_price, \
       sum(latest_min_part_prices.no_parts_in_market) as missing_parts \
    from minifigure_parts \
left join latest_min_part_prices on minifigure_parts.part_color = latest_min_part_prices.part_color_id and minifigure_parts.part_id = latest_min_part_prices.part_id \
left join latest_min_minifigure_prices on minifigure_parts.minifigure_id = latest_min_minifigure_prices.minifigure_id \
group by minifigure_id; \
 \
create view profit_center as \
select minifigure_id, \
       min_price_multiple_parts, \
       min_minifigure_price, \
       min_minifigure_price-min_price_multiple_parts as profit \
    from min_price_overview \
where missing_parts = 0 \
order by profit desc \
limit 50;')

result = connection.execute(query)