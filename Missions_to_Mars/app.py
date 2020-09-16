from flask import Flask,render_template,redirect
# from flask_pymongo import PyMongo
import pymongo 
import scrape_mars



conn ='mongodb://localhost:27017/'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client['Mars_db']
Mars_Data = db['Mars_Data']

# Create an instance of Flask
app = Flask(__name__)


Mars = db.Mars


# Scraped the mars data

@app.route('/Scrape')
def Scrape():
    Data = scrape_mars.Scrape()          
    Mars.update({},Data,upsert = True)
    return redirect("/", code=302)


@app.route('/')
def index():

    # Store the entire Mars collection in Mars_Data
    Mars_Data = Mars.find_one()
    return render_template("index.html", Mars_info=Mars_Data)

if __name__ == "__main__":
    app.run(debug=True)


