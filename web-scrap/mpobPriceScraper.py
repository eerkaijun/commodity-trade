###### DOCUMENTATION ######
# Malaysia Palm Oil Prices
# http://bepi.mpob.gov.my/admin2/daily.php
# Scrape the malaysia palm oil prices for the past 10 years + 
# Need an interactive web scraper to select year (refer to website) 
# Download chromedriver executable (https://chromedriver.chromium.org/downloads)
# Make sure to save chromedriver.exe in the same directory as this script
# Run command 'python mpobPriceScraper.py' to execute this script
###########################


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import numpy as np
import pandas as pd
import csv
import requests
import os

today = str(pd.to_datetime('today'))
currentYear = int(today[0:4])

# Returns a list of dates that are formatted and in the same sequence as the mpob data collected 
def createDates(year):
    dates = []
    day = 1
    month = 1
    for i in range(31):
        for j in range(12):
            dates.append(str(day) + "-" + str(month) + "-" + str(year))
            month += 1
        day += 1
        month = 1
    formatDates = [pd.to_datetime(date, format ="%d-%m-%Y", errors="coerce")for date in dates]
    return formatDates

# Match the date list and the price list together
def combineData(year, contents):
    dates = createDates(year)
    for i in range(len(dates)):
        dates[i] = str(dates[i].date())
    dates = [x for x in dates if x != 'NaT']
    prices = []
    for i in contents:
        new = i.split()[1:]
        for j in new:
            try:
                j = float(j.replace(',',''))
            except:
                j=''
            prices.append(j)
    for i in range(len(dates)):
        tocsv[dates[i]] = prices[i]


# Use selenium to navigate mpob's php site
tocsv = {}
try:
    with open('mpob.csv', 'r') as readFile:
        reader = list(csv.reader(readFile))
        year = int(reader[-1][0][0:4])
		#get the last year if the file exists, and only update starting from that year
    readFile.close()
except:
    year = 2008 # Starting year is 2008 in mpob website
    # Create new file mpob.csv
    with open('mpob.csv', 'a', newline='') as appendFile:
            writer = csv.writer(appendFile)
            writer.writerow(['Date','Price'])  
    
print("Opening selenium chrome bot...")
options = Options()
#link to chromedriver
bot = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')
bot.get('http://bepi.mpob.gov.my/admin2/daily.php')

while year<=currentYear:
    print("Running mpob web bot for year: "+ str(year))
    time.sleep(3)
    header = bot.find_elements_by_tag_name('h2')
    select = Select(bot.find_elements_by_name('tahun')[2])
    select.select_by_value(str(year))
    bot.find_element_by_name('Submit123').click()
    time.sleep(3)
    bot.switch_to.default_content()

    elements = bot.find_elements_by_tag_name('tr')
    contents = [el.text for el in elements]
    contents = contents[5:-1]
    combineData(year, contents)
    year+=1
    bot.back()
# Append to the file
with open('mpob.csv', 'a', newline='') as writeFile:
    writer = csv.writer(writeFile)
    try:
        for row in reader: # Check if preexisting file exists and deletes dictionary key to prevent duplicates
            if row[0] in tocsv:
                del tocsv[row[0]]
    except:
        pass
    finally:
		# Sort the items by date, list of tuples is returned 
        tocsv_items = tocsv.items()
        tocsv_sorted = sorted(tocsv_items)
        # Update all the values that do not previously exist in the csv file
        for i in tocsv_sorted:
            if i[1] == '':
                continue
            else:
                writer.writerow([i[0], i[1]])


writeFile.close()
bot.quit()
# Close file and close the bot
print("mpob data retrieval success!")
