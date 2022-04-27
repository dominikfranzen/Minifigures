from save_minifigure_prices import fetch_and_save_minifigure_prices 

def lambda_handler(event, context):   
    fetch_and_save_minifigure_prices(0)
    fetch_and_save_minifigure_prices(66)
    fetch_and_save_minifigure_prices(73)