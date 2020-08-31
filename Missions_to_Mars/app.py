#######################################################
# Configuration
#######################################################

from flask import Flask, jsonify, render_template
from flask import redirect, request, url_for
from wtforms import Form, DateField, validators
from flask_pymongo import PyMongo

import scrape_mars

#######################################################
# Flask Setup
#######################################################
# Init app
app = Flask(__name__)
#######################################################
# Database Setup
#######################################################
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
#######################################################
# Flask Routes
#######################################################

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find records of data from the mongo database
    news_data = mongo.db.mars_news
    latest_news = []
    id = 1
    for s in news_data.find():
        latest_news.append({'ID':id, 'Date' : s['Date'], 'News_Title' : s['News_Title'],
                            'News_Paragraph': s['News_Paragraph'], 'Image_Name':s['Image_Name'],
                            'Image_URL':s['Image_URL']})
        if id == 1: head_news = [s['News_Title'], s['News_Paragraph']]
        id +=1
    # Return template and data
    return render_template("home.html", data=latest_news, head_news = head_news)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    news_data = scrape_mars.latest_news()

    # Update the Mongo database using update and upsert=True
    for news in news_data:
        mongo.db.collection.update({}, news, upsert=True)

    # Redirect back to home page
    return redirect("/")

# Route that will trigger the facts html page
@app.route("/facts")
def facts():
    # Find records of data from the mongo database
    facts_data = mongo.db.mars_facts
    mars_facts = []
    for s in facts_data.find():
        mars_facts.append({'Description' : s['Description'], 'Mars_Fact' : s['Mars_Fact']})
    # Return template and data
    return render_template("facts.html", data=mars_facts)

# Route that will trigger the hemisphere html page
@app.route("/hem")
def hem():
    # Redirect back to home page
    return redirect("/")

# Route that will trigger the contacts html page
@app.route("/contacts")
def contacts():
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
