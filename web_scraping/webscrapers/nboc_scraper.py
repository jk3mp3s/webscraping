from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_nboc():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    time.sleep(5)

    start=0
    jobs = []


    
    while True:

        driver.get(f"https://emplois.bnc.ca/en_CA/careers/searchjobs/Canada/?listFilterMode=1&jobRecordsPerPage=20&jobOffset={start}")
        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'tr')
        if not job_cards:
            break

        for card in job_cards:

            try:

                # Get job title & link
                title_element = card.find_element(By.CSS_SELECTOR, 'th[data-th="Name"] a')
                title = title_element.text.strip()
                link = title_element.get_attribute("href")


                # Get location
                location_element = card.find_element(By.CSS_SELECTOR, 'td[data-th="Location"]')
                location = location_element.get_attribute("innerText").strip()
                
                jobs.append({
                    "Company": "National Bank of Canada",
                    "Job Title": title,
                    "Location": location,
                    "Link": link
                })
                
            except Exception as e:
                # Skip rows without expected structure
                continue


        start += 20

    return jobs


    


if __name__ == "__main__":
    job_listings = scrape_nboc()
    for job in job_listings:
        print(job)