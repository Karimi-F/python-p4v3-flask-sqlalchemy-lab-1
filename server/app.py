# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    """
    Fetch earthquake by its ID and return the details as JSON.
    """
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(earthquake.to_dict()),200
    else:
        return jsonify({"message":f"Earthquake {id} not found."}),404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_matching_minimum_magnitude_value(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response_data = {
        "count": len(earthquakes),
        "quakes": [earthquake.to_dict() for earthquake in earthquakes]
    }
    return jsonify(response_data),200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
