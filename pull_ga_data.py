import os
import pandas as pd
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric
)

load_dotenv()

def get_ga_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_CREDENTIALS_PATH")
    return BetaAnalyticsDataClient()

def pull_traffic_report(start_date="30daysAgo", end_date="today"):
    client = get_ga_client()
    property_id = os.getenv("GA4_PROPERTY_ID")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="pagePath"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViews"),
            Metric(name="conversions"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    response = client.run_report(request)

    rows = []
    for row in response.rows:
        record = {}
        for i, dim in enumerate(response.dimension_headers):
            record[dim.name] = row.dimension_values[i].value
        for i, metric in enumerate(response.metric_headers):
            record[metric.name] = row.metric_values[i].value
        rows.append(record)

    df = pd.DataFrame(rows)
    print(f"✅ Pulled {len(df)} rows from GA4")
    return df

if __name__ == "__main__":
    df = pull_traffic_report()
    df.to_csv("raw_ga_data.csv", index=False)
    print("Saved to raw_ga_data.csv")