# 9. Sliding Window algorithm

> Source: System Design - Grokking (Notes), Chapter 150, Pages 40-40

## Key Concepts

- "Kristie" : { "Count": 2, "StartTime": 1499828460 }
Request at 03:01:20 AM
Increment Count
"Kristie" : { "Count": 3, "StartTime": 1499828460 }
Request at 03:01:45 AM
Increment Count
"Kristie" : { "Cou

## Content

"Kristie" : { "Count": 2, "StartTime": 1499828460 }
Request at 03:01:20 AM
Increment Count
"Kristie" : { "Count": 3, "StartTime": 1499828460 }
Request at 03:01:45 AM
Increment Count
"Kristie" : { "Count": 3, "StartTime": 1499828465 }
Request at 03:01:50 AM
Reject request
Allow request
Allow request
What are some of the problems with our algorithm?
1. This is a Fixed Window algorithm since we’re resetting the ‘StartTime’ at the end of every
minute, which means it can potentially allow twice the number of requests per minute. Imagine if
Kristie sends three requests at the last second of a minute, then she can immediately send three
more requests at the very first second of the next minute, resulting in 6 requests in the span of
two seconds. The solution to this problem would be a sliding window algorithm which we’ll
discuss later.
0.0min
1.0min
2.0min
3 Requests
3 Requests
6 Requests
m1
m2
m3
m4
m5
m6
2. Atomicity: In a distributed environment, the “read-and-then-write” behavior can create a race
condition. Imagine if Kristie’s current ‘Count’ is “2” and that she issues two more requests. If two
separate processes served each of these requests and concurrently read the Count before either of
them updated it, each process would think that Kristie could have one more request and that she
had not hit the rate limit.
Request 1
1) Read Count = 2
2) 
3) Update Count = 3
Request 2
2) Read Count = 2
3) Update Count = 3
Time
If we are using Redis to store our key-value, one solution to resolve the atomicity problem is to use
Redis lock for the duration of the read-update operation. This, however, would come at the expense of
slowing down concurrent requests from the same user and introducing another layer of complexity. We
can use Memcached, but it would have comparable complications.
If we are using a simple hash-table, we can have a custom implementation for ‘locking’ each record to
solve our atomicity problems.
How much memory would we need to store all of the user data?  Let’s assume the simple
solution where we are keeping all of the data in a hash-table.
Let’s assume ‘UserID’ takes 8 bytes. Let’s also assume a 2 byte ‘Count’, which can count up to 65k, is
sufficient for our use case. Although epoch time will need 4 bytes, we can choose to store only the
minute and second part, which can fit into 2 bytes. Hence, we need a total of 12 bytes to store a user’s
data:
8 + 2 + 2 = 12 bytes
Let’s assume our hash-table has an overhead of 20 bytes for each record. If we need to track one
million users at any time, the total memory we would need would be 32MB:
(12 + 20) bytes * 1 million => 32MB
If we assume that we would need a 4-byte number to lock each user’s record to resolve our atomicity
problems, we would require a total 36MB memory.
This can easily fit on a single server; however we would not like to route all of our traffic through a
single machine. Also, if we assume a rate limit of 10 requests per second, this would translate into 10
million QPS for our rate limiter! This would be too much for a single server. Practically, we can assume
we would use a Redis or Memcached kind of a solution in a distributed setup. We’ll be storing all the
data in the remote Redis servers and all the Rate Limiter servers will read (and update) these servers
before serving or throttling any request.
9. Sliding Window algorithm
We can maintain a sliding window if we can keep track of each request per user. We can store the
timestamp of each request in a Redis Sorted Set in our ‘value’ field of hash-table.
Key
Value
UserID
{ Sorted Set <UnixTime> }
Kristie
{ 1499818000,  1499818500, 1499818860 }
:
:
:
E.g.,
Let’s assume our rate limiter is allowing three requests per minute per user, so, whenever a new
request comes in, the Rate Limiter will perform following steps:
1. Remove all the timestamps from the Sorted Set that are older than “CurrentTime - 1 minute”.
2. Count the total number of elements in the sorted set. Reject the request if this count is greater
than our throttling limit of “3”.
3. Insert the current time in the sorted set and accept the request.
Request at 03:00:00 AM
Rate Limiter allowing three requests per minute for user "Kristie"

## Examples & Scenarios

- E.g.,
Let’s assume our rate limiter is allowing three requests per minute per user, so, whenever a new
request comes in, the Rate Limiter will perform following steps:
1. Remove all the timestamps from the Sorted Set that are older than “CurrentTime - 1 minute”.
2. Count the total number of elements in the sorted set. Reject the request if this count is greater
than our throttling limit of “3”.
3. Insert the current time in the sorted set and accept the request.
Request at 03:00:00 AM
Rate Limiter allowing three requests per minute for user "Kristie"

