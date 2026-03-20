# a. Messages Handling

> Source: System Design - Grokking (Notes), Chapter 90, Pages 22-22

## Key Concepts

- 20 billion messages * 100 bytes => 2 TB/day
To store five years of chat history, we would need 3.6 petabytes of storage.
2 TB * 365 days * 5 years ~= 3.6 PB
Other than the chat messages, we would also

## Content

20 billion messages * 100 bytes => 2 TB/day
To store five years of chat history, we would need 3.6 petabytes of storage.
2 TB * 365 days * 5 years ~= 3.6 PB
Other than the chat messages, we would also need to store users’ information, messages’ metadata (ID,
Timestamp, etc.). Not to mention, the above calculation doesn’t take data compression and replication
into consideration.
Bandwidth Estimation: If our service is getting 2TB of data every day, this will give us 25MB of
incoming data for each second.
2 TB / 86400 sec ~= 25 MB/s
Since each incoming message needs to go out to another user, we will need the same amount of
bandwidth 25MB/s for both upload and download.
High level estimates:
Total messages
20 billion per day
Storage for each day
2TB
Storage for 5 years
3.6PB
Incomming data
25MB/s
Outgoing data
25MB/s
4. High Level Design
At a high-level, we will need a chat server that will be the central piece, orchestrating all the
communications between users. When a user wants to send a message to another user, they will
connect to the chat server and send the message to the server; the server then passes that message to
the other user and also stores it in the database.
The detailed workflow would look like this:
1. User-A sends a message to User-B through the chat server.
2. The server receives the message and sends an acknowledgment to User-A.
3. The server stores the message in its database and sends the message to User-B.
4. User-B receives the message and sends the acknowledgment to the server.
5. The server notifies User-A that the message has been delivered successfully to User-B.
Send a message to User B
User A
Server managing 
connection with User A
Request flow for sending a message
1 of 8
5. Detailed Component Design
Let’s try to build a simple solution first where everything runs on one server. At the high level our
system needs to handle the following use cases:
1. Receive incoming messages and deliver outgoing messages.
2. Store and retrieve messages from the database.
3. Keep a record of which user is online or has gone offline, and notify all the relevant users about
these status changes.
Let’s talk about these scenarios one by one:
a. Messages Handling
How would we efficiently send/receive messages? To send messages, a user needs to connect to
the server and post messages for the other users. To get a message from the server, the user has two
options:
1. Pull model: Users can periodically ask the server if there are any new messages for them.
2. Push model: Users can keep a connection open with the server and can depend upon the server
to notify them whenever there are new messages.
If we go with our first approach, then the server needs to keep track of messages that are still waiting to
be delivered, and as soon as the receiving user connects to the server to ask for any new message, the
server can return all the pending messages. To minimize latency for the user, they have to check the
server quite frequently, and most of the time they will be getting an empty response if there are no
pending message. This will waste a lot of resources and does not look like an efficient solution.
If we go with our second approach, where all the active users keep a connection open with the server,
then as soon as the server receives a message it can immediately pass the message to the intended user.
This way, the server does not need to keep track of the pending messages, and we will have minimum
latency, as the messages are delivered instantly on the opened connection.
How will clients maintain an open connection with the server? We can use HTTP Long

## Tables & Comparisons

| Total messages | 20 billion per day |
| --- | --- |
| Storage for each day | 2TB |
| Storage for 5 years | 3.6PB |
| Incomming data | 25MB/s |
| Outgoing data | 25MB/s |

