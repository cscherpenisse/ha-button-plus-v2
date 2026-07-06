import json
import paho.mqtt.client as mqtt

class ButtonPlusMQTT:

    def __init__(self, host, on_message):
        self.host = host
        self.client = mqtt.Client()
        self.on_message = on_message

    def connect(self):
        self.client.on_message = self._on_message
        self.client.connect(self.host, 1883, 60)
        self.client.loop_start()

        self.client.subscribe("buttonplus/+/button/+/pushbutton")
        self.client.subscribe("buttonplus/+/sensor/+")
        self.client.subscribe("buttonplus/+/displayitem/+/value/state")
        self.client.subscribe("buttonplus/+/brightness/state")
        self.client.subscribe("buttonplus/+/button/+/led/+/+/state")

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()

            try:
                payload = json.loads(payload)
            except:
                pass

            self.on_message(msg.topic, payload)

        except Exception as e:
            print("MQTT error:", e)

    def publish(self, topic, payload):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        self.client.publish(topic, payload)
