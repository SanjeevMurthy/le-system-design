# Server-Sent Events (SSEs)

> Source: System Design - Grokking (Notes), Chapter 275, Pages 80-80

## Key Concepts

- Stuck? Get help on   
DISCUSS
client and allowing for messages to be passed back and forth while keeping the connection open. In this
way, a two-way (bi-directional) ongoing conversation can take plac

## Content

Stuck? Get help on   
DISCUSS
client and allowing for messages to be passed back and forth while keeping the connection open. In this
way, a two-way (bi-directional) ongoing conversation can take place between a client and a server.
Server
Client
WebSockets Protocol
Server-Sent Events (SSEs)
Under SSEs the client establishes a persistent and long-term connection with the server. The server
uses this connection to send data to a client. If the client wants to send data to the server, it would
require the use of another technology/protocol to do so.
1. Client requests data from a server using regular HTTP.
2. The requested webpage opens a connection to the server.
3. The server sends the data to the client whenever there’s new information available.
SSEs are best when we need real-time traffic from the server to the client or if the server is generating
data in a loop and will be sending multiple events to the client.
Server
Client
Server Sent Events Protocol
←    Back
Consistent Hashing
Next    →
Contact Us
Completed
Send feedback
38 Recommendations

