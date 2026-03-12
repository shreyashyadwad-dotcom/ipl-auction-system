import socket
import ssl
import threading

HOST = "127.0.0.1"
PORT = 5000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def receive(sock):

    while True:

        try:
            msg = sock.recv(1024)

            if not msg:
                break

            print("\n" + msg.decode())

        except:
            print("\nConnection closed by server")
            break


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_sock = context.wrap_socket(sock, server_hostname=HOST)

    try:
        secure_sock.connect((HOST, PORT))
    except:
        print("Cannot connect to server")
        return

    prompt = secure_sock.recv(1024).decode()
    username = input(prompt)

    secure_sock.send(username.encode())

    threading.Thread(target=receive, args=(secure_sock,), daemon=True).start()

    while True:

        try:

            bid = input("\nEnter bid amount: ")

            if bid.strip() == "":
                continue

            secure_sock.send(bid.encode())

        except:
            print("Disconnected")
            break


main()