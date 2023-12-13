from mqtt_as import MQTTClient, config #importation des class MQTTClient et config du module mqtt_as
from machine import Pin, PWM #importation de la classe Pin du module machine
from time import sleep
import uasyncio#importation du module uasyncio
import L9110


#configuration des connections
config['server'] = "test.mosquitto.org"#hostname du  broker
config['ssid'] = "freenab"#configuration wifi
config['wifi_pw'] = "ZimDid2023"#mot de passe

#configuration des broches D22 et D23 pour moteur A
motor1 = L9110.DRL9110(2, 4)
motor2 = L9110.DRL9110(22, 23)
servo_pan = PWM(Pin(12), freq=50)
servo_tilt = PWM(Pin(13), freq=50)
motor1.stop()
motor2.stop() 
#fonction appele lors de la communication avec le broker
def callback(topic, msg, retained):        
    if topic == b'robot/mav': 
        i1=msg.decode("utf-8")  
        i1=int(i1)             
        motor1.set_speed(i1)
        motor2.set_speed(i1) 
        motor1.forward()        
        motor2.forward()
        print("i1 = ",i1)
    if topic == b'robot/mar': 
        i2=msg.decode("utf-8")
        i2=int(i2)
        motor1.set_speed(i2)
        motor2.set_speed(i2)
        motor1.reverse()
        motor2.reverse()
        print("i2 = ",i2)
    if topic == b'robot/dte': 
        i3=msg.decode("utf-8")
        i3=int(i3)
        motor1.set_speed(i3)
        motor2.set_speed(i3)
        motor1.reverse()
        motor2.forward()
        print("i3 = ",i3)
    if topic == b'robot/gau': 
        i4=msg.decode("utf-8")
        i4=int(i4)
        motor1.set_speed(i4)
        motor2.set_speed(i4)
        motor1.forward()
        motor2.reverse()
        print("i4 = ",i4)
    if topic == b'robot/servo1': 
        i5=msg.decode("utf-8")        
        i5=int(i5)
        servo_tilt.duty(i5)
    if topic == b'robot/servo2': 
        i6=msg.decode("utf-8")        
        i6=int(i6)
        servo_pan.duty(i6)
    if topic == b'robot/stop':          
        motor1.stop()
        motor2.stop() 
        
                
#souscription à tous les topics test/
async def conn_han(client):
    await client.subscribe('robot/mav', 0)
    await client.subscribe('robot/mar', 0)
    await client.subscribe('robot/dte', 0)
    await client.subscribe('robot/gau', 0)
    await client.subscribe('robot/servo1', 0)
    await client.subscribe('robot/servo2', 0)
    await client.subscribe('robot/stop', 0)
#programme principal  
async def main(client):
    await client.connect() #connection du client au broker en wifi
    while True:
        await uasyncio.sleep(1)

#configuration pour la gestion des publications et souscriptions
config['subs_cb'] = callback
config['connect_coro'] = conn_han

MQTTClient.DEBUG = True # affichage des messages de diagnostic
client = MQTTClient(config) #création de l'objet client par instanciation de la classe MQTTClient()

try:
    uasyncio.run(main(client)) #mise en route du programme principal 
finally:
    client.close()