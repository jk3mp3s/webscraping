from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def scrape_scotiabank():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Empty jobs list and row number to change pages of listings
    row = 0
    jobs =[]
    
    
    while True:

        driver.get(f"https://jobs.scotiabank.com/search/?q=internship&locationsearch=canada&startrow={row}")
        time.sleep(5)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'tr.data-row')

        if not job_cards:
            break

        for card in job_cards:
         
        #Get job title and link
            title_anchor = card.find_element(By.CSS_SELECTOR, 'a.jobTitle-link')
            title = title_anchor.get_attribute("innerText").strip()
            link = title_anchor.get_attribute("href")

            #Get location
            location_span = card.find_element(By.CSS_SELECTOR, 'span.jobLocation')
            location = location_span.text.strip()

            jobs.append({
            
                    "Company": "Scotiabank",
                    "Job Title": title,
                    "Location": location,
                    "Link": link
                })
            
        row += 25
        
    driver.quit()
    return jobs



if __name__ == "__main__":
    job_listings = scrape_scotiabank()
    for job in job_listings:
        print(job)