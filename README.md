# Mission to Mars
BC MOd 10

## Overview
This repository contains the files for a simple webpage presenting data on the  
planet Mars that has been scraped from other websites for images, an article title  
and blurb, and a table of facts regarding the red planet.  

### Resources
* PythonData Dev Environment  
* Jupyter Notebook 6.4.6  
* Python 3.7.11  
* HTML  
* Bootstrap  
* MongoDB

Python Dependencies:
* flask
* flask_pymong
* splinter
* BeautifulSoup
* webdriver_manager.chrome
* pandas  
* datetime  

## Explanation
The main components of the webpage are an html file and two python scripts. The html file  
utilizes Bootstrap 3.3 to style the page and its components, and to make the page responsive  
to different devices. It is responsive to the app.py script that inserts the web scraped text  
and images into the index page.  

The app.py script utilizes flask in order to present a simple website. Techinically there are  
two pages: an index page and a second page called 'scrape.' The second page, however, is only  
used to perform the webscrape and return the data back to the index page. The app.py script calls  
the other python script in this bundle to perform the various scraping functions.  

The scraping.py script comprises five functions, one of which calls the other four. The four  
functions gather text and images from various websites using splinter and webdriver_manager  
to navigate to and within the websites, and BeautifulSoup to navigate each website's Document  
Object Model (DOM). 
