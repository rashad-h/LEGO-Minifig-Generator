import csv
import sqlite3

# Connect to the SQLite database
db_connection = sqlite3.connect('minifigs.db')
cursor = db_connection.cursor()

# Function to get all parts for a given fig_id from the database
def get_parts_for_fig(cursor, fig_id):
    query = '''
    SELECT category, part_name, color_name
    FROM minifig_parts
    WHERE fig_id = ?
    '''
    cursor.execute(query, (fig_id,))
    return cursor.fetchall()

# Function to get the count of "Minifig" parts for a given fig_id
def get_minifig_part_count(cursor, fig_id):
    query = '''
    SELECT COUNT(*)
    FROM minifig_parts
    WHERE fig_id = ? AND category LIKE 'Minifig%'
    '''
    cursor.execute(query, (fig_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Function to format the parts in the desired format
def format_parts(fig_id, description, parts, minifig_part_count):
    output = []
    # output.append(f'"{fig_id}", "{description}"')
    for part in parts:
        category, part_name, color_name = part
        output.append(f'"{category}": "{part_name} <{color_name}>"')
    # Add the minifig parts count at the end
    # output.append(f'"Minifig parts count": "{minifig_part_count}"')

    return "\n".join(output)

# Read the CSV file
csv_file = 'results.csv'  # Replace with the path to your CSV file
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, fieldnames=["fig_id", "description"])
    i = 0
    # Loop through each row in the CSV file
    for row in csv_reader:
        fig_id = row['fig_id']
        description = row['description']

        # Get all the parts for the fig_id from the database
        parts = get_parts_for_fig(cursor, fig_id)

        # Format the output in the desired format
        if parts:
            minifig_part_count = get_minifig_part_count(cursor, fig_id)
            if minifig_part_count > 1:
                formatted_output = format_parts(fig_id, description, parts, minifig_part_count)

                # Insert the cleaned data into the new table
                cursor.execute('''
                    INSERT OR REPLACE INTO parsed_minifig_data (fig_id, description, formatted_parts)
                    VALUES (?, ?, ?)
                ''', (fig_id, description, formatted_output))


                # print(fig_id, description)
                # print(formatted_output)
                # print()  # Add a new line for readability
        else:
            print(f'No parts found for fig_id: {fig_id}\n')

        i += 1
        print(i)

# Close the database connection
db_connection.commit()
db_connection.close()
