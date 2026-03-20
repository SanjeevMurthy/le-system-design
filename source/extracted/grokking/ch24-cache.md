# 8. Cache

> Source: System Design - Grokking (Notes), Chapter 24, Pages 6-6

## Key Concepts

- This ensures each server gets unique keys. If KGS dies before assigning all the loaded keys to some
server, we will be wasting those keys–which could be acceptable, given the huge number of keys we
ha

## Content

This ensures each server gets unique keys. If KGS dies before assigning all the loaded keys to some
server, we will be wasting those keys–which could be acceptable, given the huge number of keys we
have.
KGS also has to make sure not to give the same key to multiple servers. For that, it must synchronize
(or get a lock on) the data structure holding the keys before removing keys from it and giving them to a
server.
What would be the key-DB size?  With base64 encoding, we can generate 68.7B unique six letters
keys. If we need one byte to store one alpha-numeric character, we can store all these keys in:
6 (characters per key) * 68.7B (unique keys) = 412 GB.
Isn’t KGS a single point of failure?  Yes, it is. To solve this, we can have a standby replica of KGS.
Whenever the primary server dies, the standby server can take over to generate and provide keys.
Can each app server cache some keys from key-DB?  Yes, this can surely speed things up.
Although in this case, if the application server dies before consuming all the keys, we will end up losing
those keys. This can be acceptable since we have 68B unique six-letter keys.
How would we perform a key lookup?  We can look up the key in our database to get the full
URL. If it’s present in the DB, issue an “HTTP 302 Redirect” status back to the browser, passing the
stored URL in the “Location” field of the request. If that key is not present in our system, issue an
“HTTP 404 Not Found” status or redirect the user back to the homepage.
Should we impose size limits on custom aliases?  Our service supports custom aliases. Users
can pick any ‘key’ they like, but providing a custom alias is not mandatory. However, it is reasonable
(and often desirable) to impose a size limit on a custom alias to ensure we have a consistent URL
database. Let’s assume users can specify a maximum of 16 characters per customer key (as reflected in
the above database schema).
High level system design for URL shortening
7. Data Partitioning and Replication
#
To scale out our DB, we need to partition it so that it can store information about billions of URLs. We
need to come up with a partitioning scheme that would divide and store our data into different DB
servers.
a. Range Based Partitioning: We can store URLs in separate partitions based on the first letter of
the hash key. Hence we save all the URLs starting with letter ‘A’ (and ‘a’) in one partition, save those
that start with letter ‘B’ in another partition and so on. This approach is called range-based
partitioning. We can even combine certain less frequently occurring letters into one database partition.
We should come up with a static partitioning scheme so that we can always store/find a URL in a
predictable manner.
The main problem with this approach is that it can lead to unbalanced DB servers. For example, we
decide to put all URLs starting with letter ‘E’ into a DB partition, but later we realize that we have too
many URLs that start with the letter ‘E’.
b. Hash-Based Partitioning: In this scheme, we take a hash of the object we are storing. We then
calculate which partition to use based upon the hash. In our case, we can take the hash of the ‘key’ or
the short link to determine the partition in which we store the data object.
Our hashing function will randomly distribute URLs into different partitions (e.g., our hashing
function can always map any ‘key’ to a number between [1…256]), and this number would represent
the partition in which we store our object.
This approach can still lead to overloaded partitions, which can be solved by using Consistent Hashing.
8. Cache
#
We can cache URLs that are frequently accessed. We can use some off-the-shelf solution like
Memcached, which can store full URLs with their respective hashes. The application servers, before
hitting backend storage, can quickly check if the cache has the desired URL.
How much cache memory should we have? We can start with 20% of daily traffic and, based on
clients’ usage pattern, we can adjust how many cache servers we need. As estimated above, we need
170GB memory to cache 20% of daily traffic. Since a modern-day server can have 256GB memory, we
can easily fit all the cache into one machine. Alternatively, we can use a couple of smaller servers to
store all these hot URLs.
Which cache eviction policy would best fit our needs?  When the cache is full, and we want to
replace a link with a newer/hotter URL, how would we choose? Least Recently Used (LRU) can be a
reasonable policy for our system. Under this policy, we discard the least recently used URL first. We
can use a Linked Hash Map or a similar data structure to store our URLs and Hashes, which will also
keep track of the URLs that have been accessed recently.
To further increase the efficiency, we can replicate our caching servers to distribute the load between
them.
How can each cache replica be updated? Whenever there is a cache miss, our servers would be
hitting a backend database. Whenever this happens, we can update the cache and pass the new entry to
all the cache replicas. Each replica can update its cache by adding the new entry. If a replica already
has that entry, it can simply ignore it.

## Examples & Scenarios

- The main problem with this approach is that it can lead to unbalanced DB servers. For example, we
decide to put all URLs starting with letter ‘E’ into a DB partition, but later we realize that we have too
many URLs that start with the letter ‘E’.
b. Hash-Based Partitioning: In this scheme, we take a hash of the object we are storing. We then
calculate which partition to use based upon the hash. In our case, we can take the hash of the ‘key’ or
the short link to determine the partition in which we store the data object.
Our hashing function will randomly distribute URLs into different partitions (e.g., our hashing
function can always map any ‘key’ to a number between [1…256]), and this number would represent
the partition in which we store our object.
This approach can still lead to overloaded partitions, which can be solved by using Consistent Hashing.

