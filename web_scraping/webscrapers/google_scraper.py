from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_google():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Navigate to Google careers in Canada
    driver.get("https://www.google.com/about/careers/applications/jobs/results?location=Canada&target_level=INTERN_AND_APPRENTICE#!t=jo&jid=127025001&")
    time.sleep(5)

    
    

    jobs = []
    while True:

        time.sleep(3)  # Give time for the page to load
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.lLd3Je')

        for card in job_cards:

            try:
                title = card.find_element(By.CSS_SELECTOR, 'h3.QJPWVe').text
                location = card.find_element(By.CSS_SELECTOR, 'span.r0wTof').text
                link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

                jobs.append({
                    "Company": "Google",
                    "Job Title": title,
                    "Location": location,
                    "Link": link,
                })
            except Exception as e:
                print("Skipping a card due to error:", e)

        # Try to find the Next Page button and click it
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'div[jsname="ViaHrd"] a[aria-label="Go to next page"]')
            next_link = next_button.get_attribute("href")
            if next_link:
                driver.get(next_link)
            else:
                print("No next link found.")
                break
        except Exception as e:
            print("No more pages or couldn't click next:", e)
            break


    driver.quit()
    return jobs

    
if __name__ == "__main__":
    job_listings = scrape_google()
    for job in job_listings:
        print(job)