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



# Drops collection if available to remove duplicates

Mars = db.Mars

# Use PyMongo to establish Mongo connection

# Pass connection to the pymongo instance.
# Use flask_pymongo to set up mongo connection





@app.route('/Scrape')
def Scrape():
    # Mars_Data = Mars.find_one()
    Data = scrape_mars.Scrape()
    # Mars.insert_one(Mars_Data)
    Mars.update({},Data,upsert = True)
    return redirect("/", code=302)


@app.route('/')
def index():

    # Store the entire Mars collection in a list
    Mars_Data = Mars.find_one()
    return render_template("index.html", Mars_info=Mars_Data)

if __name__ == "__main__":
    app.run(debug=True)


