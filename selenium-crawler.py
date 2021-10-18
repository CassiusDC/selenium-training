from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import pandas as pd
import csv
import time

#Initialize the list where we store our results
results = []

#Setup webdriver
driver = webdriver.Chrome()

#Load first URL
url = "http://www.tiffathai.org/member/index.php"
driver.get(url)

#Initialize other lists we will use for storing company URLs
seleniumURL = []
companyURL = []

#Change range (1,12) to how many pages the list has
#Loop can be made dynamic like: while(nextPage == True)
for x in range(1,12):
    #Get all links on this page
    seleniumURL = driver.find_elements_by_css_selector("body > table:nth-child(4) > tbody > tr:nth-child(3) > td > table > tbody > tr > td > table > tbody > tr > td > nobr > a")

    #Convert the selenium attribute to href links by using get_attribute("href")
    for url in seleniumURL:
        companyURL.append(url.get_attribute("href")) 

    #Click next page
    nextPage = driver.find_element_by_css_selector("body > table:nth-child(4) > tbody > tr:nth-child(3) > td > table > tbody > tr > td > table > tbody > tr:nth-child(24) > td > font > font + a")
    nextPage.click()

#Loop through companyURL
for urls in companyURL:
    #load URL
    driver.get(urls)

    #Get all information
    try:
        companySelector = driver.find_element_by_css_selector("body > table > tbody > tr > td > font > strong")
    except Exception as e: #if a selector doesn't exist, return set as blank ("")
        companySelector = ""

    addressSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(3) > td:nth-child(4) > pre")
    telephoneSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(4) > td:nth-child(4)")
    faxSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(5) > td:nth-child(4)")
    emailSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(6) > td:nth-child(4) > a")
    websiteSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(7) > td:nth-child(4) > a")
    contactPersonSelector = driver.find_element_by_css_selector("body > table.text2_thai > tbody > tr:nth-child(8) > td:nth-child(4)")
    
    #Put all information in a list (don't forget to add .text to the variable name)
    results.append([companySelector.text, addressSelector.text, telephoneSelector.text, faxSelector.text, emailSelector.text, websiteSelector.text, contactPersonSelector.text])

#convert list to dataframe to add column names
resultsDF = pd.DataFrame(results, columns = ("company_name", "address", "telephone", "fax", "email", "website", "contact_person"))

#convert dataframe to csv
resultsDF.to_csv("tiffa_list.csv")

