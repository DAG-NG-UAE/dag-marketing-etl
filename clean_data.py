import pandas as pd

def clean_ga_data(df: pd.DataFrame) -> pd.DataFrame:

    # 1. Rename columns to snake_case
    df = df.rename(columns={
        "date": "date",
        "sessionSource": "source",
        "sessionMedium": "medium",
        "country": "country",
        "deviceCategory": "device",
        "pagePath": "page_path",
        "sessions": "sessions",
        "totalUsers": "total_users",
        "newUsers": "new_users",
        "bounceRate": "bounce_rate",
        "averageSessionDuration": "avg_session_duration_sec",
        "screenPageViews": "page_views",
        "conversions": "conversions",
    })

    # 2. Fix data types
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    numeric_cols = ["sessions", "total_users", "new_users", 
                    "bounce_rate", "avg_session_duration_sec", 
                    "page_views", "conversions"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # 3. Round floats
    df["bounce_rate"] = df["bounce_rate"].round(4)
    df["avg_session_duration_sec"] = df["avg_session_duration_sec"].round(2)

    # 4. Replace GA "(not set)" / "(none)" placeholders
    df.replace({"(not set)": None, "(none)": "direct", "(direct)": "direct"}, inplace=True)

    # 5. Drop rows where core metrics are null
    df = df.dropna(subset=["sessions", "total_users"])

    # 6. Remove duplicates
    df = df.drop_duplicates()

    # 7. Add a derived channel column
    def classify_channel(row):
        src, med = str(row.get("source", "")).lower(), str(row.get("medium", "")).lower()
        if med == "organic": return "Organic Search"
        if med in ["cpc", "ppc", "paid"]: return "Paid Search"
        if med == "email": return "Email"
        if med in ["social", "social-network"]: return "Social"
        if src == "direct" or med == "none": return "Direct"
        if med == "referral": return "Referral"
        return "Other"

    df["channel"] = df.apply(classify_channel, axis=1)

    print(f"✅ Cleaned data: {len(df)} rows")
    return df

if __name__ == "__main__":
    raw = pd.read_csv("raw_ga_data.csv")
    cleaned = clean_ga_data(raw)
    cleaned.to_csv("clean_ga_data.csv", index=False)
    print("Saved to clean_ga_data.csv")