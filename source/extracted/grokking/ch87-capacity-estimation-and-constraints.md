# 3. Capacity Estimation and Constraints

> Source: System Design - Grokking (Notes), Chapter 87, Pages 21-21

## Key Concepts

- Stuck? Get help on   
DISCUSS
first. Load Similarly, we can have a cache for Metadata DB.
11. Load Balancer (LB)
#
We can add the Load balancing layer at two places in our system: 1) Between Clients a

## Content

Stuck? Get help on   
DISCUSS
first. Load Similarly, we can have a cache for Metadata DB.
11. Load Balancer (LB)
#
We can add the Load balancing layer at two places in our system: 1) Between Clients and Block servers
and 2) Between Clients and Metadata servers. Initially, a simple Round Robin approach can be
adopted that distributes incoming requests equally among backend servers. This LB is simple to
implement and does not introduce any overhead. Another benefit of this approach is if a server is dead,
LB will take it out of the rotation and will stop sending any traffic to it. A problem with Round Robin
LB is, it won’t take server load into consideration. If a server is overloaded or slow, the LB will not stop
sending new requests to that server. To handle this, a more intelligent LB solution can be placed that
periodically queries backend server about their load and adjusts traffic based on that.
12. Security, Permissions and File Sharing
#
One of the primary concerns users will have while storing their files in the cloud is the privacy and
security of their data, especially since in our system users can share their files with other users or even
make them public to share it with everyone. To handle this, we will be storing the permissions of each
file in our metadata DB to reflect what files are visible or modifiable by any user.
←    Back
Designing Instagram
Next    →
Designing Faceboo…
Completed
Send feedback
77 Recommendations
Designing Facebook Messenger
Let's design an instant messaging service like Facebook Messenger where users can send text messages
to each other through web and mobile interfaces.
1. What is Facebook Messenger?
Facebook Messenger is a software application which provides text-based instant messaging services to
its users. Messenger users can chat with their Facebook friends both from cell-phones and Facebook’s
website.
2. Requirements and Goals of the System
Our Messenger should meet the following requirements:
Functional Requirements:
1. Messenger should support one-on-one conversations between users.
2. Messenger should keep track of the online/offline statuses of its users.
3. Messenger should support the persistent storage of chat history.
Non-functional Requirements:
1. Users should have real-time chat experience with minimum latency.
2. Our system should be highly consistent; users should be able to see the same chat history on all
their devices.
3. Messenger’s high availability is desirable; we can tolerate lower availability in the interest of
consistency.
Extended Requirements:
Group Chats: Messenger should support multiple people talking to each other in a group.
Push notifications: Messenger should be able to notify users of new messages when they are
offline.
3. Capacity Estimation and Constraints
Let’s assume that we have 500 million daily active users and on average each user sends 40 messages
daily; this gives us 20 billion messages per day.
Storage Estimation: Let’s assume that on average a message is 100 bytes, so to store all the
messages for one day we would need 2TB of storage.
billi
*
b
TB/d

