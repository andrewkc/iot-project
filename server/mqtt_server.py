import json
from datetime import datetime
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/energy/measurements"

INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_DB = "iot_energy"

db = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
db.create_database(INFLUX_DB)
db.switch_database(INFLUX_DB)

def on_connect(client, userdata, flags, rc):
  client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
  try:
    data = json.loads(msg.payload.decode())
    influx_json = [
      {
        "measurement": "energy",
        "time": datetime.utcnow().isoformat(),
        "fields": {
          "voltage": float(data["voltage"]),
          "current": float(data["current"]),
          "power": float(data["power"]),
          "energy": float(data["energy"])
        }
      }
    ]
    db.write_points(influx_json)
  except:
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
