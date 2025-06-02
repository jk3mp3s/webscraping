from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def scrape_microsoft():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    time.sleep(5)

    start=1
    jobs = []
    
    while True:

        driver.get(f"https://jobs.careers.microsoft.com/global/en/search?q=intern&lc=Canada&l=en_us&pg={start}&pgSz=20&o=Relevance&flt=true")
        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, '.ms-List-surface .ms-List-cell')

        if not job_cards:
            break

        for card in job_cards:

            title_element = card.find_element(By.TAG_NAME, 'h2')
            title = title_element.text.strip()
        
            location = ''

            span_elements = card.find_elements(By.TAG_NAME, 'span')

            for span in span_elements:
                try:
                    icon = span.find_element(By.XPATH, 'preceding-sibling::i[1]')
                    if icon.get_attribute('data-icon-name') == 'POI':
                        location = span.text.strip()
                        break
                except:

                    continue

            parent = title_element.find_element(By.XPATH, '..')

            job_id_element = card.find_element(By.CSS_SELECTOR, 'div.ms-Stack').get_attribute('aria-label')
            job_id = job_id_element.replace("Job item ","")
            link ='https://jobs.careers.microsoft.com/global/en/job/'+ job_id

            jobs.append({
                "Company": "Microsoft",
                "Job Title": title,
                "Location": location,
                "Link": link
            })
        start += 1

    return jobs

if __name__ == "__main__":
    job_listings = scrape_microsoft()
    for job in job_listings:
        print(job)



