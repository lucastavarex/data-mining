import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv # Add this import

load_dotenv() # Add this line to load .env file

# Load and process data from a JSON files
def load_and_process_data(file_path):
    
    data = pd.read_json(file_path, encoding='latin-1') 
    # Convert columns to the correct data types
    data['latitude'] = data['latitude'].str.replace(',', '.').astype(float)
    data['longitude'] = data['longitude'].str.replace(',', '.').astype(float)
    data['velocidade'] = data['velocidade'].astype(int)
    

    return data

# Process all JSON files in a folder
def process_folder(folder_path, engine):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            data = load_and_process_data(file_path)
            data.to_sql('bus_positions', engine, if_exists='append', index=False, method='multi')
        

# Path to the main folder with the JSON files
main_folder_path = "C:/" # TODO: Update this to the correct folder path e.g. "final/" or "validation/"

# Create a connection to the database
database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, client_encoding='latin-1')



# Add a column for ID if it doesn't exist
add_id_column_query = """
ALTER TABLE bus_positions
ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
"""

with engine.connect() as conn:
    conn.execute(text(add_id_column_query))
    conn.commit()

# After fixing the ID column, you'll likely want to process the files.
# Make sure main_folder_path is correct before uncommenting and running the next line:
# process_folder(main_folder_path, engine)
# print(f"Finished processing files in {main_folder_path}")