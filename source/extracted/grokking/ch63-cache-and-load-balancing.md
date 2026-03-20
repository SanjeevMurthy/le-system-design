# 13. Cache and Load balancing

> Source: System Design - Grokking (Notes), Chapter 63, Pages 15-15

## Key Concepts

- to move a partition, we only have to update the config file to announce the change.
11. Ranking and News Feed Generation
To create the News Feed for any given user, we need to fetch the latest, most p

## Content

to move a partition, we only have to update the config file to announce the change.
11. Ranking and News Feed Generation
To create the News Feed for any given user, we need to fetch the latest, most popular and relevant
photos of the people the user follows.
For simplicity, let’s assume we need to fetch top 100 photos for a user’s News Feed. Our application
server will first get a list of people the user follows and then fetch metadata info of latest 100 photos
from each user. In the final step, the server will submit all these photos to our ranking algorithm which
will determine the top 100 photos (based on recency, likeness, etc.) and return them to the user. A
possible problem with this approach would be higher latency as we have to query multiple tables and
perform sorting/merging/ranking on the results. To improve the efficiency, we can pre-generate the
News Feed and store it in a separate table.
Pre-generating the News Feed: We can have dedicated servers that are continuously generating
users’ News Feeds and storing them in a ‘UserNewsFeed’ table. So whenever any user needs the latest
photos for their News Feed, we will simply query this table and return the results to the user.
Whenever these servers need to generate the News Feed of a user, they will first query the
UserNewsFeed table to find the last time the News Feed was generated for that user. Then, new News
Feed data will be generated from that time onwards (following the steps mentioned above).
What are the different approaches for sending News Feed contents to the users?
1. Pull: Clients can pull the News Feed contents from the server on a regular basis or manually
whenever they need it. Possible problems with this approach are a) New data might not be shown to
the users until clients issue a pull request b) Most of the time pull requests will result in an empty
response if there is no new data.
2. Push: Servers can push new data to the users as soon as it is available. To efficiently manage this,
users have to maintain a Long Poll request with the server for receiving the updates. A possible
problem with this approach is, a user who follows a lot of people or a celebrity user who has millions of
followers; in this case, the server has to push updates quite frequently.
3. Hybrid: We can adopt a hybrid approach. We can move all the users who have a high number of
follows to a pull-based model and only push data to those users who have a few hundred (or thousand)
follows. Another approach could be that the server pushes updates to all the users not more than a
certain frequency, letting users with a lot of follows/updates to regularly pull data.
For a detailed discussion about News Feed generation, take a look at Designing Facebook’s Newsfeed.
12. News Feed Creation with Sharded Data
One of the most important requirement to create the News Feed for any given user is to fetch the latest
photos from all people the user follows. For this, we need to have a mechanism to sort photos on their
time of creation. To efficiently do this, we can make photo creation time part of the PhotoID. As we will
have a primary index on PhotoID, it will be quite quick to find the latest PhotoIDs.
Stuck? Get help on   
DISCUSS
We can use epoch time for this. Let’s say our PhotoID will have two parts; the first part will be
representing epoch time and the second part will be an auto-incrementing sequence. So to make a new
PhotoID, we can take the current epoch time and append an auto-incrementing ID from our keygenerating DB. We can figure out shard number from this PhotoID ( PhotoID % 10) and store the
photo there.
What could be the size of our PhotoID ? Let’s say our epoch time starts today, how many bits we
would need to store the number of seconds for next 50 years?
86400 sec/day * 365 (days a year) * 50 (years) => 1.6 billion seconds
We would need 31 bits to store this number. Since on the average, we are expecting 23 new photos per
second; we can allocate 9 bits to store auto incremented sequence. So every second we can store (2^9
=> 512) new photos. We can reset our auto incrementing sequence every second.
We will discuss more details about this technique under ‘Data Sharding’ in Designing Twitter.
13. Cache and Load balancing
Our service would need a massive-scale photo delivery system to serve the globally distributed users.
Our service should push its content closer to the user using a large number of geographically
distributed photo cache servers and use CDNs (for details see Caching).
We can introduce a cache for metadata servers to cache hot database rows. We can use Memcache to
cache the data and Application servers before hitting database can quickly check if the cache has
desired rows. Least Recently Used (LRU) can be a reasonable cache eviction policy for our system.
Under this policy, we discard the least recently viewed row first.
How can we build more intelligent cache? If we go with 80-20 rule, i.e., 20% of daily read
volume for photos is generating 80% of traffic which means that certain photos are so popular that the
majority of people read them. This dictates that we can try caching 20% of daily read volume of photos
and metadata.
←    Back
Designing Pastebin
Next    →
Designing Dropbox
Completed
Send feedback
145 Recommendations

