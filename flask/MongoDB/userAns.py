from MongoDB.get_database import get_database

class userAns:

    def __init__(self):    

        dbname = get_database()
        self.db = dbname["User"]

    def get(self):
        return self.db.find()

    def post(self,newAnswer):

        self.db.insert_one(newAnswer)