#!/usr/bin/env python
# coding: utf-8

# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


## ARTICLE SCRAPING
# def mars news app
def mars_news(browser):

    # visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

## IMAGE SCRAPING FROM JPL
# def featured_image app
def featured_imaged(browser):

    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    
    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # try/except for error handling
    try:

        # find relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # add base url to create absolute url
     img_url = f'https://spaceimages=mars.com/{img_url_rel}'
    
    return img_url

## GATHERING MARS FACTS
# def mars facts app
def mars_facts():

    #try / except clause
    try:
        # reading in table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of df
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # convert df into HTML format, add bootstrap
    return df.to_html()

browser.quit()

