from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def scrape_cisco():

    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to Cisco's Canada job listings page
    driver.get("https://jobs.cisco.com/jobs/SearchJobs/?21178=%5B207800%5D&21178_format=6020&21180=%5B33821095%2C166%2C164%2C165%5D&21180_format=6022&listFilterMode=1")
    time.sleep(5)  # Wait for JavaScript to load content.

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs = []
    table = soup.find("table", attrs={"class": ["table_basic-1", "table_striped", "table_overflow"]})
    rows = table.find("tbody").find_all("tr") if table else []  
    
    for row in rows:
        cols = row.find_all("td")
        # Assuming the location is within a sibling element; adjust as necessary
        if len(cols) >= 4:
            title_tag = cols[0].find("a")
            title = title_tag.text.strip() if title_tag else "N/A"
            link = title_tag["href"] if title_tag and title_tag.has_attr("href") else "N/A"
            role = cols[1].text.strip()
            area_of_interest = cols[2].text.strip()
            location = cols[3].text.strip()

            jobs.append({
                "Company": "Cisco",
                "Job Title": title,
                "Location": location,
                "Link": link,
            })

    return jobs

if __name__ == "__main__":
    job_listings = scrape_cisco()
    for job in job_listings:
        print(job)