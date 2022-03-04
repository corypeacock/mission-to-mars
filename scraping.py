#!/usr/bin/env python
# coding: utf-8

# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    # set up Splinter / Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in dict
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': hemi_scrape(browser)
        }

    # stop webdriver and return data
    browser.quit()
    return data

## ARTICLE SCRAPING
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
def featured_image(browser):

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
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

## GATHERING MARS FACTS
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
    return df.to_html(classes='table table-striped')

# Hemisphere data scrape function
def hemi_scrape(browser):

    # visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # create a list to hold the images and titles.
    hemisphere_image_urls = []

    # retrieve the image urls and titles for each hemisphere.
    html = browser.html
    first_soup = soup(html, 'html.parser')
    hemis = first_soup.find_all('div', class_='item')    

    for hemi in hemis:
        hemispheres = {}

        hemi_desc = hemi.find('div', class_='description')
        alink = hemi_desc.find('a')
        href = alink['href']
        title = alink.find('h3').get_text()

        full_url = f'https://marshemispheres.com/{href}'    
        browser.visit(full_url)
        new_html = browser.html

        hemi_soup = soup(new_html, 'html.parser')
        img_list = hemi_soup.find_all('li')

        for li in img_list:
            url_scrape = li.find('a')['href']
            if '.jpg' in url_scrape:
                enhanced_url = f'https://marshemispheres.com/{url_scrape}'
                hemispheres['img_url'] = enhanced_url
                hemispheres['title'] = title
                hemisphere_image_urls.append(hemispheres)

    # quit browser
    browser.quit()

    # return dictionary
    return hemisphere_image_urls


if __name__ == '__main__':
    # if running as script, print scraped data
    print(scrape_all())
