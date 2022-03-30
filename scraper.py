from gettext import install
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from splinter import Browser
import pymongo
import pandas as pd
import numpy as np

#db.mars.drop()
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.planets
mars = db.mars




def scrape():
        #Latest article and para
    mars_data = {}
        
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="content_title")
    mars_data["news_title"] = str(results[0].text)

    results2 = soup.find_all('div', class_="rollover_description_inner")
    mars_data["news_p"] =str(results2[0].text)

    #Featured image
    url = 'https://spaceimages-mars.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.find_by_css('a.showimg.fancybox-thumbs').click()
    href = browser.links.find_by_partial_href('image')
    mars_data["featured_image_url"] = href["href"]
    browser.quit()

    ##Table
    import markupsafe
    url = 'https://galaxyfacts-mars.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # = soup.find('table', class_="table table-striped")
    df_pandas = pd.read_html(url, attrs = {'class': 'table table-striped'},  flavor='bs4', thousands ='.')
    table = df_pandas[0].to_html(classes='data', header="true")
    mars_data["Table"]= markupsafe.Markup(table)
    result = {}
    for row in soup.table.find_all('tr'):
        row_header = row.th.get_text()
        row_cells = row.find_all('td')
        row_data = [row_cells[0].get_text(), row_cells[1].get_text()] 
        result[row_header] =  row_data
    mars_data["Table2"]= result
    #data = df_pandas[0].values
    #print(data)
    #tabledic={}
    #for row in data:
    #    tabledic["data"]=row
    #for heading in headings:
    #    tabledic["headings"] = headings
    #

    #hemispheres
    url = 'https://marshemispheres.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hemispheres = []
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    for x in range(4):
        hemispheres_dic={}
        browser.find_by_css("a.product-item h3")[x].click()
        title = browser.find_by_css("h2.title").text
        hemispheres_dic["title"]=title
        href= browser.links.find_by_text('Sample').first
        url = href['href']
        browser.back()
        hemispheres_dic["img_url"]=url
        hemispheres.append(hemispheres_dic)
        
    mars_data["hemispheres_dic"] = hemispheres
    print(mars_data['featured_image_url'])

    browser.quit()
    mars.insert_one(mars_data)
    #
    return mars_data

mars_data = scrape()
print(list(mars.find()))
    
       
