
# FILE: main.py
# PURPOSE: The master controller — runs all 3 steps in order:
#          1. Pull data from Google Analytics
#          2. Clean and transform the data
#          3. Load clean data into PostgreSQL

from pull_google_analytics_data import pull_traffic_report
from clean_data import clean_ga_data
from load_to_db import load_to_db


def run_pipeline(start_date="2026-04-01", end_date="today"):
    """
    Runs the full marketing data pipeline from start to finish.
    start_date: Fixed at April 1st 2026 — our data starting point
    end_date:   Always 'today' — so every run includes the latest data
    """

    # STEP 1 — Pull raw traffic data from Google Analytics
    print("── Step 1: Pulling from GA4 ──")
    raw_df = pull_traffic_report(start_date, end_date)

    # STEP 2 — Clean and transform the raw data
    print("\n── Step 2: Cleaning data ──")
    clean_df = clean_ga_data(raw_df)

    # STEP 3 — Load the clean data into PostgreSQL
    print("\n── Step 3: Loading to database ──")
    load_to_db(clean_df, table_name="ga_traffic")

    print("\n🎉 Pipeline complete!")


# This runs the pipeline when you type: python main.py
if __name__ == "__main__":
    run_pipeline()