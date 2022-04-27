import save_part_prices

def lambda_handler(event, context):   
    save_part_prices.fetch_and_save_part_prices()
