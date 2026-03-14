import socket
import ssl
import threading
import time

HOST="127.0.0.1"
PORT=5000

BID_TIMEOUT=30
TEAM_BUDGET=20000000
MAX_PLAYERS=11
REQUIRED_CLIENTS=4

teams={
"RCB":{"budget":TEAM_BUDGET,"players":[]},
"CSK":{"budget":TEAM_BUDGET,"players":[]},
"MI":{"budget":TEAM_BUDGET,"players":[]},
"KKR":{"budget":TEAM_BUDGET,"players":[]}
}

clients={}
lock=threading.Lock()

current_bid=0
current_winner=None
last_bid_time=None
auction_open=False

context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem","key.pem")


players=[

{"name":"Virat Kohli","type":"batsman","runs":7263,"avg":37.2,"base":200000},
{"name":"Rohit Sharma","type":"batsman","runs":6211,"avg":30.5,"base":180000},
{"name":"KL Rahul","type":"batsman","runs":4163,"avg":46.8,"base":200000},
{"name":"Shubman Gill","type":"batsman","runs":2790,"avg":37.5,"base":150000},
{"name":"David Warner","type":"batsman","runs":6397,"avg":41.5,"base":200000},
{"name":"Faf du Plessis","type":"batsman","runs":3403,"avg":34.4,"base":150000},
{"name":"Ruturaj Gaikwad","type":"batsman","runs":1797,"avg":39.9,"base":120000},
{"name":"Ishan Kishan","type":"batsman","runs":2324,"avg":29.4,"base":120000},
{"name":"Rishabh Pant","type":"batsman","runs":2838,"avg":34.1,"base":150000},
{"name":"Sanju Samson","type":"batsman","runs":3888,"avg":29.5,"base":120000},

{"name":"Suryakumar Yadav","type":"batsman","runs":3249,"avg":32.7,"base":180000},
{"name":"Jos Buttler","type":"batsman","runs":3223,"avg":38.3,"base":200000},
{"name":"Devdutt Padikkal","type":"batsman","runs":1521,"avg":28.7,"base":120000},
{"name":"Nitish Rana","type":"batsman","runs":2636,"avg":27.1,"base":120000},
{"name":"Rahul Tripathi","type":"batsman","runs":2071,"avg":27.6,"base":120000},
{"name":"Quinton de Kock","type":"batsman","runs":3157,"avg":32.4,"base":180000},
{"name":"Nicholas Pooran","type":"batsman","runs":1276,"avg":26.5,"base":120000},
{"name":"Shimron Hetmyer","type":"batsman","runs":1133,"avg":31.4,"base":120000},
{"name":"Shreyas Iyer","type":"batsman","runs":2776,"avg":31.5,"base":150000},
{"name":"Kane Williamson","type":"batsman","runs":2101,"avg":36.2,"base":150000},

{"name":"Prithvi Shaw","type":"batsman","runs":1694,"avg":25.6,"base":100000},
{"name":"Mayank Agarwal","type":"batsman","runs":2599,"avg":22.9,"base":100000},
{"name":"Manish Pandey","type":"batsman","runs":3648,"avg":29.8,"base":100000},
{"name":"Ajinkya Rahane","type":"batsman","runs":4400,"avg":30.5,"base":120000},
{"name":"Dinesh Karthik","type":"batsman","runs":4516,"avg":26.3,"base":100000},
{"name":"Ambati Rayudu","type":"batsman","runs":4190,"avg":29.7,"base":100000},
{"name":"Wriddhiman Saha","type":"batsman","runs":2427,"avg":24.2,"base":80000},
{"name":"Devon Conway","type":"batsman","runs":924,"avg":42.0,"base":120000},
{"name":"Rahmanullah Gurbaz","type":"batsman","runs":391,"avg":21.7,"base":80000},
{"name":"Abhishek Sharma","type":"batsman","runs":893,"avg":24.3,"base":90000},

{"name":"Hardik Pandya","type":"allrounder","runs":2309,"avg":28.1,"base":200000},
{"name":"Ravindra Jadeja","type":"allrounder","runs":2692,"avg":26.5,"base":180000},
{"name":"Andre Russell","type":"allrounder","runs":2326,"avg":29.7,"base":200000},
{"name":"Ben Stokes","type":"allrounder","runs":920,"avg":25.4,"base":200000},
{"name":"Sam Curran","type":"allrounder","runs":337,"avg":21.3,"base":150000},
{"name":"Marcus Stoinis","type":"allrounder","runs":1472,"avg":27.9,"base":150000},
{"name":"Axar Patel","type":"allrounder","runs":1400,"avg":22.3,"base":150000},
{"name":"Glenn Maxwell","type":"allrounder","runs":2719,"avg":27.4,"base":180000},
{"name":"Moeen Ali","type":"allrounder","runs":1034,"avg":24.6,"base":120000},
{"name":"Shakib Al Hasan","type":"allrounder","runs":793,"avg":23.5,"base":120000},

{"name":"Jasprit Bumrah","type":"bowler","runs":50,"avg":8.1,"base":200000},
{"name":"Mohammed Shami","type":"bowler","runs":40,"avg":7.2,"base":180000},
{"name":"Bhuvneshwar Kumar","type":"bowler","runs":60,"avg":8.4,"base":150000},
{"name":"Yuzvendra Chahal","type":"bowler","runs":20,"avg":9.1,"base":180000},
{"name":"Rashid Khan","type":"bowler","runs":70,"avg":10.2,"base":200000},
{"name":"Kuldeep Yadav","type":"bowler","runs":45,"avg":7.5,"base":150000},
{"name":"Trent Boult","type":"bowler","runs":25,"avg":6.8,"base":150000},
{"name":"Kagiso Rabada","type":"bowler","runs":35,"avg":8.0,"base":180000},
{"name":"Pat Cummins","type":"bowler","runs":80,"avg":9.3,"base":180000},
{"name":"Anrich Nortje","type":"bowler","runs":30,"avg":7.9,"base":150000}
]


def broadcast(msg):
    for c in clients:
        try:
            c.send((msg+"\n").encode())
        except:
            pass


def show_purse():

    broadcast("\nTEAM PURSE STATUS")

    for t in teams:
        broadcast(f"{t} | Purse: {teams[t]['budget']} | Players: {len(teams[t]['players'])}/11")

    broadcast("-----------------------------------")


def handle_client(conn):

    global current_bid,current_winner,last_bid_time

    conn.send("Enter team name (RCB/CSK/MI/KKR): ".encode())
    team=conn.recv(1024).decode().strip()

    clients[conn]=team
    broadcast(f"{team} joined auction")

    while True:

        try:
            data=conn.recv(1024)

            if not data or not auction_open:
                continue

            bid=int(data.decode())

            with lock:

                if team==current_winner:
                    conn.send("Cannot bid twice consecutively\n".encode())
                    continue

                if bid<=current_bid:
                    conn.send("Bid must be higher\n".encode())
                    continue

                if bid>teams[team]["budget"]:
                    conn.send("Budget exceeded\n".encode())
                    continue

                if len(teams[team]["players"])>=MAX_PLAYERS:
                    conn.send("Team full\n".encode())
                    continue

                current_bid=bid
                current_winner=team
                last_bid_time=time.time()

                broadcast(f"NEW BID {bid} by {team}")

        except:
            break


def run_player(player):

    global current_bid,current_winner,last_bid_time,auction_open

    current_bid=player["base"]
    current_winner=None
    last_bid_time=time.time()

    auction_open=True

    show_purse()

    broadcast("\nPLAYER DETAILS")
    broadcast(f"NAME: {player['name']}")
    broadcast(f"TYPE: {player['type']}")
    broadcast(f"RUNS: {player['runs']}")
    broadcast(f"AVG: {player['avg']}")
    broadcast(f"BASE PRICE: {player['base']}")
    broadcast("START BIDDING")

    while True:

        if time.time()-last_bid_time>BID_TIMEOUT:

            auction_open=False

            if current_winner is None:

                broadcast("PLAYER UNSOLD")
                print(player["name"],"UNSOLD")

            else:

                teams[current_winner]["budget"]-=current_bid
                teams[current_winner]["players"].append(player["name"])

                broadcast(f"SOLD to {current_winner} for {current_bid}")

                show_purse()

                print(player["name"],"->",current_winner)

            break

        time.sleep(1)


def accept_clients(sock):

    while True:

        client,addr=sock.accept()
        print("Client connected:",addr)

        secure=context.wrap_socket(client,server_side=True)

        threading.Thread(target=handle_client,args=(secure,),daemon=True).start()


sock=socket.socket()
sock.bind((HOST,PORT))
sock.listen()

print("Auction Server Started")

threading.Thread(target=accept_clients,args=(sock,),daemon=True).start()

while len(clients)<REQUIRED_CLIENTS:
    time.sleep(1)

print("All teams connected. Starting auction...")

for p in players:
    run_player(p)

print("\nFINAL TEAMS")

for t in teams:
    print(t,teams[t]["players"])