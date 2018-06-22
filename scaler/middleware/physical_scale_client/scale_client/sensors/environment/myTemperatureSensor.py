from scale_client.sensors.virtual_sensor import VirtualSensor

import logging
import os
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
log = logging.getLogger(__name__)

sensor=Adafruit_DHT.DHT11
gpio=17
class myTemperatureSensor(VirtualSensor):

    """
    Temperature sensor that only reports data when it's above some threshold.
    """
    def __init__(self, broker, interval=1, threshold=10.0, event_type="MYtemperature", **kwargs):
        super(myTemperatureSensor, self).__init__(broker, interval=interval, event_type=event_type, **kwargs)
        self._threshold = threshold
    DEFAULT_PRIORITY = 5

    def read_raw(self):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        if humidity is not None and temperature is not None:
            print temperature, humidity
            return "temperature: "+str(1.8*temperature + 32)+", humidity: "+str(humidity)
            #return temperature
        else:
            temperature = 24
            humidity = 60
            print('Failed to get reading. Try again!')
            return "temperature: "+str(1.8*temperature + 32)+", humidity: "+str(humidity)
        return 100
   
    def read(self):
        event = super(myTemperatureSensor, self).read()
        event.condition = {
            "threshold": {
                "operator": ">",
                "value": self._threshold
            }
        }

        return event

    def policy_check(self, event):
        return event.data > self._threshold
