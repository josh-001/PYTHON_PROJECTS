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
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, date

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
current_date=datetime.now().date()

base_url = 'https://ackodrive.com/cars/'
print("Initializing WebDriver...")
service = Service(executable_path="/home/c1/Downloads/chromedriver-linux64/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service)
cities_to_scrape=[   "Bangalore",   "Chennai",  "Faridabad",  "Ghaziabad",  "Gurgaon", 
                   "Hyderabad","Mumbai","Noida","Pune"]
try:
        
    driver.get(base_url)
    time.sleep(2)
    for city in cities_to_scrape:
        driver.refresh()

        driver.find_element(By.CSS_SELECTOR,"div.iLBWHU").click()

        city_ele=WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.kuNGpK"))
        )

        
        for ele in city_ele:
            print(ele.text)
            time.sleep(2)
            if str(ele.text)==city:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(ele)).click()
                print(city)
                WebDriverWait(driver, 15).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.ixyjBB"), city)
                )

                for i in range(1, 6):
                    page_url = f'{base_url}page/{i}/'
                    print(f"  > Scraping page {i} of {6}...")
                    
                    try:
                        # Navigate to the specific page
                        driver.get(page_url)
                        

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
                            var = re.findall(r'(\d+)/?\d* variants', x.text)
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
                            
                            
                            dd=soup.find("div",class_=lambda x: x in ['styles__DateText-sc-a6403e05-31 NBVEP',
                                                                      'styles__DateText-sc-a6403e05-31 jMWUPS'])
                            if dd:
                                if 'within' in dd.text:
                                    x=re.findall(r'within (\d+) ',dd.text)
                                    Delivery_Timeline.append(x[0])
                                else:
                                    parsed_date = datetime.strptime(dd.text, "%d %b'%y").date()
                                    # Calculate the difference in days
                                    difference = parsed_date - current_date
                                    y=re.findall(r'(\d.) days,',str(difference))
                                    Delivery_Timeline.append(y[0])
                            else:
                                Delivery_Timeline.append(np.nan)
                    except (TimeoutException, NoSuchElementException) as e:
                        print(f"    > No more listings or element not found on page {i}. Stopping page iteration for {city}.")
                        break
                break
finally:
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
"Delivery_Days":Delivery_Timeline,
"Location":Location,
}
df_hyd=pd.DataFrame(data)
df_hyd.to_csv("carsdata.csv")
time.sleep(30)

print("\n--- Data Collected ---")
print(f"Total Brands: {len(Brand)}")
print(f"Total Models: {len(Model)}")
print(f"Locations: {len(Location)}")