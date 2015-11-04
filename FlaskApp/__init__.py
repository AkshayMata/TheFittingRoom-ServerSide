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

# Send clothing information for app to use
@app.route('/getProducts/<username>')
@app.route('/getProducts/<username>/<filterParams>')
def getProducts(username,filterParams=None):
    cursor = db.shirt.find()
    clothes = ""
    for document in cursor:
        clothes += str(document)
    return clothes
    #return 'getProducts' + username + str(filterParams)

# Send previously liked clothing for a user for the app to use
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
    #return Response(json.dumps(recentlyLiked), mimetype='application/json')

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

