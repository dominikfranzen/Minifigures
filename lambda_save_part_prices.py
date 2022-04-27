from save_part_prices import fetch_and_save_part_prices 

def lambda_handler(event, context):   
    fetch_and_save_part_prices(0)