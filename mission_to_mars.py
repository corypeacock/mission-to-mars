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
# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


## AFTER running the previous cell
# we look at the page itself looking for the tag that will give us the title of the articles
slide_elem.find('div', class_='content_title')

# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


## IMAGE SCRAPING FROM JPL
### featured images

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

# add base url to create absolute url
img_url = f'https://spaceimages=mars.com/{img_url_rel}'
img_url


## GATHERING MARS FACTS
# reading in table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

browser.quit()

