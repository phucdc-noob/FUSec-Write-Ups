from flask import Flask, session, request, render_template, render_template_string
from flask_session import Session
from random import randint as hack
from waitress import serve
import builtins

app = Flask(__name__, template_folder="template")
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)
authCode = "C4n 1 Trust Y0u? Player "


# Our bot detected that some users had gained access to the system by malicious function, so we decided to ban it.
blacklist = ["'", '"', "request", "readlines", "+", "%2b", "%22", "%27", "linecache"]


def authCheck(input):
    if session.get(input) == None:
        return ""
    return session.get(input)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        session.pop("userCode")
        session.pop("winner")
    except:
        pass
    if request.method == "POST":
        ok = request.form["ok"]
        for ban in blacklist:
            if ban in request.form["name"]:
                return render_template_string("Hacker Alert!!!")
        session["userCode"] = request.form["name"]
        if ok == "Let's play!":
            session["check"] = "access"
            # bypass this? No way haha :D
            winner = "cocailonditconbamay"
            session["winner"] = winner
            return render_template_string(
                "Generating winner hash...<script>setInterval(function(){ window.location='/doanxem'; }, 500);</script>"
            )
    return render_template("index.html")


@app.route("/doanxem", methods=["GET", "POST"])
def doanxem():
    try:
        if authCheck("check") == "":
            return render_template_string(authCode + authCheck("userCode"))
        else:
            if request.method == "POST":
                winner_input = request.form["winner"]
                if winner_input == authCheck("winner"):
                    mess = (
                        "You are the real winner!!!!!!!!!! "
                        + authCheck("userCode")
                        + ", here your flag: https://youtu.be/dQw4w9WgXcQ"
                    )
                elif winner_input != authCheck("winner"):
                    mess = "Wrong! You die!<script>setInterval(function(){ window.location='/choilai'; }, 1200);</script>"
                return render_template_string(mess)
            return render_template("doanxem.html")
    except:
        pass
    return render_template_string(authCode + authCheck("userCode"))


@app.route("/choilai")
def reset_access():
    try:
        session.pop("check")
        return render_template_string(
            "You got an Extra Change. Gud luck :D!!!!!!<script>setInterval(function(){ window.location='/'; }, 500);</script>"
        )
    except:
        pass
    print(authCheck("userCode"))
    return render_template_string(authCode + authCheck("userCode"))


if __name__ == "__main__":
    app.secret_key = "###########"
    serve(app, host="0.0.0.0", port=8900)
