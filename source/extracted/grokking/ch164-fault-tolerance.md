# 7. Fault Tolerance

> Source: System Design - Grokking (Notes), Chapter 164, Pages 44-44

## Key Concepts

- that can map a TweetID to a storage server where we can store that tweet object.
How can we create system-wide unique TweetIDs? If we are getting 400M new tweets each
day, then how many tweet objects 

## Content

that can map a TweetID to a storage server where we can store that tweet object.
How can we create system-wide unique TweetIDs? If we are getting 400M new tweets each
day, then how many tweet objects we can expect in five years?
400M * 365 days * 5 years => 730 billion
This means we would need a five bytes number to identify TweetIDs uniquely. Let’s assume we have a
service that can generate a unique TweetID whenever we need to store an object (The TweetID
discussed here will be similar to TweetID discussed in Designing Twitter). We can feed the TweetID to
our hash function to find the storage server and store our tweet object there.
2. Index: What should our index look like? Since our tweet queries will consist of words, let’s build
the index that can tell us which word comes in which tweet object. Let’s first estimate how big our
index will be. If we want to build an index for all the English words and some famous nouns like people
names, city names, etc., and if we assume that we have around 300K English words and 200K nouns,
then we will have 500k total words in our index. Let’s assume that the average length of a word is five
characters. If we are keeping our index in memory, we need 2.5MB of memory to store all the words:
500K * 5 => 2.5 MB
Let’s assume that we want to keep the index in memory for all the tweets from only past two years.
Since we will be getting 730B tweets in 5 years, this will give us 292B tweets in two years. Given that
each TweetID will be 5 bytes, how much memory will we need to store all the TweetIDs?
292B * 5 => 1460 GB
So our index would be like a big distributed hash table, where ‘key’ would be the word and ‘value’ will
be a list of TweetIDs of all those tweets which contain that word. Assuming on average we have 40
words in each tweet and since we will not be indexing prepositions and other small words like ‘the’,
‘an’, ‘and’ etc., let’s assume we will have around 15 words in each tweet that need to be indexed. This
means each TweetID will be stored 15 times in our index. So total memory we will need to store our
index:
(1460 * 15) + 2.5MB ~= 21 TB
Assuming a high-end server has 144GB of memory, we would need 152 such servers to hold our index.
We can partition our data based on two criteria:
Sharding based on Words: While building our index, we will iterate through all the words of a
tweet and calculate the hash of each word to find the server where it would be indexed. To find all
tweets containing a specific word we have to query only the server which contains this word.
We have a couple of issues with this approach:
1. What if a word becomes hot? Then there will be a lot of queries on the server holding that word.
This high load will affect the performance of our service.
2. Over time, some words can end up storing a lot of TweetIDs compared to others, therefore,
i
i i
if
di
ib
i
f
d
hil
i
i
i
i k
maintaining a uniform distribution of words while tweets are growing is quite tricky.
To recover from these situations we either have to repartition our data or use Consistent Hashing.
Sharding based on the tweet object:  While storing, we will pass the TweetID to our hash function
to find the server and index all the words of the tweet on that server. While querying for a particular
word, we have to query all the servers, and each server will return a set of TweetIDs. A centralized
server will aggregate these results to return them to the user.
Detailed component design
7. Fault Tolerance
#
What will happen when an index server dies? We can have a secondary replica of each server and if the
primary server dies it can take control after the failover. Both primary and secondary servers will have
the same copy of the index.
What if both primary and secondary servers die at the same time? We have to allocate a new server and
rebuild the same index on it. How can we do that? We don’t know what words/tweets were kept on this
server. If we were using ‘Sharding based on the tweet object’, the brute-force solution would be to
iterate through the whole database and filter TweetIDs using our hash function to figure out all the
required tweets that would be stored on this server. This would be inefficient and also during the time
when the server was being rebuilt we would not be able to serve any query from it, thus missing some
tweets that should have been seen by the user.
How can we efficiently retrieve a mapping between tweets and the index server? We have to build a
reverse index that will map all the TweetID to their index server. Our Index-Builder server can hold
this information. We will need to build a Hashtable where the ‘key’ will be the index server number and
the ‘value’ will be a HashSet containing all the TweetIDs being kept at that index server. Notice that we
are keeping all the TweetIDs in a HashSet; this will enable us to add/remove tweets from our index
quickly. So now, whenever an index server has to rebuild itself, it can simply ask the Index-Builder
server for all the tweets it needs to store and then fetch those tweets to build the index. This approach
will surely be fast. We should also have a replica of the Index-Builder server for fault tolerance.

