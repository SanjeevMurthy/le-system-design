# 9. Data Partitioning

> Source: System Design - Grokking (Notes), Chapter 190, Pages 52-52

## Key Concepts

- then jump to that FeedItemID in our hash-map and return next batch/page of feed items from there.
How many feed items should we store in memory for a user’s feed?  Initially, we can decide
to store 50

## Content

then jump to that FeedItemID in our hash-map and return next batch/page of feed items from there.
How many feed items should we store in memory for a user’s feed?  Initially, we can decide
to store 500 feed items per user, but this number can be adjusted later based on the usage pattern. For
example, if we assume that one page of a user’s feed has 20 posts and most of the users never browse
more than ten pages of their feed, we can decide to store only 200 posts per user. For any user who
wants to see more posts (more than what is stored in memory), we can always query backend servers.
Should we generate (and keep in memory) newsfeeds for all users?  There will be a lot of
users that don’t login frequently. Here are a few things we can do to handle this; 1) a more
straightforward approach could be, to use a LRU based cache that can remove users from memory that
haven’t accessed their newsfeed for a long time 2) a smarter solution can figure out the login pattern of
users to pre-generate their newsfeed, e.g., at what time of the day a user is active and which days of the
week does a user access their newsfeed? etc.
Let’s now discuss some solutions to our “live updates” problems in the following section.
b. Feed publishing
The process of pushing a post to all the followers is called a fanout. By analogy, the push approach is
called fanout-on-write, while the pull approach is called fanout-on-load. Let’s discuss different options
for publishing feed data to users.
1. “Pull” model or Fan-out-on-load: This method involves keeping all the recent feed data in
memory so that users can pull it from the server whenever they need it. Clients can pull the feed
data on a regular basis or manually whenever they need it. Possible problems with this approach
are a) New data might not be shown to the users until they issue a pull request, b) It’s hard to find
the right pull cadence, as most of the time pull requests will result in an empty response if there is
no new data, causing waste of resources.
2. “Push” model or Fan-out-on-write: For a push system, once a user has published a post, we
can immediately push this post to all the followers. The advantage is that when fetching feed you
don’t need to go through your friend’s list and get feeds for each of them. It significantly reduces
read operations. To efficiently handle this, users have to maintain a Long Poll request with the
server for receiving the updates. A possible problem with this approach is that when a user has
millions of followers (a celebrity-user) the server has to push updates to a lot of people.
3. Hybrid: An alternate method to handle feed data could be to use a hybrid approach, i.e., to do a
combination of fan-out-on-write and fan-out-on-load. Specifically, we can stop pushing posts
from users with a high number of followers (a celebrity user) and only push data for those users
who have a few hundred (or thousand) followers. For celebrity users, we can let the followers pull
the updates. Since the push operation can be extremely costly for users who have a lot of friends
or followers, by disabling fanout for them, we can save a huge number of resources. Another
alternate approach could be that, once a user publishes a post, we can limit the fanout to only her
online friends. Also, to get benefits from both the approaches, a combination of ‘push to notify’
and ‘pull for serving’ end users is a great way to go. Purely a push or pull model is less versatile.
How many feed items can we return to the client in each request? We should have a
St
k? G t h l
DISCUSS
How many feed items can we return to the client in each request?  We should have a
maximum limit for the number of items a user can fetch in one request (say 20). But, we should let the
client specify how many feed items they want with each request as the user may like to fetch a different
number of posts depending on the device (mobile vs. desktop).
Should we always notify users if there are new posts available for their newsfeed?  It
could be useful for users to get notified whenever new data is available. However, on mobile devices,
where data usage is relatively expensive, it can consume unnecessary bandwidth. Hence, at least for
mobile devices, we can choose not to push data, instead, let users “Pull to Refresh” to get new posts.
8. Feed Ranking
The most straightforward way to rank posts in a newsfeed is by the creation time of the posts, but
today’s ranking algorithms are doing a lot more than that to ensure “important” posts are ranked
higher. The high-level idea of ranking is first to select key “signals” that make a post important and
then to find out how to combine them to calculate a final ranking score.
More specifically, we can select features that are relevant to the importance of any feed item, e.g.,
number of likes, comments, shares, time of the update, whether the post has images/videos, etc., and
then, a score can be calculated using these features. This is generally enough for a simple ranking
system. A better ranking system can significantly improve itself by constantly evaluating if we are
making progress in user stickiness, retention, ads revenue, etc.
9. Data Partitioning
a. Sharding posts and metadata
Since we have a huge number of new posts every day and our read load is extremely high too, we need
to distribute our data onto multiple machines such that we can read/write it efficiently. For sharding
our databases that are storing posts and their metadata, we can have a similar design as discussed
under Designing Twitter.
b. Sharding feed data
For feed data, which is being stored in memory, we can partition it based on UserID. We can try storing
all the data of a user on one server. When storing, we can pass the UserID to our hash function that will
map the user to a cache server where we will store the user’s feed objects. Also, for any given user, since
we don’t expect to store more than 500 FeedItmeIDs, we will not run into a scenario where feed data
for a user doesn’t fit on a single server. To get the feed of a user, we would always have to query only
one server. For future growth and replication, we must use Consistent Hashing.
←    Back
Designing a Web C…
Next    →
Designing Yelp or …
Completed

## Examples & Scenarios

- users to pre-generate their newsfeed, e.g., at what time of the day a user is active and which days of the
week does a user access their newsfeed? etc.
Let’s now discuss some solutions to our “live updates” problems in the following section.
b. Feed publishing
The process of pushing a post to all the followers is called a fanout. By analogy, the push approach is
called fanout-on-write, while the pull approach is called fanout-on-load. Let’s discuss different options
for publishing feed data to users.
1. “Pull” model or Fan-out-on-load: This method involves keeping all the recent feed data in
memory so that users can pull it from the server whenever they need it. Clients can pull the feed
data on a regular basis or manually whenever they need it. Possible problems with this approach

- More specifically, we can select features that are relevant to the importance of any feed item, e.g.,
number of likes, comments, shares, time of the update, whether the post has images/videos, etc., and
then, a score can be calculated using these features. This is generally enough for a simple ranking
system. A better ranking system can significantly improve itself by constantly evaluating if we are
making progress in user stickiness, retention, ads revenue, etc.
9. Data Partitioning
a. Sharding posts and metadata
Since we have a huge number of new posts every day and our read load is extremely high too, we need
to distribute our data onto multiple machines such that we can read/write it efficiently. For sharding
our databases that are storing posts and their metadata, we can have a similar design as discussed

