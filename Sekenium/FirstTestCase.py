# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import os
# import shutil
# import time

# # --- CONFIGURATION ---
# chromedriver_path = "/home/c1/Downloads/chromedriver-linux64/chromedriver-linux64/chromedriver"
# url_to_visit = "https://www.zeptonow.com/cn/masala-dry-fruits-more/masala-dry-fruits-more/cid/0c2ccf87-e32c-4438-9560-8d9488fc73e0/scid/8b44cef2-1bab-407e-aadd-29254e6778fa"

# # --- STEP 1: Create a unique temporary directory for the user data ---
# temp_user_data_dir = os.path.join("/tmp", f"chrome_profile_selenium_{os.getpid()}")

# # --- STEP 2: Configure Chrome Options to use this directory ---
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")

# # --- STEP 3: Set up the Service with logging ---
# log_file_path = "chromedriver_session_debug.log"
# service = Service(
#     executable_path=chromedriver_path,
#     log_output=log_file_path,  # This tells the service to write logs to a file
#     service_args=["--verbose"]  # This makes the logs more detailed
# )

# driver = None
# try:
#     print("Attempting to start a new Chrome session...")
#     print(f"Using temporary user data directory: {temp_user_data_dir}")
#     print(f"Writing ChromeDriver logs to: {log_file_path}")
    
#     # --- STEP 4: Initialize the WebDriver with the configured options ---
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     print("WebDriver session created successfully.")

#     # ... (rest of your code remains the same) ...
#     driver.get(url_to_visit)
#     print(f"Navigated to: {driver.current_url}")
#     print(f"Page Title: {driver.title}")

#     time.sleep(5) # Keep the browser open for a few seconds to observe

# except Exception as e:
#     print(f"\nAn error occurred during WebDriver operation: {e}")

# finally:
#     if driver:
#         driver.quit()
#         print("WebDriver closed.")
    
#     if os.path.exists(temp_user_data_dir):
#         try:
#             shutil.rmtree(temp_user_data_dir)
#             print(f"Cleaned up temporary directory: {temp_user_data_dir}")
#         except OSError as e:
#             print(f"Error removing temporary directory: {e}")

import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
service = Service(executable_path="/home/c1/Downloads/chromedriver-linux64/chromedriver-linux64/chromedriver")

driver=webdriver.Chrome(service=service)


driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(3)
driver.find_element(By.ID,"username").send_keys("joshuakakarla555@gmail.com")
driver.find_element(By.ID,"password").send_keys("Cse@19665@connect")
driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
driver.find_element(By.CSS_SELECTOR,"a.global-nav__primary-link[href*='/jobs/']").click()
time.sleep(5)
# driver.find_element(By.XPATH, "//a[contains(@href, 'jobs/collections/easy-apply')]").click()
# driver.find_element(By.CSS_SELECTOR, "a[aria-label='Show all Explore with job collections']").click()
# print("Waiting for the 'Show all' link using a flexible locator...")
driver.find_element(By.CSS_SELECTOR,"a[aria-label^='Show all']").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR,"a.t-black.link-without-visited-state.jobs-search-discovery-tabs__tab[href*='easy-apply']").click()


job_list_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-layout__list ")
    
while True:
        # Get the current scroll height of the CONTAINER
        old_height = driver.execute_script("return arguments[0].scrollHeight", job_list_container)

        # Scroll the CONTAINER down to its bottom
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", job_list_container)
        
        # Give it a moment to load new jobs
        print("scrolling...")
        time.sleep(2)

        # Get the new scroll height of the CONTAINER
        new_height = driver.execute_script("return arguments[0].scrollHeight", job_list_container)
        print(f"Old Height: {old_height}, New Height: {new_height}")

        # If the height hasn't changed, we've reached the end of the scrollable content
        if new_height == old_height:
                print("Reached the bottom of the container. All jobs loaded.")
                break
                
        # 6. Now that all jobs are loaded, find all the links
        print("All jobs loaded. Finding all the job links now...")
        job_elements = driver.find_elements(By.CSS_SELECTOR,"a.job-card-list__title--link[href*='/jobs/view']")

        print(f"Total jobs found on the page: {len(job_elements)}")
        

x=driver.find_elements(By.CSS_SELECTOR,"a.job-card-list__title--link[href*='/jobs/view']")
print(len(x))
# for i in driver.find_elements(By.CSS_SELECTOR,"a.job-card-list__title--link[href*='/jobs/view']"):
#     i.click()
#     time.sleep(3)
# show_all_link = WebDriverWait(driver, 30).until(
# EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label^='Show all']"))
# )
print("Browser will stay open for 60 seconds. You can observe the page.")
time.sleep(60)

# This command closes the browser and ends the WebDriver session
print("Closing the browser.")
driver.quit()

print("Script finished.")
































        ###  wokring one but   i ddit understand


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time # Import the time module for pausing

# # --- Setup ---
# service = Service(executable_path="/home/c1/Downloads/chromedriver-linux64/chromedriver-linux64/chromedriver")
# driver = webdriver.Chrome(service=service)
# driver.get("http://opensource-demo.orangehrmlive.com/")

# # Add an explicit wait for the username input field to be visible.
# # This waits up to 10 seconds. If the element appears sooner, it continues immediately.
# print("Waiting for the username input field to be visible...")
# try:
#     # Use the WebDriverWait to wait for the element to be located and visible.
#     # The `by=` and `value=` arguments are now correctly used inside the tuple.
#     username_input = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.NAME, "username"))
#     )

#     # If the wait is successful, the element is found and stored in `username_input`.
#     print("Username input field found! Sending keys...")
    
#     # Now, use the element you found to send keys.
#     username_input.send_keys("Admin")

#     # Now, find the password field. Since the page is loaded, this should work.
#     password_input = driver.find_element(By.NAME, "password")
#     password_input.send_keys("admin123")
    
#     # After login, you would click the login button, for example:
#     login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
#     login_button.click()
    
#     print("Login credentials entered and button clicked.")

#     # Keep the browser open for a moment to see the dashboard
#     print("Pausing for 5 seconds to observe the result.")
#     time.sleep(5)

# except Exception as e:
#     # This block will catch the TimeoutException if the element is not found in 10 seconds.
#     print(f"An error occurred: {e}")
#     print("The element was not found within the specified time.")

# finally:
#     # Always close the driver in a finally block to ensure it closes even if an error occurs.
#     print("Closing the browser.")
#     driver.quit()