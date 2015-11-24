"""
    This init file is loaded by apache2 (via wcgi scripts) and 
    handles various web services for TheFittingRoom. 
"""
import cgi
import cgitb; cgitb.enable()
import json
from bson.objectid import ObjectId
from flask import Flask, render_template, request, jsonify, Response
from pymongo import MongoClient

print("Content-Type: text/html\n\n")


def connect():
    """ 
        Connect to MongoDB 
        Returns MongoDB adapter
    """
    client = MongoClient()
    db = client.test
    return db


def verifyUserToken(username,token):
    """ 
        Check input token is correct for the user
        Returns bool
    """
    try:
        user = db.users.find({'username': username,'_id': ObjectId(token)})[0]
        return True
    except:
        return False


def checkFilters(filter_params, document):
    """ 
        Check to see if the clothing fits the filter critera
        Returns the clothing information if the filter criteria is met
    """
    if filter_params is None:
        return str(document)

    #Get gender information from filter parameters
    if "Men" in filter_params:
        gender = "Men"
    elif "Women" in filter_params:
        gender = "Women"
    else:
        gender = ""
    filters = filter_params.replace(gender,"").split(',')
    if not gender == "":
        filters.remove("")

    category = document['category']

    #Find filter options in clothing category
    if not any(gender in tag for tag in category):
       return "" 
    
    if not filters or any(key in tag for tag in category for key in filters):
        return str(document)

    return ""


app = Flask(__name__)
db = connect()


@app.route('/getProducts/<user>/<token>')
@app.route('/getProducts/<user>/<token>/<filter_params>')
def getProducts(user, token, filter_params=None):
    """ 
        Send clothing information to the client
        Returns a JSON string of clothing objects
    """ 
    if not verifyUserToken(user,token):
        return "Invalid user/token combination"
    cursor = db.shirt.find()
    clothes = ""
    clothes = "".join([checkFilters(filter_params, doc) for doc in cursor])
    return clothes


@app.route('/getLikedProducts/<user>/<token>')
@app.route('/getLikedProducts/<user>/<token>/<filter_params>')
def getLikedProducts(user, token, filter_params=None):
    """ 
        Get liked clothing for a user
        Returns a JSON string previously liked clothing for the user
    """
    if not verifyUserToken(user,token):
        return "Invalid user/token combination"
    userInfo = db.users.find({'username': user})[0]
    recentlyLiked = userInfo['prevApproved'][-50:][::-1]
    likedClothes = ""
    for clothingid in recentlyLiked:
        cursor = db.shirt.find({'_id': ObjectId(clothingid)})
        likedClothes += "".join([checkFilters(filter_params, doc)\
                                for doc in cursor])
    return likedClothes


@app.route('/updateLikedProducts/<user>/<token>/<product_id>/<int:status>')
def updateLikedProducts(user, token, product_id, status):
    """
        Update user data for products approved or disapproved
    """
    try:

        if not verifyUserToken(user,token):
            return "Invalid user/token combination"
        if status:
            db.users.update(
                {'username': user},
                {'$push': { 'prevApproved': product_id}}
            )
        else:
            db.users.update(
                {'username': user},
                {'$push': { 'prevRejected': product_id }}
            )
        return "Updated liked products."
    except:
        return "Updating liked products failed."


@app.route('/authenticate/<user>/<password>')
def authenticate(user, password):
    """
        Authenticate user information
        Returns the user token or an error message.
    """
    try:
        userId = db.users.find({'username': user})[0]
        if userId['password'] == password:
            return str(userId['_id'])
        return "Invalid User/Password Combination"
    except:
        return "User Not Registered"
