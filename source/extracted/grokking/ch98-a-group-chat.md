# a. Group chat

> Source: System Design - Grokking (Notes), Chapter 98, Pages 24-24

## Key Concepts

- change happens. Since we are maintaining a connection object on the server for all active users, we can
easily figure out the user’s current status from this. With 500M active users at any time, if we

## Content

change happens. Since we are maintaining a connection object on the server for all active users, we can
easily figure out the user’s current status from this. With 500M active users at any time, if we have to
broadcast each status change to all the relevant active users, it will consume a lot of resources. We can
do the following optimization around this:
1. Whenever a client starts the app, it can pull the current status of all users in their friends’ list.
2. Whenever a user sends a message to another user that has gone offline, we can send a failure to
the sender and update the status on the client.
3. Whenever a user comes online, the server can always broadcast that status with a delay of a few
seconds to see if the user does not go offline immediately.
4. Clients can pull the status from the server about those users that are being shown on the user’s
viewport. This should not be a frequent operation, as the server is broadcasting the online status
of users and we can live with the stale offline status of users for a while.
5. Whenever the client starts a new chat with another user, we can pull the status at that time.
Detailed component design for Facebook messenger
Design Summary: Clients will open a connection to the chat server to send a message; the server
will then pass it to the requested user. All the active users will keep a connection open with the server
to receive messages. Whenever a new message arrives, the chat server will push it to the receiving user
on the long poll request. Messages can be stored in HBase, which supports quick small updates, and
range based searches. The servers can broadcast the online status of a user to other relevant users.
Clients can pull status updates for users who are visible in the client’s viewport on a less frequent basis.
6. Data partitioning
Si
ill b
t
i
l t f d t (3 6PB f
fi
)
d t di t ib t it
t
lti l
Since we will be storing a lot of data (3.6PB for five years), we need to distribute it onto multiple
database servers. What will be our partitioning scheme?
Partitioning based on UserID: Let’s assume we partition based on the hash of the UserID so that
we can keep all messages of a user on the same database. If one DB shard is 4TB, we will have
“3.6PB/4TB ~= 900” shards for five years. For simplicity, let’s assume we keep 1K shards. So we will
find the shard number by “hash(UserID) % 1000” and then store/retrieve the data from there. This
partitioning scheme will also be very quick to fetch chat history for any user.
In the beginning, we can start with fewer database servers with multiple shards residing on one
physical server. Since we can have multiple database instances on a server, we can easily store multiple
partitions on a single server. Our hash function needs to understand this logical partitioning scheme so
that it can map multiple logical partitions on one physical server.
Since we will store an unlimited history of messages, we can start with a big number of logical
partitions, which will be mapped to fewer physical servers, and as our storage demand increases, we
can add more physical servers to distribute our logical partitions.
Partitioning based on MessageID: If we store different messages of a user on separate database
shards, fetching a range of messages of a chat would be very slow, so we should not adopt this scheme.
7. Cache
We can cache a few recent messages (say last 15) in a few recent conversations that are visible in a
user’s viewport (say last 5). Since we decided to store all of the user’s messages on one shard, the cache
for a user should entirely reside on one machine too.
8. Load balancing
We will need a load balancer in front of our chat servers; that can map each UserID to a server that
holds the connection for the user and then direct the request to that server. Similarly, we would need a
load balancer for our cache servers.
9. Fault tolerance and Replication
What will happen when a chat server fails? Our chat servers are holding connections with the
users. If a server goes down, should we devise a mechanism to transfer those connections to some
other server? It’s extremely hard to failover TCP connections to other servers; an easier approach can
be to have clients automatically reconnect if the connection is lost.
Should we store multiple copies of user messages?  We cannot have only one copy of the user’s
data, because if the server holding the data crashes or is down permanently, we don’t have any
mechanism to recover that data. For this, either we have to store multiple copies of the data on
different servers or use techniques like Reed-Solomon encoding to distribute and replicate it.
10. Extended Requirements
a. Group chat

