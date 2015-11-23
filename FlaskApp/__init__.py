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

#Check input token is correct for the user
def verifyUserToken(username,token):
    try:
        user = db.users.find({'username': username,'_id': ObjectId(token)})
        return True
    except:
        return False

def checkFilterCriteria(filterParams, document):
    if filterParams is None:
        return str(document)

    #Get gender information from filter parameters
    if "Men" in filterParams:
        gender = "Men"
    elif "Women" in filterParams:
        gender = "Women"
    else:
        gender = ""
    filters = filterParams.replace(gender,"").split(',')
    if not gender == "":
        filters.remove("")

    category = document["category"]

    #Find filter options in clothing category
    if not any(gender in tag for tag in category):
       return "" 
    
    if not filters or any(key in tag for tag in category for key in filters):
        return str(document)

    return ""

app = Flask(__name__)
db = connect()

#Send clothing information for app to use
@app.route('/getProducts/<user>/<token>')
@app.route('/getProducts/<user>/<token>/<filterParams>')
def getProducts(user, token, filterParams=None):
    if not verifyUserToken(user,token):
        return "Invalid user/token combination"
    cursor = db.shirt.find()
    clothes = ""
    clothes = "".join([checkFilterCriteria(filterParams, doc) for doc in cursor]) 
    return clothes


#Get liked clothing of user
@app.route('/getLikedProducts/<user>/<token>')
@app.route('/getLikedProducts/<user>/<token>/<filterParams>')
def getLikedProducts(user, token, filterParams=None):
    if not verifyUserToken(user,token):
        return "Invalid user/token combination"
    recentlyLiked = db.users.find({'username': 'AkshayMata'})[0]["prevApproved"]
    recentlyLiked = recentlyLiked[-50:][::-1]
    likedClothes = ""
    for clothingid in recentlyLiked:
        cursor = db.shirt.find({'_id':ObjectId(clothingid)})
        likedClothes += "".join([checkFilterCriteria(filterParams, doc) for doc in cursor])
    return likedClothes

# Update user database for products approved or disapproved
@app.route('/updateLikedProducts/<user>/<token>/<productId>/<int:status>')
def updateLikedProducts(user, token, productId, status):
    if not verifyUserToken(user,token):
        return "Invalid user/token combination"
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

#Authenticate user infomation
@app.route('/authenticate/<user>/<password>')
def authenticate(user, password):
    try:
        userId = db.users.find({'username':user})[0]
        if userId["password"] == password:
            return str(userId["_id"])
        return "Invalid User/Password Combination"
    except:
        return "User Not Registered"
