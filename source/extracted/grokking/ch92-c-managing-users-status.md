# c. Managing user’s status

> Source: System Design - Grokking (Notes), Chapter 92, Pages 23-23

## Key Concepts

- How will clients maintain an open connection with the server?  We can use HTTP Long
Polling or WebSockets. In long polling, clients can request information from the server with the
expectation that th

## Content

How will clients maintain an open connection with the server?  We can use HTTP Long
Polling or WebSockets. In long polling, clients can request information from the server with the
expectation that the server may not respond immediately. If the server has no new data for the client
when the poll is received, instead of sending an empty response, the server holds the request open and
waits for response information to become available. Once it does have new information, the server
immediately sends the response to the client, completing the open request. Upon receipt of the server
response, the client can immediately issue another server request for future updates. This gives a lot of
improvements in latencies, throughputs, and performance. The long polling request can timeout or can
receive a disconnect from the server, in that case, the client has to open a new request.
How can the server keep track of all the opened connection to redirect messages to the
users efficiently? The server can maintain a hash table, where “key” would be the UserID and
“value” would be the connection object. So whenever the server receives a message for a user, it looks
up that user in the hash table to find the connection object and sends the message on the open request.
What will happen when the server receives a message for a user who has gone offline?  If
the receiver has disconnected, the server can notify the sender about the delivery failure. If it is a
temporary disconnect, e.g., the receiver’s long-poll request just timed out, then we should expect a
reconnect from the user. In that case, we can ask the sender to retry sending the message. This retry
could be embedded in the client’s logic so that users don’t have to retype the message. The server can
also store the message for a while and retry sending it once the receiver reconnects.
How many chat servers we need?  Let’s plan for 500 million connections at any time. Assuming a
modern server can handle 50K concurrent connections at any time, we would need 10K such servers.
How do we know which server holds the connection to which user?  We can introduce a
software load balancer in front of our chat servers; that can map each UserID to a server to redirect the
request.
How should the server process a ‘deliver message’ request?  The server needs to do the
following things upon receiving a new message: 1) Store the message in the database 2) Send the
message to the receiver and 3) Send an acknowledgment to the sender.
The chat server will first find the server that holds the connection for the receiver and pass the message
to that server to send it to the receiver. The chat server can then send the acknowledgment to the
sender; we don’t need to wait for storing the message in the database (this can happen in the
background). Storing the message is discussed in the next section.
How does the messenger maintain the sequencing of the messages?  We can store a
timestamp with each message, which is the time the message is received by the server. This will still
not ensure correct ordering of messages for clients. The scenario where the server timestamp cannot
determine the exact order of messages would look like this:
1. User-1 sends a message M1 to the server for User-2.
2. The server receives M1 at T1.
3. Meanwhile, User-2 sends a message M2 to the server for User-1.
4. The server receives the message M2 at T2, such that T2 > T1.
5. The server sends message M1 to User-2 and M2 to User-1.
So User-1 will see M1 first and then M2, whereas User-2 will see M2 first and then M1.
To resolve this, we need to keep a sequence number with every message for each client. This sequence
number will determine the exact ordering of messages for EACH user. With this solution, both clients
will see a different view of the message sequence, but this view will be consistent for them on all
devices.
b. Storing and retrieving the messages from the database
Whenever the chat server receives a new message, it needs to store it in the database. To do so, we have
two options:
1. Start a separate thread, which will work with the database to store the message.
2. Send an asynchronous request to the database to store the message.
We have to keep certain things in mind while designing our database:
1. How to efficiently work with the database connection pool.
2. How to retry failed requests.
3. Where to log those requests that failed even after some retries.
4. How to retry these logged requests (that failed after the retry) when all the issues have resolved.
Which storage system we should use?  We need to have a database that can support a very high
rate of small updates and also fetch a range of records quickly. This is required because we have a huge
number of small messages that need to be inserted in the database and, while querying, a user is
mostly interested in sequentially accessing the messages.
We cannot use RDBMS like MySQL or NoSQL like MongoDB because we cannot afford to read/write a
row from the database every time a user receives/sends a message. This will not only make the basic
operations of our service run with high latency but also create a huge load on databases.
Both of our requirements can be easily met with a wide-column database solution like HBase. HBase is
a column-oriented key-value NoSQL database that can store multiple values against one key into
multiple columns. HBase is modeled after Google’s BigTable and runs on top of Hadoop Distributed
File System (HDFS). HBase groups data together to store new data in a memory buffer and, once the
buffer is full, it dumps the data to the disk. This way of storage not only helps to store a lot of small
data quickly but also fetching rows by the key or scanning ranges of rows. HBase is also an efficient
database to store variable sized data, which is also required by our service.
How should clients efficiently fetch data from the server?  Clients should paginate while
fetching data from the server. Page size could be different for different clients, e.g., cell phones have
smaller screens, so we need a fewer number of message/conversations in the viewport.
c. Managing user’s status
We need to keep track of user’s online/offline status and notify all the relevant users whenever a status

## Examples & Scenarios

- temporary disconnect, e.g., the receiver’s long-poll request just timed out, then we should expect a
reconnect from the user. In that case, we can ask the sender to retry sending the message. This retry
could be embedded in the client’s logic so that users don’t have to retype the message. The server can
also store the message for a while and retry sending it once the receiver reconnects.
How many chat servers we need?  Let’s plan for 500 million connections at any time. Assuming a
modern server can handle 50K concurrent connections at any time, we would need 10K such servers.
How do we know which server holds the connection to which user?  We can introduce a
software load balancer in front of our chat servers; that can map each UserID to a server to redirect the
request.
How should the server process a ‘deliver message’ request?  The server needs to do the

- fetching data from the server. Page size could be different for different clients, e.g., cell phones have
smaller screens, so we need a fewer number of message/conversations in the viewport.
c. Managing user’s status
We need to keep track of user’s online/offline status and notify all the relevant users whenever a status

