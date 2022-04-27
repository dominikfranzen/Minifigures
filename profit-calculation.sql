drop view if exists latest_min_part_prices;
drop view if exists latest_min_minifigure_prices;
drop view if exists min_price_overview;
drop view if exists profit_center;

create view latest_min_part_prices as
select part_id, part_color_id, max(capture_week), unit_price as min_part_price, no_parts_in_market
            from part_prices group by part_id, part_color_id;

create view latest_min_minifigure_prices as
select minifigure_id, max(capture_week) as latest_request, min_minifigure_price
    from (select minifigure_id, capture_week, min(unit_price) as min_minifigure_price
            from minifigure_prices group by minifigure_id, capture_week) as min_prices_by_capture_date
group by minifigure_id;

create view min_price_overview as
select minifigure_parts.*,
       latest_min_part_prices.min_part_price,
       sum(minifigure_parts.part_quantity*latest_min_part_prices.min_part_price) as min_price_multiple_parts,
       latest_min_minifigure_prices.min_minifigure_price,
       sum(latest_min_part_prices.no_parts_in_market) as missing_parts
    from minifigure_parts
left join latest_min_part_prices on minifigure_parts.part_color = latest_min_part_prices.part_color_id and minifigure_parts.part_id = latest_min_part_prices.part_id
left join latest_min_minifigure_prices on minifigure_parts.minifigure_id = latest_min_minifigure_prices.minifigure_id
group by minifigure_id;

create view profit_center as
select minifigure_id,
       round(min_price_multiple_parts, 2) as min_price_multiple_parts,
       round(min_minifigure_price, 2) as min_minifigure_price,
       round(min_minifigure_price-min_price_multiple_parts, 2) as profit
    from min_price_overview
where missing_parts = 0
order by profit desc
limit 50;