import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def load_to_db(df: pd.DataFrame, table_name: str = "ga_traffic"):
    db_url = os.getenv("DB_URL")
    engine = create_engine(db_url)

    # Write to DB — replace table each run, or use 'append' for incremental
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",   # Options: 'replace', 'append', 'fail'
        index=False,
        chunksize=1000,
    )
    print(f"✅ Loaded {len(df)} rows into '{table_name}'")

    # Verify
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f"   DB row count: {count}")

if __name__ == "__main__":
    df = pd.read_csv("clean_ga_data.csv")
    load_to_db(df)