import rebrick
import sqlite3
import json
from dotenv import load_dotenv
import os
import csv
import categories
import aiohttp
import asyncio

load_dotenv(dotenv_path='config.env')

api_key = os.getenv('LEGO_API_KEY')
rebrick.init(api_key)

def get_fig_ids_from_csv(file_path):
    fig_ids = []
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            fig_ids.append(row['fig_id'])
    
    return fig_ids

# Example usage
file_path = 'results.csv'  # Replace with the actual file path
fig_ids = get_fig_ids_from_csv(file_path)
total_figs = len(fig_ids)
print(f"Total number of fig_ids: {total_figs}")
# fig_ids = fig_ids[10100:]

# Connect to the SQLite database
db_connection = sqlite3.connect('minifigs.db')
cursor = db_connection.cursor()

progress_log = []  # List to store progress messages

async def insert_to_db_batch(batch):
    """Inserts a batch of rows into the database"""
    cursor.executemany('''
        INSERT INTO minifig_parts (fig_id, element_id, part_num, part_name, category, color_name)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', batch)
    db_connection.commit()

async def get_minifig_elements(session, fig_id, fig_counter, batch, retries=5):
    """Fetches elements and adds them to the batch for database insertion with error handling and progress tracking"""
    for attempt in range(retries):
        try:
            async with session.get(f"https://rebrickable.com/api/v3/lego/minifigs/{fig_id}/parts/") as response:
                if response.status == 200:
                    json_data = await response.json()
                    print(f"Success: Fetched data for {fig_id}")  # Debugging line

                    if 'results' in json_data:
                        for result in json_data['results']:
                            part_id = result['id']
                            part_num = result['part']['part_num']
                            part_name = result['part']['name']
                            category = categories.categories.get(result['part']['part_cat_id'], 'Unknown Category')
                            color_name = result['color']['name']

                            # Append to the batch
                            batch.append((fig_id, part_id, part_num, part_name, category, color_name))

                        print(f"Progress: {fig_counter}/{total_figs} fig_ids processed.")
                    else:
                        print(f"Error processing {fig_id}: 'results' key not found in the response.")
                elif response.status == 429:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited for {fig_id}. Waiting for {wait_time} seconds before retrying...")  # Debugging line
                    await asyncio.sleep(wait_time)
                    with open("not-added.txt", 'a') as log_file:
                        log_file.write(f"Rate limited for {fig_id}. Waiting for {wait_time} seconds before retrying...\n")
                    continue  # Retry the same fig_id
                elif response.status == 403:
                    print(f"Error processing {fig_id}: Forbidden (403). Check API key and permissions.")  # Debugging line
                    break  # Exit loop on 403 error
                else:
                    print(f"Error processing {fig_id}: Received status code {response.status}")  # Debugging line
                    break  # Exit loop on other errors

                break  # Exit the retry loop on success or 403

        except Exception as e:
            print(f"Error processing {fig_id}: {e}")
            await asyncio.sleep(1)  # Wait a moment before retrying on exception

async def fetch_all_minifigs(fig_ids, batch_size=10, delay_between_batches=9):
    async with aiohttp.ClientSession(headers={'Authorization': f'key {api_key}'}) as session:
        for i in range(0, len(fig_ids), batch_size):
            batch = fig_ids[i:i + batch_size]
            tasks = []
            batch_data = []  # Initialize an empty batch for storing data

            for idx, fig_id in enumerate(batch, start=i + 1):
                tasks.append(get_minifig_elements(session, fig_id, idx, batch_data))
            await asyncio.gather(*tasks)

            # Insert the collected batch data into the database after processing the batch
            if batch_data:
                await insert_to_db_batch(batch_data)

            # Delay after each batch
            print(f"Waiting for {delay_between_batches} seconds before processing the next batch...")
            await asyncio.sleep(delay_between_batches)

async def main():
    await fetch_all_minifigs(fig_ids, batch_size=10, delay_between_batches=9)

# Run the async main function
asyncio.run(main())

# Close the database connection
db_connection.close()
