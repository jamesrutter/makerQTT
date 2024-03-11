# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

import paho.mqtt.client as mqtt
import paho.mqtt.enums as enums 
import ssl 

# MQTT Broker Settings
MQTT_BROKER = '80cd98a8ff724b559bad56104395d810.s1.eu.hivemq.cloud'
MQTT_PORT = 8883  # Use 8883 for TLS
MQTT_TOPIC = "maker-exchange/#"  # Subscribe to all topics under 'maker-exchange'
MQTT_USER = ''
MQTT_PASSWORD = ''

# Client API VERSION 
VERSION = enums.CallbackAPIVersion.VERSION2

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback when receiving a message from the MQTT broker
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

# Setup MQTT Client
client = mqtt.Client(callback_api_version=VERSION, client_id="rpi3b+_haystack_jdr", protocol=mqtt.MQTTv5)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)  # Set MQTT broker username and password
client.on_connect = on_connect
client.on_message = on_message

# enable TLS for secure connection
# client.tls_set(tls_version=mqtt_client.ssl.PROTOCOL_TLS)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

# Connect to MQTT Broker
client.connect(MQTT_BROKER, MQTT_PORT)

# Loop forever, to maintain connection
client.loop_forever()