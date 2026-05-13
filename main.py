from pull_ga_data import pull_traffic_report
from clean_data import clean_ga_data
from load_to_db import load_to_db

def run_pipeline(start_date="30daysAgo", end_date="today"):
    print("── Step 1: Pulling from GA4 ──")
    raw_df = pull_traffic_report(start_date, end_date)

    print("\n── Step 2: Cleaning data ──")
    clean_df = clean_ga_data(raw_df)

    print("\n── Step 3: Loading to database ──")
    load_to_db(clean_df, table_name="ga_traffic")

    print("\n🎉 Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()