from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_thomsonreuters():

    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []

    driver.get('https://careers.thomsonreuters.com/us/en/search-results?keywords=intern')
    time.sleep(10)

    # Wait for the Country accordion to be clickable, then click it
    try:

        wait = WebDriverWait(driver, 15)

        # Wait until the button is visible and interactable
        country_button = wait.until(EC.presence_of_element_located((By.ID, "CountryAccordion")))
        driver.execute_script("arguments[0].scrollIntoView(true);", country_button)

        # Wait for it to be *visible* (not just in DOM)
        wait.until(EC.visibility_of(country_button))
        wait.until(EC.element_to_be_clickable((By.ID, "CountryAccordion")))

        # JavaScript click (more reliable for hidden or animated elements)
        driver.execute_script("arguments[0].click();", country_button)

        print("✅ Clicked Country accordion")

    except Exception as e:
        print(f"⚠️ Failed to click Country accordion: {e}")

    try:
    # Wait for the checkbox to be present in the DOM
        wait = WebDriverWait(driver, 10)
        canada_checkbox = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-ph-at-text="Canada"]'))
        )

        # Scroll it into view just in case
        driver.execute_script("arguments[0].scrollIntoView(true);", canada_checkbox)
        time.sleep(1)

        # Check if it's already selected using aria-checked
        if canada_checkbox.get_attribute("aria-checked") != "true":
            driver.execute_script("arguments[0].click();", canada_checkbox)
            print("✅ Clicked Canada checkbox")
            time.sleep(3)  # Wait for filter to apply

            # Re-fetch the element to verify updated state
            canada_checkbox = driver.find_element(By.CSS_SELECTOR, 'input[data-ph-at-text="Canada"]')
            if canada_checkbox.get_attribute("aria-checked") == "true":
                print("✅ Confirmed Canada checkbox is now selected.")
            else:
                print("⚠️ Tried to click but checkbox is still not selected.")
        else:
            print("ℹ️ Canada checkbox was already selected.")

    except Exception as e:
        print(f"❌ Error interacting with Canada checkbox: {e}")

    while True:

        time.sleep(3)
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.jobs-list-item')

        for card in job_cards:

            #Extract title element
            title_element =  card.find_element(By.CSS_SELECTOR, 'span[data-ph-id="ph-page-element-page21-0hSvAK"]')
            title = title_element.text.strip()

            #Extract job link
            link_element = card.find_element(By.CSS_SELECTOR, 'a[data-ph-at-id="job-link"]' )
            link = link_element.get_attribute("href")

            #Extract location info
            try:

                #First attempt to find single location span
                location_element = card.find_element(By.CSS_SELECTOR, 'span.job-location')
                location = location_element.text.replace("Location", "").strip()

            except NoSuchElementException:
                # Fall back to multiple locations inside a <ul>
                    location_items = card.find_elements(By.CSS_SELECTOR, 'ul[data-ph-at-id="job-multi-locations-list"] li[data-ph-at-id="job-multi-location-item"]')
                    location = "; ".join([item.get_attribute("aria-label").strip() for item in location_items if item.get_attribute("aria-label")])
            
            jobs.append({

                    "Company": "Thomson Reuters",
                    "Job Title": title,
                    "Location": location,
                    "Link": link
                    })
            
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-ph-at-id="pagination-next-link"]')

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)  # small wait after scroll

            if "disabled" in next_button.get_attribute("class"):
                break

            next_button.click()
            time.sleep(3)

        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            break  # No next button, so stop
            
    driver.quit()
    return jobs



if __name__ == "__main__":
    job_listings = scrape_thomsonreuters()
    for job in job_listings:
        print(job)