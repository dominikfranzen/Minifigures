from save_parts import fetch_and_save_minifigure_parts 

def lambda_handler(event, context):   
    fetch_and_save_minifigure_parts(0)