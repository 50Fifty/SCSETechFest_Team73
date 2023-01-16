from MongoDB.get_database import get_database

class ml:

    def __init__(self):    

        dbname = get_database()
        self.db = dbname["ML"]

    def get(self):
        return self.db.find()

    def get(self , role):
        return self.db.find_one({"role":role})

    
    def put(self , role , answer):
        self.db.find_one_and_update({'role':role}, { '$set': { "answer" : answer} } )
        