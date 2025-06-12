import os
import importlib.util
import csv
import pandas as pd
import clean_listings
from datetime import datetime

def load_scrapers(folder_path):
    scrapers = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # strip .py
            file_path = os.path.join(folder_path, filename)

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find a scrape_ function inside the module
            for attr in dir(module):
                if attr.startswith("scrape_") and callable(getattr(module, attr)):
                    scrapers.append(getattr(module, attr))
                    break  # Only one scrape function per module

    return scrapers

def main():
    all_jobs = []
    folder = "webscrapers"

    scrapers = load_scrapers(folder)

    for scraper in scrapers:
        try:
            jobs = scraper()
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"Error running {scraper.__name__}: {e}")

    # Sort alphabetically by Company
    all_jobs.sort(key=lambda x: x["Company"])

    # Write to CSV
    file_exists = os.path.isfile("all_jobs.csv")
    with open("all_jobs.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Company", "Job Title", "Location", "Link","Date Added"])

        if not file_exists:
            writer.writeheader()

        for job in all_jobs:
            job["Date Added"] = datetime.now().strftime("%Y-%m-%d")
            writer.writerow(job)

    print(f"\n✅ Scraped {len(all_jobs)} jobs into all_jobs.csv")

    clean_listings.clean_jobs("all_jobs.csv")

    # Optional: also save as Excel
    try:
        df = pd.read_csv("all_jobs.csv")
        df.to_excel("all_jobs.xlsx", index=False, engine="openpyxl")
        print("📄 Also saved as all_jobs.xlsx")
    except Exception as e:
        print(f"⚠️ Failed to save Excel file: {e}")

    

if __name__ == "__main__":
    main()