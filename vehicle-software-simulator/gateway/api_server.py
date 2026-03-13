from flask import Flask, jsonify
from vehicle_state import vehicle_state

app = Flask(__name__)

@app.route("/vehicle/speed")
def get_speed():
    return jsonify({"vehicle_speed": vehicle_state.vehicle_speed})

@app.route("/vehicle/doors")
def get_doors():
    return jsonify({"door_open": vehicle_state.door_open})

@app.route("/vehicle/climate")
def get_climate():
    return jsonify({"temperature": vehicle_state.temperature})

@app.route("/vehicle/media")
def get_media():
    return jsonify({"media_state": vehicle_state.media_state})