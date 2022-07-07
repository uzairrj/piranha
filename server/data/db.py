from pymongo import mongo_client

con = mongo_client.MongoClient("mongodb://localhost:27017")

db = con.piranha