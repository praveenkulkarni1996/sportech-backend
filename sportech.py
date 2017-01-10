from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_restful import Resource, Api
# import sqlite3

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app)

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer)
    name = db.Column(db.String(60))
    email = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    # team : backref from persons

    def validate(self, json):
        pass

    def from_json(self, json):
        self.validate(json)
        self.name = json['name']
        self.email = json['email']
        self.phone = json['phone']
        return self

    def to_json(self):
        json_resp = {}
        json_resp['name'] = self.name
        json_resp['email'] = self.email
        json_resp['phone'] = self.phone
        json_resp['team'] = self.team_id
        return json_resp

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Boolean) # Male = True, Female = False
    persons = db.relationship('Person', backref='team', cascade='all', lazy='dynamic')
    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id'))
    # institute : backref from Institute
    # events: backref from TeamSport

    def validate(self, json):
        pass


    def from_json(self, json):
        pass


    def to_json(self):
        pass


class Institute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    teams = db.relationship('Team', backref='institute', cascade='all', lazy='dynamic')

    def validate(self, json):
        pass

    def from_json(self):
        # self.validate(json)
        self.name = request.args.get('name')
        return self

    def to_json(self):
        return { 'id' : self.id, 'name' : self.name }



class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    fee = db.Column(db.Integer)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id')) #with the sport model
    # teams : backref form TeamEvent
    # sport : from the sports table

    def validate(self, json):
        pass

    def from_json(self, json):
        pass

    def to_json(self, json):
        pass


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    limit = db.Column(db.Integer)
    events = db.relationship('Event', backref='sport', cascade='all', lazy='dynamic')

    def validate(self, json):
        pass

    def from_json(self, json):
        pass

    def to_json(self, json):
        pass


class TeamEvent(db.Model):
    __tablename__ = 'team_event'
    __table_args__ = (UniqueConstraint('team_id', 'event_id', name="uc_team_id_event_id"),)
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'))
    team = db.relationship('Team', backref=db.backref("events"))
    event = db.relationship('Event', backref=db.backref("teams"))


class InstitutesAPI(Resource):

    def get(self):
        institutes = [insti.to_json() for insti in Institute.query.all()]
        return jsonify({'institutes': institutes })

    def post(self):
        insti = Institute().from_json()
        db.session.add(insti)
        db.session.commit()
        return 201

api.add_resource(InstitutesAPI, '/api/institutes/')

if __name__ == '__main__':
    db.create_all()
    app.run()
