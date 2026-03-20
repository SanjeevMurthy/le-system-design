# 12. Security and Permissions

> Source: System Design - Grokking (Notes), Chapter 28, Pages 7-7

## Key Concepts

- Access a shortened URL
Client
Return error, URL not found
Find Orignal URL
Find original URL
URL found
Server
URL found
URL not found
Cache
URL
t f
d
URL found
Update cache
Yes, return HTTP error 401


## Content

Access a shortened URL
Client
Return error, URL not found
Find Orignal URL
Find original URL
URL found
Server
URL found
URL not found
Cache
URL
t f
d
URL found
Update cache
Yes, return HTTP error 401
No, redirect to original URL
Request flow for accessing a shortened URL
1 of 11
9. Load Balancer (LB)
#
We can add a Load balancing layer at three places in our system:
1. Between Clients and Application servers
2. Between Application Servers and database servers
3. Between Application Servers and Cache servers
Initially, we could use a simple Round Robin approach that distributes incoming requests equally
among backend servers. This LB is simple to implement and does not introduce any overhead. Another
benefit of this approach is that if a server is dead, LB will take it out of the rotation and will stop
sending any traffic to it.
A problem with Round Robin LB is that we don’t take the server load into consideration. If a server is
overloaded or slow, the LB will not stop sending new requests to that server. To handle this, a more
intelligent LB solution can be placed that periodically queries the backend server about its load and
adjusts traffic based on that.
10. Purging or DB cleanup
#
Should entries stick around forever or should they be purged? If a user-specified expiration time is
reached, what should happen to the link?
If we chose to actively search for expired links to remove them, it would put a lot of pressure on our
database. Instead, we can slowly remove expired links and do a lazy cleanup. Our service will make
sure that only expired links will be deleted, although some expired links can live longer but will never
be returned to users.
Whenever a user tries to access an expired link, we can delete the link and return an error to the
user.
A separate Cleanup service can run periodically to remove expired links from our storage and
cache. This service should be very lightweight and can be scheduled to run only when the user
traffic is expected to be low.
We can have a default expiration time for each link (e.g., two years).
After removing an expired link, we can put the key back in the key-DB to be reused.
Should we remove links that haven’t been visited in some length of time, say six months? This
ld b t i k
Si
t
i
tti
h
d
id t k
li k f
could be tricky. Since storage is getting cheap, we can decide to keep links forever.
Detailed component design for URL shortening
11. Telemetry
#
How many times a short URL has been used, what were user locations, etc.? How would we store these
statistics? If it is part of a DB row that gets updated on each view, what will happen when a popular
URL is slammed with a large number of concurrent requests?
Some statistics worth tracking: country of the visitor, date and time of access, web page that refers the
click, browser, or platform from where the page was accessed.
12. Security and Permissions
#
Can users create private URLs or allow a particular set of users to access a URL?
We can store the permission level (public/private) with each URL in the database. We can also create a
separate table to store UserIDs that have permission to see a specific URL. If a user does not have
permission and tries to access a URL, we can send an error (HTTP 401) back. Given that we are storing
our data in a NoSQL wide-column database like Cassandra, the key for the table storing permissions
would be the ‘Hash’ (or the KGS generated ‘key’). The columns will store the UserIDs of those users
that have the permission to see the URL.
←    Back
System Design Inte…
Next    →
Designing Pastebin
Completed

## Examples & Scenarios

- We can have a default expiration time for each link (e.g., two years).
After removing an expired link, we can put the key back in the key-DB to be reused.
Should we remove links that haven’t been visited in some length of time, say six months? This
ld b t i k
Si
t
i
tti
h
d

