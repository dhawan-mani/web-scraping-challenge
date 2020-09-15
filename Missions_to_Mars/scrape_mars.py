from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import requests
import time
import pandas as pd

def init_browser():
    executable_path ={'executable_path':r'C:\Users\sunandan\Downloads\chromedriver_win32\chromedriver.exe'}
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    return Browser('chrome',**executable_path,headless=False,options=options)
    time.sleep(1)

def Scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

     # Scrape page into Soup
    response = requests.get(url)
    Soup = BeautifulSoup(response.text,'lxml')
#First title on the Web Page
    Title_Results = Soup.find_all('div',class_="content_title")
    Title_list=[]
    for result in Title_Results:
        Title_list.append(result.text.strip())
        new_title = Title_list[0] 

#First Paragraph on the Web Page................................................
    Paragraphs_Results = Soup.find_all('div',class_="rollover_description_inner")
    Paragraphs_List = []
    for result in Paragraphs_Results:
        Paragraphs_List.append(result.text.strip())
        new_p = Paragraphs_List[0]

#Finding Featured image's url...................................................
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    image = browser.find_by_id("full_image").first.click()
    find_image=browser.find_by_css('div[class="fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open"] img')
    for i in find_image:
        featured_image_url =i["src"]
    print(featured_image_url)

#Finding the Facts related to Mars..............................................
    Table = pd.read_html("https://space-facts.com/mars/")
    Mars_df = Table[0]
    Mars_df.columns = ['Attribute','value']
    Mars_df.to_html("Table.html")
    Mars_Table = Mars_df.to_html(index=False).replace('\n','')

#Mars Hemisphere..................................................................
    
    Hemisphere_list= []
    for i in range(0,4,1):
        browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
        full_image = browser.find_by_tag('h3')[i].click()
        find_image=browser.find_by_css('img[class ="wide-image"]')
        find_title=browser.find_by_css('section[class="block metadata"]').find_by_tag('h2').text
        for i in find_image:
            Hemisphere_dict = {}
            image_url = i["src"]
            Hemisphere_dict["title"] = find_title
            Hemisphere_dict["img_url"] = image_url
            Hemisphere_list.append( Hemisphere_dict)


    Dict = {
        "Latest_Title" : new_title,
        "Latest_Paragraph": new_p,
        "Featured_Image" : featured_image_url,
        "Hemisphere_Data" : Hemisphere_list,
        "Mars_Facts" : Mars_Table

    }
    
    browser.quit()
    return Dict

