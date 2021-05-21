import paho.mqtt.client as mqtt
from tkinter import *
import time


def on_connect(client, userdata, flags, rc):
    print("connected - rc:", rc)


def on_message(client, userdata, message):
    global FLAG
    global chat1
    global chat2
    if str(message.topic) != pubtop:
        msg = str(message.payload.decode("utf-8"))
        if msg == "Stop" or msg == "stop":
            FLAG = False
        else:
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "BOT: " + msg + '\n\n')
            ChatLog.config(foreground="#007bff", font=("Verdana", 12))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))


def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))


def on_disconnet(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnection")


def on_click():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)
    if msg != "stop":
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))
        client.publish(pubtop, msg)


# Creating a window
base = Tk()
base.title("Chat App")
base.geometry("600x700")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
Header = Label(text="Welcome To Chat App", bg="#e1e1e1", font="cursive")
ChatLog = Text(base, bd=0, bg="#f2f2f2", height="10", width="60", font="Verdana", )
ChatLog.config(state=DISABLED)
# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="10", height=5,
                    bd=0, bg="#007bff", activebackground="#3c9d9b", fg='#ffffff',
                    command=on_click)
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")
# Create the box to enter message

# EntryBox.bind("<Return>", send)
# Place all components on the screen
# scrollbar.place(x=550, y=6, height=600)
Header.place(x=0, y=0, height=50, width=600)
ChatLog.place(x=40, y=60, height=580, width=520)
EntryBox.place(x=40, y=600, height=50, width=400)
SendButton.place(x=440, y=600, height=50)

broker_address = "4f6c627a13d848f4881c8c092b62c851.s1.eu.hivemq.cloud"
port = 8883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("shivam1250", "Shivam@123")

client.connect(broker_address, port)

time.sleep(1)

pubtop = "subscriber@shivam"
subtop = "publisher@shivam"
FLAG = True

client.loop_start()
client.subscribe(subtop)

time.sleep(1)

base.mainloop()
client.disconnect()
client.loop_stop()
