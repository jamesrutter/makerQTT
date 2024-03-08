# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

import time
import ssl
import paho.mqtt.client as paho
from paho.mqtt import client as mqtt_client
from paho import mqtt # This seems to be nothing, and out of date module? 
import paho.mqtt.enums as enums
ver = enums.CallbackAPIVersion.VERSION2

# from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, rc=None, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
# client = paho.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="james", userdata=None, protocol=paho.MQTTv5)
client = paho.Client(callback_api_version=ver, client_id="james", protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
# client.tls_set(tls_version=mqtt_client.ssl.PROTOCOL_TLS)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("haystack", "YOUR_PASSWORD_GOES_HERE") # you need to change this, the program will fail to connect otherwise
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("80cd98a8ff724b559bad56104395d810.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("maker-exchange/#", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("maker-exchange/welcome", payload="Hello, Maker!", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()