import uuid
from flask import Blueprint, jsonify, session, url_for, redirect

from required_decorators import login_required


class Trip:

    def __init__(self, owner):
        self.trip_id = str(uuid.uuid4())
        self.owner = owner
        self.members = [owner]

    def to_dict(self):
        return {
            'trip_id': self.trip_id,
            'owner': self.owner,
            'members': self.members
        }


all_trips = {}
trip_apis = Blueprint('trip', __name__)


@trip_apis.post('/create')
@login_required
def create_trip():
    trip = Trip(session['username'])
    all_trips[trip.trip_id] = trip

    return jsonify(trip.to_dict()), 201


@trip_apis.get('/get/<string:trip_id>')
@login_required
def get_trip(trip_id):
    if trip_id not in all_trips:
        return 'Trip not found!'

    return jsonify(all_trips[trip_id].to_dict())


@trip_apis.get('/list')
def list_trips():
    if 'username' not in session:
        return redirect(url_for('login'))

    return jsonify([trip.to_dict() for trip in all_trips.values() if trip.owner == session['username']])


@trip_apis.get('/all')
def get_all_trips():
    return jsonify([trip.to_dict() for trip in all_trips.values()])
