from flask import Flask, jsonify
from vehicle_state import vehicle_state

app = Flask(__name__)

@app.route("/vehicle/speed")
def get_speed():
    return jsonify({"speed": vehicle_state.speed})

@app.route("/vehicle/doors")
def get_doors():
    return jsonify({"door_open": vehicle_state.door_open})

@app.route("/vehicle/climate")
def get_climate():
    return jsonify({"temperature": vehicle_state.temperature})
