#!/usr/bin/env python
# coding: utf-8

#dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# use flask_pymong to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# setting up the index route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# set up the scraping route
@app.route('/scrape')
def scrape():
    mars = mong.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {'$set':mars_data}, upsert=True)
    return rediret('/', code=302)

if __name__ == '__main__':
    app.run()

