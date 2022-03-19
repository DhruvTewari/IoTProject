# import time
# import datetime
# from smbus2 import SMBus
# from mlx90614 import MLX90614
# bus = SMBus(1)
# sensor = MLX90614(bus, address=0x5A)
# while(True):
#     amb = sensor.get_amb_temp()
#     obj = sensor.get_obj_temp()
#     print("Ambient Temperature :", amb)
#     print("Object Temperature :", obj)
#     print("\n")
#     
#     time.sleep(3)
#     
# bus.close()

import paho.mqtt.client as mqtt
import serial
import time
import datetime
from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
password = ""
if __name__ == '__main__':
    def on_connect(client, userdata, flag, rc):
        print("Connected with " + str(rc))
        client.subscribe('password/')
        
    def on_message(client, userdata, msg):
#         print(str(msg.payload))
        print("Password changed")
        global password
        password = (msg.payload).decode("utf-8")
        return msg.payload
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set('ycwkztoh', 'pqAyogI67TkG')
    client.connect("driver.cloudmqtt.com",18970, 60)
    
    client.loop_start()
    time.sleep(1)
    
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
    ser.flush()
    
    try:
        cnt = 0
        while password == "":
            cnt+=1
            if cnt >= 5:
                password = "1234"
            continue
        while True:
           
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                
                #print(password)
                
                print("\n")
                amb = sensor.get_amb_temp()
                obj = sensor.get_obj_temp()
                print("Ambient Temperature :", amb)
                print("Object Temperature :", obj)
                print("\n")
                
                if float(obj) <= 37 and line == password:
                    print("1 : Access Granted. Welcome to the society.")
                    client.publish("test/", 'Access Granted')
                    ser.write(b"green")
                elif float(obj) > 37 or line != password:
                    print("0 : Either the password is incorrect or body temp is high.")
                    client.publish('test/', 'Access Denied')
                    ser.write(b"yellow")
                else:
                    ser.write(b"all\n")
                 
                
                time.sleep(3)

#     bus.close()


    


    finally:
        client.loop_stop()
        client.disconnect()
    

    # Connecting to MQTT broker and subscribing
        
#     while True:
#         if len(password)> 0:
#             print(password)
#             password=""
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)
#             
#             #print(password)
#             
#             print("\n")
#             amb = sensor.get_amb_temp()
#             obj = sensor.get_obj_temp()
#             print("Ambient Temperature :", amb)
#             print("Object Temperature :", obj)
#             print("\n")
#             
#             if float(obj) <= 37:
#                 print("1")
#                 ser.write(b"greeen")
#             elif float(obj) > 37:
#                 print("0")
#                 ser.write(b"yellow")
#             else:
#                 ser.write(b"all\n")
#              
#             
#             time.sleep(3)
# 
bus.close()
# 
# 
#     
# 
