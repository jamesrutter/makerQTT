from machine import Pin
import network
import utime
import json
from umqtt.simple import MQTTClient


# -------- CONFIGURATION --------- #

# WiFi credentials
WIFI_SSID = ''
WIFI_PASSWORD = ''

# HiveMQ details
MQTT_BROKER = '80cd98a8ff724b559bad56104395d810.s1.eu.hivemq.cloud'
MQTT_PORT = 0 
MQTT_USER = ''
MQTT_PASSWORD = ''	

# Device ID for MQTT Client
CLIENT_ID = b"esp32c3_haystack_jdr" # custom named client

# Generic Maker Exchange Message Format 
TOPIC = "maker-exchange/haystack"
PAYLOAD = json.dumps({
  "sender": "Haystack Fab Lab",
  "location": "Deer Isle, ME",
  "messageType": "broadcast",
  "content": "Hello, Maker!",
  "timestamp": "2024-03-10T15:00:00Z"
})

# LED Setup
led = Pin(21, Pin.OUT)
led.value(0) # ensure that the LED is off by default

# Button Setup # 
button = Pin(5, Pin.IN, Pin.PULL_UP)

DEBOUNCE_TIME = 500  # milliseconds
LAST_PRESS_TIME = 0

# Function to handle button press 
def button_pressed():
    global LAST_PRESS_TIME
    current_time = utime.ticks_ms()
    if button.value() == 0 and utime.ticks_diff(current_time, LAST_PRESS_TIME) > DEBOUNCE_TIME:
        LAST_PRESS_TIME = current_time
        return True
    return False

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

# MQTT Callback Function for when message is received
def on_message(topic, msg):
    print("\nReceived MQTT Message!")
    print(f"Topic: {topic.decode()}")
    print(f"Message: {msg.decode()}\n")
    
    # Blink the LED briefly to signal that a message was received
    led.on()
    utime.sleep(0.5)
    led.off()

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
    client.set_callback(on_message)  # Set the callback function for incoming messages
    client.connect()
    print("Connecting to MQTT Broker...")
    client.subscribe("maker-exchange/#")  # Subscribe to all topics related to esp32c3
    print("Subscribing to topics...")
    return client

# Function to publish messages to the MQTT broker 
def publish(topic, payload):
    print("Publishing message...\n\n")
    print(f"Topic: {topic} /n Payload: {payload}")
    client.publish(topic, payload)
    print("\n\nPublishing complete!")
    
    
# ---------- SETUP --------------- #

# Step 1. Establish WiFi connection
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

# Step 2. Setup MQTT and connect
client = connectMQTT()

# ---------- MAIN LOOP ----------- #
while True:
    if button_pressed():
        led.on()
        publish(TOPIC, PAYLOAD)
        utime.sleep(0.5)
        led.off()
    else:
        print("Waiting for message...")
        client.check_msg()  # Check for new messages (non-blocking)
        utime.sleep(0.1)
