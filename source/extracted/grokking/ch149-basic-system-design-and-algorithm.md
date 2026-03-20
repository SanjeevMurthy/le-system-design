# 8. Basic System Design and Algorithm

> Source: System Design - Grokking (Notes), Chapter 149, Pages 39-39

## Key Concepts

- threshold if the system has some resources available. For example, if a user is allowed only 100
messages a minute, we can let the user send more than 100 messages a minute when there are free
resourc

## Content

threshold if the system has some resources available. For example, if a user is allowed only 100
messages a minute, we can let the user send more than 100 messages a minute when there are free
resources available in the system.
6. What are different types of algorithms used for Rate Limiting?
Following are the two types of algorithms used for Rate Limiting:
Fixed Window Algorithm: In this algorithm, the time window is considered from the start of the
time-unit to the end of the time-unit. For example, a period would be considered 0-60 seconds for a
minute irrespective of the time frame at which the API request has been made. In the diagram below,
there are two messages between 0-1 second and three messages between 1-2 seconds. If we have a rate
limiting of two messages a second, this algorithm will throttle only ‘m5’.
0.0s
1.0s
2.0s
m1
m2
m3
m4
m5
Fixed Window - 2 messages
Fixed Window - 3 messages
Rolling Window - 4 messages
Rolling Window Algorithm: In this algorithm, the time window is considered from the fraction of
the time at which the request is made plus the time window length. For example, if there are two
messages sent at the 300th millisecond and 400th millisecond of a second, we’ll count them as two
messages from the 300th millisecond of that second up to the 300th millisecond of next second. In the
above diagram, keeping two messages a second, we’ll throttle ‘m3’ and ‘m4’.
7. High level design for Rate Limiter
Rate Limiter will be responsible for deciding which request will be served by the API servers and which
request will be declined. Once a new request arrives, the Web Server first asks the Rate Limiter to
decide if it will be served or throttled. If the request is not throttled, then it’ll be passed to the API
servers.
High level design for Rate Limiter
8. Basic System Design and Algorithm
Let’s take the example where we want to limit the number of requests per user. Under this scenario, for
each unique user, we would keep a count representing how many requests the user has made and a
timestamp when we started counting the requests. We can keep it in a hashtable, where the ‘key’ would
be the ‘UserID’ and ‘value’ would be a structure containing an integer for the ‘Count’ and an integer for
the Epoch time:
Key
Value
UserID
{ Count, StartTime }
Kristie
{ 3, 1499818564 }
:
:
:
E.g.,
Let’s assume our rate limiter is allowing three requests per minute per user, so whenever a new request
comes in, our rate limiter will perform the following steps:
1. If the ‘UserID’ is not present in the hash-table, insert it, set the ‘Count’ to 1, set ‘StartTime’ to the
current time (normalized to a minute), and allow the request.
2. Otherwise, find the record of the ‘UserID’ and if CurrentTime – StartTime >= 1 min , set the
‘StartTime’ to the current time, ‘Count’ to 1, and allow the request.
3. If CurrentTime - StartTime <= 1 min  and
If ‘Count < 3’, increment the Count and allow the request.
If ‘Count >= 3’, reject the request.
"Kristie" : { "Count": 1, "StartTime": 1499828400 }
Request at 03:00:00 AM
Insert into hashtable
Allow request
Rate Limiter allowing three requests per minute for user "Kristie"
"Kristie" : { "Count": 2, "StartTime": 1499828400 }
Request at 03:00:10 AM
Increment Count
"Kristie" : { "Count": 1, "StartTime": 1499828460 }
Request at 03:01:05 AM
Reset Count and StartTime
R
t
t 03 01 20 AM
Allow request
Allow request

## Examples & Scenarios

- threshold if the system has some resources available. For example, if a user is allowed only 100
messages a minute, we can let the user send more than 100 messages a minute when there are free
resources available in the system.
6. What are different types of algorithms used for Rate Limiting?
Following are the two types of algorithms used for Rate Limiting:
Fixed Window Algorithm: In this algorithm, the time window is considered from the start of the
time-unit to the end of the time-unit. For example, a period would be considered 0-60 seconds for a
minute irrespective of the time frame at which the API request has been made. In the diagram below,
there are two messages between 0-1 second and three messages between 1-2 seconds. If we have a rate
limiting of two messages a second, this algorithm will throttle only ‘m5’.

- the time at which the request is made plus the time window length. For example, if there are two
messages sent at the 300th millisecond and 400th millisecond of a second, we’ll count them as two
messages from the 300th millisecond of that second up to the 300th millisecond of next second. In the
above diagram, keeping two messages a second, we’ll throttle ‘m3’ and ‘m4’.
7. High level design for Rate Limiter
Rate Limiter will be responsible for deciding which request will be served by the API servers and which
request will be declined. Once a new request arrives, the Web Server first asks the Rate Limiter to
decide if it will be served or throttled. If the request is not throttled, then it’ll be passed to the API
servers.
High level design for Rate Limiter

- E.g.,
Let’s assume our rate limiter is allowing three requests per minute per user, so whenever a new request
comes in, our rate limiter will perform the following steps:
1. If the ‘UserID’ is not present in the hash-table, insert it, set the ‘Count’ to 1, set ‘StartTime’ to the
current time (normalized to a minute), and allow the request.
2. Otherwise, find the record of the ‘UserID’ and if CurrentTime – StartTime >= 1 min , set the
‘StartTime’ to the current time, ‘Count’ to 1, and allow the request.
3. If CurrentTime - StartTime <= 1 min  and
If ‘Count < 3’, increment the Count and allow the request.
If ‘Count >= 3’, reject the request.

