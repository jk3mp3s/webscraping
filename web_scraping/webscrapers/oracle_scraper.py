from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_oracle():

    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs =[]
    driver.get('https://careers.oracle.com/en/sites/jobsearch/jobs?keyword=internship&lastSelectedFacet=locations&mode=location&selectedLocationsFacet=300000000106749')
    time.sleep(5)




    # Load all job listings by clicking "Show More Results"
    while True:
        try:
            show_more_button = driver.find_element(By.CSS_SELECTOR, 'button[data-bind*="loadMore"]')
            if show_more_button.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", show_more_button)
                print("🔄 Clicked 'Show More Results'")
                time.sleep(3)
            else:
                break
        except NoSuchElementException:
            print("✅ No more listings to load.")
            break

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.job-tile')
    
    for card in job_cards:

        #Extract title element
        title_element = card.find_element(By.CSS_SELECTOR, 'span.job-tile__title')
        title = title_element.text.strip()
        
        #Extract job link
        link_element = card.find_element(By.CSS_SELECTOR, 'a.job-grid-item__link')
        link = link_element.get_attribute('href')

        #Extract location info
        try:

            #First attempt to find single location span
            location_element = card.find_element(By.CSS_SELECTOR, 'span[data-bind="html: primaryLocation"]')
            location = location_element.text.strip()

        except NoSuchElementException:
            location_element = card.find_element(By.CSS_SELECTOR, 'div.posting-locations__anchor')
            locations = location_element.get_attribute("aria-label").strip()

    
        jobs.append({


                "Company": "Oracle",
                "Job Title": title,
                "Location": location,
                "Link": link
                })
        
        

    return jobs


if __name__ == "__main__":
    job_listings = scrape_oracle()
    for job in job_listings:
        print(job)