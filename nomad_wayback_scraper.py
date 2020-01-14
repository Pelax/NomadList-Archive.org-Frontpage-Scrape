from typing import TextIO
from selenium import webdriver
from selenium.webdriver import Chrome as Chrome
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import os
import shutil
import time
import datetime
from selenium.webdriver.common.keys import Keys
import tkinter as tk
from tkinter import filedialog

# path to config file
config_file_path = "config.txt"
# create if it doesn't exists, let user select it
if not os.path.exists(config_file_path):
    root = tk.Tk()
    root.withdraw()
    config_file = open(config_file_path, "w")
    config_file.write(filedialog.askdirectory())
    config_file.close()
# read the config file. First line is the path to the wayback_data
config_file = open(config_file_path, "r")
wayback_data_dir_path = config_file.readline()

wayback_data_csv_path = wayback_data_dir_path + '/wayback_nomadlist_urls.csv'

#os.chdir(r'C:\Users\sleep\Documents\Work\Freelancing\Investor GE\Digital Nomads\data\wayback_data\')
# Webdriver points to the Selenium chromedriver file; driver initiates it

driver = webdriver.Chrome()

'''You only need to run the year/day URL scraper code if you don't have the CSV file with the dates and URLS
If you have the CSV, you can skip to the code that scrapes the frontpage for every day's URL'''
if not os.path.exists(wayback_data_csv_path):
    # Assemble list of year urls from 2015 to current year
    # Each URL links to a page with links to certain months/days
    year_url_list = [str("https://web.archive.org/web/" + str(year) + "0701000000*/nomadlist.com")
                     for year in range(2015, int(datetime.datetime.now().year) + 1)]

    # Open every year URL and put every link from every day on that year page into a dictionary

    day_url_dict = {}

    for url in year_url_list:
        driver.get(url)
        web_elements = driver.find_elements_by_css_selector(".calendar-day a")
        for element in web_elements:
            day_url_dict[element.get_attribute('href')[28:36]] = element.get_attribute('href')
        time.sleep(1)

    # Put the dictionary of year URLs into a CSV file so you don't have to crawl the site again
    # You'll have to change the storage directory to your own
    day_url_df = pd.DataFrame.from_dict(day_url_dict, orient="index")
    day_url_df.to_csv(wayback_data_csv_path)


''' FRONTPAGE SCRAPING CODE STARTS HERE'''
# Read the CSV back into a Pandas dataframe so you can open and download every day's data
# Again, change the directory
nomadlist_data = pd.read_csv(wayback_data_csv_path)
nomadlist_data.columns = ["Date", "URL"]

# Download frontpages in specified index range
''' The frontpage gets remodeled every now and then, so double-check the 
output files periodically to make sure you're getting at least
a few hundred cities loaded per scrape'''

for index, row in nomadlist_data[0:2].iterrows():
    driver.get(row.URL)
    with open(str("nomadlist" + str(row.Date) + '.txt'), "w", encoding = "utf-8") as f:
        f.write(driver.page_source)

# After a certain date, a lot of content goes behind an infinite scroll
# The mess below is trying to get the content to scroll a few times before it scrapes,
# then it has to stop loading so Selenium will move on to the next page
# May not be possible to scroll for all pages--some have content that just doesn't load; probably not stored on Archive

# Most serious problems start after index 72

for index, row in nomadlist_data[73:100].iterrows():
    driver.get(row.URL)
    driver.execute_script('window.scrollTo(0, 4000')
    with open(str("nomadlist" + str(row.Date) + '.txt'), "w", encoding = "utf-8") as f:
        f.write(driver.page_source)


element = driver.find_element_by_css_selector(".dynamic-item-75");
driver.get('https://web.archive.org/web/20180718015001/https://nomadlist.com/')

if element.is_displayed == False:
  driver.execute_script("arguments[1].scrollIntoView();", element)

driver.execute_script('arguments[0].scrollIntoView();", element')

webdriver.find_element_by_class_name('dynamic-item-75')

driver.execute_script('scrollTo(0, 4000)')









'''Below can be ignored for now'''

# Trying to get all the city data is kind of a lot--might just focus on Tbilisi
# nomadlist_city_data = pd.DataFrame(columns=["Date", "City", "Nomad Score", "Nomad Cost", "Internet Speed", "Air Quality", "Temperature", "Region"])
# nomadlist_city_data['Date'] = day_url_dict.keys()
# nomadlist_city_data = nomadlist_city_data.set_index([nomadlist_city_data['Date']])
#
#
# for key in day_url_dict.keys():
#     url = day_url_dict[key]
#     driver.get(url)
#     for city in
#     nomadlist_city_data.loc[str(key)].
#     break
#
# with open("nomadlist_info.csv", 'w') as file:





# for year in range(2016, int(datetime.datetime.now().year) + 1):
#     for month in range(1, 13):
#         # Georgian government air website; different reports accessible by altering dates in the URL
#         url = "http://air.gov.ge/en/reports_page?station=AGMS%2CKZBG%2CVRKT%2CTSRT%2CTBL01&report_type=monthly&date_from=" \
#               + str(year) + "-" + str(month)
#
#         # Open URL, find the XLS download button, and click it using JS
#         driver.get(url)
#         driver.find_element_by_id('xls').click()
#
#         # Wait for the file to download so we can rename and move it
#         while "export.xlsx" not in os.listdir(r"C:\Users\sleep\Downloads"):
#             time.sleep(0.1)
#
#         # Move the file to the project folder
#         shutil.move(r"C:\Users\sleep\Downloads" + "\\" + "export.xlsx",
#                     r"C:\Users\sleep\Documents\Projects\Data Analysis\tbilisi_air_pollution\xls_data" + "\\" + "export.xlsx")
#
#         # Rename the file with the correct date (because date info isn't in the file)
#         os.rename(r"C:\Users\sleep\Documents\Projects\Data Analysis\tbilisi_air_pollution\xls_data\export.xlsx",
#                   r"C:\Users\sleep\Documents\Projects\Data Analysis\tbilisi_air_pollution\xls_data"
#                   + "\\" + str(year) + "-" + str(month) + ".xlsx")
#         date_list.append((year, month))
#
