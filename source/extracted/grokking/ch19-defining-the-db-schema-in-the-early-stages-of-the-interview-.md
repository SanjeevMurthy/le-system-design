# ��      Defining the DB schema in the early stages of the interview would help to

> Source: System Design - Grokking (Notes), Chapter 19, Pages 4-4

## Key Concepts

- Let s assume that each stored object will be approximately 500 bytes (just a ballpark estimate we will
dig into it later). We will need 15TB of total storage:
30 billion * 500 bytes = 15 TB
Bandwidth 

## Content

Let s assume that each stored object will be approximately 500 bytes (just a ballpark estimate we will
dig into it later). We will need 15TB of total storage:
30 billion * 500 bytes = 15 TB
Bandwidth estimates: For write requests, since we expect 200 new URLs every second, total
incoming data for our service will be 100KB per second:
200 * 500 bytes = 100 KB/s
For read requests, since every second we expect ~20K URLs redirections, total outgoing data for our
service would be 10MB per second:
20K * 500 bytes = ~10 MB/s
Memory estimates: If we want to cache some of the hot URLs that are frequently accessed, how
much memory will we need to store them? If we follow the 80-20 rule, meaning 20% of URLs generate
80% of traffic, we would like to cache these 20% hot URLs.
Since we have 20K requests per second, we will be getting 1.7 billion requests per day:
20K * 3600 seconds * 24 hours = ~1.7 billion
To cache 20% of these requests, we will need 170GB of memory.
0.2 * 1.7 billion * 500 bytes = ~170GB
One thing to note here is that since there will be a lot of duplicate requests (of the same URL),
therefore, our actual memory usage will be less than 170GB.
High level estimates: Assuming 500 million new URLs per month and 100:1 read:write ratio,
following is the summary of the high level estimates for our service:
New URLs
200/s
URL redirections
20K/s
URL redirections
20K/s
Incoming data
100KB/s
Outgoing data
10MB/s
Storage for 5 years
15TB
Memory for cache
170GB
4. System APIs
#
��      Once we've finalized the requirements, it's always a good idea to define the
system APIs. This should explicitly state what is expected from the system.
We can have SOAP or REST APIs to expose the functionality of our service. Following could be the
definitions of the APIs for creating and deleting URLs:
createURL(api_dev_key, original_url, custom_alias=None, user_name=None, expire_dat
e=None)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
original_url (string): Original URL to be shortened.
custom_alias (string): Optional custom key for the URL.
user_name (string): Optional user name to be used in the encoding.
expire_date (string): Optional expiration date for the shortened URL.
Returns: (string)
A successful insertion returns the shortened URL; otherwise, it returns an error code.
deleteURL(api_dev_key, url_key)
Where “url_key” is a string representing the shortened URL to be retrieved. A successful deletion
returns ‘URL Removed’.
How do we detect and prevent abuse? A malicious user can put us out of business by consuming
all URL keys in the current design. To prevent abuse, we can limit users via their api_dev_key. Each
api_dev_key can be limited to a certain number of URL creations and redirections per some time
period (which may be set to a different duration per developer key).
5. Database Design
#
��      Defining the DB schema in the early stages of the interview would help to

## Tables & Comparisons

| URL redirections | 20K/s |
| --- | --- |
|  |  |
| Incoming data | 100KB/s |
| Outgoing data | 10MB/s |
| Storage for 5 years | 15TB |
| Memory for cache | 170GB |

| New URLs | 200/s |
| --- | --- |
| URL redirections | 20K/s |
|  |  |

