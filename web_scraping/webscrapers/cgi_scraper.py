from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time


def scrape_cgi():

    options = Options()
    options.add_argument('--headless')  # Run in headless mode.
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #Navigate to CGI careers in Canada
    driver.get("https://cgi.njoyn.com/corp/xweb/xweb.asp?NTKN=c&clid=21001&Page=joblisting")
    time.sleep(5)

    #Enter Canada as keyword
    try:
        keyword_box = driver.find_element(By.ID, "Inp_Keywords")  # or try By.NAME or By.CSS_SELECTOR
        keyword_box.clear()
        keyword_box.send_keys("Canada")
    except Exception as e:
        print("Keyword input not found:", e)

    # Click the "Advanced Search Parameters" button
    try:
        advanced_button = driver.find_element(By.ID, "expandASP")
        driver.execute_script("arguments[0].click();", advanced_button)

        # Wait for the advanced search panel to become visible
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "searchFilter").get_attribute("style") == "display: block;"
        )
        print("✅ Advanced Search Parameters expanded.")
    except Exception as e:
        print("⚠️ Failed to expand advanced search:", e)

    # === NEW: Select "Student Internship" in Employment Type dropdown ===
    try:
        # Wait for the select element to be present
        job_type_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Inp_CGI_Cand_jobtype"))
        )

        select = Select(job_type_dropdown)
        select.deselect_all()  # Deselect others in case it's a multi-select
        select.select_by_visible_text("Student Internship")
        print("✅ Selected 'Student Internship' employment type.")
    except Exception as e:
        print("⚠️ Failed to select employment type:", e)

    # === Click the Search button ===
    try:
       
       search_button = driver.find_element(By.ID, "joblistingsearchbutton")
       driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
       time.sleep(1)  # short pause after scroll
       driver.execute_script("arguments[0].click();", search_button)
       time.sleep(3)

       print("New page title:", driver.title)
       print("Job count after search:", len(driver.page_source))

    except Exception as e:
        print("Search button not found:", e)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    

    jobs = []
    while True:

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", class_="views-table table-result-search cols-5 responsive")

        if not table:
            print("No job table found on this page.")
            break

        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            job_id_link = cols[0].find("a")
            title = cols[1].text.strip()
            location = cols[3].text.strip()
            link = (
                "https://cgi.njoyn.com/corp/xweb/" + job_id_link["href"]
                if job_id_link and job_id_link.has_attr("href")
                else "N/A"
            )

            jobs.append({
                "Company": "CGI",
                "Job Title": title,
                "Location": location,
                "Link": link,
            })

        # Check if a "Next" link exists and click it
        try:
            next_button = driver.find_element("link text", "Next")
            next_button.click()
            time.sleep(3)
        except:
            print("No more pages.")
            break

    driver.quit()
    return jobs

if __name__ == "__main__":
    jobs = scrape_cgi()
    for job in jobs:
        print(job)