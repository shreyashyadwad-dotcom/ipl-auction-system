import socket
import ssl
import threading

HOST="127.0.0.1"
PORT=5000

context=ssl.create_default_context()
context.check_hostname=False
context.verify_mode=ssl.CERT_NONE

def receive(sock):

    while True:
        try:
            msg=sock.recv(1024)
            if not msg:
                break
            print(msg.decode())
        except:
            break

sock=socket.socket()
secure=context.wrap_socket(sock,server_hostname=HOST)

secure.connect((HOST,PORT))

prompt=secure.recv(1024).decode()
team=input(prompt)

secure.send(team.encode())

threading.Thread(target=receive,args=(secure,),daemon=True).start()

while True:
    bid=input("Enter bid: ")
    secure.send(bid.encode())