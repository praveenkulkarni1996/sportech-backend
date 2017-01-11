from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_restful import Resource, Api
import json

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

    def from_json(self, json, team_id):
        self.validate(json)
        self.name = json['name']
        self.email = json['email']
        self.phone = json['phone']
        self.team_id = team_id
        return self

    def to_json(self):
        json_resp = {}
        json_resp['name'] = self.name
        json_resp['email'] = self.email
        json_resp['phone'] = self.phone
        # json_resp['team'] = self.team_id
        return json_resp

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Boolean) # Male = True, Female = False
    persons = db.relationship('Person', backref='team', cascade='all', lazy='dynamic')
    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id'))
    # institute : backref from Institute
    # events: backref from TeamSport

    def validate(self):
        pass

    def from_json(self, json):
        self.validate()
        # self.id = json['id']
        self.gender = json['gender'] == 'male'
        self.institute_id = json['institute_id']
        # players = []
        # for person in request.args.get('players'):
        #     players.append(Person().from_json(person))
        return self

    def to_json(self):
        resp = {}
        resp['id'] = self.id
        resp['gender'] = 'male' if self.gender else 'female'
        resp['players'] = [person.to_json() for person in Person.query.all()]
        resp['institute'] = self.institute.to_json()
        resp['events'] = [event.to_json() for event in self.events]
        return resp

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

    def validate(self):
        pass

    def from_json(self):
        self.validate()
        self.name = request.args.get('name')
        self.min_players = int(request.args.get('min_players'))
        self.max_players = int(request.args.get('max_players'))
        self.gender = request.args.get('gender') == 'male'
        self.fee = int(request.args.get('fee'))
        self.sport_id = int(request.args.get('sport_id'))
        return self

    def to_json(self):
        resp = {}
        resp['name'] = self.name
        resp['min_players'] = self.min_players
        resp['max_players'] = self.max_players
        resp['gender'] = 'male' if self.gender else 'female'
        resp['fee'] = self.fee
        resp['sport'] = self.sport.to_json()
        return resp

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    limit = db.Column(db.Integer)
    events = db.relationship('Event', backref='sport', cascade='all', lazy='dynamic')

    def validate(self):
        pass

    def from_json(self):
        self.validate()
        self.name = request.args.get('name')
        self.limit = int(request.args.get('limit', default=1))
        return self


    def to_json(self):
        return {'id' : self.id, 'name' : self.name, 'limit': self.limit }

class TeamEvent(db.Model):
    __tablename__ = 'team_event'
    __table_args__ = (UniqueConstraint('team_id', 'event_id', name="uc_team_id_event_id"),)
    id = db.Column(db.Integer, primary_key=True)
    # paid = db.Column(db.Boolean)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'))
    team = db.relationship('Team', backref=db.backref("events"))
    event = db.relationship('Event', backref=db.backref("teams"))

    def __init__(self, event_id, team_id):
        self.team_id = team_id
        self.event_id = event_id
        # self.paid = False

    #
    # def validate(self):
    #     pass
    #
    # def from_json(self, events, team_id):
    #     pass
    #
    def to_json(self):
        return {'event' : self.event.to_json() }
        return {}

class InstitutesAPI(Resource):
    ''' returns a list of institutions '''

    def get(self):
        institutes = [insti.to_json() for insti in Institute.query.all()]
        return jsonify({'institutes': institutes })

    def post(self):
        insti = Institute().from_json()
        db.session.add(insti)
        db.session.commit()
        return 201

class InstituteAPI(Resource):
    def get(self, id):
        insti = Institute.query.get_or_404(id)
        return jsonify({ 'institute' : insti.to_json() })

class SportsAPI(Resource):

    def get(self):
        sports = [sport.to_json() for sport in Sport.query.all()]
        return jsonify({'sports': sports })

    def post(self):
        sport = Sport().from_json()
        db.session.add(sport)
        db.session.commit()
        return {}, 201

class SportAPI(Resource):

    def get(self, id):
        sport = Sport.query.get_or_404(id)
        return jsonify({ 'sport' : sport.to_json() })

class EventsAPI(Resource):

    def get(self):
        events = [event.to_json() for event in Event.query.all()]
        return jsonify({'events': events})

    def post(self):
        event = Event().from_json()
        db.session.add(event)
        db.session.commit()
        return {}, 201

class TeamsAPI(Resource):
    def get(self):
        teams = [team.to_json() for team in Team.query.all()]
        return jsonify({'teams': teams})

    def post(self):
        pass
        # teams =

class RegisterAPI(Resource):
    def get(self):
        regists = [regist.to_json() for regist in TeamEvent.query.all() ]
        return jsonify({'registrations':regists})


    def post(self):
        json_data = json.loads(request.data)
        team  = Team().from_json(json_data)
        events = json_data['events']

        db.session.add(team)
        db.session.commit()

        for player in json_data['players']:
            person = Person().from_json(player, team.id)
            db.session.add(person)
        db.session.commit()

        for event_id in events:
            team_event = TeamEvent(event_id, team.id)
            db.session.add(team_event)
        db.session.commit()

        return 201


        return jsonify({'input' : json_data })
        # return jsonify({'input': request.data.to_dict() })
    #     create_a_team
    #
    #     # team = Team()
    #     # pass

class PlayersAPI(Resource):
    def get(self):
        players = [player.to_json() for player in Person.query.all()]
        return jsonify({'players': players})

# routes
# team
api.add_resource(InstitutesAPI, '/api/institutes/')
api.add_resource(InstituteAPI, '/api/institute/<int:id>')
api.add_resource(SportsAPI, '/api/sports/')
api.add_resource(SportAPI, '/api/sport/<int:id>')
api.add_resource(EventsAPI, '/api/events/')
api.add_resource(TeamsAPI, '/api/teams/')
api.add_resource(RegisterAPI, '/api/register/')
api.add_resource(PlayersAPI, '/api/players/')

if __name__ == '__main__':
    db.create_all()
    # app.run(debug=True)
    app.run()
