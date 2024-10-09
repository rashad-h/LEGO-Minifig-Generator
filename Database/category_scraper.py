import rebrick
import json
from dotenv import load_dotenv
import os
import csv

load_dotenv(dotenv_path='config.env')


api_key = os.getenv('LEGO_API_KEY')
rebrick.init(api_key)


category_dict = {}

category_id = 1



while category_id < 100:
    try:
        response = rebrick.lego.get_category(category_id)            
        json_data = json.loads(response.read())

        category_name = json_data.get('name')
        if category_name:
            category_dict[category_id] = category_name
        print(f"Category ID {category_id} was found. '{category_name}'")
    except:
        print(f"Category ID {category_id} not found. Stopping the loop.")
    category_id += 1



print(category_dict)