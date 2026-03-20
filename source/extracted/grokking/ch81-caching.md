# 10. Caching

> Source: System Design - Grokking (Notes), Chapter 81, Pages 20-20

## Key Concepts

- Detailed component design for Dropbox
7. File Processing Workflow
#
The sequence below shows the interaction between the components of the application in a scenario
when Client A updates a file that i

## Content

Detailed component design for Dropbox
7. File Processing Workflow
#
The sequence below shows the interaction between the components of the application in a scenario
when Client A updates a file that is shared with Client B and C, so they should receive the update too. If
the other clients are not online at the time of the update, the Message Queuing Service keeps the
update notifications in separate response queues for them until they come online later.
1. Client A uploads chunks to cloud storage.
2. Client A updates metadata and commits changes.
3. Client A gets confirmation and notifications are sent to Clients B and C about the changes.
4. Client B and C receive metadata changes and download updated chunks.
8. Data Deduplication
#
Data deduplication is a technique used for eliminating duplicate copies of data to improve storage
utilization. It can also be applied to network data transfers to reduce the number of bytes that must be
sent. For each new incoming chunk, we can calculate a hash of it and compare that hash with all the
hashes of the existing chunks to see if we already have the same chunk present in our storage.
We can implement deduplication in two ways in our system:
a. Post-process deduplication
With post-process deduplication, new chunks are first stored on the storage device and later some
process analyzes the data looking for duplication. The benefit is that clients will not need to wait for
the hash calculation or lookup to complete before storing the data, thereby ensuring that there is no
degradation in storage performance. Drawbacks of this approach are 1) We will unnecessarily be
storing duplicate data, though for a short time, 2) Duplicate data will be transferred consuming
bandwidth.
b. In-line deduplication
Alternatively, deduplication hash calculations can be done in real-time as the clients are entering data
on their device. If our system identifies a chunk that it has already stored, only a reference to the
existing chunk will be added in the metadata, rather than a full copy of the chunk. This approach will
give us optimal network and storage usage.
9. Metadata Partitioning
#
To scale out metadata DB, we need to partition it so that it can store information about millions of
users and billions of files/chunks. We need to come up with a partitioning scheme that would divide
and store our data in different DB servers
and store our data in different DB servers.
1. Vertical Partitioning: We can partition our database in such a way that we store tables related to
one particular feature on one server. For example, we can store all the user related tables in one
database and all files/chunks related tables in another database. Although this approach is
straightforward to implement it has some issues:
1. Will we still have scale issues? What if we have trillions of chunks to be stored and our database
cannot support storing such a huge number of records? How would we further partition such
tables?
2. Joining two tables in two separate databases can cause performance and consistency issues. How
frequently do we have to join user and file tables?
2. Range Based Partitioning: What if we store files/chunks in separate partitions based on the first
letter of the File Path? In that case, we save all the files starting with the letter ‘A’ in one partition and
those that start with the letter ‘B’ into another partition and so on. This approach is called range based
partitioning. We can even combine certain less frequently occurring letters into one database partition.
We should come up with this partitioning scheme statically so that we can always store/find a file in a
predictable manner.
The main problem with this approach is that it can lead to unbalanced servers. For example, if we
decide to put all files starting with the letter ‘E’ into a DB partition, and later we realize that we have
too many files that start with the letter ‘E’, to such an extent that we cannot fit them into one DB
partition.
3. Hash-Based Partitioning: In this scheme we take a hash of the object we are storing and based
on this hash we figure out the DB partition to which this object should go. In our case, we can take the
hash of the ‘FileID’ of the File object we are storing to determine the partition the file will be stored.
Our hashing function will randomly distribute objects into different partitions, e.g., our hashing
function can always map any ID to a number between [1…256], and this number would be the partition
we will store our object.
This approach can still lead to overloaded partitions, which can be solved by using Consistent Hashing.
10. Caching
#
We can have two kinds of caches in our system. To deal with hot files/chunks we can introduce a cache
for Block storage. We can use an off-the-shelf solution like Memcached that can store whole chunks
with its respective IDs/Hashes and Block servers before hitting Block storage can quickly check if the
cache has desired chunk. Based on clients’ usage pattern we can determine how many cache servers we
need. A high-end commercial server can have 144GB of memory; one such server can cache 36K
chunks.
Which cache replacement policy would best fit our needs?  When the cache is full, and we
want to replace a chunk with a newer/hotter chunk, how would we choose? Least Recently Used (LRU)
can be a reasonable policy for our system. Under this policy, we discard the least recently used chunk
first Load Similarly we can have a cache for Metadata DB

## Examples & Scenarios

- one particular feature on one server. For example, we can store all the user related tables in one
database and all files/chunks related tables in another database. Although this approach is
straightforward to implement it has some issues:
1. Will we still have scale issues? What if we have trillions of chunks to be stored and our database
cannot support storing such a huge number of records? How would we further partition such
tables?
2. Joining two tables in two separate databases can cause performance and consistency issues. How
frequently do we have to join user and file tables?
2. Range Based Partitioning: What if we store files/chunks in separate partitions based on the first
letter of the File Path? In that case, we save all the files starting with the letter ‘A’ in one partition and

- The main problem with this approach is that it can lead to unbalanced servers. For example, if we
decide to put all files starting with the letter ‘E’ into a DB partition, and later we realize that we have
too many files that start with the letter ‘E’, to such an extent that we cannot fit them into one DB
partition.
3. Hash-Based Partitioning: In this scheme we take a hash of the object we are storing and based
on this hash we figure out the DB partition to which this object should go. In our case, we can take the
hash of the ‘FileID’ of the File object we are storing to determine the partition the file will be stored.
Our hashing function will randomly distribute objects into different partitions, e.g., our hashing
function can always map any ID to a number between [1…256], and this number would be the partition
we will store our object.

