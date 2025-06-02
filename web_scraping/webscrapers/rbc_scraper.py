from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_rbc():

    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Empty jobs list and start number to change pages of listings
    start=0
    jobs =[]

    while True:

        driver.get(f"https://jobs.rbc.com/ca/en/search-results?keywords=internship%20canada&from={start}&s=1")
        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.jobs-list-item')

        if not job_cards:
            break

        for card in job_cards:
            
            #Get job title and link
            title_element = card.find_element(By.CSS_SELECTOR, 'div.job-title span')
            title = title_element.text.strip()

            #Get link to job
            link = card.find_element(By.CSS_SELECTOR, 'a[data-ph-at-id="job-link"]').get_attribute("href")

            try:
            # First try to find the single location span
                location_span = card.find_element(By.CSS_SELECTOR, 'span.job-location')
                location = location_span.text.strip().replace("Location", "").strip()

            except NoSuchElementException:

                try:

                    # Fall back to multiple locations inside a <ul>
                    location_items = card.find_elements(By.CSS_SELECTOR, 'ul[data-ph-at-id="job-multi-locations-list"] li.location')
                    location = "; ".join([item.text.strip() for item in location_items])

                except NoSuchElementException:
                    location = "Unknown"
            

            jobs.append({

                "Company": "RBC",
                "Job Title": title,
                "Location": location,
                "Link": link
                })
           
        start += 10
        
    driver.quit()
    return jobs

if __name__ == "__main__":
    job_listings = scrape_rbc()
    for job in job_listings:
        print(job)
