# Secure TCP Auction System

## Project Overview
This project implements a secure online auction system using TCP socket programming with SSL/TLS encryption. Multiple clients connect to a central auction server and place bids in real time.

## Features
- TCP socket communication
- SSL/TLS encrypted connections
- Multiple concurrent clients
- Real-time bid broadcasting
- Auction winner determination
- Bid history tracking

## Architecture

Client → TCP + TLS → Auction Server

Multiple clients connect concurrently and submit bids.

## Technologies Used
- Python
- TCP Sockets
- SSL/TLS Encryption
- Multithreading

## How to Run

### 1. Generate SSL certificate
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem


### 2. Start server

python3 server.py




### 3. Start clients

python3 client.py


Run multiple clients in different terminals.

## Example Output

NEW HIGHEST BID: 200 by Alice


## Concepts Demonstrated
- TCP Socket Programming
- Secure Communication (SSL/TLS)
- Client–Server Architecture
- Concurrent Client Handling

# Project Structure
secure-auction-socket-project
│
├── server.py        # Secure auction server
├── client.py        # Auction client
├── cert.pem         # SSL certificate
├── key.pem          # SSL private key
└── README.md


# Setup Instructions

1 Install Python

Ensure Python 3 is installed.

python3 --version
2 Generate SSL Certificates

Run this command in the project directory:

openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

This generates:

cert.pem
key.pem

These enable TLS encrypted communication.

3 Start the Server
python3 server.py

Example output:

Secure Auction Server Started
Item: Laptop
Auction Duration: 60 seconds
4 Start Clients

Open multiple terminals and run:

python3 client.py

Enter username and start bidding.

Example:

Enter username: Alice
Enter bid amount: 100
Example Auction Session

Client 1:

Alice → 100

Client 2:

Bob → 200

Server broadcast:

NEW HIGHEST BID: 200 by Bob

When auction time expires:

===== AUCTION ENDED =====
Winner: Bob
Winning Bid: 200
Performance Evaluation

The system was tested with multiple concurrent clients.

Test scenario:

Clients	Result
1	Normal operation
3	Real-time updates
5+	Concurrent bidding handled successfully

Observed characteristics:

Low latency bid updates

Reliable message delivery

Stable server operation under multiple clients

Failure Handling

The system includes mechanisms for handling runtime failures:

Failure	Handling Method
Client disconnect	Client removed from active list
Invalid bid input	Server rejects bid
Network error	Connection safely closed
Server shutdown	Final auction result displayed
Key Computer Networks Concepts Demonstrated

TCP Socket Programming

Secure Communication (SSL/TLS)

Client-Server Architecture

Concurrent Client Handling

Thread Synchronization

Reliable Data Transmission

Time-Critical Distributed Systems

Future Improvements

Possible enhancements:

Multiple auction items

Bid timestamps

User authentication

Web interface for auction clients

Auction extension for last-second bids