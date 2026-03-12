import socket
import ssl
import threading
import time
import signal
import sys

HOST = "127.0.0.1"
PORT = 5000

AUCTION_DURATION = 100
CLIENT_ENTRY_WINDOW = 60

auction_start_time = time.time()
auction_end_time = auction_start_time + AUCTION_DURATION
entry_deadline = auction_start_time + CLIENT_ENTRY_WINDOW

clients = []
usernames = {}

lock = threading.Lock()

item = "Laptop"
highest_bid = 0
highest_bidder = "None"
last_bidder = None
bid_history = []

auction_active = True

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


def broadcast(msg):
    for c in clients:
        try:
            c.send((msg + "\n").encode())
        except:
            pass


def handle_client(client):

    global highest_bid, highest_bidder, last_bidder

    try:

        client.send("Enter username: ".encode())
        username = client.recv(1024).decode().strip()

        usernames[client] = username
        clients.append(client)

        broadcast(f"{username} joined the auction")

        client.send(
            f"\nAuction Item: {item}\nCurrent Highest Bid: {highest_bid}\nEnter bid amount:\n".encode()
        )

        while auction_active:

            try:

                data = client.recv(1024)

                if not data:
                    break

                bid_text = data.decode().strip()

                try:
                    bid = int(bid_text)
                except:
                    client.send("Invalid bid. Enter a number.\n".encode())
                    continue

                with lock:

                    if username == last_bidder:
                        client.send(
                            "You cannot bid twice in a row. Wait for another bidder.\n".encode()
                        )
                        continue

                    if bid > highest_bid:

                        highest_bid = bid
                        highest_bidder = username
                        last_bidder = username
                        bid_history.append((username, bid))

                        broadcast(f"NEW HIGHEST BID: {bid} by {username}")

                    else:
                        client.send("Bid too low\n".encode())

            except:
                break

    finally:

        if client in clients:
            clients.remove(client)

        if client in usernames:
            broadcast(f"{usernames[client]} disconnected")
            del usernames[client]

        client.close()


def auction_timer():

    global auction_active

    while True:

        remaining = int(auction_end_time - time.time())

        if remaining <= 0:

            auction_active = False

            broadcast("\n===== AUCTION ENDED =====")
            broadcast(f"Winner: {highest_bidder}")
            broadcast(f"Winning Bid: {highest_bid}")

            print("\n===== FINAL RESULT =====")
            print("Winner:", highest_bidder)
            print("Winning Bid:", highest_bid)

            print("\nBid History:")
            for user, bid in bid_history:
                print(user, "->", bid)

            break

        time.sleep(1)


def start_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print("Secure Auction Server Started")
    print("Auction Duration:", AUCTION_DURATION, "seconds")
    print("Client Entry Window:", CLIENT_ENTRY_WINDOW, "seconds")

    threading.Thread(target=auction_timer, daemon=True).start()

    while True:

        try:

            client, addr = sock.accept()

            if time.time() > entry_deadline:

                client.send(
                    "Auction already started. No new clients allowed.\n".encode()
                )
                client.close()
                print("Rejected client:", addr)
                continue

            secure_client = context.wrap_socket(client, server_side=True)

            print("Client connected:", addr)

            threading.Thread(
                target=handle_client,
                args=(secure_client,),
                daemon=True
            ).start()

        except:
            break


def shutdown(signal, frame):
    print("\nServer shutting down")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)

start_server()