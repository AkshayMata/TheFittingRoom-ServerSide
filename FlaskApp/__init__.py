from flask import Flask, render_template, request, jsonify, Response
import cgi
import cgitb; cgitb.enable()
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

print("Content-Type: text/html\n\n")

# Connect to Mongo database
def connect():
    client = MongoClient()
    db = client.test
    return db

app = Flask(__name__)
db = connect()

#Send clothing information for app to use
@app.route('/getProducts/<username>')
@app.route('/getProducts/<username>/<filterParams>')
def getProducts(username,filterParams=None):
    cursor = db.shirt.find()
    clothes = ""
    for document in cursor:
        if filterParams is None:
            clothes += str(document)
        else:
            #Get gender information from filter parameters
            if "Men" in filterParams:
                gender = "Men"
            elif "Women" in filterParams:
                gender = "Women"
            else:
                gender = ""
            filters = filterParams.replace(gender,"").split(',')
            filters.remove("")

            category = document["category"]

            #Find filter options in clothing category
            if not any(gender in tag for tag in category):
                continue 
            
            if not filters or any(key in tag for tag in category for key in filters):
                clothes += str(document)

    return clothes

#Get liked clothing of user
@app.route('/getLikedProducts/<user>')
@app.route('/getLikedProducts/<user>/<filterParams>')
def getLikedProducts(user, filterParams=None):
    recentlyLiked = db.users.find({'username': 'AkshayMata'})[0]["prevApproved"]
    recentlyLiked = recentlyLiked[-50:][::-1]
    likedClothes = ""
    for clothingid in recentlyLiked:
        cursor = db.shirt.find({'_id':ObjectId(clothingid)})
        likedClothes += "".join([str(document) for document in cursor])
    return likedClothes

# Update user database for products approved or disapproved
@app.route('/updateLikedProducts/<user>/<productId>/<int:status>')
def updateLikedProducts(user, productId, status):
    if status:
        db.users.update(
            {'username': user},
            {'$push': { 'prevApproved': productId}}
        )
    else:
        db.users.update(
            {'username': user},
            {'$push': { 'prevRejected': productId }}
        )
    return "Updated liked products."
