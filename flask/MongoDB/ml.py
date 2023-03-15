#from MongoDB.get_database import get_database
from get_database import get_database

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

if __name__ == "__main__":
    ML = ml()

    data= {
  "role": "Software Dev",
  "answer": {   
        "1": {
        "weight": 0,
        "times": 0
        },
        "2": {
        "weight": 1,
        "times": 0
        },
        "3": {
        "weight": 1,
        "times": 0
        },
        "4": {
        "weight": 0,
        "times": 0
        },
        "5": {
        "weight": 0,
        "times": 0
        },
        "6": {
        "weight": 0,
        "times": 0
        },
        "7": {
        "weight": 0,
        "times": 0
        },
        "8": {
        "weight": 0,
        "times": 0
        },
        "9": {
        "weight": 1,
        "times": 0
        },
        "10": {
        "weight": 1,
        "times": 0
        },
        "11": {
        "weight": 1,
        "times": 0
        },
        "12": {
        "weight": 0,
        "times": 0
        },
        "13": {
        "weight": 0,
        "times": 0
        },
        "14": {
        "weight": 1,
        "times": 0
        },
        "15": {
        "weight": 1,
        "times": 0
        },
        "16": {
        "weight": 0,
        "times": 0
        },
        "17": {
        "weight": 0,
        "times": 0
        },
        "18": {
        "weight": 0,
        "times": 0
        }
    }
    }
    ML.create(data)