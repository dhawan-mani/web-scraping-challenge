from flask import Flask,render_template,redirect
# from flask_pymongo import PyMongo
import pymongo 
import scrape_mars



conn ='mongodb://localhost:27017/'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client['Data']
Data = db['Data']
Collection = Data.Collection

# Collection.insert_one ({
#     "Name" :"Himani Dhawan",
# });
app = Flask(__name__)

@app.route('/Scrape')
def Scrape():
    # Mars_Data = Mars.find_one()
    Data = scrape_mars.Scrape()
    # Mars.insert_one(Data)
    Collection.update({},Data,upsert = True)
    return redirect("/", code=302)
if __name__ == "__main__":
    app.run(debug=True)
