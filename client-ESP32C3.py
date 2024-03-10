import machine
import network
import utime
from umqtt.simple import MQTTClient
from morse import blink_morse_code

# WiFi credentials
WIFI_SSID = ''
WIFI_PASSWORD = ''

# HiveMQ details
# IMPORTANT! YOU NEED TO PUT YOUR SPECIFIC INFORMATION HERE OR DEVICE WILL NOT CONNECT
MQTT_BROKER = '' # Insert your HiveMQ Cluster URL 
MQTT_PORT = 0 # Set to 0 even though default port is 8883 
MQTT_USER = '' # Insert HiveMQ username 
MQTT_PASSWORD = '' # Insert HiveMQ password

# Device ID for MQTT Client
# CLIENT_ID = machine.unique_id() use auto-generated UUID format for identifying clients 
CLIENT_ID = b"jdr_esp32c3" # custom named client, use your own format or way to identify your devices  

# LED Setup
led = machine.Pin(21, machine.Pin.OUT) # ensure you use the correct pin value depending on your circuit. 
led.value(0) # ensure that the LED is off by default 

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
    client = MQTTClient(client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        keepalive=7200,
        ssl=True,
        ssl_params={'server_hostname': MQTT_BROKER}
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
    
    blink_morse_code(led, 'Hello') 
    
    #delay 5 seconds
    utime.sleep(5)

