# 6. High Level System Design

> Source: System Design - Grokking (Notes), Chapter 187, Pages 50-50

## Key Concepts

- requests per second.
Storage estimates: On average, let’s assume we need to have around 500 posts in every user’s feed
that we want to keep in memory for a quick fetch. Let’s also assume that on avera

## Content

requests per second.
Storage estimates: On average, let’s assume we need to have around 500 posts in every user’s feed
that we want to keep in memory for a quick fetch. Let’s also assume that on average each post would be
1KB in size. This would mean that we need to store roughly 500KB of data per user. To store all this
data for all the active users we would need 150TB of memory. If a server can hold 100GB we would
need around 1500 machines to keep the top 500 posts in memory for all active users.
4. System APIs
��      Once we have finalized the requirements, it’s always a good idea to define
the system APIs. This should explicitly state what is expected from the system.
We can have SOAP or REST APIs to expose the functionality of our service. The following could be the
definition of the API for getting the newsfeed:
getUserFeed(api_dev_key, user_id, since_id, count, max_id, exclude_replies)
Parameters:
api_dev_key (string): The API developer key of a registered can be used to, among other things,
throttle users based on their allocated quota.
user_id (number): The ID of the user for whom the system will generate the newsfeed.
since_id (number): Optional; returns results with an ID higher than (that is, more recent than) the
specified ID.
count (number): Optional; specifies the number of feed items to try and retrieve up to a maximum
of 200 per distinct request.
max_id (number): Optional; returns results with an ID less than (that is, older than) or equal to the
specified ID.
exclude_replies(boolean): Optional; this parameter will prevent replies from appearing in the
returned timeline.
Returns: (JSON) Returns a JSON object containing a list of feed items.
5. Database Design
There are three primary objects: User, Entity (e.g. page, group, etc.), and FeedItem (or Post). Here are
some observations about the relationships between these entities:
A User can follow other entities and can become friends with other users.
Both users and entities can post FeedItems which can contain text, images, or videos.
Each FeedItem will have a UserID which will point to the User who created it. For simplicity, let’s
assume that only users can create feed items, although, on Facebook Pages can post feed item too.
Each FeedItem can optionally have an EntityID pointing to the page or the group where that post
was created.
If
i
l ti
l d t b
ld
d t
d l t
l ti
U
E tit
l ti
d
If we are using a relational database, we would need to model two relations: User-Entity relation and
FeedItem-Media relation. Since each user can be friends with many people and follow a lot of entities,
we can store this relation in a separate table. The “Type” column in “UserFollow” identifies if the entity
being followed is a User or Entity. Similarly, we can have a table for FeedMedia relation.
6. High Level System Design
At a high level this problem can be divided into two parts:
Feed generation: Newsfeed is generated from the posts (or feed items) of users and entities (pages
and groups) that a user follows. So, whenever our system receives a request to generate the feed for a
user (say Jane), we will perform the following steps:
1. Retrieve IDs of all users and entities that Jane follows.
2. Retrieve latest, most popular and relevant posts for those IDs. These are the potential posts that
we can show in Jane’s newsfeed.
3. Rank these posts based on the relevance to Jane. This represents Jane’s current feed.
4. Store this feed in the cache and return top posts (say 20) to be rendered on Jane’s feed.
5. On the front-end, when Jane reaches the end of her current feed, she can fetch the next 20 posts
from the server and so on.
One thing to notice here is that we generated the feed once and stored it in the cache. What about new
incoming posts from people that Jane follows? If Jane is online, we should have a mechanism to rank
and add those new posts to her feed. We can periodically (say every five minutes) perform the above
steps to rank and add the newer posts to her feed. Jane can then be notified that there are newer items
in her feed that she can fetch.

