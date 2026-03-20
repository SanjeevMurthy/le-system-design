# 3. Capacity Estimation and Constraints

> Source: System Design - Grokking (Notes), Chapter 183, Pages 49-49

## Key Concepts

- Stuck? Get help on   
DISCUSS
that cause a crawler to crawl indefinitely. Some crawler traps are unintentional. For example, a
symbolic link within a file system can create a cycle. Other crawler trap

## Content

Stuck? Get help on   
DISCUSS
that cause a crawler to crawl indefinitely. Some crawler traps are unintentional. For example, a
symbolic link within a file system can create a cycle. Other crawler traps are introduced intentionally.
For example, people have written traps that dynamically generate an infinite Web of documents. The
motivations behind such traps vary. Anti-spam traps are designed to catch crawlers used by spammers
looking for email addresses, while other sites use traps to catch search engine crawlers to boost their
search ratings.
←    Back
Designing Twitter S…
Next    →
Designing Faceboo…
Completed
Send feedback
40 Recommendations
Designing Facebook’s Newsfeed
Let's design Facebook's Newsfeed, which would contain posts, photos, videos, and status updates from all
the people and pages a user follows.
Similar Services: Twitter Newsfeed, Instagram Newsfeed, Quora Newsfeed
Difficulty Level: Hard
1. What is Facebook’s newsfeed?
A Newsfeed is the constantly updating list of stories in the middle of Facebook’s homepage. It includes
status updates, photos, videos, links, app activity, and ‘likes’ from people, pages, and groups that a user
follows on Facebook. In other words, it is a compilation of a complete scrollable version of your
friends’ and your life story from photos, videos, locations, status updates, and other activities.
For any social media site you design - Twitter, Instagram, or Facebook - you will need some newsfeed
system to display updates from friends and followers.
2. Requirements and Goals of the System
Let’s design a newsfeed for Facebook with the following requirements:
Functional requirements:
1. Newsfeed will be generated based on the posts from the people, pages, and groups that a user
follows.
2. A user may have many friends and follow a large number of pages/groups.
3. Feeds may contain images, videos, or just text.
4. Our service should support appending new posts as they arrive to the newsfeed for all active
users.
Non-functional requirements:
1. Our system should be able to generate any user’s newsfeed in real-time - maximum latency seen
by the end user would be 2s.
2. A post shouldn’t take more than 5s to make it to a user’s feed assuming a new newsfeed request
comes in.
3. Capacity Estimation and Constraints
Let’s assume on average a user has 300 friends and follows 200 pages.
Traffic estimates: Let’s assume 300M daily active users with each user fetching their timeline an
average of five times a day. This will result in 1.5B newsfeed requests per day or approximately 17,500

## Examples & Scenarios

- that cause a crawler to crawl indefinitely. Some crawler traps are unintentional. For example, a
symbolic link within a file system can create a cycle. Other crawler traps are introduced intentionally.
For example, people have written traps that dynamically generate an infinite Web of documents. The
motivations behind such traps vary. Anti-spam traps are designed to catch crawlers used by spammers
looking for email addresses, while other sites use traps to catch search engine crawlers to boost their
search ratings.
←    Back
Designing Twitter S…
Next    →
Designing Faceboo…

