#from MongoDB.get_database import get_database
from MongoDB.get_database import get_database
from bson.objectid import ObjectId

class question:

    def __init__(self):    

        dbname = get_database()
        self.db = dbname["Question List"]

    def get(self):
        return self.db.find_one({ "_id" : ObjectId("63c534d342c3b53658814b03") })

    def post(self,newQuestions):    
        self.db.find_one_and_update({ "_id" : ObjectId("63c534d342c3b53658814b03") }, { '$set': { "questions" : newQuestions} } )

