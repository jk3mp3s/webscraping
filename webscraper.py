import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_tesla():
    url = "https://www.tesla.com/careers/search"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    job_cards = soup.find_all('div', class_='tds-job-listing__item')
    for card in job_cards:
        title_tag = card.find('a', class_='tds-link')
        location_tag = card.find('span', class_='tds-job-listing__meta')
        if title_tag:
            jobs.append({
                "Company": "Tesla",
                "Job Title": title_tag.text.strip(),
                "Location": location_tag.text.strip() if location_tag else "N/A",
                "Link": "https://www.tesla.com" + title_tag['href'],
                "Date Posted": "",
                "Start Date": "",
                "End Date": ""
            })
    return jobs


def scrape_city_of_toronto():
    url = "https://jobs.toronto.ca/jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    rows = soup.find_all('tr', class_='job')
    for row in rows:
        title_tag = row.find('a')
        location = row.find('td', class_='location')
        date_posted = row.find('td', class_='posted')
        if title_tag:
            jobs.append({
                "Company": "City of Toronto",
                "Job Title": title_tag.text.strip(),
                "Location": location.text.strip() if location else "N/A",
                "Link": "https://jobs.toronto.ca" + title_tag['href'],
                "Date Posted": date_posted.text.strip() if date_posted else "",
                "Start Date": "",
                "End Date": ""
            })
    return jobs

def main():
    all_jobs = []


    scraper_functions = [
        scrape_tesla,
        scrape_city_of_toronto,
    ]

    for scraper in scraper_functions:
        try:
            jobs = scraper()
            all_jobs.extend(jobs)
            print(f"Scraped {len(jobs)} jobs from {jobs[0]['Company'] if jobs else 'Unknown'}")
        except Exception as e:
            print(f"Error with scraper {scraper.__name__}: {e}")

    df = pd.DataFrame(all_jobs)
    df.to_csv("jobs_html_scraper.csv", index=False)
    print("Saved to jobs_html_scraper.csv")

if __name__ == "__main__":
    main()
