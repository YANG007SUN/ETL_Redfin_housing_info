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

@ app.route("/scrape")
def scraper():
    redfin = mongo.db.redfin
    house_data = scrape_redfin.data_cleaner(scrape_redfin.scraper())
    house_data_dict = scrape_redfin.summary(house_data)
    redfin.update({},house_data_dict, upsert = True)
    scrape_redfin.plot_data(house_data)
    return redirect("/", code=302)

@app.route("/data")
def data_display():
    house_data = mongo.db.redfin.find_one()
    return render_template("data.html", redfin = house_data)


if __name__=="__main__":
    app.run(debug=True)


