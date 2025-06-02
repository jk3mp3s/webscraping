from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_nvidia():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea529c3b93ba3236&jobFamilyGroup=0c40f6bd1d8f10ae43ffda1e8d447e94")
    time.sleep(5)
    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.css-1q2dra3')
    print(f"Found {len(job_cards)} job cards")
    for card in job_cards:

        title_element = card.find_element(By.CSS_SELECTOR, 'h3 a')
        title = title_element.text.strip()
        link = "https://nvidia.wd5.myworkdayjobs.com" + title_element.get_attribute("href")

        location_element = card.find_element(By.CSS_SELECTOR, 'dd.css-129m7dg')
        location = location_element.text.strip()

        jobs.append({

                "Company": "Nvidia",
                "Job Title": title,
                "Location": location,
                "Link": link,
            
            })
    
    driver.quit()
    return jobs

if __name__ == "__main__":
    job_listings = scrape_nvidia()
    for job in job_listings:
        print(job)