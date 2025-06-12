import pandas as pd
from datetime import datetime, timedelta

def clean_jobs(file_path="jobs.csv"):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("No jobs.csv found to clean.")
        return

    # Convert scrape date to datetime
    df["Scrape Date"] = pd.to_datetime(df["Scrape Date"], errors='coerce')

    # Remove duplicates based on key columns
    df = df.drop_duplicates(subset=["Company", "Job Title", "Location", "Link"])

    # Remove rows older than 7 days
    cutoff = datetime.today() - timedelta(days=7)
    df = df[df["Scrape Date"] >= cutoff]

    df.to_csv(file_path, index=False)
    print(f"Cleaned job data saved to {file_path}")

if __name__ == "__main__":
    clean_jobs()