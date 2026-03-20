# 11. Ranking

> Source: System Design - Grokking (Notes), Chapter 208, Pages 57-57

## Key Concepts

- What if both primary and secondary servers die at the same time?  We have to allocate a new
server and rebuild the same QuadTree on it. How can we do that, since we don’t know what places
were kept on

## Content

What if both primary and secondary servers die at the same time?  We have to allocate a new
server and rebuild the same QuadTree on it. How can we do that, since we don’t know what places
were kept on this server? The brute-force solution would be to iterate through the whole database and
filter LocationIDs using our hash function to figure out all the required places that will be stored on
this server. This would be inefficient and slow; also, during the time when the server is being rebuilt,
we will not be able to serve any query from it, thus missing some places that should have been seen by
users.
How can we efficiently retrieve a mapping between Places and QuadTree server?  We have
to build a reverse index that will map all the Places to their QuadTree server. We can have a separate
QuadTree Index server that will hold this information. We will need to build a HashMap where the
‘key’ is the QuadTree server number and the ‘value’ is a HashSet containing all the Places being kept on
that QuadTree server. We need to store LocationID and Lat/Long with each place because information
servers can build their QuadTrees through this. Notice that we are keeping Places’ data in a HashSet,
this will enable us to add/remove Places from our index quickly. So now, whenever a QuadTree server
needs to rebuild itself, it can simply ask the QuadTree Index server for all the Places it needs to store.
This approach will surely be quite fast. We should also have a replica of the QuadTree Index server for
fault tolerance. If a QuadTree Index server dies, it can always rebuild its index from iterating through
the database.
9. Cache
To deal with hot Places, we can introduce a cache in front of our database. We can use an off-the-shelf
solution like Memcache, which can store all data about hot places. Application servers, before hitting
the backend database, can quickly check if the cache has that Place. Based on clients’ usage pattern, we
can adjust how many cache servers we need. For cache eviction policy, Least Recently Used (LRU)
seems suitable for our system.
10. Load Balancing (LB)
We can add LB layer at two places in our system 1) Between Clients and Application servers and 2)
Between Application servers and Backend server. Initially, a simple Round Robin approach can be
adopted; that will distribute all incoming requests equally among backend servers. This LB is simple to
implement and does not introduce any overhead. Another benefit of this approach is if a server is dead
the load balancer will take it out of the rotation and will stop sending any traffic to it.
A problem with Round Robin LB is, it won’t take server load into consideration. If a server is
overloaded or slow, the load balancer will not stop sending new requests to that server. To handle this,
a more intelligent LB solution would be needed that periodically queries backend server about their
load and adjusts traffic based on that.
11. Ranking
How about if we want to rank the search results not just by proximity but also by popularity or
relevance?
How can we return most popular places within a given radius?  Let’s assume we keep track of
Stuck? Get help on   
DISCUSS
the overall popularity of each place. An aggregated number can represent this popularity in our system,
e.g., how many stars a place gets out of ten (this would be an average of different rankings given by
users)? We will store this number in the database as well as in the QuadTree. While searching for the
top 100 places within a given radius, we can ask each partition of the QuadTree to return the top 100
places with maximum popularity. Then the aggregator server can determine the top 100 places among
all the places returned by different partitions.
Remember that we didn’t build our system to update place’s data frequently. With this design, how can
we modify the popularity of a place in our QuadTree? Although we can search a place and update its
popularity in the QuadTree, it would take a lot of resources and can affect search requests and system
throughput. Assuming the popularity of a place is not expected to reflect in the system within a few
hours, we can decide to update it once or twice a day, especially when the load on the system is
minimum.
Our next problem, Designing Uber backend, discusses dynamic updates of the QuadTree in detail.
←    Back
Designing Faceboo…
Next    →
Designing Uber ba…
Completed
Send feedback
55 Recommendations

## Examples & Scenarios

- e.g., how many stars a place gets out of ten (this would be an average of different rankings given by
users)? We will store this number in the database as well as in the QuadTree. While searching for the
top 100 places within a given radius, we can ask each partition of the QuadTree to return the top 100
places with maximum popularity. Then the aggregator server can determine the top 100 places among
all the places returned by different partitions.
Remember that we didn’t build our system to update place’s data frequently. With this design, how can
we modify the popularity of a place in our QuadTree? Although we can search a place and update its
popularity in the QuadTree, it would take a lot of resources and can affect search requests and system
throughput. Assuming the popularity of a place is not expected to reflect in the system within a few
hours, we can decide to update it once or twice a day, especially when the load on the system is

