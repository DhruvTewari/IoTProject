from random import randint
import time                                                 #Publish     
import paho.mqtt.client as mqtt
import keyboard
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime
import csv  


data = ""

def on_connect( client, userdata, flags, rc):               
    print ( "Connected with Code:" + str(rc))

    client.subscribe("test/")                              #Subscribe Topic

def on_message( client, userdata, msg):
    print (str(msg.payload))
    global data
    dt = datetime.now()
    print(str(dt))
    data = msg.payload.decode('utf-8').rstrip()
    fields=[dt, data]
    with open(r'authentication.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return msg.payload                                      # here I have been told the data is in csv format thus no parsing requires

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("ycwkztoh", "pqAyogI67TkG")
client.connect("driver.cloudmqtt.com", 18970, 60)

#client.loop_forever()

client.loop_start()
time.sleep(1)

try:
    time_stamp = time.time()
    s = smtplib.SMTP('smtp.gmail.com', 587)
  
    # start TLS for security
    s.starttls()
    s.login("dhruvprojectiot@gmail.com", "IoT!3210")
    database = []
    with open('resident_database') as file:
        lines = file.readlines()
        # print(line)
        count=0
        for line in lines:
            count += 1
            database.append(line.strip())
            

    print(database)

    while(1):
        newtime_stamp = time.time()

        if newtime_stamp - time_stamp >= 60:
            print(1)
            print('Password Changes sending now')
            
            passw = ""
            for i in range(4):
                num = randint(0,9)
                passw += str(num)
            print(s)
            msg = EmailMessage()
            msg.set_content(f'The Authenticated Protocol has updated the password to {passw}')
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("dhruvprojectiot@gmail.com", "IoT!3210")
            msg['Subject'] = 'Password Update (ADMIN)'
            msg['From'] = "dhruvprojectiot@gmail.com"
            
            for i in database:
                msg['To'] = i
                server.send_message(msg)
                del msg['To']



            client.publish("password/", passw)    
            time_stamp = newtime_stamp

    server.quit()



finally:
    client.loop_stop()
    client.disconnect()
