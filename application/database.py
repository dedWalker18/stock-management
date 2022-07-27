from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint

# Creating a database variable to communicate with the database file! Using SQLAlchemy ORM for it
db = SQLAlchemy()

class Trackers(db.Model):
    __tablename__ = "Trackers"
    TrackerId = db.Column(db.Integer, primary_key = True, autoincrement = True)
    TrackerName = db.Column(db.String, nullable = False)
    TrackerDesc = db.Column(db.String, nullable = False)
    TrackerType = db.Column(db.String, nullable = False)
    
class Logs(db.Model):
    __tablename__ = "Logs"
    LogId = db.Column(db.Integer, primary_key = True, autoincrement = True)
    LogValue = db.Column(db.Integer, nullable = False)
    TrackerId = db.Column(db.Integer, db.ForeignKey(Trackers.TrackerId), nullable=False)
    
    
