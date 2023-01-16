from flask import Flask, render_template, request, Response, session
import json
from MongoDB.question import question
from MongoDB.userAns import userAns
from MongoDB.ml import ml
from test_questions import Sample
import random
from algo import getNextQuestionOrCareer
from scraper import scraper

#x = scraper("ux frontend developer dbs")
#print(x)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = 'ABCDEFG'
questionTable = question()
userAnsTable = userAns()
mlTable = ml()

def getWeight(ansJson, index):
    
    if (ansJson.get(index)):
        return ansJson[index]
    else:
        return 0.5

def createNewRole(ansJson, role):
    data= {
  "role": role,
  "answer": {
        "1": {
        "weight": getWeight(ansJson, "1"),
        "times": 0
        },
        "2": {
        "weight": getWeight(ansJson, "2"),
        "times": 0
        },
        "3": {
        "weight": getWeight(ansJson, "3"),
        "times": 0
        },
        "4": {
        "weight": getWeight(ansJson, "4"),
        "times": 0
        },
        "5": {
        "weight": getWeight(ansJson, "5"),
        "times": 0
        },
        "6": {
        "weight": getWeight(ansJson, "6"),
        "times": 0
        },
        "7": {
        "weight": getWeight(ansJson, "7"),
        "times": 0
        },
        "8": {
        "weight": getWeight(ansJson, "8"),
        "times": 0
        },
        "9": {
        "weight": getWeight(ansJson, "9"),
        "times": 0
        },
        "10": {
        "weight": getWeight(ansJson, "10"),
        "times": 0
        },
        "11": {
        "weight": getWeight(ansJson, "11"),
        "times": 0
        },
        "12": {
        "weight": getWeight(ansJson, "12"),
        "times": 0
        },
        "13": {
        "weight": getWeight(ansJson, "13"),
        "times": 0
        },
        "14": {
        "weight": getWeight(ansJson, "14"),
        "times": 0
        },
        "15": {
        "weight": getWeight(ansJson, "15"),
        "times": 0
        },
        "16": {
        "weight": getWeight(ansJson, "16"),
        "times": 0
        },
        "17": {
        "weight": getWeight(ansJson, "17"),
        "times": 0
        },
        "18": {
        "weight": getWeight(ansJson, "18"),
        "times": 0
        }
    }
    }
    mlTable.create(data)

def updateML(ansJson, role):
    currentWeight = mlTable.get2(role)
    print(currentWeight)
    if (currentWeight == None):
        createNewRole(ansJson, role)
    else:
        for ans in ansJson:
            currentWeight['answer'][ans]['times'] += 1
            if(ansJson[ans] != currentWeight['answer'][ans]['weight']):
                currentWeight['answer'][ans]['weight'] = (ansJson[ans] + currentWeight['answer'][ans]['weight']) / (currentWeight['answer'][ans]['times'] + 1)
            
        mlTable.put(role , currentWeight['answer'])


@app.route("/")
def homepage():
    session.clear()
    return render_template("index.html")

@app.route("/predict")
def predictpage():
    # session.clear()
    # session["QID"] = str(1)
    session["qBank"] = [str(x) for x in range(1, len(questionTable.get()["questions"])+1)]
    session["answers"] = dict()
    # 1. Check if session[answers] contains all answers to questions
    #   1.1 Else redirect back to homepage
    # 2. Convert all key and values from strings to integers
    # 3. Pass new dict to model
    return render_template("predict.html", role="Software sdada")

@app.route("/guess")
def guesspage():
    # 1. Check if session[answers] contains all answers to questions
    #   1.1 Else redirect back to homepage
    # 2. Convert all key and values from strings to integers
    # 3. Pass new dict to model
    return render_template("guess.html", role="Software sdada")

    
@app.route("/result")
def resultpage():
    # 1. Check if session[answers] contains all answers to questions
    #   1.1 Else redirect back to homepage
    # 2. Convert all key and values from strings to integers
    # 3. Pass new dict to model
    x = scraper(session["career"])
    return render_template("result.html", role=session["career"])

# @app.route("/api/scrape", methods=["POST"])
# def scrapeJobs():
#     if "career" in request.get_json():
#         x = scraper(request.get_json()["career"])

#     else:
#         return ("Invalid parameters", 400)

@app.route("/api/check", methods=["GET"])
def check():
    #questions and answers
    questions_so_far = [int(x) for x in list(session["answers"].keys())]
    answers_so_far = [int(x) for x in list(session["answers"].values())]
    result = getNextQuestionOrCareer(questions_so_far, answers_so_far)
    print(result)
    if len(session["qBank"]) == 0 or result[1] > 0.9:
        session["career"] = result[0]
        response = Response(
            response=json.dumps({
                "completed" : True
            }),
            mimetype="application/json",
            status=200
        )
    else:
        response = Response(
            response=json.dumps({
                "completed" : False
            }),
            mimetype="application/json",
            status=200
        )
    return response
    

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    # for question in questionTable.get():
    #     print (question)

    # return {"question" : "abcdef?"}
    session["QID"] = str(random.choice(session["qBank"]))
    print(session["QID"])
    response = Response(
        # response=json.dumps(questionTable.get()),
        response=json.dumps({
            # "question": Sample.Questions[int(session["QID"])],
            "question": questionTable.get()["questions"][str(session["QID"])],
            "questionID": str(session["QID"])
        }),
        mimetype="application/json",
        status=200
    )
    temp = session["qBank"].copy()
    temp.remove(str(session["QID"]))
    session["qBank"] = temp
    print("Questions Left:", len(session["qBank"]))

    # response = Response(
    #     response=json.dumps(db),
    #     mimetype="application/json",
    #     status=200
    # )
    return response

@app.route("/api/receiveAnswer", methods=["POST"])
def receiveAnswer():
    """
    """
    print(request.get_json())
    if "question" in request.get_json() and "answer" in request.get_json():
        
        session["answers"][str(session["QID"])] = request.get_json()["answer"]

        print(session["answers"])
        session["QID"] = str(int(session["QID"]) + 1)
        return {"success": True}
    else:
        print("inside")
        return ("Invalid parameters", 400)

@app.route("/api/updateModel", methods=["POST"])
def updateModel():
    """
    """
    print(request.get_json())
    
    questions_so_far = [int(x) for x in list(session["answers"].keys())]
    answers_so_far = [int(x) for x in list(session["answers"].values())]
    ansJson = dict()
    for key, value in session["answers"].items():
        ansJson[(key)] = int(value)
    print(ansJson)

    updateML(ansJson, request.get_json()["role"])

    return "success"

if __name__ == "__main__":
    app.run()