# 8. Replication and Fault Tolerance

> Source: System Design - Grokking (Notes), Chapter 205, Pages 56-56

## Key Concepts

- p
p
g
g
g g
y g
g
p
g
p
pointers.
Once we have nearby LocationIDs, we can query the backend database to find details about those
places.
What will be the search workflow? We will first find the node t

## Content

p
p
g
g
g g
y g
g
p
g
p
pointers.
Once we have nearby LocationIDs, we can query the backend database to find details about those
places.
What will be the search workflow? We will first find the node that contains the user’s location. If
that node has enough desired places, we can return them to the user. If not, we will keep expanding to
the neighboring nodes (either through the parent pointers or doubly linked list) until either we find the
required number of places or exhaust our search based on the maximum radius.
How much memory will be needed to store the QuadTree?  For each Place, if we cache only
LocationID and Lat/Long, we would need 12GB to store all places.
24 * 500M => 12 GB
Since each grid can have a maximum of 500 places, and we have 500M locations, how many total grids
we will have?
500M / 500 => 1M grids
Which means we will have 1M leaf nodes and they will be holding 12GB of location data. A QuadTree
with 1M leaf nodes will have approximately 1/3rd internal nodes, and each internal node will have 4
pointers (for its children). If each pointer is 8 bytes, then the memory we need to store all internal
nodes would be:
1M * 1/3 * 4 * 8 = 10 MB
So, total memory required to hold the whole QuadTree would be 12.01GB. This can easily fit into a
modern-day server.
How would we insert a new Place into our system?  Whenever a new Place is added by a user,
we need to insert it into the databases as well as in the QuadTree. If our tree resides on one server, it is
easy to add a new Place, but if the QuadTree is distributed among different servers, first we need to
find the grid/server of the new Place and then add it there (discussed in the next section).
7. Data Partitioning
What if we have a huge number of places such that our index does not fit into a single machine’s
memory? With 20% growth each year we will reach the memory limit of the server in the future. Also,
what if one server cannot serve the desired read traffic? To resolve these issues, we must partition our
QuadTree!
We will explore two solutions here (both of these partitioning schemes can be applied to databases,
too):
a. Sharding based on regions: We can divide our places into regions (like zip codes), such that all
places belonging to a region will be stored on a fixed node. To store a place we will find the server
through its region and, similarly, while querying for nearby places we will ask the region server that
contains user’s location. This approach has a couple of issues:
contains user s location. This approach has a couple of issues:
1. What if a region becomes hot? There would be a lot of queries on the server holding that region,
making it perform slow. This will affect the performance of our service.
2. Over time, some regions can end up storing a lot of places compared to others. Hence,
maintaining a uniform distribution of places, while regions are growing is quite difficult.
To recover from these situations, either we have to repartition our data or use consistent hashing.
b. Sharding based on LocationID: Our hash function will map each LocationID to a server where
we will store that place. While building our QuadTree, we will iterate through all the places and
calculate the hash of each LocationID to find a server where it would be stored. To find places near a
location, we have to query all servers and each server will return a set of nearby places. A centralized
server will aggregate these results to return them to the user.
Will we have different QuadTree structure on different partitions?  Yes, this can happen
since it is not guaranteed that we will have an equal number of places in any given grid on all
partitions. However, we do make sure that all servers have approximately an equal number of Places.
This different tree structure on different servers will not cause any issue though, as we will be
searching all the neighboring grids within the given radius on all partitions.
The remaining part of this chapter assumes that we have partitioned our data based on LocationID.
8. Replication and Fault Tolerance
Having replicas of QuadTree servers can provide an alternate to data partitioning. To distribute read
traffic, we can have replicas of each QuadTree server. We can have a master-slave configuration where
replicas (slaves) will only serve read traffic; all write traffic will first go to the master and then applied
to slaves. Slaves might not have some recently inserted places (a few milliseconds delay will be there),
but this could be acceptable.
What will happen when a QuadTree server dies? We can have a secondary replica of each server and, if
primary dies, it can take control after the failover. Both primary and secondary servers will have the
same QuadTree structure.
What if both primary and secondary servers die at the same time? We have to allocate a new

