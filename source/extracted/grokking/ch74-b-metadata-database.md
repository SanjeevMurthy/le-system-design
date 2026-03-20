# b. Metadata Database #

> Source: System Design - Grokking (Notes), Chapter 74, Pages 18-18

## Key Concepts

- a. Client #
The Client Application monitors the workspace folder on the user’s machine and syncs all files/folders
in it with the remote Cloud Storage. The client application will work with the storag

## Content

a. Client #
The Client Application monitors the workspace folder on the user’s machine and syncs all files/folders
in it with the remote Cloud Storage. The client application will work with the storage servers to upload,
download, and modify actual files to backend Cloud Storage. The client also interacts with the remote
Synchronization Service to handle any file metadata updates, e.g., change in the file name, size,
modification date, etc.
Here are some of the essential operations for the client:
1. Upload and download files.
2. Detect file changes in the workspace folder.
3. Handle conflict due to offline or concurrent updates.
How do we handle file transfer efficiently?  As mentioned above, we can break each file into
smaller chunks so that we transfer only those chunks that are modified and not the whole file. Let’s say
we divide each file into fixed sizes of 4MB chunks. We can statically calculate what could be an optimal
chunk size based on 1) Storage devices we use in the cloud to optimize space utilization and
input/output operations per second (IOPS) 2) Network bandwidth 3) Average file size in the storage
etc. In our metadata, we should also keep a record of each file and the chunks that constitute it.
Should we keep a copy of metadata with Client?  Keeping a local copy of metadata not only
enable us to do offline updates but also saves a lot of round trips to update remote metadata.
How can clients efficiently listen to changes happening with other clients?  One solution
could be that the clients periodically check with the server if there are any changes. The problem with
this approach is that we will have a delay in reflecting changes locally as clients will be checking for
changes periodically compared to a server notifying whenever there is some change. If the client
frequently checks the server for changes, it will not only be wasting bandwidth, as the server has to
return an empty response most of the time, but will also be keeping the server busy. Pulling
information in this manner is not scalable.
A solution to the above problem could be to use HTTP long polling. With long polling the client
requests information from the server with the expectation that the server may not respond
immediately. If the server has no new data for the client when the poll is received, instead of sending
an empty response, the server holds the request open and waits for response information to become
available. Once it does have new information, the server immediately sends an HTTP/S response to
the client, completing the open HTTP/S Request. Upon receipt of the server response, the client can
immediately issue another server request for future updates.
Based on the above considerations, we can divide our client into following four parts:
I. Internal Metadata Database will keep track of all the files, chunks, their versions, and their
location in the file system.
II. Chunker will split the files into smaller pieces called chunks. It will also be responsible for
reconstructing a file from its chunks. Our chunking algorithm will detect the parts of the files that have
been modified by the user and only transfer those parts to the Cloud Storage; this will save us
been modified by the user and only transfer those parts to the Cloud Storage; this will save us
bandwidth and synchronization time.
III. Watcher will monitor the local workspace folders and notify the Indexer (discussed below) of any
action performed by the users, e.g. when users create, delete, or update files or folders. Watcher also
listens to any changes happening on other clients that are broadcasted by Synchronization service.
IV. Indexer will process the events received from the Watcher and update the internal metadata
database with information about the chunks of the modified files. Once the chunks are successfully
submitted/downloaded to the Cloud Storage, the Indexer will communicate with the remote
Synchronization Service to broadcast changes to other clients and update remote metadata database.
How should clients handle slow servers? Clients should exponentially back-off if the server is
busy/not-responding. Meaning, if a server is too slow to respond, clients should delay their retries and
this delay should increase exponentially.
Should mobile clients sync remote changes immediately?  Unlike desktop or web clients,
mobile clients usually sync on demand to save user’s bandwidth and space.
b. Metadata Database #
The Metadata Database is responsible for maintaining the versioning and metadata information about
files/chunks, users, and workspaces. The Metadata Database can be a relational database such as
MySQL, or a NoSQL database service such as DynamoDB. Regardless of the type of the database, the
Synchronization Service should be able to provide a consistent view of the files using a database,
especially if more than one user is working with the same file simultaneously. Since NoSQL data stores
do not support ACID properties in favor of scalability and performance, we need to incorporate the
support for ACID properties programmatically in the logic of our Synchronization Service in case we
opt for this kind of database. However, using a relational database can simplify the implementation of
the Synchronization Service as they natively support ACID properties.
The metadata Database should be storing information about following objects:

## Examples & Scenarios

- Synchronization Service to handle any file metadata updates, e.g., change in the file name, size,
modification date, etc.
Here are some of the essential operations for the client:
1. Upload and download files.
2. Detect file changes in the workspace folder.
3. Handle conflict due to offline or concurrent updates.
How do we handle file transfer efficiently?  As mentioned above, we can break each file into
smaller chunks so that we transfer only those chunks that are modified and not the whole file. Let’s say
we divide each file into fixed sizes of 4MB chunks. We can statically calculate what could be an optimal
chunk size based on 1) Storage devices we use in the cloud to optimize space utilization and

