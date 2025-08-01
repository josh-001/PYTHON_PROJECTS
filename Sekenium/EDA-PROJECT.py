import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Data Lists (as provided) ---
Brand = []
Model = []
Body_Type = []
Seating_Capacity = []
Variant_Number = []
Variant_Name = []
Fuel_Type = []
Transmission = []
Available_Colors = []
On_Road_Pric = []
Location = []
Delivery_Timeline = []

# --- Configuration for Selenium ---
# A list of cities you want to scrape
cities_to_scrape = ['Gurgaon', 'Hyderabad', 'Bangalore', 'Mumbai']
base_url = 'https://ackodrive.com/cars/'
total_pages = 5  # Number of pages to scrape for each city

# Set up Chrome options to run in headless mode (runs in the background without a UI)
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the Chrome WebDriver using webdriver-manager
print("Initializing WebDriver...")
service = Service(executable_path="/home/c1/Downloads/chromedriver-linux64/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service)# options=chrome_options)

try:
    # --- Main loop to iterate through each city ---
        
    # 1. Navigate to the base URL
    driver.get(base_url)
    time.sleep(2)
    # driver.find_element(By.CSS_SELECTOR,"div.iLBWHU").click()
    # time.sleep(2)
    # soups = BeautifulSoup(driver.page_source, 'lxml')
    # time.sleep(1)
    # x=soup.find("div",class_="styles__Item-sc-c3ba0dce-10 kuNGpK")
    # for i in soups.find_all("div",class_="styles__Item-sc-c3ba0dce-10 kuNGpK"):
    #     print(i.text)
    #     driver.find_element(By.CSS_SELECTOR,"div.kuNGpK").click()
    #     time.sleep(2)

    # x=driver.find_elements(By.CSS_SELECTOR,"div.kuNGpK")
    # for i in x:
    #     if str(i.text) in cities_to_scrape:
    #         print(i.text) 
    #         i.click()
    #         time.sleep(4)
    #         driver.find_element(By.CSS_SELECTOR,"div.iLBWHU").click()
            
    #     else:
    #         continue

    for city in cities_to_scrape:
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.iLBWHU"))
        ).click()

        city_ele=WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.kuNGpK"))
        )
        for ele in city_ele:
            if str(ele.text)==city:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(ele)).click()
                print(city)
                WebDriverWait(driver, 15).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.ixyjBB"), city)
                )

                for i in range(1, total_pages + 1):
                    page_url = f'{base_url}page/{i}/'
                    print(f"  > Scraping page {i} of {total_pages}...")
                    
                    try:
                        # Navigate to the specific page
                        driver.get(page_url)
                        
                        # Wait for the car listings to be present on the page
                        # WebDriverWait(driver, 10).until(
                        #     EC.presence_of_all_elements_located((By.CLASS_NAME, "styles__Wrapper-sc-ad1b3a08-0"))
                        # )

                        # Get the page source after the content has loaded
                        soups = BeautifulSoup(driver.page_source, 'lxml')

                        # --- Scraping Logic (from your original code) ---
                        for soup in soups.find_all("div", class_="styles__Wrapper-sc-ad1b3a08-0 iTGjuL"):
                            # Brand & Model
                            b = soup.find("span", class_="styles__Make-sc-a6403e05-5 etWSJY")
                            Brand.append(b.text if b else np.nan)
                        
                            m = soup.find("span", class_="styles__ModelName-sc-a6403e05-6 hGuUnc")
                            Model.append(m.text if m else np.nan)

                            # Body Type & Seating Capacity
                            x = soup.find("div", class_="styles__ModelInfo-sc-a6403e05-8 eNUijV")
                            if x:
                                # Regex to extract Seating Capacity (e.g., '7 S') and Body Type (e.g., 'SUV')
                                ss = re.findall(r'(\d+) S', x.text)
                                Seating_Capacity.append(ss[0] if ss else np.nan)
                                
                                ty = re.findall(r'([\w]+)\s*\d+\s*S', x.text) # More robust regex
                                Body_Type.append(ty[0] if ty else np.nan)
                            else:
                                Seating_Capacity.append(np.nan)
                                Body_Type.append(np.nan)

                            # Variant Number
                            var = re.findall(r'(\d+)/?\d* variants', x.text) # Robust for '1/8 variants' or '1 variants'
                            Variant_Number.append(var[0] if var else np.nan)

                            # Fuel Type, Transmission, Available Colors
                            y = soup.find("div", class_="styles__VariantInfo-sc-a6403e05-12 bkhKsh")
                            if y:
                                ft = re.findall(r'(Petrol|Diesel|Electric|CNG)', y.text)
                                Fuel_Type.append(ft[0] if ft else np.nan)
                                
                                tr = re.findall(r'(Manual|Automatic)', y.text)
                                Transmission.append(tr[0] if tr else np.nan)
                                
                                av = re.findall(r'in (\d+) colors', y.text) # Using \d+ to match one or more digits
                                Available_Colors.append(av[0] if av else np.nan)
                            else:
                                Fuel_Type.append(np.nan)
                                Transmission.append(np.nan)
                                Available_Colors.append(np.nan)

                            # On-Road Price
                            pp = soup.find("div", class_="styles__Price-sc-a6403e05-18 bsWAfs")
                            ppp = re.findall(r'₹(\d+\.?\d*) L', pp.text.replace(',', '')) # Handle comma and decimal points
                            On_Road_Pric.append(ppp[0] if ppp else np.nan)

                            # Location
                            ll = soup.find("div", class_="styles__CityName-sc-a6403e05-17 fZrHFu")
                            lls = re.findall(r'in ([\w]+)', ll.text)
                            Location.append(lls[0] if lls else np.nan)
                            
                            # Delivery Timeline
                            # Assuming a class or element for this exists
                            # Based on the text, it's a simple text search, e.g., 'within 11 days'
                            delivery_info = soup.find("div", class_="styles__DeliveryInfo-sc-a6403e05-23 gHqfD") # Example class name
                            if delivery_info:
                                timeline = re.findall(r'within (\d+) days', delivery_info.text)
                                Delivery_Timeline.append(timeline[0] if timeline else np.nan)
                            else:
                                Delivery_Timeline.append(np.nan)


                    except (TimeoutException, NoSuchElementException) as e:
                        print(f"    > No more listings or element not found on page {i}. Stopping page iteration for {city}.")
                        break  # Exit the page loop if no elements are found
                
                break

    # --- Nested loop to iterate through pages for the current city ---
        # for i in range(1, total_pages + 1):
        #     page_url = f'{base_url}page/{i}/'
        #     print(f"  > Scraping page {i} of {total_pages}...")
            
        #     try:
        #         # Navigate to the specific page
        #         driver.get(page_url)
                
        #         # Wait for the car listings to be present on the page
        #         WebDriverWait(driver, 10).until(
        #             EC.presence_of_all_elements_located((By.CLASS_NAME, "styles__Wrapper-sc-ad1b3a08-0"))
        #         )

        #         # Get the page source after the content has loaded
        #         soups = BeautifulSoup(driver.page_source, 'lxml')

        #         # --- Scraping Logic (from your original code) ---
        #         for soup in soups.find_all("div", class_="styles__Wrapper-sc-ad1b3a08-0 iTGjuL"):
        #             # Brand & Model
        #             b = soup.find("span", class_="styles__Make-sc-a6403e05-5 etWSJY")
        #             Brand.append(b.text if b else np.nan)
                
        #             m = soup.find("span", class_="styles__ModelName-sc-a6403e05-6 hGuUnc")
        #             Model.append(m.text if m else np.nan)

        #             # Body Type & Seating Capacity
        #             x = soup.find("div", class_="styles__ModelInfo-sc-a6403e05-8 eNUijV")
        #             if x:
        #                 # Regex to extract Seating Capacity (e.g., '7 S') and Body Type (e.g., 'SUV')
        #                 ss = re.findall(r'(\d+) S', x.text)
        #                 Seating_Capacity.append(ss[0] if ss else np.nan)
                        
        #                 ty = re.findall(r'([\w]+)\s*\d+\s*S', x.text) # More robust regex
        #                 Body_Type.append(ty[0] if ty else np.nan)
        #             else:
        #                 Seating_Capacity.append(np.nan)
        #                 Body_Type.append(np.nan)

        #             # Variant Number
        #             var = re.findall(r'(\d+)/?\d* variants', x.text) # Robust for '1/8 variants' or '1 variants'
        #             Variant_Number.append(var[0] if var else np.nan)

        #             # Fuel Type, Transmission, Available Colors
        #             y = soup.find("div", class_="styles__VariantInfo-sc-a6403e05-12 bkhKsh")
        #             if y:
        #                 ft = re.findall(r'(Petrol|Diesel|Electric|CNG)', y.text)
        #                 Fuel_Type.append(ft[0] if ft else np.nan)
                        
        #                 tr = re.findall(r'(Manual|Automatic)', y.text)
        #                 Transmission.append(tr[0] if tr else np.nan)
                        
        #                 av = re.findall(r'in (\d+) colors', y.text) # Using \d+ to match one or more digits
        #                 Available_Colors.append(av[0] if av else np.nan)
        #             else:
        #                 Fuel_Type.append(np.nan)
        #                 Transmission.append(np.nan)
        #                 Available_Colors.append(np.nan)

        #             # On-Road Price
        #             pp = soup.find("div", class_="styles__Price-sc-a6403e05-18 bsWAfs")
        #             ppp = re.findall(r'₹(\d+\.?\d*) L', pp.text.replace(',', '')) # Handle comma and decimal points
        #             On_Road_Pric.append(ppp[0] if ppp else np.nan)

        #             # Location
        #             ll = soup.find("div", class_="styles__CityName-sc-a6403e05-17 fZrHFu")
        #             lls = re.findall(r'in ([\w]+)', ll.text)
        #             Location.append(lls[0] if lls else np.nan)
                    
        #             # Delivery Timeline
        #             # Assuming a class or element for this exists
        #             # Based on the text, it's a simple text search, e.g., 'within 11 days'
        #             delivery_info = soup.find("div", class_="styles__DeliveryInfo-sc-a6403e05-23 gHqfD") # Example class name
        #             if delivery_info:
        #                 timeline = re.findall(r'within (\d+) days', delivery_info.text)
        #                 Delivery_Timeline.append(timeline[0] if timeline else np.nan)
        #             else:
        #                 Delivery_Timeline.append(np.nan)


        #     except (TimeoutException, NoSuchElementException) as e:
        #         print(f"    > No more listings or element not found on page {i}. Stopping page iteration for {city}.")
        #         break  # Exit the page loop if no elements are found
        # driver.find_element(By.CSS_SELECTOR,"div.iLBWHU").click()
        # time.sleep(2)
finally:
    # --- Close the browser ---
    print("\nScraping complete. Closing the browser.")
    driver.quit()
data={
"Brand":Brand,
"Model":Model,
"Seating_Capacity":Seating_Capacity,
"Body_Type":Body_Type,
"Variant_Number":Variant_Number,
"Fuel_Type":Fuel_Type,
"Transmission":Transmission,
"Available_Colors":Available_Colors,
"On_Road_Pric":On_Road_Pric,
"Location":Location,
}
df_hyd=pd.DataFrame(data)
df_hyd.to_csv("carsdata")
time.sleep(30)
# --- Print the collected data for verification ---
# You can save this to a DataFrame or CSV file here
print("\n--- Data Collected ---")
print(f"Total Brands: {len(Brand)}")
print(f"Total Models: {len(Model)}")
print(f"Locations: {len(Location)}")
print(f"Example Data:")
for i in range(min(5, len(Brand))):
    print(f"  - Brand: {Brand[i]}, Model: {Model[i]}, Location: {Location[i]}, Price: {On_Road_Pric[i]}")