from flask import render_template, redirect, Flask
from flask_pymongo import PyMongo
import pymongo
import scrape_redfin
from config import username, password
from flask import request


app = Flask(__name__)

# set up mongodb connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/house_app")



@app.route("/")
def home():
    house_data = mongo.db.redfin.find_one()
    return render_template("index.html",redfin = house_data)

@ app.route("/scrape")
def scraper():
    # create two collections in mongo
    redfin = mongo.db.redfin
    redfin_raw = mongo.db.redfin_rawdata
    # store sraped data for plotting and summarze
    house_data = scrape_redfin.data_cleaner(scrape_redfin.scraper())
    house_data_dict = scrape_redfin.summary(house_data)
    scrape_redfin.plot_data(house_data)
    # update summarize data into redfin collections
    redfin.update({},house_data_dict, upsert = True)
    # add rawdata into redfin_raw collection
    rawdata = scrape_redfin.scraper()
    for row in rawdata:
        redfin_raw.insert_one(row)
    
    return redirect("/", code=302)

@app.route("/data")
def data_display():
    house_data = mongo.db.redfin.find_one()
    return render_template("data.html", redfin = house_data)


if __name__=="__main__":
    app.run(debug=True)


