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

def updateML():
    ansJson =  {
    "1": 1,
    "2": 1,
    "3": 1,
    "4": 1,
    "5": 0,
    "6": 1,
    "7": 1,
    "8": 1,
    "9": 1,
    "10": 1,
    "11": 1,
    "12": 1,
    "13": 1,
    "14": 1,
    "15": 1,
    "16": 1,
    "17": 1,
    "18": 1,
    "19": 1,
    "20": 1
  }
    role = "Frontend"

    currentWeight = mlTable.get2(role)
    print(currentWeight)
    for ans in ansJson:
        currentWeight['answer'][ans]['times'] += 1
        if(ansJson[ans] != currentWeight['answer'][ans]['weight']):
            currentWeight['answer'][ans]['weight'] = (ansJson[ans] + currentWeight['answer'][ans]['weight']) / (currentWeight['answer'][ans]['times'] + 1)
        
    mlTable.put(role , currentWeight['answer'])

# updateML()

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
    print(x)
    return render_template("result.html", role=session["career"], jobs=x)

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

if __name__ == "__main__":
    app.run()