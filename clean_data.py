
# FILE: clean_data.py
# PURPOSE: Clean and transform the raw data pulled from GA4
#          before loading it into the PostgreSQL database

import pandas as pd


def clean_ga_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the raw GA4 data and returns a clean, structured table.
    Steps: rename columns, fix data types, remove junk, add channel column.
    """

    # Rename GA4's default column names to clean snake_case names
    df = df.rename(columns={
        "date":                     "date",
        "sessionSource":            "source",
        "sessionMedium":            "medium",
        "country":                  "country",
        "deviceCategory":           "device",
        "pagePath":                 "page_path",
        "sessions":                 "sessions",
        "totalUsers":               "total_users",
        "newUsers":                 "new_users",
        "bounceRate":               "bounce_rate",
        "averageSessionDuration":   "avg_session_duration_sec",
        "screenPageViews":          "page_views",
        "conversions":              "conversions",
    })

    # Convert date column from string (e.g. "20260401") to proper date format
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

    # Convert metric columns from text to numbers
    numeric_cols = [
        "sessions", "total_users", "new_users",
        "bounce_rate", "avg_session_duration_sec",
        "page_views", "conversions"
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Round decimals for cleaner presentation
    df["bounce_rate"] = df["bounce_rate"].round(4)
    df["avg_session_duration_sec"] = df["avg_session_duration_sec"].round(2)

    # Replace GA4 placeholder values with cleaner alternatives
    df.replace({
        "(not set)": None,
        "(none)":    "direct",
        "(direct)":  "direct"
    }, inplace=True)

    # Remove rows where core metrics are missing
    df = df.dropna(subset=["sessions", "total_users"])

    # Remove any duplicate rows
    df = df.drop_duplicates()

    # Add a channel column — groups traffic into meaningful marketing categories
    def classify_channel(row):
        src = str(row.get("source", "")).lower()
        med = str(row.get("medium", "")).lower()
        if med == "organic":                    return "Organic Search"
        if med in ["cpc", "ppc", "paid"]:       return "Paid Search"
        if med == "email":                      return "Email"
        if med in ["social", "social-network"]: return "Social"
        if src == "direct" or med == "none":    return "Direct"
        if med == "referral":                   return "Referral"
        return "Other"

    df["channel"] = df.apply(classify_channel, axis=1)

    print(f"✅ Cleaned data: {len(df)} rows")
    return df


if __name__ == "__main__":
    raw = pd.read_csv("raw_ga_data.csv")
    cleaned = clean_ga_data(raw)
    cleaned.to_csv("clean_ga_data.csv", index=False)
    print("Saved clean data to clean_ga_data.csv")