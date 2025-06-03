import os
import importlib.util
import csv

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
    with open("all_jobs.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Company", "Job Title", "Location", "Link"])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"\n✅ Scraped {len(all_jobs)} jobs into all_jobs.csv")

if __name__ == "__main__":
    main()