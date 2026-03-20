# 9. Reliability and Redundancy

> Source: System Design - Grokking (Notes), Chapter 59, Pages 13-13

## Key Concepts

- recent photos first.
We can store photos in a distributed file storage like HDFS or S3.
We can store the above schema in a distributed key-value store to enjoy the benefits offered by NoSQL.
All the m

## Content

recent photos first.
We can store photos in a distributed file storage like HDFS or S3.
We can store the above schema in a distributed key-value store to enjoy the benefits offered by NoSQL.
All the metadata related to photos can go to a table where the ‘key’ would be the ‘PhotoID’ and the
‘value’ would be an object containing PhotoLocation, UserLocation, CreationTimestamp, etc.
We need to store relationships between users and photos, to know who owns which photo. We also
need to store the list of people a user follows. For both of these tables, we can use a wide-column
datastore like Cassandra. For the ‘UserPhoto’ table, the ‘key’ would be ‘UserID’ and the ‘value’ would
be the list of ‘PhotoIDs’ the user owns, stored in different columns. We will have a similar scheme for
the ‘UserFollow’ table.
Cassandra or key-value stores in general, always maintain a certain number of replicas to offer
reliability. Also, in such data stores, deletes don’t get applied instantly, data is retained for certain days
(to support undeleting) before getting removed from the system permanently.
7. Data Size Estimation
Let’s estimate how much data will be going into each table and how much total storage we will need for
10 years.
User: Assuming each “int” and “dateTime” is four bytes, each row in the User’s table will be of 68
bytes:
UserID (4 bytes) + Name (20 bytes) + Email (32 bytes) + DateOfBirth (4 bytes) + CreationDate (4
bytes) + LastLogin (4 bytes) = 68 bytes
If we have 500 million users, we will need 32GB of total storage.
500 million * 68 ~= 32GB
Photo: Each row in Photo’s table will be of 284 bytes:
PhotoID (4 bytes) + UserID (4 bytes) + PhotoPath (256 bytes) + PhotoLatitude (4 bytes) +
A straightforward approach for storing the above schema would be to use an RDBMS like MySQL since
we require joins. But relational databases come with their challenges, especially when we need to scale
them. For details, please take a look at SQL vs. NoSQL.
PhotoID (4 bytes) + UserID (4 bytes) + PhotoPath (256 bytes) + PhotoLatitude (4 bytes) +
PhotLongitude(4 bytes) + UserLatitude (4 bytes) + UserLongitude (4 bytes) + CreationDate (4 bytes) =
284 bytes
If 2M new photos get uploaded every day, we will need 0.5GB of storage for one day:
2M * 284 bytes ~= 0.5GB per day
For 10 years we will need 1.88TB of storage.
UserFollow: Each row in the UserFollow table will consist of 8 bytes. If we have 500 million users
and on average each user follows 500 users. We would need 1.82TB of storage for the UserFollow
table:
500 million users * 500 followers * 8 bytes ~= 1.82TB
Total space required for all tables for 10 years will be 3.7TB:
32GB + 1.88TB + 1.82TB ~= 3.7TB
8. Component Design
Photo uploads (or writes) can be slow as they have to go to the disk, whereas reads will be faster,
especially if they are being served from cache.
Uploading users can consume all the available connections, as uploading is a slow process. This means
that ‘reads’ cannot be served if the system gets busy with all the write requests. We should keep in
mind that web servers have a connection limit before designing our system. If we assume that a web
server can have a maximum of 500 connections at any time, then it can’t have more than 500
concurrent uploads or reads. To handle this bottleneck we can split reads and writes into separate
services. We will have dedicated servers for reads and different servers for writes to ensure that
uploads don’t hog the system.
Separating photos’ read and write requests will also allow us to scale and optimize each of these
operations independently.
9. Reliability and Redundancy

