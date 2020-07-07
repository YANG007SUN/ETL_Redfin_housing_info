from flask import render_template, redirect, Flask
from flask_pymongo import PyMongo
import pymongo
import scrape_redfin
from config import username, password


app = Flask(__name__)

# set up mongodb connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/house_app")


@app.route("/")
def home():
    house_data = mongo.db.redfin.find_one()
    return render_template("index.html",redfin = house_data)

@app.route("/scrape")
def scraper():
    redfin = mongo.db.redfin
    house_data = scrape_redfin.summary(scrape_redfin.data_cleaner(scrape_redfin.scraper()))
    redfin.update({},house_data, upsert = True)
    return redirect("/", code=302)

if __name__=="__main__":
    app.run(debug=True)

