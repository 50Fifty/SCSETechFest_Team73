from MongoDB.get_database import get_database

class ml:

    def __init__(self):    

        dbname = get_database()
        # dbname = dbname.create_collection("ML", validator={
        #     '$jsonSchema': {
        #         'bsonType': 'object',
        #         'additionalProperties': True,
        #         'required': ['component', 'path'],
        #         'properties': {
        #             'component': {
        #                 'bsonType': 'string'
        #             },
        #             'path': {
        #                 'bsonType': 'string',
        #                 'description': 'Set to default value'
        #             }
        #         }
        #     }
        # })
        self.db = dbname["ML"]

    def get(self):
        return self.db.find()

    def get2(self , role):
        return self.db.find_one({"role":role})

    def create(self,role):
        return self.db.insert_one(role)
    
    def put(self , role , answer):
        self.db.find_one_and_update({'role':role}, { '$set': { "answer" : answer} } )
        