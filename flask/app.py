from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/getQuestion", methods=["POST"])
def getQuestion():
    """
    Add code here to get question.
    """
    return {"question" : "abcdef"}

if __name__ == "__main__":
    app.run()
