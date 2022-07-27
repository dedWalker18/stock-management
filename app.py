from flask import Flask, render_template, redirect, url_for
from application.database import *
from flask import request
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

user = "Lakshya"
password = "abcd"

from application.database import db

# Creating the flask app variable
app = Flask(__name__)

# Initialising the DB using SQLAlchemy, pushing content to the app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()

@app.route("/")
@app.route("/homepage")
def home():   
    return render_template("home.html")

@app.route("/rewards", methods=["GET", "POST"])
def rewards():
    numoftrackers = Trackers.query.filter_by().count()
    numoflogs= Logs.query.filter_by().count()
    XP = (numoftrackers * 200) + (numoflogs * 50)
    level = (XP // 1000) + 1
    width = XP / (level * 1000) * 100
    return render_template("rewards.html", numoftrackers=numoftrackers, numoflogs=numoflogs, level=level, width=width)

@app.route("/motivation")
def motivation():

    return render_template("motivation.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")
    
@app.route("/dashboard", methods={"GET", "POST"})
def dashboard():
    TrackersTable = Trackers.query.all()
    numoflogs = Logs.query.filter_by().count()
    numoftrackers = Trackers.query.filter_by().count()
    T1 = Trackers.query.filter_by(TrackerType = "Integer").all()
    T2 = Trackers.query.filter_by(TrackerType = "MC").all()
    intloglist = []
    for i in T1:
        l = Logs.query.filter_by(TrackerId = i.TrackerId).all()
        intloglist.extend(l)
    mcloglist = []
    for i in T2:
        l = Logs.query.filter_by(TrackerId = i.TrackerId).all()
        mcloglist.extend(l)

    y = np.array([len(intloglist), len(mcloglist)])
    mylabels = ["Number of integer Logs", " Number of Multiple Choice Logs"]


    plt.pie(y, labels = mylabels)
    #plt.savefig("static/chart.jpg")
    
    return render_template("dashboard.html", trackers=TrackersTable, numoflogs=numoflogs, numoftrackers=numoftrackers) 

@app.route("/trackers/<TrackerId>", methods=["POST", "GET"])
def trackerspage(TrackerId):
    if request.method == "POST":
        l = Logs(LogValue=request.form.get("LogValue"), TrackerId=TrackerId)
        db.session.add(l)
        db.session.commit()
        return redirect("/dashboard")
    if request.method == "GET":
        T1 = Trackers.query.filter_by(TrackerId=TrackerId).first() 
        loglist = Logs.query.filter_by(TrackerId=TrackerId)
        if T1.TrackerType == "Integer":
            return render_template("addlogint.html", TrackerId = TrackerId, loglist=loglist)
        else:
            return render_template("addlogmc.html", TrackerId=TrackerId, loglist=loglist)
   
@app.route("/updatelog/<logid>", methods=["POST", "GET"])
def updatelog(logid):
    if request.method == "POST":
        logid = int(logid)
        l = Logs.query.filter_by(LogId = logid).first()
        l.LogValue = request.form.get("LogValue")
        db.session.commit()
        return redirect("/dashboard")
    if request.method == "GET":
        logid = int(logid)
        l = Logs.query.filter_by(LogId = logid).first()
        T = Trackers.query.filter_by(TrackerId = l.TrackerId).first()
        type = T.TrackerType        
        return render_template("updatelog.html", logid=logid, TrackerType=type)


@app.route("/deletelog/<logid>", methods=["GET"])
def deletelog(logid):
    logid = int(logid)
    l = Logs.query.filter_by(LogId = logid).first()
    db.session.delete(l)
    db.session.commit()
    return redirect("/dashboard")
     
        
@app.route("/loginpage", methods=["GET", "POST"])
def loginpage():
    name = request.form.get("name")
    password = request.form.get("pass")

    if not name or not password:
        return "Please enter all the details"
    if name == name and password == password:
        return redirect("/dashboard")
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8100)