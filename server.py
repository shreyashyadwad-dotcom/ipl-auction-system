import socket
import ssl
import threading
import signal
import sys

HOST = "127.0.0.1"
PORT = 5000

clients = []
usernames = {}
lock = threading.Lock()

item = "Laptop"
highest_bid = 0
highest_bidder = "None"
bid_history = []

# TLS setup
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


def broadcast(msg):
    for c in clients:
        try:
            c.send((msg + "\n").encode())
        except:
            pass


def handle_client(client):

    global highest_bid, highest_bidder

    client.send("Enter username: ".encode())
    username = client.recv(1024).decode().strip()

    usernames[client] = username
    clients.append(client)

    broadcast(f"{username} joined the auction")

    client.send(
        f"\nAuction Item: {item}\nCurrent Highest Bid: {highest_bid}\nEnter bid amount:\n".encode()
    )

    while True:

        try:
            data = client.recv(1024).decode().strip()

            if not data:
                break

            try:
                bid = int(data)
            except:
                client.send("Enter a valid number\n".encode())
                continue

            with lock:

                if bid > highest_bid:

                    highest_bid = bid
                    highest_bidder = username
                    bid_history.append((username, bid))

                    broadcast(f"NEW HIGHEST BID: {bid} by {username}")

                else:
                    client.send("Bid too low\n".encode())

        except:
            break

    clients.remove(client)
    broadcast(f"{username} left auction")
    client.close()


def start_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print("Secure Auction Server Started")
    print("TLS Enabled")
    print("Item:", item)

    while True:

        client, addr = sock.accept()

        secure_client = context.wrap_socket(client, server_side=True)

        print("Client connected:", addr)

        threading.Thread(
            target=handle_client,
            args=(secure_client,),
            daemon=True
        ).start()


def end_auction(signal, frame):

    print("\n===== FINAL RESULT =====")
    print("Item:", item)
    print("Winner:", highest_bidder)
    print("Winning Bid:", highest_bid)

    print("\nBid History:")
    for user, bid in bid_history:
        print(user, "->", bid)

    sys.exit(0)


signal.signal(signal.SIGINT, end_auction)

start_server()