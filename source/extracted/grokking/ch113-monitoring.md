# 12. Monitoring

> Source: System Design - Grokking (Notes), Chapter 113, Pages 28-28

## Key Concepts

- 1483228800 000004
…
If we make our TweetID 64bits (8 bytes) long, we can easily store tweets for the next 100 years and
also store them for mili-seconds granularity.
In the above approach, we still ha

## Content

1483228800 000004
…
If we make our TweetID 64bits (8 bytes) long, we can easily store tweets for the next 100 years and
also store them for mili-seconds granularity.
In the above approach, we still have to query all the servers for timeline generation, but our reads (and
writes) will be substantially quicker.
1. Since we don’t have any secondary index (on creation time) this will reduce our write latency.
2. While reading, we don’t need to filter on creation-time as our primary key has epoch time
included in it.
8. Cache
We can introduce a cache for database servers to cache hot tweets and users. We can use an off-theshelf solution like Memcache that can store the whole tweet objects. Application servers, before hitting
database, can quickly check if the cache has desired tweets. Based on clients’ usage patterns we can
determine how many cache servers we need.
Which cache replacement policy would best fit our needs?  When the cache is full and we
want to replace a tweet with a newer/hotter tweet, how would we choose? Least Recently Used (LRU)
can be a reasonable policy for our system. Under this policy, we discard the least recently viewed tweet
first.
How can we have a more intelligent cache? If we go with 80-20 rule, that is 20% of tweets
generating 80% of read traffic which means that certain tweets are so popular that a majority of people
read them. This dictates that we can try to cache 20% of daily read volume from each shard.
What if we cache the latest data? Our service can benefit from this approach. Let’s say if 80% of
our users see tweets from the past three days only; we can try to cache all the tweets from the past
three days. Let’s say we have dedicated cache servers that cache all the tweets from all the users from
the past three days. As estimated above, we are getting 100 million new tweets or 30GB of new data
every day (without photos and videos). If we want to store all the tweets from last three days, we will
need less than 100GB of memory. This data can easily fit into one server, but we should replicate it
onto multiple servers to distribute all the read traffic to reduce the load on cache servers. So whenever
we are generating a user’s timeline, we can ask the cache servers if they have all the recent tweets for
that user. If yes, we can simply return all the data from the cache. If we don’t have enough tweets in the
cache, we have to query the backend server to fetch that data. On a similar design, we can try caching
photos and videos from the last three days.
Our cache would be like a hash table where ‘key’ would be ‘OwnerID’ and ‘value’ would be a doubly
linked list containing all the tweets from that user in the past three days. Since we want to retrieve the
most recent data first, we can always insert new tweets at the head of the linked list, which means all
the older tweets will be near the tail of the linked list. Therefore, we can remove tweets from the tail to
make space for newer tweets.
9. Timeline Generation
For a detailed discussion about timeline generation, take a look at Designing Facebook’s Newsfeed.
10. Replication and Fault Tolerance
Since our system is read-heavy, we can have multiple secondary database servers for each DB partition.
Secondary servers will be used for read traffic only. All writes will first go to the primary server and
then will be replicated to secondary servers. This scheme will also give us fault tolerance, since
whenever the primary server goes down we can failover to a secondary server.
11. Load Balancing
We can add Load balancing layer at three places in our system 1) Between Clients and Application
servers 2) Between Application servers and database replication servers and 3) Between Aggregation
servers and Cache server. Initially, a simple Round Robin approach can be adopted; that distributes
incoming requests equally among servers. This LB is simple to implement and does not introduce any
overhead. Another benefit of this approach is that if a server is dead, LB will take it out of the rotation
and will stop sending any traffic to it. A problem with Round Robin LB is that it won’t take servers load
into consideration. If a server is overloaded or slow, the LB will not stop sending new requests to that
server. To handle this, a more intelligent LB solution can be placed that periodically queries backend
server about their load and adjusts traffic based on that.
12. Monitoring
Having the ability to monitor our systems is crucial. We should constantly collect data to get an instant
insight into how our system is doing. We can collect following metrics/counters to get an
understanding of the performance of our service:
1. New tweets per day/second, what is the daily peak?
2. Timeline delivery stats, how many tweets per day/second our service is delivering.

