from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

def scrape_kpmg():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []
    
    driver.get("https://careers.kpmg.ca/students/jobs?limit=100&page=1&tags1=Intern%2FCo-op")
    time.sleep(5)

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'mat-expansion-panel-header.mat-expansion-panel-header')

    for card in job_cards:

        #Find title element
        title_element = card.find_element(By.CSS_SELECTOR, 'span[itemprop="title"]')
        title = title_element.text.strip()

        #Find link element 
        link_element = card.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]')
        partial_link = link_element.get_attribute("href")
        link = ("https://careers.kpmg.ca/" + partial_link)

        #Find location element 
        location_element = card.find_element(By.CSS_SELECTOR, 'span.location')
        location = location_element.text.strip()

        jobs.append({
            
                "Company": "KPMG",
                "Job Title": title,
                "Location": location,
                "Link": link
            })
    
    return jobs
        

if __name__ == "__main__":
    job_listings = scrape_kpmg()
    for job in job_listings:
        print(job)