# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask import Flask, render_template
from flask_pymongo import pymongo
import scrape
import pandas as pd
import time

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

@app.route("/")
def home():
    mars_data = db.collection.find()
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.collection.insert_one(mars_data)
    


if __name__ == "__main__":
     app.run(debug=True)