PESU IPL Auction System (Secure TCP Socket Project)
Project Overview

This project implements a secure real-time IPL-style player auction system using TCP socket programming with SSL/TLS encryption.

Multiple clients represent IPL teams, while the server acts as the auctioneer. Teams bid on players in real time until the bidding timeout expires. The system automatically assigns players to the highest bidder or marks them unsold.

The auction supports multiple teams, budgets, player statistics, and fairness constraints similar to the real IPL auction process.

# Features
Secure Communication

All communication between server and clients uses SSL/TLS encryption to ensure secure data exchange.

TCP Socket Programming

The system uses low-level TCP sockets for communication between server and team clients.

Real-Time Bidding

Teams can place bids on players in real time.

Player Auction System

100 IPL players included in the system

Players auctioned sequentially

Player statistics displayed before bidding begins

Team Management

4 teams participate in the auction

Each team has a budget of ₹2 Crore

Each team can buy maximum 11 players

Player Types

Players are categorized as:

Batsman

Bowler

Allrounder

Player Statistics

Depending on player type, statistics include:

Runs and batting average

Wickets and economy rate

Runs and wickets for allrounders

Auction Constraints

Minimum bid must be greater than current highest bid

Teams cannot exceed budget

Teams cannot exceed player limit

Time-Critical Bidding

Each player auction has a bid timeout.
If no new bid is received within the timeout period, the player is sold to the highest bidder.

Unsold Players

Players with no bids are automatically marked UNSOLD.

Concurrent Client Handling

Multiple teams connect simultaneously using multithreading.

System Architecture
              Auction Server
                    |
      ---------------------------------
      |        |        |        |
     RCB      CSK       MI      KKR
   (Client)  (Client) (Client) (Client)

Each client maintains a secure TCP connection with the server.

Technologies Used

Python

TCP Socket Programming

SSL/TLS Encryption

Multithreading

Project Structure
auction_project/
│
├── server.py        # Auction server
├── client.py        # Team client
├── cert.pem         # SSL certificate
├── key.pem          # SSL key
└── README.md
Setup Instructions
1 Install Python

Ensure Python 3 is installed:

python3 --version
2 Generate SSL Certificates

Run the following command in the project directory:

openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

This generates:

cert.pem
key.pem
3 Start the Server

Run:

python3 server.py

Example output:

PESU IPL Auction Server Started
Press ENTER when teams connected
4 Start Clients (Teams)

Open four terminals and run:

python3 client.py

Enter team names:

RCB
CSK
MI
KKR
Usage

Start the auction server.

Connect four team clients.

Begin the auction.

Teams place bids for players.

Player sold after timeout if no new bids occur.

Auction continues until all players are processed.

Example:

PLAYER: Virat Kohli
TYPE: batsman
BASE PRICE: 200000

RCB -> 220000
MI -> 250000
RCB -> 300000

SOLD to RCB for 300000
Example Auction Result
AUCTION COMPLETE

RCB
Players: [Virat Kohli, Bumrah, Gill...]

CSK
Players: [...]

MI
Players: [...]

KKR
Players: [...]
Key Computer Networks Concepts Demonstrated

TCP Socket Programming

Client–Server Architecture

SSL/TLS Secure Communication

Concurrent Client Handling

Real-Time Distributed Systems

Reliable Data Transmission