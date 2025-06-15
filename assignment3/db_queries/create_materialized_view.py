from sqlalchemy import create_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv # Add this import

load_dotenv() # Add this line to load .env file

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, client_encoding='latin-1')

# SQL to create PostGIS extension if it doesn't exist
create_postgis_extension_query = """
CREATE EXTENSION IF NOT EXISTS postgis;
"""

create_view_query = """
CREATE MATERIALIZED VIEW IF NOT EXISTS bus_positions_filtered_materialize AS
SELECT  
        row_number() OVER () AS id,
        ordem, 
        latitude,
        longitude,
		ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography as geom,
        TO_TIMESTAMP(datahora / 1000) as datahora,
        velocidade,
        linha,
        TO_TIMESTAMP(datahoraservidor / 1000) as datahoraservidor
        
FROM bus_positions
WHERE EXTRACT(HOUR FROM TO_TIMESTAMP(datahoraservidor / 1000)) BETWEEN 4 AND 23
AND linha IN ('483', '864', '639', '3', '309', '774', '629', '371', '397', '100', '838', '315', '624', '388', '918', '665', '328', '497', '878', '355', '138', '606', '457', '550', '803', '917', '638', '2336', '399', '298', '867', '553', '565', '422', '756', '186012003', '292', '554', '634', '232', '415', '2803', '324', '852', '557', '759', '343', '779', '905', '108');
"""

add_index_query = """
CREATE INDEX IF NOT EXISTS idx_linha ON bus_positions_filtered_materialize (linha);
"""

with engine.connect() as conn:
    conn.execute(text(create_postgis_extension_query)) # Execute PostGIS extension creation
    conn.commit() # Commit extension creation
    print("Attempted to create PostGIS extension if not exists.")

    conn.execute(text(create_view_query))
    print("Attempted to create materialized view.")
    
    conn.execute(text(add_index_query))
    print("Attempted to create index on materialized view.")
    
    conn.commit()
    print("All operations committed.")

