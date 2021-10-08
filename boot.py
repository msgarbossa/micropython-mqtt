
import micropython
import esp
import network
import machine
import time
from mqtt import MQTTClient 
import ubinascii

import gc
gc.collect()

esp.osdebug(None)

ssid = '<SSID>'
password = '<WIFI_PW>'
mqtt_server = '<MQTT_IP>'
mqtt_user = '<MQTT_User>'
mqtt_password = '<MQTT_PW>'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'home/leak3/cmd'
topic_pub = b'home/leak3/metrics'

last_message = 0
message_interval = 300
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

