from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper
import pymongo

# Create an instance of Flask
app = Flask(__name__)




conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.planets
mars = db.mars
print(mars)



# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    #mongo.db.collection.update_many({}, {'$set': mars}, upsert=True)
    #db.mars.insert_many(mars)
    marsdata = list(mars.find())
    # Return template and data
    return render_template("index.html", marsdata=marsdata)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    db.mars.drop()
    data = scraper.scrape()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
