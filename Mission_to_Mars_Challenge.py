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


# ## article scraping
# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## image scraping from jpl
# ### featured images
# visit url
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# add base url
img_url = f'https://spaceimages=mars.com/{img_url_rel}'
img_url


# ## gathering mars facts
# reading in table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# ## Deliverable 1: Scrape Full-Res images
# To focus on Deliverable 1, uncomment next two sections below
# # dependencies
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd

# # set up Splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
        if '.tif' in url_scrape:
            enhanced_url = f'https://marshemispheres.com/{url_scrape}'
            hemispheres['img_url'] = enhanced_url
            hemispheres['title'] = title
            hemisphere_image_urls.append(hemispheres)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
