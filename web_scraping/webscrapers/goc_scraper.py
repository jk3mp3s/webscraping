from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

def scrape_goc():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []

    base_url = "https://emploisfp-psjobs.cfp-psc.gc.ca/"
    driver.get("https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page2440?tab=1&title=&locationsFilter=&studentProgram=studentProgram&departments=&officialLanguage=&referenceNumber=&selectionProcessNumber=&search=Search%20jobs&log=false")
    time.sleep(5)

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.searchResult')

    for card in job_cards:

        #Get link and title attributes
        title_anchor = card.find_element(By.CSS_SELECTOR, 'a')
        title = title_anchor.text.strip()
        partial_link = title_anchor.get_attribute("href")
        link = base_url + partial_link

        # Get the first .tableCell div
        table_cell = card.find_element(By.CSS_SELECTOR, "div.tableCell")
        
        # Extract all text and split by line breaks
        lines = table_cell.get_attribute("innerText").split("\n")

        # Location is assumed to be the last non-empty line
        location = lines[-1].strip() if lines else "Unknown"

        jobs.append({
            
                "Company": "Government of Canada",
                "Job Title": title,
                "Location": location,
                "Link": link
            })

    return jobs

        
if __name__ == "__main__":
    job_listings = scrape_goc()
    for job in job_listings:
        print(job)