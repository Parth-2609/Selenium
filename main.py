from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


# Set up Chrome WebDriver
s = Service("C:/Users/dell/OneDrive/Desktop/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get("https://www.greatplacetowork.in/certified-companies")
driver.maximize_window()
time.sleep(5)

#Change the number of companies visible on the initial page
dropdown = driver.find_element(By.XPATH, "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[1]/div[1]/div/label/select")
drop = driver.find_element(By.XPATH, "/html/body/article/div/div[1]/section[3]/div/div/div/section/div/div[1]/div/div[3]/div/div/a")
driver.execute_script("arguments[0].scrollIntoView();", drop)
time.sleep(2)
quant = Select(dropdown)
quant.select_by_visible_text("100")
time.sleep(6)


all_data = pd.DataFrame(columns=["Organization Name", "Industry", "No. of Employees", "Certification Period"])

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

    # Collect data for this page
    org = [i.text for i in org_name]
    indus = [i.text for i in industry]
    employee = [i.text for i in employees]
    certification = [i.text for i in cert_period]

    # Create a DataFrame for this page's data
    page_data = pd.DataFrame({
        "Organization Name": org,
        "Industry": indus,
        "No. of Employees": employee,
        "Certification Period": certification
    })

    return page_data

try:
    while True:
        try:
            # Scrape data from the current page
            page_data = scrape_data()

            # Append the page data to the main DataFrame
            all_data = pd.concat([all_data, page_data], ignore_index=True)

            # Find and click the "Next" button to go to the next page
            element_to_click = driver.find_element(By.XPATH,
                                                   "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[3]/div[2]/div/ul/li[9]/a")

            element_to_view = driver.find_element(By.XPATH,
                                                  "/html/body/article/div/div[1]/section[5]/div/div/div/div/div/div/div[2]/div[2]/div/table/tbody/tr[97]")
            driver.execute_script("arguments[0].scrollIntoView();", element_to_view)
            time.sleep(3)

            # Perform the click action
            actions = ActionChains(driver)
            actions.move_to_element(element_to_click).click().perform()
            print("Navigated to the next page.")

            # Wait for the next page content to load
            time.sleep(3)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

finally:
    # Save the data to a CSV file after the loop ends
    all_data.to_csv("Great_Place_to_Work.csv", index=False)
    print("Data saved to 'Great_Place_to_Work.csv'")

    # Close the WebDriver
    driver.quit()