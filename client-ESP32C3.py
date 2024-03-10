import machine
from machine import Pin

import network
import utime

from umqtt.simple import MQTTClient
import ssl

# WiFi credentials
WIFI_SSID = ''
WIFI_PASSWORD = ''

# HiveMQ details
MQTT_BROKER = ''
MQTT_PORT = 0 
MQTT_USER = ''
MQTT_PASSWORD = ''

# Device ID for MQTT Client
CLIENT_ID = machine.unique_id()

# Connect to WiFi function 
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connecting to WiFi...")
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        utime.sleep(1)
    print("Connected to WiFi!")
    print(wlan.ifconfig())

# Establish WiFi connection
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

# Function to setup and return an MQTT client
def connectMQTT():
    client = MQTTClient(client_id=b"jdr_esp32c3",
        server=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        keepalive=7200,
        ssl=True,
        ssl_params={'server_hostname':'80cd98a8ff724b559bad56104395d810.s1.eu.hivemq.cloud'}
        )
    client.connect()
    print("Connecting to MQTT Broker...")
    return client

# Setup MQTT and connect
client = connectMQTT()
client.connect()

# Function to publish messages to the MQTT broker 
def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publish Done")

# Super loop to run program indefinitely
while True:
    print("Getting ready to publish message...")
    message = "Hello, Maker!"
    
    # publish as MQTT payload
    publish('esp32c3/hello', message)
    
    #delay 5 seconds
    utime.sleep(5)

