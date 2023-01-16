from MongoDB.get_database import get_database

class question:

    def __init__(self):    

        dbname = get_database()
        self.db = dbname["Question List"]

    def get(self):
        return self.db.find()

    def post(self,newQuestions):

        self.db.insert_one(newQuestions)



