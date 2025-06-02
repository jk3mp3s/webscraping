from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time


def scrape_bdo():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []
    
    driver.get("https://bdo.wd3.myworkdayjobs.com/en-US/BDO?workerSubType=f2258eb0c3fe01be4bc2baac7a158d0c")
    time.sleep(5)

    while True:

        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.css-1q2dra3')

        for card in job_cards:

            #Extract job title and link from a tag
            title_anchor = card.find_element(By.CSS_SELECTOR, 'a.css-19uc56f')
            title = title_anchor.text.strip()

            partial_link = title_anchor.get_attribute("href")
            link = "https://bdo.wd3.myworkdayjobs.com" + partial_link if partial_link.startswith("/") else partial_link

            location_element = card.find_element(By.CSS_SELECTOR, 'dd.css-129m7dg')
            location = location_element.text.strip()

            jobs.append({
            
                "Company": "BDO",
                "Job Title": title,
                "Location": location,
                "Link": link
            })

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="next"]')
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            break  # Exit if no next button or can't click
    
        
    driver.quit()
    return jobs

if __name__ == "__main__":
    job_listings = scrape_bdo()
    for job in job_listings:
        print(job)