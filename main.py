import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

# Streamlit app
st.title("Web Scraping with Selenium")
st.write("Scrape data from the 'Great Place to Work' website.")

# Button to trigger scraping
if st.button("Start Scraping"):
    # Display progress and status
    status_text = st.empty()
    status_text.text("Initializing the scraping process...")

    # Set up Chrome WebDriver
    try:
        s = Service("C:/Users/dell/OneDrive/Desktop/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=s)
        driver.get("https://www.greatplacetowork.in/certified-companies")
        driver.maximize_window()
        time.sleep(5)

        # Change the number of companies visible on the initial page
        dropdown = driver.find_element(By.XPATH,
                                       "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[1]/div[1]/div/label/select")
        drop = driver.find_element(By.XPATH,
                                   "/html/body/article/div/div[1]/section[3]/div/div/div/section/div/div[1]/div/div[3]/div/div/a")
        driver.execute_script("arguments[0].scrollIntoView();", drop)
        time.sleep(2)
        quant = Select(dropdown)
        quant.select_by_visible_text("100")
        time.sleep(3)

        all_data = pd.DataFrame(
            columns=["Organization Name", "Industry", "No. of Employees", "Certification Period", "Profile URL"])


        def scrape_data():
            """Scrape data from the current page."""
            org_name = driver.find_elements(By.XPATH,
                                            "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[1]")
            industry = driver.find_elements(By.XPATH,
                                            "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[2]")
            employees = driver.find_elements(By.XPATH,
                                             "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[3]")
            cert_period = driver.find_elements(By.XPATH,
                                               "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[4]")

            # Extract profile URLs from the 'a' tags in the last column
            profile_links = driver.find_elements(By.XPATH,
                                                 "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[5]//a")

            # Collect data for this page
            org = [i.text for i in org_name]
            indus = [i.text for i in industry]
            employee = [i.text for i in employees]
            certification = [i.text for i in cert_period]
            profile_urls = [link.get_attribute("href") for link in profile_links]  # Extract 'href' from 'a' tags

            # Debugging step to check lengths of lists
            print(f"Organization Names Length: {len(org)}")
            print(f"Industries Length: {len(indus)}")
            print(f"Employees Length: {len(employee)}")
            print(f"Certification Period Length: {len(certification)}")
            print(f"Profile URLs Length: {len(profile_urls)}")

            # Ensure all lists have the same length by filling missing data with 'None' or empty strings
            max_length = max(len(org), len(indus), len(employee), len(certification), len(profile_urls))
            org.extend([None] * (max_length - len(org)))
            indus.extend([None] * (max_length - len(indus)))
            employee.extend([None] * (max_length - len(employee)))
            certification.extend([None] * (max_length - len(certification)))
            profile_urls.extend([None] * (max_length - len(profile_urls)))

            return pd.DataFrame({
                "Organization Name": org,
                "Industry": indus,
                "No. of Employees": employee,
                "Certification Period": certification,
                "Profile URL": profile_urls,
            })


        # Scrape data
        while True:
            try:
                # Scrape current page
                page_data = scrape_data()
                all_data = pd.concat([all_data, page_data], ignore_index=True)

                # Go to the next page
                next_btn = driver.find_element(By.XPATH,
                                               "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[3]/div[2]/div/ul/li[9]/a")
                view_btn = driver.find_element(By.XPATH,
                                               "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr[99]")
                driver.execute_script("arguments[0].scrollIntoView();", view_btn)
                time.sleep(3)
                actions = ActionChains(driver)
                actions.move_to_element(next_btn).click().perform()
                time.sleep(3)
                status_text.text("Scraping next page...")

            except Exception as e:
                st.error(f"Scraping completed with error: {e}")
                break

        # Save data to a CSV
        csv_path = "Great_Place_to_Work.csv"
        all_data.to_csv(csv_path, index=False)
        st.success("Scraping completed successfully!")
        status_text.empty()

        # Provide download link
        with open(csv_path, "rb") as f:
            st.download_button("Download CSV", f, file_name="Great_Place_to_Work.csv")

    finally:
        driver.quit()