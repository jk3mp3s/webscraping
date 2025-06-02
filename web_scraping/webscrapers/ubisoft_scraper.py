from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def scrape_ubisoft():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.ubisoft.com/en-us/company/careers/search?countries=ca")
    time.sleep(5)  # Wait for JavaScript to load content.

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs = []
    job_cards = soup.find_all('a', class_='dark-gray db mb3 link underline hover-primary-magenta')
    
    for card in job_cards:
        title = card.text.strip()
        link = "https://www.ubisoft.com" + card['href']

        #Find location in tags
        job_container = card.find_parent("article")
        location_tag = job_container.find("p", class_="job-location") if job_container else None
        location_span = location_tag.find("span") if location_tag else None
        location = location_span.text.strip() if location_span else "N/A"

        jobs.append({
            "Company": "Ubisoft",
            "Job Title": title,
            "Location": location,
            "Link": link
        })
    return jobs

if __name__ == "__main__":
    job_listings = scrape_ubisoft()
    for job in job_listings:
        print(job)