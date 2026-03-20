# 6. Detailed Component Design

> Source: System Design - Grokking (Notes), Chapter 160, Pages 43-43

## Key Concepts

- Designing Twitter Search
Twitter is one of the largest social networking service where users can share photos, news, and text-based
messages. In this chapter, we will design a service that can store a

## Content

Designing Twitter Search
Twitter is one of the largest social networking service where users can share photos, news, and text-based
messages. In this chapter, we will design a service that can store and search user tweets.
Similar Problems: Tweet search.
Difficulty Level: Medium
1. What is Twitter Search?
#
Twitter users can update their status whenever they like. Each status (called tweet) consists of plain
text and our goal is to design a system that allows searching over all the user tweets.
2. Requirements and Goals of the System
#
Let’s assume Twitter has 1.5 billion total users with 800 million daily active users.
On average Twitter gets 400 million tweets every day.
The average size of a tweet is 300 bytes.
Let’s assume there will be 500M searches every day.
The search query will consist of multiple words combined with AND/OR.
We need to design a system that can efficiently store and query tweets.
3. Capacity Estimation and Constraints
#
Storage Capacity: Since we have 400 million new tweets every day and each tweet on average is 300
bytes, the total storage we need, will be:
400M * 300 => 120GB/day
Total storage per second:
120GB / 24hours / 3600sec ~= 1.38MB/second
4. System APIs
#
We can have SOAP or REST APIs to expose the functionality of our service; following could be the
definition of the search API:
search(api_dev_key, search_terms, maximum_results_to_return, sort, page_token)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
search_terms (string): A string containing the search terms.
maximum_results_to_return (number): Number of tweets to return.
sort (number): Optional sort mode: Latest first (0 - default), Best matched (1), Most liked (2).
page_token (string): This token will specify a page in the result set that should be returned.
Returns: (JSON)
A JSON containing information about a list of tweets matching the search query. Each result entry can
have the user ID & name, tweet text, tweet ID, creation time, number of likes, etc.
5. High Level Design
#
At the high level, we need to store all the statues in a database and also build an index that can keep
track of which word appears in which tweet. This index will help us quickly find tweets that users are
trying to search.
High level design for Twitter search
6. Detailed Component Design
#
1. Storage: We need to store 120GB of new data every day. Given this huge amount of data, we need
to come up with a data partitioning scheme that will be efficiently distributing the data onto multiple
servers. If we plan for next five years, we will need the following storage:
120GB * 365days * 5years ~= 200TB
If we never want to be more than 80% full at any time, we approximately will need 250TB of total
storage. Let’s assume that we want to keep an extra copy of all tweets for fault tolerance; then, our total
storage requirement will be 500TB. If we assume a modern server can store up to 4TB of data, we
would need 125 such servers to hold all of the required data for the next five years.
Let’s start with a simplistic design where we store the tweets in a MySQL database. We can assume that
we store the tweets in a table having two columns, TweetID and TweetText. Let’s assume we partition
our data based on TweetID. If our TweetIDs are unique system-wide, we can define a hash function
h
h
h
bj

