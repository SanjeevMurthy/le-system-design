# 10. Data Sharding

> Source: System Design - Grokking (Notes), Chapter 60, Pages 14-14

## Key Concepts

- Losing files is not an option for our service. Therefore, we will store multiple copies of each file so that
if one storage server dies we can retrieve the photo from the other copy present on a diffe

## Content

Losing files is not an option for our service. Therefore, we will store multiple copies of each file so that
if one storage server dies we can retrieve the photo from the other copy present on a different storage
server.
This same principle also applies to other components of the system. If we want to have high availability
of the system, we need to have multiple replicas of services running in the system, so that if a few
services die down the system still remains available and running. Redundancy removes the single point
of failure in the system.
If only one instance of a service is required to run at any point, we can run a redundant secondary copy
of the service that is not serving any traffic, but it can take control after the failover when primary has a
problem.
Creating redundancy in a system can remove single points of failure and provide a backup or spare
functionality if needed in a crisis. For example, if there are two instances of the same service running in
production and one fails or degrades, the system can failover to the healthy copy. Failover can happen
automatically or require manual intervention.
10. Data Sharding
Let’s discuss different schemes for metadata sharding:
a. Partitioning based on UserID  Let’s assume we shard based on the ‘UserID’ so that we can keep
all photos of a user on the same shard. If one DB shard is 1TB, we will need four shards to store 3.7TB
of data. Let’s assume for better performance and scalability we keep 10 shards.
So we’ll find the shard number by UserID % 10 and then store the data there. To uniquely identify any
photo in our system, we can append shard number with each PhotoID.
How can we generate PhotoIDs? Each DB shard can have its own auto-increment sequence for
PhotoIDs and since we will append ShardID with each PhotoID, it will make it unique throughout our
system.
What are the different issues with this partitioning scheme?
1. How would we handle hot users? Several people follow such hot users and a lot of other people
p
p
p
p
see any photo they upload.
2. Some users will have a lot of photos compared to others, thus making a non-uniform distribution
of storage.
3. What if we cannot store all pictures of a user on one shard? If we distribute photos of a user onto
multiple shards will it cause higher latencies?
4. Storing all photos of a user on one shard can cause issues like unavailability of all of the user’s
data if that shard is down or higher latency if it is serving high load etc.
b. Partitioning based on PhotoID  If we can generate unique PhotoIDs first and then find a shard
number through “PhotoID % 10”, the above problems will have been solved. We would not need to
append ShardID with PhotoID in this case as PhotoID will itself be unique throughout the system.
How can we generate PhotoIDs? Here we cannot have an auto-incrementing sequence in each
shard to define PhotoID because we need to know PhotoID first to find the shard where it will be
stored. One solution could be that we dedicate a separate database instance to generate autoincrementing IDs. If our PhotoID can fit into 64 bits, we can define a table containing only a 64 bit ID
field. So whenever we would like to add a photo in our system, we can insert a new row in this table and
take that ID to be our PhotoID of the new photo.
Wouldn’t this key generating DB be a single point of failure?  Yes, it would be. A workaround
for that could be defining two such databases with one generating even numbered IDs and the other
odd numbered. For the MySQL, the following script can define such sequences:
KeyGeneratingServer1:
auto-increment-increment = 2
auto-increment-offset = 1
 
KeyGeneratingServer2:
auto-increment-increment = 2
auto-increment-offset = 2
We can put a load balancer in front of both of these databases to round robin between them and to deal
with downtime. Both these servers could be out of sync with one generating more keys than the other,
but this will not cause any issue in our system. We can extend this design by defining separate ID
tables for Users, Photo-Comments, or other objects present in our system.
Alternately, we can implement a ‘key’ generation scheme similar to what we have discussed in
Designing a URL Shortening service like TinyURL.
How can we plan for the future growth of our system?  We can have a large number of logical
partitions to accommodate future data growth, such that in the beginning, multiple logical partitions
reside on a single physical database server. Since each database server can have multiple database
instances on it, we can have separate databases for each logical partition on any server. So whenever
we feel that a particular database server has a lot of data, we can migrate some logical partitions from it
to another server. We can maintain a config file (or a separate database) that can map our logical
partitions to database servers; this will enable us to move partitions around easily. Whenever we want
t
titi
l h
t
d t th
fi fil t
th
h

## Examples & Scenarios

- functionality if needed in a crisis. For example, if there are two instances of the same service running in
production and one fails or degrades, the system can failover to the healthy copy. Failover can happen
automatically or require manual intervention.
10. Data Sharding
Let’s discuss different schemes for metadata sharding:
a. Partitioning based on UserID  Let’s assume we shard based on the ‘UserID’ so that we can keep
all photos of a user on the same shard. If one DB shard is 1TB, we will need four shards to store 3.7TB
of data. Let’s assume for better performance and scalability we keep 10 shards.
So we’ll find the shard number by UserID % 10 and then store the data there. To uniquely identify any
photo in our system, we can append shard number with each PhotoID.

