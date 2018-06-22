import paho.mqtt.client as mqtt
import random
import pymysql
import pymysql.cursors
import re
import time
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot-1/d/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    dbConn = pymysql.connect(host='***', 
        port=3306, user='***', password='***', db='vaData')
    cursor = dbConn.cursor()
    #print(str(msg.payload))
    try:
        dataStr = str(msg.payload)
        timestamp = int(float(re.findall(r'timestamp": (.*?),', dataStr)[0]))
        #print(timestamp)
        event = re.findall(r'event": "(.*?)",', dataStr)[0]
        print(event)
        if event=="MYtemperature":
            #print(dataStr)
            temperature = float(re.findall(r"\d+\.?\d*", dataStr)[1])
            #print(temperature)
            humidity = float(re.findall(r"\d+\.?\d*", dataStr)[2])
            #print(humidity)
            hour = int(time.strftime('%H',time.localtime(time.time())))+1;
            date = time.strftime("%Y%m%d", time.localtime())
            sql = 'INSERT INTO '+'table_'+str(date)+'(hour, temperature, humidity, pressure, cond) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql,(hour,temperature,humidity,0,0))
            dbConn.commit()
            print("insert successfully")
        if event=="current_condition": 
            #print(dataStr)
            hour = int(time.strftime('%H',time.localtime(time.time())))+1;
            date = time.strftime("%Y%m%d", time.localtime())
            sql = 'SELECT cond from table_'+str(date)+' WHERE hour='+str(hour)
            cursor.execute(sql)
            res = cursor.fetchall()
            cond = res[0][0]
            #print(cond)
            if str(cond) == '0':
                condition = re.findall(r'"value": "(.*?)"', dataStr)[0]
                #print(condition)
                #condition = condition.replace(' ','_')
                sql = 'UPDATE table_'+date+' SET cond=\''+condition+'\' WHERE hour='+str(hour)
                #print(sql)
                cursor.execute(sql)
                dbConn.commit()
                #print("condition sucess")
            #print(type(res))
            #print(res)
            #print("cond yes")
        if event=="pressure":
            hour = int(time.strftime('%H',time.localtime(time.time())))+1;
            date = time.strftime("%Y%m%d", time.localtime())
            sql = 'SELECT pressure from table_'+str(date)+' WHERE hour='+str(hour)
            #print(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            pre = res[0][0]
            if float(pre) == 0:
                print(dataStr)
                pressure = re.findall(r'"value": (.*?),', dataStr)[0]
                print(pressure)
                sql = 'UPDATE table_'+date+' SET pressure='+pressure+' WHERE hour='+str(hour)
                print(sql)
                cursor.execute(sql)
                dbConn.commit()
                #print("pressure sucess")
        cursor.close();
        dbConn.close();
    except:
        print("wrong msg format")

#def on_log(client, userdata, level, buf):
    #print(buf);

dbConn = pymysql.connect(host='***', 
    port=3306, user='***', password='***', db='vaData')
cursor = dbConn.cursor()
startTime = time.time()
date = time.strftime("%Y%m%d", time.localtime())
try:
    create_table = "CREATE TABLE IF NOT EXISTS "+ 'table_'+str(date) + "(hour int NOT NULL AUTO_INCREMENT, temperature decimal(5,1) NOT NULL, humidity decimal(5,1) NOT NULL, pressure decimal(5,1) NOT NULL, cond varchar(30) NOT NULL, PRIMARY KEY (hour))ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"
    cursor.execute(create_table)
    dbConn.commit()
except:
    print("table exists")
dbConn.close()

client = mqtt.Client(client_id="client"+str(random.randint(1,100000)), transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
#client.on_log = on_log
client.connect('iqueue.ics.uci.edu', 8000, 60)
client.loop_forever()

while(True):
    curDate = time.strftime("%Y%m%d", time.localtime())
    if curDate != date:
        date = curDate
        dbConn = pymysql.connect(host='***', 
            port=3306, user='***', password='***', db='vaData')
        cursor = dbConn.cursor()
        try:
            create_table = "CREATE TABLE IF NOT EXISTS "+ 'table_'+str(date) + "(hour int NOT NULL AUTO_INCREMENT, temperature decimal(5,1) NOT NULL, humidity decimal(5,1) NOT NULL, pressure decimal(5,1) NOT NULL, cond varchar(30) NOT NULL, PRIMARY KEY (hour))ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"
            cursor.execute(create_table)
            dbConn.commit()
        except:
            print("table exists")
            dbConn.close()
    time.sleep(60)