# 12. Should we rate limit by IP or by user?

> Source: System Design - Grokking (Notes), Chapter 153, Pages 42-42

## Key Concepts

- we would need 60 entries for each user. We would need a total of 1.6KB to store one user’s data:
8 + (4 + 2 + 20 (Redis hash overhead)) * 60 + 20 (hash-table overhead) = 1.6KB
If we need to track one 

## Content

we would need 60 entries for each user. We would need a total of 1.6KB to store one user’s data:
8 + (4 + 2 + 20 (Redis hash overhead)) * 60 + 20 (hash-table overhead) = 1.6KB
If we need to track one million users at any time, total memory we would need would be 1.6GB:
1.6KB * 1 million ~= 1.6GB
So, our ‘Sliding Window with Counters’ algorithm uses 86% less memory than the simple sliding
window algorithm.
11. Data Sharding and Caching
We can shard based on the ‘UserID’ to distribute the user’s data. For fault tolerance and replication we
should use Consistent Hashing. If we want to have different throttling limits for different APIs, we can
choose to shard per user per API. Take the example of URL Shortener; we can have different rate
limiter for createURL()  and deleteURL()  APIs for each user or IP.
If our APIs are partitioned, a practical consideration could be to have a separate (somewhat smaller)
rate limiter for each API shard as well. Let’s take the example of our URL Shortener where we want to
limit each user not to create more than 100 short URLs per hour. Assuming we are using Hash-Based
Partitioning for our createURL()  API, we can rate limit each partition to allow a user to create not
more than three short URLs per minute in addition to 100 short URLs per hour.
Our system can get huge benefits from caching recent active users. Application servers can quickly
check if the cache has the desired record before hitting backend servers. Our rate limiter can
significantly benefit from the Write-back cache by updating all counters and timestamps in cache
only. The write to the permanent storage can be done at fixed intervals. This way we can ensure
minimum latency added to the user’s requests by the rate limiter. The reads can always hit the cache
first; which will be extremely useful once the user has hit their maximum limit and the rate limiter will
only be reading data without any updates.
Least Recently Used (LRU) can be a reasonable cache eviction policy for our system.
12. Should we rate limit by IP or by user?
Let’s discuss the pros and cons of using each one of these schemes:
IP: In this scheme, we throttle requests per-IP; although it’s not optimal in terms of differentiating
between ‘good’ and ‘bad’ actors, it’s still better than not have rate limiting at all. The biggest problem
with IP based throttling is when multiple users share a single public IP like in an internet cafe or
smartphone users that are using the same gateway. One bad user can cause throttling to other users.
Another issue could arise while caching IP-based limits, as there are a huge number of IPv6 addresses
available to a hacker from even one computer, it’s trivial to make a server run out of memory tracking
IPv6 addresses!
User: Rate limiting can be done on APIs after user authentication. Once authenticated, the user will be
provided with a token which the user will pass with each request. This will ensure that we will rate
Stuck? Get help on   
DISCUSS
limit against a particular API that has a valid authentication token. But what if we have to rate limit on
the login API itself? The weakness of this rate-limiting would be that a hacker can perform a denial of
service attack against a user by entering wrong credentials up to the limit; after that the actual user will
not be able to log-in.
How about if we combine the above two schemes?
Hybrid: A right approach could be to do both per-IP and per-user rate limiting, as they both have
weaknesses when implemented alone, though, this will result in more cache entries with more details
per entry, hence requiring more memory and storage.
←    Back
Designing Typeahe…
Next    →
Designing Twitter S…
Completed
Send feedback
52 Recommendations

