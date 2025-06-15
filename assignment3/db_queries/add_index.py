from sqlalchemy import create_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv # Add this import

load_dotenv() # Add this line to load .env file

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, client_encoding='latin-1')  

# Corrected view name and added IF NOT EXISTS
create_index_sql = """
CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_linha ON bus_positions_filtered_materialize(linha);

CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_ordem ON bus_positions_filtered_materialize(ordem);

-- Assuming x and y columns might not exist in bus_positions_filtered_materialize
-- If they do, you can uncomment the following. Check the view definition in create_materialized_view.py
-- CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_x_y ON bus_positions_filtered_materialize(x, y);

CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_ordem_linha ON bus_positions_filtered_materialize(ordem, linha);

CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_datahoraservidor ON bus_positions_filtered_materialize (datahoraservidor);

-- Assuming time_ranking column might not exist. If it does, uncomment:
-- CREATE INDEX IF NOT EXISTS idx_bus_pos_filtered_time_ranking ON bus_positions_filtered_materialize(time_ranking);
"""

try:
    with engine.connect() as conn:
        conn.execute(text(create_index_sql))
        conn.commit()
        print("Successfully created indexes on bus_positions_filtered_materialize (if they didn't already exist).")
except Exception as e:
    print(f"An error occurred while creating indexes: {e}")