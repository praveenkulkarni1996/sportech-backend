import requests
import json

URL = 'http://127.0.0.1:5000/'
SPORTS = URL + 'api/sports/'
EVENTS = URL + 'api/events/'
TEAMS = URL + 'api/teams/'
REGISTER = URL + 'api/register/'
PLAYERS = URL + 'api/players/'
INSTITUTES = URL + 'api/institutes/'
# print requests.get(SPORTS).json()
# print requests.get(TEAMS).json()
# print requests.get(REGISTER).json()


baddy_doubles_M = {
    'name' : 'Badminton Doubles Male',
    'min_players' : 2,
    'max_players' : 2,
    'gender' : 'male',
    'fee' : 300,
    'sport_id' : 1
}

baddy_doubles_W = {
    'name' : 'Badminton Doubles Female',
    'min_players' : 2,
    'max_players' : 2,
    'gender' : 'female',
    'fee' : 300,
    'sport_id' : 1
}

# requests.post(EVENTS, params=baddy_doubles_W)
# print requests.get(EVENTS).json()

# print requests.post(EVENTS, params=baddy_doubles)

team1 = json.dumps({
    'institute_id' : 1,
    'gender' : 'male',
    'players' : [
        {'name' : 'Praveen', 'phone' : 7838482553, 'email' : 'test2@test.com'},
        {'name' : 'Kapil', 'phone' : 7838482553, 'email' : 'test1@test.com'}
    ],
    'events' : [1, 2]
})

basketball = {
    'name' : 'Baskelball',
    'limit' : 1, 
}

# print requests.post(REGISTER, data=team1).text
# print requests.get(PLAYERS).json()
from pprint import pprint
# pprint(requests.get(REGISTER).json())

# pprint(requests.post(SPORTS, params=basketball))


# pprint(requests.post(INSTITUTES, params={'name' : 'IIT Kanpur'}).json())
pprint(requests.get(SPORTS).json())
pprint(requests.get(EVENTS).json())
pprint(requests.get(INSTITUTES).json())


