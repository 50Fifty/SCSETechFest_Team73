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
    session["QID"] = 0
    return render_template("index.html")

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    # for question in questionTable.get():
    #     print (question)

    # return {"question" : "abcdef?"}
    print(session["QID"])
    response = Response(
        response=json.dumps(questionTable.get()),
        response=json.dumps({
            "question": Sample.Questions[session["QID"]],
            "questionID": session["QID"]
        }),
        mimetype="application/json",
        status=200
    )

    session["QID"] += 1

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
        
        qn, ans = request.json["question"], request.json["answer"]
        """
        TODO
        Add code here to return question and answer back to model
        """
        return {"success": True}
    else:
        print("inside")
        return ("Invalid parameters", 400)

if __name__ == "__main__":
    app.run()