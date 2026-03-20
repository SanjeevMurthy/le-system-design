# 7. Detailed Component Design

> Source: System Design - Grokking (Notes), Chapter 188, Pages 51-51

## Key Concepts

- Feed publishing: Whenever Jane loads her newsfeed page, she has to request and pull feed items
from the server. When she reaches the end of her current feed, she can pull more data from the server.
Fo

## Content

Feed publishing: Whenever Jane loads her newsfeed page, she has to request and pull feed items
from the server. When she reaches the end of her current feed, she can pull more data from the server.
For newer items either the server can notify Jane and then she can pull, or the server can push, these
new posts. We will discuss these options in detail later.
At a high level, we will need following components in our Newsfeed service:
1. Web servers: To maintain a connection with the user. This connection will be used to transfer
data between the user and the server.
2. Application server: To execute the workflows of storing new posts in the database servers. We
will also need some application servers to retrieve and to push the newsfeed to the end user.
3. Metadata database and cache: To store the metadata about Users, Pages, and Groups.
4. Posts database and cache: To store metadata about posts and their contents.
5. Video and photo storage, and cache: Blob storage, to store all the media included in the
posts.
6. Newsfeed generation service: To gather and rank all the relevant posts for a user to generate
newsfeed and store in the cache. This service will also receive live updates and will add these
newer feed items to any user’s timeline.
7. Feed notification service: To notify the user that there are newer items available for their
newsfeed.
Following is the high-level architecture diagram of our system. User B and C are following User A.
Facebook Newsfeed Architecture
7. Detailed Component Design
Let’s discuss different components of our system in detail.
a. Feed generation
Let’s take the simple case of the newsfeed generation service fetching most recent posts from all the
users and entities that Jane follows; the query would look like this:
(SELECT FeedItemID FROM FeedItem WHERE UserID in (
    SELECT EntityOrFriendID FROM UserFollow WHERE UserID = <current_user_id> and t
ype = 0(user))
)
UNION
(SELECT FeedItemID FROM FeedItem WHERE EntityID in (
    SELECT EntityOrFriendID FROM UserFollow WHERE UserID = <current_user_id> and t
ype = 1(entity))
)
ORDER BY CreationDate DESC 
LIMIT 100
Here are issues with this design for the feed generation service:
1. Crazy slow for users with a lot of friends/follows as we have to perform sorting/merging/ranking
of a huge number of posts.
2. We generate the timeline when a user loads their page. This would be quite slow and have a high
latency.
3. For live updates, each status update will result in feed updates for all followers. This could result
in high backlogs in our Newsfeed Generation Service.
4. For live updates, the server pushing (or notifying about) newer posts to users could lead to very
heavy loads, especially for people or pages that have a lot of followers. To improve the efficiency,
we can pre-generate the timeline and store it in a memory.
Offline generation for newsfeed: We can have dedicated servers that are continuously generating
users’ newsfeed and storing them in memory. So, whenever a user requests for the new posts for their
feed, we can simply serve it from the pre-generated, stored location. Using this scheme, user’s
newsfeed is not compiled on load, but rather on a regular basis and returned to users whenever they
request for it.
Whenever these servers need to generate the feed for a user, they will first query to see what was the
last time the feed was generated for that user. Then, new feed data would be generated from that time
onwards. We can store this data in a hash table where the “key” would be UserID and “value” would be
a STRUCT like this:
Struct {
    LinkedHashMap<FeedItemID, FeedItem> feedItems;
    DateTime lastGenerated;
}
We can store FeedItemIDs in a data structure similar to Linked HashMap or TreeMap, which can allow
us to not only jump to any feed item but also iterate through the map easily. Whenever users want to
fetch more feed items, they can send the last FeedItemID they currently see in their newsfeed, we can

