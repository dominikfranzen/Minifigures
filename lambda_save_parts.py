import save_parts

def lambda_handler(event, context):   
    save_parts.fetch_and_save_minifigure_parts(0)
    save_parts.fetch_and_save_minifigure_parts(66)
    save_parts.fetch_and_save_minifigure_parts(73)