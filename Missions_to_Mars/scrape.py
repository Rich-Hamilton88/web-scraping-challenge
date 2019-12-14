 #Automates browser actions
from splinter import Browser
# Parses the html
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('div', class_='list_text')
    nasa_headline = article.find('div', class_='content_title').text
    nasa_teaser = article.find('div', class_ ='article_teaser_body').text
    mars_data["nasa_headline"] = nasa_headline
    mars_data["nasa_teaser"] = nasa_teaser

    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    #used to drill down to the more info button
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    image_url = soup.select_one("figure.lede a img").get("src")
    image_path = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + image_url
    mars_data["featured_image_src"] = image_path
    

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather_tweet = soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })

    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    mars_data["weather_summary"] = mars_weather


    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)

    Mars = pd.read_html(url_facts)
    Mars_df = Mars[0]
    Mars_df.rename(columns={"Mars": "0", "Facts": "1"})
    mars_facts = Mars_df.to_html(index = True, header =True)
    mars_data["fact_table"] = mars_facts

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
        
        browser.visit(url_hemi)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemi_links = soup.find_all('a', class_='product-item')
        hemi_name = hemi_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        
        hemi_dict['title'] = hemi_name.strip()
        
        
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

    mars_data["hemisphere_imgs"] = hemi_dicts
    
    browser.quit()
        
    return mars_data



