from flask import Flask, jsonify, request
from influxdb import InfluxDBClient
import paho.mqtt.publish as publish

INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_DB = "iot_energy"

db = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
db.switch_database(INFLUX_DB)

MQTT_BROKER = "localhost"
MQTT_TOPIC_CONTROL = "iot/energy/control"

app = Flask(__name__)

@app.route("/api/latest", methods=["GET"])
def latest():
  query = "SELECT * FROM energy ORDER BY time DESC LIMIT 1"
  result = db.query(query)
  points = list(result.get_points())
  if len(points) == 0:
    return jsonify({"error": "no data"}), 404
  return jsonify(points[0])

@app.route("/api/history", methods=["GET"])
def history():
  query = "SELECT * FROM energy ORDER BY time DESC LIMIT 100"
  result = db.query(query)
  return jsonify(list(result.get_points()))

@app.route("/api/control", methods=["POST"])
def control():
  body = request.get_json()
  action = body.get("action")
  publish.single(MQTT_TOPIC_CONTROL, action, hostname=MQTT_BROKER)
  return jsonify({"status": "ok", "action": action})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
