from flask import Flask, render_template, request, Response
import json
from MongoDB.question import question
from MongoDB.userAns import userAns

app = Flask(__name__)
questionTable = question
userAnsTable = userAns

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    for question in questionTable.get():
        print (question)

    # return {"question" : "abcdef?"}
    response = Response(
        response=json.dumps(db),
        mimetype="application/json",
        status=200
    )
    return response

@app.route("/api/receiveAnswer", methods=["POST"])
def receiveAnswer():
    """
    """
    if "question" in request.json and "answer" in request.json:
        qn, ans = request.json["question"], request.json["answer"]
        """
        TODO
        Add code here to return question and answer back to model
        """
        return {"success": True}
    else:
        return ("Invalid parameters", 400)

if __name__ == "__main__":
    app.run()
