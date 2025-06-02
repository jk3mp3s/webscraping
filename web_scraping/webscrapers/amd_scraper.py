from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_amd():


    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []

    page = 1
    while True:

        driver.get(f"https://careers.amd.com/careers-home/jobs?keywords=Canada&sortBy=relevance&page={page}&categories=Student%20%2F%20Intern%20%2F%20Temp")
        time.sleep(3)

        job_cards = driver.find_elements(By.CSS_SELECTOR, '.mat-expansion-panel')

        if not job_cards:
            break

        for card in job_cards:
            # Job Title and Link
            title_anchor = card.find_element(By.CSS_SELECTOR, 'a.job-title-link')
            title = title_anchor.text.strip()
            link = title_anchor.get_attribute("href")

            # Location
            location_span = card.find_element(By.CSS_SELECTOR, 'span.location.label-value')
            location = location_span.text.replace("\n", ", ").strip()

            jobs.append({
            
                "Company": "AMD",
                "Job Title": title,
                "Location": location,
                "Link": link
            })
        
        page +=1
    
    driver.quit()
    return jobs



if __name__ == "__main__":
    job_listings = scrape_amd()
    for job in job_listings:
        print(job)