import paho.mqtt.client as mqtt
import random
import pymysql
import pymysql.cursors
import re

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot-1/d/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    dbConn = pymysql.connect(host='localhost', port=3306, user='middleU', password='123', db='middleware', 
    	charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = dbConn.cursor()
    print(str(msg.payload))
    try:
        dataStr = str(msg.payload)
        timestamp = int(float(re.findall(r'timestamp": (.*?),', dataStr)[0]))
        print(timestamp)
        event = re.findall(r'event": "(.*?)",', dataStr)[0]
        print(event)
        if event=="temperature":
            value = float(re.findall(r'value": (.*?),', dataStr)[0])
            print(value)
            sql = 'INSERT INTO Temperature(timestamp, deviceId, value) VALUES (%s, %s, %s)'
            cursor.execute(sql,(timestamp,"0001",value))
            dbConn.commit()
            print("insert successfully")
        cursor.close();
        dbConn.close();
    except:
    	print("wrong msg format")

def on_log(client, userdata, level, buf):
    print(buf);

client = mqtt.Client(client_id="client"+str(random.randint(1,100000)), transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.connect('iqueue.ics.uci.edu', 8000, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()