import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as soup
import urllib2
from urllib2 import urlopen



def indeed(title,location):  

    driver = webdriver.Chrome("/Users/cynthiacheng/Desktop/linkedScrapper/chromedriver")
    
    filename = "jobs.csv" 
    f = open(filename,"w")
    headers = "Title, Company, Location, Link\n"
    f.write(headers)

    URLCount = "http://www.indeed.com/jobs?q=cyber+security&l=USA&limit=60&filter=0"
    soupCount = soup(urlopen(URLCount).read(), 'html.parser')
    numResults = soupCount.find("div", attrs = {"id": "searchCount"}).text
    resultsNum = int(numResults.split(' ')[-1].replace(',', ''))

    for x in range(1): # max pages is resultsNum/55 but not gicen to us
        url = "https://www.indeed.com/jobs?q={}&l={}&limit=50&start={}".format(title, location, str(x*50))
        driver.get(url)

        titles = driver.find_elements_by_class_name("jobtitle")
        companies = driver.find_elements_by_class_name("company")
        locations = driver.find_elements_by_class_name("location")
        links = driver.find_elements_by_css_selector('.jobtitle a')




        for i in range(0,len(companies)):
            if (i < 3 or i > 52):
                try: 
                    f.write('"' + titles[i].text[0:len(titles[i].text)-9] + '","' + companies[i].text+ '","' +locations[i].text  + '"\n') #
                except UnicodeEncodeError:
                    pass
            else:
                try: 
                    f.write('"' + titles[i].text[0:len(titles[i].text)-9] + '","' + companies[i].text+ '","' +locations[i].text + '","' + links[x].get_attribute('href') + '"\n')
                except UnicodeEncodeError:
                    pass
                x+=1


        # page_html = driver.page_source.encode('ascii', 'ignore')
        # html = soup(page_html, "html.parser")
        # containers = html.findAll("div",{"class":"search-result__info"})

        # for container in containers:
        #     step1 = container.findAll("p",{"class":"search-result__snippets"})

        #     if step1 and "Current:" in step1[0].text and "at" in step1[0].text:
        #         step2 = step1[0].text 
        #         step3 = step2[step2.find(":")+1: ] 
        #         step4 = step3.split(" at ")
        #         position = step4[0].strip()
        #         company = step4[1].strip()
        #         positions.append(position)
        #         companies.append(company)

        #     else:
        #         positions.append("Position Not Found")
        #         companies.append("Company Not Found") 

    f.close()
    driver.quit()

print("Scraping Indeed...")
indeed("Cyber+Security","USA")
print("Information scraped to file labeled \"jobs.csv\"")
