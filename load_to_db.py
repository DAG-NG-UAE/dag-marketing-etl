
# FILE: load_to_db.py
# PURPOSE: Load the cleaned GA4 data into PostgreSQL database

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load database connection details from .env file
load_dotenv()


def load_to_db(df: pd.DataFrame, table_name: str = "ga_traffic"):
    """
    Takes the cleaned data and loads it into PostgreSQL.
    table_name: The table to load into (default: ga_traffic)
    if_exists='replace': Clears the table and reloads fresh data every run
    """

    # Get the database connection URL from .env file
    db_url = os.getenv("DB_URL")

    # Create a connection engine — this is the bridge between Python and PostgreSQL
    engine = create_engine(db_url)

    # Write the DataFrame into the PostgreSQL table
    df.to_sql(
        name=table_name,        # Table name in PostgreSQL
        con=engine,             # The database connection
        if_exists="replace",    # Replace table completely on each run
        index=False,            # Don't write the row numbers as a column
        chunksize=1000,         # Write 1000 rows at a time (handles large datasets)
    )

    print(f"✅ Loaded {len(df)} rows into '{table_name}'")

    # Verify the load was successful by counting rows in the database
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f"   DB row count: {count}")


if __name__ == "__main__":
    df = pd.read_csv("clean_ga_data.csv")
    load_to_db(df)