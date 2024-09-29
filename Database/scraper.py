import rebrick
import json
from dotenv import load_dotenv
import os
import csv

load_dotenv(dotenv_path='config.env')


api_key = os.getenv('LEGO_API_KEY')
rebrick.init(api_key)


# Function to save results to a CSV file
def save_results(results, filename="results.csv"):
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["fig_id", "description"], quoting=csv.QUOTE_ALL)
        if f.tell() == 0:  # Check if the file is empty
            writer.writeheader()
        writer.writerows(results)

print("Get minifig:")
page_num = 1
results = []
next_url = True

while next_url:
    print(f"Fetching data for page: {page_num}")

    response = rebrick.lego.get_minifigs(page=page_num)
    json_data = json.loads(response.read())
    
    if json_data is None:
        print("Failed to fetch data. Saving progress and exiting.")
        save_results(results)
        break
    
    # Extract 'set_num' and 'name' for each result
    for result in json_data['results']:
        set_num = result['set_num']
        name = result['name']
        results.append({"fig_id": set_num, "description": name})


    save_results(results)
    print(f"Saved progress for page: {page_num}")
    results = []  

    # Update the next URL
    next_url = json_data.get('next')
    if next_url:
        page_num += 1


print(f"Finished processing. Total pages: {page_num}")