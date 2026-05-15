# DAG Industries Nigeria — Marketing Data Pipeline

## What This Project Does

This project automatically pulls marketing data from DAG Industries Nigeria's 
Google Analytics account, cleans it up, and stores it in a PostgreSQL database 
where it can be queried, analysed and connected to reporting dashboards.

Instead of manually logging into Google Analytics every day and downloading 
CSV files, this pipeline does everything automatically with one command:

```bash
python main.py
```

---

## The Story Behind It

DAG Industries Nigeria needed a reliable way to track and analyse their website 
marketing performance — where visitors come from, which products they look at, 
which countries they're in, and how engaged they are.

This pipeline solves that by:
- Connecting directly to Google Analytics via the official API
- Pulling clean, structured data into a database every time it runs
- Making that data ready for SQL analysis and dashboard reporting

---

## What the Data Covers

Every time the pipeline runs, it pulls the following information for each visit:

| Data Point | What It Tells Us |
|---|---|
| Date | When the visit happened |
| Source | Where the visitor came from (Google, Facebook, direct etc) |
| Medium | How they arrived (organic search, referral, social etc) |
| Channel | Grouped marketing channel (Organic Search, Social, Direct etc) |
| Country | Which country the visitor is from |
| Device | Whether they used desktop, mobile or tablet |
| Page Path | Which page on the website they visited |
| Sessions | Number of visits |
| Total Users | Number of unique people |
| New Users | First time visitors |
| Bounce Rate | Percentage who left without clicking anything |
| Avg Session Duration | How long they stayed on the site (in seconds) |
| Page Views | How many pages they viewed |
| Conversions | How many completed a goal |

---

## Tech Stack

| Tool | What It's Used For |
|---|---|
| Python 3.12 | The programming language everything is written in |
| Google Analytics Data API (v1beta) | Official Google API for pulling GA4 data |
| pandas | Cleaning, transforming and structuring the data |
| SQLAlchemy | Connecting Python to the PostgreSQL database |
| psycopg2 | The PostgreSQL driver that SQLAlchemy uses under the hood |
| python-dotenv | Keeps sensitive credentials out of the code |
| PostgreSQL 18 | The database where clean data is stored |
| pgAdmin 4 | Visual tool for managing and querying the database |
| VS Code | Code editor |

---

## Project Structure

ga-pipeline/
│
├── pull_google_analytics_data.py   # Step 1: Connects to GA4 and pulls raw data
├── clean_data.py                   # Step 2: Cleans and transforms the raw data
├── load_to_db.py                   # Step 3: Loads clean data into PostgreSQL
├── main.py                         # Master controller — runs all 3 steps
│
├── .env                            # Your private credentials (never pushed to GitHub)
├── credentials.json                # Google service account key (never pushed to GitHub)
├── .gitignore                      # Tells Git which files to ignore
├── requirements.txt                # List of Python libraries needed
└── README.md                       # This file

---

## How the Pipeline Works

Think of it like a factory assembly line:

Google Analytics (raw data)
↓
pull_google_analytics_data.py  →  fetches raw data from GA4 API
↓
clean_data.py                  →  cleans, transforms and structures the data
↓
load_to_db.py                  →  loads clean data into PostgreSQL
↓
PostgreSQL — ga_traffic table  →  ready for analysis and dashboards

---

## File by File Explanation

---

### 1. pull_google_analytics_data.py

This file is responsible for connecting to Google Analytics and pulling the 
raw marketing data.

It authenticates using the service account credentials in `credentials.json`, 
connects to the DAG Industries Nigeria GA4 property (Property ID: 421868260), 
and requests 6 dimensions and 7 metrics for every day from April 1st 2026 
to today.

Google sends the data back in a complex format — this file unpacks it into 
a clean table (DataFrame) that the next step can work with.

**Key function:**
```python
pull_traffic_report(start_date="2026-04-01", end_date="today")
```
- `start_date` is fixed at April 1st 2026 — our data starting point
- `end_date` is always "today" — so every run automatically includes the latest data

---

### 2. clean_data.py

This file takes the raw messy data from Google Analytics and transforms it 
into something clean, consistent and ready for analysis.

Here is exactly what it does step by step:

**Step 1 — Rename columns**
Google Analytics uses technical names like `sessionSource` and `totalUsers`. 
This step renames them to clean, readable names like `source` and `total_users`.

**Step 2 — Fix data types**
Google sends everything as text — even numbers. This step converts sessions, 
users, bounce rate etc into proper numbers so we can do maths on them.

**Step 3 — Fix the date format**
Google sends dates as `"20260401"` — this converts them to proper dates 
like `2026-04-01`.

**Step 4 — Clean up placeholder values**
Google Analytics uses `(not set)`, `(none)` and `(direct)` as placeholders 
when data is missing. This step replaces them with cleaner values or NULL.

**Step 5 — Remove bad rows**
Drops any rows where sessions or users are missing — these rows are useless 
for analysis.

**Step 6 — Remove duplicates**
Removes any rows that appear more than once.

**Step 7 — Add a Channel column**
Creates a new column that groups traffic into meaningful marketing categories:

| Source/Medium | Channel |
|---|---|
| google / organic | Organic Search |
| any / cpc or ppc | Paid Search |
| any / email | Email |
| any / social | Social |
| direct / none | Direct |
| any / referral | Referral |

---

### 3. load_to_db.py

This file takes the clean data and loads it into the `ga_traffic` table 
in the `marketing_db` PostgreSQL database.

It uses SQLAlchemy to connect to PostgreSQL and pandas to write the data 
in chunks of 1,000 rows at a time — which keeps things efficient even 
when the dataset grows large.

The `if_exists="replace"` setting means every time the pipeline runs, 
the old data is replaced with a complete fresh load from April 1st to today.

After loading, it runs a quick count query to confirm the rows landed 
successfully in the database.

---

### 4. main.py

This is the master controller. It doesn't do any heavy lifting itself — 
it simply calls the other three files in the right order:

Step 1 → pull_google_analytics_data.py
Step 2 → clean_data.py
Step 3 → load_to_db.py

This is the only file you ever need to run:
```bash
python main.py
```

---

## Setup Instructions

### Prerequisites
- Python 3.12 installed
- PostgreSQL installed and running
- Google Cloud project with GA4 Data API enabled
- Service account with Viewer access to the GA4 property

---

### Step 1 — Clone the Repository
```bash
git clone https://github.com/DAG-NG-UAE/dag-marketing-etl.git
cd dag-marketing-etl
```

---

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 3 — Add Your Credentials

Create a `.env` file in the project folder:
```env
GA4_PROPERTY_ID=421868260
GOOGLE_CREDENTIALS_PATH=./credentials.json
DB_URL=postgresql://postgres:yourpassword@localhost:5432/marketing_db
```

Place your `credentials.json` service account key file in the project folder.

---

### Step 4 — Create the Database

In pgAdmin or psql run:
```sql
CREATE DATABASE marketing_db;
```

---

### Step 5 — Run the Pipeline
```bash
python main.py
```

You should see:

Step 1: Pulling from GA4 ──
a. Pulled 1489 rows from GA4
Step 2: Cleaning data ──
b. Cleaned data: 1489 rows
Step 3: Loading to database ──
c. Loaded 1489 rows into 'ga_traffic'
DB row count: 1489
Pipeline complete!

---

## Querying the Data

Once the pipeline runs, open pgAdmin and use these queries to analyse the data:

**Where is our traffic coming from?**
```sql
SELECT channel, SUM(sessions) AS total_sessions
FROM ga_traffic
GROUP BY channel
ORDER BY total_sessions DESC;
```

**Which countries are our users from?**
```sql
SELECT country, SUM(sessions) AS total_sessions
FROM ga_traffic
GROUP BY country
ORDER BY total_sessions DESC;
```

**Which pages are most visited?**
```sql
SELECT page_path, SUM(sessions) AS total_sessions
FROM ga_traffic
GROUP BY page_path
ORDER BY total_sessions DESC
LIMIT 10;
```

**Weekly traffic trend**
```sql
SELECT DATE_TRUNC('week', date) AS week,
       SUM(sessions) AS total_sessions
FROM ga_traffic
GROUP BY week
ORDER BY week ASC;
```

---

## Security Notes

The following files contain sensitive credentials and are excluded from 
GitHub via `.gitignore`:

- `.env` — contains your database password and GA4 Property ID
- `credentials.json` — contains your Google service account private key

Never share or commit these files. If the credentials.json key is ever 
exposed, revoke it immediately in Google Cloud Console and generate a new one.

---

## Next Steps

- [ ] Schedule the pipeline to run automatically daily using Windows Task Scheduler
- [ ] Connect `marketing_db` to Power BI or Metabase for visual dashboards
- [ ] Move PostgreSQL to a cloud server (AWS RDS or Supabase) for team access
- [ ] Add error handling and email alerts if the pipeline fails
- [ ] Expand data pull to include additional GA4 dimensions and metrics