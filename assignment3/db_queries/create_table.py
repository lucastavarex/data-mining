from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"Connecting to database: {database_url}") # Add print statement

if not database_url:
    print("Error: DATABASE_URL environment variable not set.")
    exit()

try:
    engine = create_engine(database_url, client_encoding='latin-1')

    # Create the table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bus_positions (
        ordem VARCHAR(20),
        latitude NUMERIC(9, 6),
        longitude NUMERIC(9, 6),
        datahora BIGINT,
        velocidade SMALLINT,
        linha VARCHAR(10),
        datahoraenvio BIGINT,
        datahoraservidor BIGINT,
        datahora_ts TIMESTAMP,
        datahoraenvio_ts TIMESTAMP,
        datahoraservidor_ts TIMESTAMP
    );
    """
    check_table_exists_query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'bus_positions';
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
        conn.commit() # Add commit
        print("Table 'bus_positions' creation attempted successfully.") # Add success message

        result = conn.execute(text(check_table_exists_query))
        table_exists = result.fetchone()
        if table_exists:
            print(f"Verification: Table '{table_exists[0]}' found in 'public' schema.")
        else:
            print("Verification: Table 'bus_positions' NOT found in 'public' schema.")
        conn.commit() # Ensure this transaction is also committed if any read happened

except Exception as e:
    print(f"An error occurred: {e}") # Add error handling

