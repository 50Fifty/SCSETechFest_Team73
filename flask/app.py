from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    """
    TODO
    Add code here to get question.
    """
    # return {"question" : "abcdef?"}
    response = Response(
        response=json.dumps({"question": "abcdefg?"}),
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
