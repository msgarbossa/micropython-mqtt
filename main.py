
def sub_cb(topic, msg):
  # print((topic, msg))
  last_receive = time.time()
  print('%s: received message on topic %s with msg: %s' % (last_receive, topic, msg))
  if topic == b'home/leak3/cmd' and msg == b'ping':
    client.publish(topic_pub, b'pong')
    print('sent pong')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, port=1883, user=mqtt_user, password=mqtt_password)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()  

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    time.sleep(1)
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      print('%s: published message on topic %s' % (last_message, topic_pub))
      counter += 1
  except OSError as e:
    restart_and_reconnect()

