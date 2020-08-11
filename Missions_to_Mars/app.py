# Import the various dependencies and setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#-------------------#

# Flask Setup
app = Flask(__name__)

#-------------------#

# PyMongo Database set-up
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#-------------------#

# Flask Routes

# Set route to query MongoDB and render the Mars data in HTML
@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

# Set route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert = True)
    return redirect("/")

#-------------------#

if __name__ == "__main__":
    app.run(debug = False)