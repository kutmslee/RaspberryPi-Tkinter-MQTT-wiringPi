import paho.mqtt.client as mqtt
import wiringpi
import tkinter as tk

wiringpi.wiringPiSetup()
wiringpi.pinMode(25,1)

client = mqtt.Client()

    
def ButtonClick1():
    topic = editbox1.get()
    msg = editbox2.get()
    #print(topic + '/' + msg)
    client.publish(topic, msg, 1)
    
def ButtonClick2():
    topic = editbox3.get()
    msg = editbox4.get()
    #print(topic + '/' + msg)
    client.publish(topic, msg, 1)

def on_check():
    if check1.get()==True:
        ButtonClick3()
    else:
        ButtonClick4()
        

def ButtonClick3():
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect('mqtt-dashboard.com', 1883)
    client.loop_start()
    client.subscribe('testtopic/1', 1)
    #client.loop_forever()
    
def ButtonClick4():
    client.loop_stop()
    client.disconnect('mqtt-dashboard.com', 1883)
    
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('connected OK')
    else:
        print('Bad connection Returned code=', rc)
        
def on_disconnect(client, userdata, flags, rc=0):
    print('disconnect OK')
    
def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribed: message ID ' + str(mid))# + ' ' + str(granted_qos))
    
def on_message(client, userdata, msg):
    #print(str(msg.payload.decode('utf-8')))
    if msg.payload.decode('utf-8')=='ON':
        print('ON~')
        wiringpi.digitalWrite(25,1)
    elif msg.payload.decode('utf-8')=='OFF':
        print('OFF~')
        wiringpi.digitalWrite(25,0)


y1=50
y2=100
y3=150

box=tk.Tk()
box.geometry('450x200')
box.title('이모세')

label1=tk.Label(box, text='토픽')
label1.place(x=50, y=y1)
editbox1=tk.Entry(width=10)
editbox1.place(x=100, y=y1)

label2=tk.Label(box, text='메시지')
label2.place(x=200, y=y1)
editbox2=tk.Entry(width=10)
editbox2.place(x=250, y=y1)

button1=tk.Button(box, text='게시', command=ButtonClick1)
button1.place(x=350, y=y1-4)

label3=tk.Label(box, text='토픽')
label3.place(x=50, y=y2)
editbox3=tk.Entry(width=10)
editbox3.place(x=100, y=y2)

label4=tk.Label(box, text='메시지')
label4.place(x=200, y=y2)
editbox4=tk.Entry(width=10)
editbox4.place(x=250, y=y2)

button2=tk.Button(box, text='게시', command=ButtonClick2)
button2.place(x=350, y=y2-4)

button2=tk.Button(box, text='Connect', command=ButtonClick3)
button2.place(x=50, y=y3)

button2=tk.Button(box, text='Disconnect', command=ButtonClick4)
button2.place(x=150, y=y3)

check1=tk.IntVar()
checkbutton1=tk.Checkbutton(box, text='Connect', variable=check1, command=on_check)
checkbutton1.pack()

box.mainloop()
