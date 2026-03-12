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