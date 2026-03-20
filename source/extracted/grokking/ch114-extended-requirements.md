# 13. Extended Requirements

> Source: System Design - Grokking (Notes), Chapter 114, Pages 29-29

## Key Concepts

- Stuck? Get help on   
DISCUSS
3. Average latency that is seen by the user to refresh timeline.
By monitoring these counters, we will realize if we need more replication, load balancing, or caching.
13

## Content

Stuck? Get help on   
DISCUSS
3. Average latency that is seen by the user to refresh timeline.
By monitoring these counters, we will realize if we need more replication, load balancing, or caching.
13. Extended Requirements
How do we serve feeds? Get all the latest tweets from the people someone follows and merge/sort
them by time. Use pagination to fetch/show tweets. Only fetch top N tweets from all the people
someone follows. This N will depend on the client’s Viewport, since on a mobile we show fewer tweets
compared to a Web client. We can also cache next top tweets to speed things up.
Alternately, we can pre-generate the feed to improve efficiency; for details please see ‘Ranking and
timeline generation’ under Designing Instagram.
Retweet: With each Tweet object in the database, we can store the ID of the original Tweet and not
store any contents on this retweet object.
Trending Topics: We can cache most frequently occurring hashtags or search queries in the last N
seconds and keep updating them after every M seconds. We can rank trending topics based on the
frequency of tweets or search queries or retweets or likes. We can give more weight to topics which are
shown to more people.
Who to follow? How to give suggestions?  This feature will improve user engagement. We can
suggest friends of people someone follows. We can go two or three levels down to find famous people
for the suggestions. We can give preference to people with more followers.
As only a few suggestions can be made at any time, use Machine Learning (ML) to shuffle and reprioritize. ML signals could include people with recently increased follow-ship, common followers if
the other person is following this user, common location or interests, etc.
Moments: Get top news for different websites for past 1 or 2 hours, figure out related tweets,
prioritize them, categorize them (news, support, financial, entertainment, etc.) using ML – supervised
learning or Clustering. Then we can show these articles as trending topics in Moments.
Search: Search involves Indexing, Ranking, and Retrieval of tweets. A similar solution is discussed in
our next problem Design Twitter Search.
←    Back
Designing Faceboo…
Next    →
Designing Youtube…
Completed
Send feedback
41 Recommendations

