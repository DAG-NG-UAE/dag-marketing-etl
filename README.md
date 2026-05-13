# DAG Industries Nigeria - Marketing Data Pipeline

Automated ETL pipeline that pulls marketing data from Google Analytics 4,
cleans it, and loads it into a PostgreSQL database.

## Tech Stack
- Python 3.12
- Google Analytics Data API (v1beta)
- pandas
- SQLAlchemy + psycopg2
- PostgreSQL

## Project Structure
ga-pipeline/
├── pull_ga_data.py # Pull data from GA4
├── clean_data.py # Clean and transform data
├── load_to_db.py # Load data into PostgreSQL
├── main.py # Run the full pipeline
├── .env # Environment variables (not pushed to GitHub)
└── credentials.json # Google service account key (not pushed to GitHub)

## Setup
1. Add your credentials.json file
2. Create a .env file with your GA4 Property ID and DB URL
3. Install dependencies: pip install -r requirements.txt
4. Run: python main.py