# Summary

> Source: System Design - Grokking (Notes), Chapter 9, Pages 2-2

## Key Concepts

- these scenarios. On the backend, we need an efficient database that can store all the tweets and can
support a huge number of reads. We will also need a distributed file storage system for storing pho

## Content

these scenarios. On the backend, we need an efficient database that can store all the tweets and can
support a huge number of reads. We will also need a distributed file storage system for storing photos
and videos.
Step 6: Detailed design
Dig deeper into two or three major components; interviewer’s feedback should always guide us to what
parts of the system need further discussion. We should be able to present different approaches, their
pros and cons, and explain why we will prefer one approach on the other. Remember there is no single
answer; the only important thing is to consider tradeoffs between different options while keeping
system constraints in mind.
Since we will be storing a massive amount of data, how should we partition our data to distribute
it to multiple databases? Should we try to store all the data of a user on the same database? What
issue could it cause?
How will we handle hot users who tweet a lot or follow lots of people?
Since users’ timeline will contain the most recent (and relevant) tweets, should we try to store our
data in such a way that is optimized for scanning the latest tweets?
How much and at which layer should we introduce cache to speed things up?
What components need better load balancing?
Step 7: Identifying and resolving bottlenecks
Try to discuss as many bottlenecks as possible and different approaches to mitigate them.
Is there any single point of failure in our system? What are we doing to mitigate it?
Do we have enough replicas of the data so that if we lose a few servers, we can still serve our
users?
Similarly, do we have enough copies of different services running such that a few failures will not
cause total system shutdown?
How are we monitoring the performance of our service? Do we get alerts whenever critical
Stuck? Get help on   
DISCUSS
components fail or their performance degrades?
Summary
In short, preparation and being organized during the interview are the keys to be successful in system
design interviews. The steps mentioned above should guide you to remain on track and cover all the
different aspects while designing a system.
Let’s apply the above guidelines to design a few systems that are asked in SDIs.
Next    →
Designing a URL S…
Completed
Send feedback
122 Recommendations

