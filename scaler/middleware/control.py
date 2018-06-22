import time
import datetime
from datetime import date
import pymysql
import pymysql.cursors
import train
import predict
import pandas as pd
import re

maps = {'unknown': 0, 'clear': 1, 'scattered clouds': 2, 'mist': 3, 'haze': 4, 'shallow fog': 5,
        'patches of fog': 6, 'fog': 7, 'partly cloudy': 8, 'mostly cloudy': 9, 'overcast': 10,
        'funnel cloud': 11, 'light drizzle': 12, 'drizzle': 13, 'light rain': 14, 'rain': 15,
        'heavy rain': 16, 'light thunderstorms and rain': 17, 'thunderstorms and rain': 18,
        'thunderstorm': 19, 'smoke': 20}
maps_inverse = {0: 'unknown', 1: 'clear', 2: 'scattered clouds', 3: 'mist', 4: 'haze', 5: 'shallow fog',
                6: 'patches of fog', 7: 'fog', 8: 'partly cloudy', 9: 'mostly cloudy', 10: 'overcast',
                11: 'funnel cloud', 12: 'light drizzle', 13: 'drizzle', 14: 'light rain', 15: 'rain',
                16: 'heavy rain', 17: 'light thunderstorms and rain', 18: 'thunderstorms and rain',
                19: 'thunderstorm', 20: 'smoke'}
def getLast24HoursData():
    inputList = list()
    from datetime import date
    today = date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    today = today.strftime("%Y%m%d")
    yesterday = yesterday.strftime("%Y%m%d")
    yesterdayTable = 'table_' + yesterday
    todayTable = 'table_' + today
    print(todayTable)
    dbConn = pymysql.connect(host='***',
                             port=3306, user='***', password='***', db='vaData')

    cursor = dbConn.cursor()
    try:
        sql = "SELECT * from " + yesterdayTable
        cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            if data[4].lower() not in maps:
                print(data[4])
                continue
            inputList.append(maps[data[4].lower()])
            inputList.append(data[1])
            inputList.append(data[3])  # pressure
            inputList.append(data[2])
        sql = "SELECT * from " + todayTable
        cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            if data[4].lower() not in maps:
                continue
            inputList.append(maps[data[4].lower()])
            inputList.append(data[1])
            inputList.append(data[3])  # pressure
            inputList.append(data[2])
        inputList = inputList[len(inputList) - 4 * 24:len(inputList)]
    except:
        print("read data fails")
    dbConn.close()
    #print(inputList)
    return inputList


day = time.strftime("%d", time.localtime())
hour = time.strftime("%H", time.localtime())
minute = time.strftime("%m", time.localtime())
second = time.strftime("%s", time.localtime())
print(minute)
print(second)
curDay = day
curHour = hour
curMinute = minute
curSecond = second
model, scaler = train.Train('data.csv', maps).model()
h = 2

while True:
    day = time.strftime("%d", time.localtime())
    hour = time.strftime("%H", time.localtime())
    minute = time.strftime("%m", time.localtime())
    second = time.strftime("%s", time.localtime())
    curDay = day
    today = date.today()
    todayStr = today.strftime("%Y%m%d")
    dbConn = pymysql.connect(host='***',
                             port=3306, user='***', password='***', db='vaData')
    cursor = dbConn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS " + 'cond_' + todayStr + \
          "(hour int NOT NULL AUTO_INCREMENT, cond varchar(30) NOT NULL, " \
          "PRIMARY KEY (hour))ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"
    cursor.execute(sql)
    dbConn.commit()
    dbConn.close()
    if int(minute) > int(curMinute)+10:
        h = 0
        print(minute)
        engine = train.Train('data.csv', maps)
        model, scaler = engine.model()
        curDay = day
        today = date.today()
        todayStr = today.strftime("%Y%m%d")
        dbConn = pymysql.connect(host='***',
                                 port=3306, user='**', password='***', db='vaData')
        cursor = dbConn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS " + 'cond_' + todayStr + \
              "(hour int NOT NULL AUTO_INCREMENT, cond varchar(30) NOT NULL, " \
              "PRIMARY KEY (hour))ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"
        cursor.execute(sql)
        dbConn.commit()
        dbConn.close()
        curMinute = minute
    if int(second) > int(curSecond)+10:
        print(second)
        if hour > curHour:
            curHour = hour
        input = getLast24HoursData()
        print(input)
        pre = predict.Predict(model, input, scaler)
        output = pre.predict()
        output = [round(x) for x in output]
        print(output)
        curSecond = second
        today = date.today()
        todayStr = today.strftime("%Y%m%d")
        dbConn = pymysql.connect(host='***',
                                 port=3306, user='***', password='***', db='vaData')
        cursor = dbConn.cursor()
        sql = "INSERT INTO " + "cond_" + todayStr + "(hour, cond) VALUES (%s, %s)"
        if round(output[0]) in maps_inverse:
            res = maps_inverse[round(output[0])]
        else:
            res = 'unknown'
        cursor.execute(sql, (h, res))
        dbConn.commit()
        dbConn.close()
        h += 1
    time.sleep(1)
