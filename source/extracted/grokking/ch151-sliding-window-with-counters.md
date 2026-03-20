# 10. Sliding Window with Counters

> Source: System Design - Grokking (Notes), Chapter 151, Pages 41-41

## Key Concepts

- "Kristie" : { 1499828400 }
Insert into hashtable
Allow request
"Kristie" : { 1499828465 }
Request at 03:01:05 AM
Remove old timestamps and insert the current time
"Kristie" : { 1499828465, 1499828480 

## Content

"Kristie" : { 1499828400 }
Insert into hashtable
Allow request
"Kristie" : { 1499828465 }
Request at 03:01:05 AM
Remove old timestamps and insert the current time
"Kristie" : { 1499828465, 1499828480 }
Request at 03:01:20 AM
Insert the current time
"Kristie" : { 1499828465, 1499828480, 1499828505 }
Request at 03:01:45 AM
Insert the current time
"Kristie" : { 1499828465, 1499828480,1499828505 }
Request at 03:01:50 AM
Reject request
"Kristie" : { 1499828480, 1499828505, 1499828530 }
Request at 03:02:10 AM
Remove old timestamps and insert the current time
Allow request
Allow request
Allow request
Allow request
How much memory would we need to store all of the user data for sliding window?  Let’s
assume ‘UserID’ takes 8 bytes. Each epoch time will require 4 bytes. Let’s suppose we need a rate
limiting of 500 requests per hour. Let’s assume 20 bytes overhead for hash-table and 20 bytes
overhead for the Sorted Set. At max, we would need a total of 12KB to store one user’s data:
8 + (4 + 20 (sorted set overhead)) * 500 + 20 (hash-table overhead) = 12KB
Here we are reserving 20 bytes overhead per element. In a sorted set, we can assume that we need at
least two pointers to maintain order among elements — one pointer to the previous element and one to
the next element. On a 64bit machine, each pointer will cost 8 bytes. So we will need 16 bytes for
pointers. We added an extra word (4 bytes) for storing other overhead.
If we need to track one million users at any time, total memory we would need would be 12GB:
12KB * 1 million ~= 12GB
Sliding Window Algorithm takes a lot of memory compared to the Fixed Window; this would be a
scalability issue. What if we can combine the above two algorithms to optimize our memory usage?
10. Sliding Window with Counters
What if we keep track of request counts for each user using multiple fixed time windows, e.g., 1/60th
the size of our rate limit’s time window. For example, if we have an hourly rate limit we can keep a
count for each minute and calculate the sum of all counters in the past hour when we receive a new
request to calculate the throttling limit. This would reduce our memory footprint. Let’s take an
example where we rate-limit at 500 requests per hour with an additional limit of 10 requests per
minute. This means that when the sum of the counters with timestamps in the past hour exceeds the
request threshold (500), Kristie has exceeded the rate limit. In addition to that, she can’t send more
than ten requests per minute. This would be a reasonable and practical consideration, as none of the
real users would send frequent requests. Even if they do, they will see success with retries since their
limits get reset every minute.
We can store our counters in a Redis Hash since it offers incredibly efficient storage for fewer than 100
keys. When each request increments a counter in the hash, it also sets the hash to expire an hour later.
We will normalize each ‘time’ to a minute.
"Kristie" : { 1499828400: 1 }
Request at 03:00:00 AM
Insert into hashtable
Allow request
Rate Limiter allowing three requests per minute for user "Kristie"
"Kristie" : { 1499828400: 1, 
                  1499828460: 1 }
Request at 03:01:05 AM
Insert another timestamp
Request at 03:01:20 AM
Increment counter for current timestamp
Request at 03:01:45 AM
Increment counter for current timestamp
Request at 03:01:50 AM
Reject request
"Kristie" : { 1499828460: 3,
                   1499832060: 1  }
Request at 04:01:00 AM
Remove old timestamps and insert the current time
Allow request
Allow request
Allow request
Allow request
"Kristie" : { 1499828400: 1, 
                  1499828460:  2 }
"Kristie" : { 1499828400: 1, 
                  1499828460: 3 }
"Kristie" : { 1499828400: 1, 
                  1499828460: 3 }
How much memory we would need to store all the user data for sliding window with
counters? Let’s assume ‘UserID’ takes 8 bytes. Each epoch time will need 4 bytes, and the Counter
would need 2 bytes. Let’s suppose we need a rate limiting of 500 requests per hour. Assume 20 bytes
overhead for hash-table and 20 bytes for Redis hash. Since we’ll keep a count for each minute, at max,

## Examples & Scenarios

- What if we keep track of request counts for each user using multiple fixed time windows, e.g., 1/60th
the size of our rate limit’s time window. For example, if we have an hourly rate limit we can keep a
count for each minute and calculate the sum of all counters in the past hour when we receive a new
request to calculate the throttling limit. This would reduce our memory footprint. Let’s take an
example where we rate-limit at 500 requests per hour with an additional limit of 10 requests per
minute. This means that when the sum of the counters with timestamps in the past hour exceeds the
request threshold (500), Kristie has exceeded the rate limit. In addition to that, she can’t send more
than ten requests per minute. This would be a reasonable and practical consideration, as none of the
real users would send frequent requests. Even if they do, they will see success with retries since their
limits get reset every minute.

