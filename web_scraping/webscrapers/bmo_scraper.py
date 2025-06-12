from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def scrape_bmo():
    
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Empty jobs list and start number to change pages of listings
    start=0
    jobs =[]
    
    while True:

        if start == 0:
            url = "https://jobs.bmo.com/ca/en/search-results?keywords=student"
        else:
            url = f"https://jobs.bmo.com/ca/en/interns?from={start}&s=1&rk=l-student"

        driver.get(url)
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

            location_span = card.find_element(By.CSS_SELECTOR, 'span.job-location')
            location = location_span.text.replace("Location\n", "").strip()

            jobs.append({

                "Company": "BMO",
                "Job Title": title,
                "Location": location,
                "Link": link
                })
            
        start += 10
        
    
    driver.quit()
    return jobs

if __name__ == "__main__":
    job_listings = scrape_bmo()
    for job in job_listings:
        print(job)