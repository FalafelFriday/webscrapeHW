from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd 
import requests 
import time

def in_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

mars_info={}

def scrape():
    try:
      browser=in_browser()
      url = 'https://mars.nasa.gov/news/'
      browser.visit(url)
      html = browser.html
      soup = BeautifulSoup(html, 'html.parser')
      news_title=soup.find('div',class_='content_title').find('a').text
      news_p=soup.find('div',class_='article_teaser_body').text
      mars_info['news_title'] = news_title
      mars_info['news_paragraph'] = news_p
    return mars_info
    finally:
        browser.quit()


def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = in_browser()
        image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)
        time.sleep(1)
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(1)
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        time.sleep(1)


        html_image = browser.html

        soup = BeautifulSoup(html_image, 'html.parser')
        main_url=  'https://www.jpl.nasa.gov'

        featured_image_url = soup.find('img',class_='fancybox-image')['src']

        image_path=main_url+featured_image_url
        
        image_path

        # Dictionary entry from FEATURED IMAGE
        mars_info['image_path'] = image_path
        
        return mars_info
    finally:

        browser.quit()

def scrape_mars_weather():
    try:
        browser=in_browser()
        weather_url='https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        html_weather = browser.html
        soup=BeautifulSoup(html_weather, 'html.parser')
        mars_weather = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" ).text
        mars_info['weather_tweet'] = weather_tweet        
        return mars_info
    finally:
        browser.quit()

def scrape_mars_facts():
    
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info

def scrape_mars_hemispheres():
try:
    browser=in_browser()
    hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemi_html=browser.html
    soup=BeautifulSoup(hemi_html, 'html.parser')
    hemi_img_urls=[]
    items=soup.find_all('div', class_='item')
    for i in items:
    title=i.find('h3').text
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    browser.visit(hemispheres_url+partial_img_url)
    partial_img_html = browser.html
    soup = BeautifulSoup( partial_img_html, 'html.parser')
    im_url = hemispheres_url + soup.find('img')['src']
    hemi_img_urls.append({"title" : title, "img_url" : im_url})
    mars_info['hemi_img_urls']=hemi_img_urls
    return mars_info
finally:
    browser.quit()