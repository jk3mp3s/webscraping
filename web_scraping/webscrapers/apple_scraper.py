from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape_apple():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://jobs.apple.com/en-ca/search?location=canada-CANC&key=intern")

    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, '#search-result-set .job-title.job-list-item')

    for card in job_cards:
        try:
            title_element = card.find_element(By.TAG_NAME, 'h3')
            title = title_element.text.strip()

            link_element = card.find_element(By.TAG_NAME, 'a')
            link = link_element.get_attribute('href')

            # Try to get the team name (e.g. Apple Retail)
            try:
                location_container = card.find_element(By.CSS_SELECTOR, 'div.job-title-location')
                location_element = location_container.find_element(By.TAG_NAME, 'span')
                location = location_element.text.strip()
            except Exception as e:
                location = "N/A"

            jobs.append({
                "Company": "Apple",
                "Job Title": title,
                "Location": location,
                "Link": link,
            })
        except Exception as e:
            print("Skipping a job due to error:", e)

    driver.quit()
    return jobs

if __name__ == "__main__":
    job_listings = scrape_apple()
    for job in job_listings:
        print(job)
