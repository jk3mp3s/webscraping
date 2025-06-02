from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time


def scrape_td():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Empty jobs list and row number to change pages of listings
    driver.get("https://td.wd3.myworkdayjobs.com/en-US/TD_Bank_Careers?q=internship&locationCountry=a30a87ed25634629aa6c3958aa2b91ea")
    time.sleep(5)
    jobs =[]
    
    while True:
        
        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.css-1q2dra3')

        if not job_cards:
            break

        for card in job_cards:
            
            #Get job title and link
            title_anchor = card.find_element(By.CSS_SELECTOR, 'a.css-19uc56f')
            title = title_anchor.text.strip()
            link = title_anchor.get_attribute("href")


            location_element = card.find_element(By.CSS_SELECTOR, 'dd.css-129m7dg')
            location = location_element.text.strip()

            jobs.append({

            
                "Company": "TD",
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
            break

    return jobs


if __name__ == "__main__":
    job_listings = scrape_td()
    for job in job_listings:
        print(job)