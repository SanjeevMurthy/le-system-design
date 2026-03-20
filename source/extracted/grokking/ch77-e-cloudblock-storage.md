# e. Cloud/Block Storage #

> Source: System Design - Grokking (Notes), Chapter 77, Pages 19-19

## Key Concepts

- 1. Chunks
2. Files
3. User
4. Devices
5. Workspace (sync folders)
c. Synchronization Service #
The Synchronization Service is the component that processes file updates made by a client and applies
the

## Content

1. Chunks
2. Files
3. User
4. Devices
5. Workspace (sync folders)
c. Synchronization Service #
The Synchronization Service is the component that processes file updates made by a client and applies
these changes to other subscribed clients. It also synchronizes clients’ local databases with the
information stored in the remote Metadata DB. The Synchronization Service is the most important
part of the system architecture due to its critical role in managing the metadata and synchronizing
users’ files. Desktop clients communicate with the Synchronization Service to either obtain updates
from the Cloud Storage or send files and updates to the Cloud Storage and, potentially, other users. If a
client was offline for a period, it polls the system for new updates as soon as they come online. When
the Synchronization Service receives an update request, it checks with the Metadata Database for
consistency and then proceeds with the update. Subsequently, a notification is sent to all subscribed
users or devices to report the file update.
The Synchronization Service should be designed in such a way that it transmits less data between
clients and the Cloud Storage to achieve a better response time. To meet this design goal, the
Synchronization Service can employ a differencing algorithm to reduce the amount of the data that
needs to be synchronized. Instead of transmitting entire files from clients to the server or vice versa, we
can just transmit the difference between two versions of a file. Therefore, only the part of the file that
has been changed is transmitted. This also decreases bandwidth consumption and cloud data storage
for the end user. As described above, we will be dividing our files into 4MB chunks and will be
transferring modified chunks only. Server and clients can calculate a hash (e.g., SHA-256) to see
whether to update the local copy of a chunk or not. On the server, if we already have a chunk with a
similar hash (even from another user), we don’t need to create another copy, we can use the same
chunk. This is discussed in detail later under Data Deduplication.
To be able to provide an efficient and scalable synchronization protocol we can consider using a
communication middleware between clients and the Synchronization Service. The messaging
middleware should provide scalable message queuing and change notifications to support a high
number of clients using pull or push strategies. This way, multiple Synchronization Service instances
can receive requests from a global request Queue, and the communication middleware will be able to
balance its load.
d. Message Queuing Service #
An important part of our architecture is a messaging middleware that should be able to handle a
substantial number of requests. A scalable Message Queuing Service that supports asynchronous
message-based communication between clients and the Synchronization Service best fits the
requirements of our application. The Message Queuing Service supports asynchronous and loosely
coupled message-based communication between distributed components of the system. The Message
Q
i
S
i
h
ld b
bl t
ffi i
tl
t
b
f
i
hi hl
il bl
Queuing Service should be able to efficiently store any number of messages in a highly available,
reliable and scalable queue.
The Message Queuing Service will implement two types of queues in our system. The Request Queue is
a global queue and all clients will share it. Clients’ requests to update the Metadata Database will be
sent to the Request Queue first, from there the Synchronization Service will take it to update metadata.
The Response Queues that correspond to individual subscribed clients are responsible for delivering
the update messages to each client. Since a message will be deleted from the queue once received by a
client, we need to create separate Response Queues for each subscribed client to share update
messages.
e. Cloud/Block Storage #
Cloud/Block Storage stores chunks of files uploaded by the users. Clients directly interact with the
storage to send and receive objects from it. Separation of the metadata from storage enables us to use
any storage either in the cloud or in-house.

## Examples & Scenarios

- transferring modified chunks only. Server and clients can calculate a hash (e.g., SHA-256) to see
whether to update the local copy of a chunk or not. On the server, if we already have a chunk with a
similar hash (even from another user), we don’t need to create another copy, we can use the same
chunk. This is discussed in detail later under Data Deduplication.
To be able to provide an efficient and scalable synchronization protocol we can consider using a
communication middleware between clients and the Synchronization Service. The messaging
middleware should provide scalable message queuing and change notifications to support a high
number of clients using pull or push strategies. This way, multiple Synchronization Service instances
can receive requests from a global request Queue, and the communication middleware will be able to
balance its load.

