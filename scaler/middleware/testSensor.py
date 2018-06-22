import paho.mqtt.client as mqtt
import random
import pymysql
import pymysql.cursors
import re
import time
# The callback for when the client receives a CONNACK response from the server.
myNum = 0
curCondNum = 0
pressureNum = 0
condNum = 0

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot-1/d/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        dataStr = str(msg.payload)
        timestamp = int(float(re.findall(r'timestamp": (.*?),', dataStr)[0]))
        #print(timestamp)
        event = re.findall(r'event": "(.*?)",', dataStr)[0]
        #print(event)
        if event=="MYtemperature":
            print("myNum: "+str(time.time()))
        if event=="current_condition": 
            print("curCondNum: "+str(time.time()))
        if event=="pressure":
            print("pressureNum: "+str(time.time()))
        if event=="condition":
            print("condNum: "+str(time.time()))
    except:
        print("wrong msg format")

#def on_log(client, userdata, level, buf):
    #print(buf);


client = mqtt.Client(client_id="client"+str(random.randint(1,100000)), transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
#client.on_log = on_log
client.connect('iqueue.ics.uci.edu', 8000, 60)
t = time.time()
ct = t
while ct-t<60*60*3:
	client.loop()
	ct = time.time()