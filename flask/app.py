from flask import Flask, render_template, request, Response, session
import json
from MongoDB.question import question
from MongoDB.userAns import userAns
from MongoDB.ml import ml
from test_questions import Sample

app = Flask(__name__)
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

    currentWeight = mlTable.get(role)
    for ans in ansJson:
        currentWeight['answer'][ans]['times'] += 1
        if(ansJson[ans] != currentWeight['answer'][ans]['weight']):
            currentWeight['answer'][ans]['weight'] = (ansJson[ans] + currentWeight['answer'][ans]['weight']) / (currentWeight['answer'][ans]['times'] + 1)
        
    mlTable.put(role , currentWeight['answer'])

@app.route("/")
def homepage():
    session["QID"] = str(1)
    session["answers"] = dict()
    return render_template("index.html")

@app.route("/result")
def resultpage():
    # 1. Check if session[answers] contains all answers to questions
    #   1.1 Else redirect back to homepage
    # 2. Convert all key and values from strings to integers
    # 3. Pass new dict to model
    return render_template("result.html", role="Software Engineer")

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    # for question in questionTable.get():
    #     print (question)

    # return {"question" : "abcdef?"}
    print(session["QID"])
    response = Response(
        response=json.dumps(questionTable.get()),
        response=json.dumps({
            "question": Sample.Questions[int(session["QID"])],
            "questionID": str(session["QID"])
        }),
        mimetype="application/json",
        status=200
    )

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
    print("TEST")
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