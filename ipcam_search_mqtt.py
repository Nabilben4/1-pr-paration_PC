# lancer cette application avant de brancher les caméras
import time
import numpy as np
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from pynput.keyboard import Key, Controller, Listener
keyboard = Controller()

#MQTT
BROKER = 'test.mosquitto.org'
BASE_TOPIC = 'ipcam'
MQTT_SERVER = BROKER
MQTT_PATH = BASE_TOPIC+"/#"
# exemple: ipcam/cam5 '172.127.113.203'
#mosquitto_sub -d -h pimqtt.local -t "ipcam/#"
#mosquitto_pub -d -h pimqtt.local  -t "ipcam/cam5" -m '172.127.113.203'



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected MQTT with result code "+str(rc))
    print(" vous pouvez maintenant brancher les caméras :-)")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    # The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    #print("topic:",topic,"   payload:",payload)
    if payload != 'colliger': # colliger déclenche une réponse des caméras
        num_cam = topic.split('/')[-1]
        ip_cam = payload
        #print("num_cam:",num_cam,"  ip_cam:",ip_cam)
        print(f'''nom: {num_cam}    ip: http://{ip_cam}/live''')
    
                
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
#publish.single("ipcam/cam1/led", "1", hostname=MQTT_SERVER)
#publish.single("ipcam/cam1/led", "0", hostname=MQTT_SERVER)

client.loop_start() #lancer thread mqtt
touche = ' '
def on_press(key):
    global touche
    try:
        #print(f'Alphanumeric key pressed: {key.char}')
        touche = key.char
    except AttributeError:
        #print(f'special key pressed: {key}')
        pass

def on_release(key):
    global touche
    #print(f'Key released: {key}')
    if key == Key.esc:
        return False # Stop listener

listener = Listener(on_press=on_press,on_release=on_release)
listener.start() #lancer thread pynput

while True:
    # if touche == 'p':#if p is pressed
    #     touche = ''
    #     client.publish("ipcam", "colliger", qos=0, retain=False)
    #     time.sleep(1)
           
    time.sleep(0.5)
    #keyboard.press('p') #appui sur touche virtuellement et relance une photo
