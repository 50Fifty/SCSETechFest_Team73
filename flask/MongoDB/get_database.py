from pymongo import MongoClient

def get_database():

   CONNECTION_STRING = "mongodb+srv://scsetechfest:yXsrnTfh1GoCoUG9@cluster0.hndfgtv.mongodb.net/test"
 
   client = MongoClient(CONNECTION_STRING)
 
   return client['Questions']
  