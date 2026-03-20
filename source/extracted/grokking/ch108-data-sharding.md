# 7. Data Sharding

> Source: System Design - Grokking (Notes), Chapter 108, Pages 27-27

## Key Concepts

- 6. Database Schema
We need to store data about users, their tweets, their favorite tweets, and people they follow.
Tweet
TweetID: int
PK
UserID: int
Content: varchar(140)
TweetLatitude: int
TweetLongi

## Content

6. Database Schema
We need to store data about users, their tweets, their favorite tweets, and people they follow.
Tweet
TweetID: int
PK
UserID: int
Content: varchar(140)
TweetLatitude: int
TweetLongitude: int
UserLatitude: int
UserLongitude: int
CreationDate: datetime
NumFavorites: int
User
UserID: int
PK
Name: varchar(20)
Email: varchar(32)
DateOfBirth: datetime
CreationDate: datetime
LastLogin: datatime
UserFollow
UserID1: int
UserID2: int
PK
Favorite
TweetID:
int
UserID: int
PK
CreationDate: datetime
For choosing between SQL and NoSQL databases to store the above schema, please see ‘Database
schema’ under Designing Instagram.
7. Data Sharding
Since we have a huge number of new tweets every day and our read load is extremely high too, we need
to distribute our data onto multiple machines such that we can read/write it efficiently. We have many
options to shard our data; let’s go through them one by one:
Sharding based on UserID: We can try storing all the data of a user on one server. While storing,
we can pass the UserID to our hash function that will map the user to a database server where we will
store all of the user’s tweets, favorites, follows, etc. While querying for tweets/follows/favorites of a
user, we can ask our hash function where can we find the data of a user and then read it from there.
This approach has a couple of issues:
1. What if a user becomes hot? There could be a lot of queries on the server holding the user. This
high load will affect the performance of our service.
2. Over time some users can end up storing a lot of tweets or having a lot of follows compared to
others. Maintaining a uniform distribution of growing user data is quite difficult.
To recover from these situations either we have to repartition/redistribute our data or use consistent
hashing.
Sharding based on TweetID: Our hash function will map each TweetID to a random server where
we will store that Tweet. To search for tweets, we have to query all servers, and each server will return a
set of tweets. A centralized server will aggregate these results to return them to the user. Let’s look into
timeline generation example; here are the number of steps our system has to perform to generate a
user’s timeline:
1. Our application (app) server will find all the people the user follows.
2. App server will send the query to all database servers to find tweets from these people.
3. Each database server will find the tweets for each user, sort them by recency and return the top
tweets.
4. App server will merge all the results and sort them again to return the top results to the user.
This approach solves the problem of hot users, but, in contrast to sharding by UserID, we have to query
all database partitions to find tweets of a user, which can result in higher latencies.
We can further improve our performance by introducing cache to store hot tweets in front of the
database servers.
Sharding based on Tweet creation time:  Storing tweets based on creation time will give us the
advantage of fetching all the top tweets quickly and we only have to query a very small set of servers.
The problem here is that the traffic load will not be distributed, e.g., while writing, all new tweets will
be going to one server and the remaining servers will be sitting idle. Similarly, while reading, the server
holding the latest data will have a very high load as compared to servers holding old data.
What if we can combine sharding by TweetID and Tweet creation time?  If we don’t store
tweet creation time separately and use TweetID to reflect that, we can get benefits of both the
approaches. This way it will be quite quick to find the latest Tweets. For this, we must make each
TweetID universally unique in our system and each TweetID should contain a timestamp too.
We can use epoch time for this. Let’s say our TweetID will have two parts: the first part will be
representing epoch seconds and the second part will be an auto-incrementing sequence. So, to make a
new TweetID, we can take the current epoch time and append an auto-incrementing number to it. We
can figure out the shard number from this TweetID and store it there.
What could be the size of our TweetID? Let’s say our epoch time starts today, how many bits we would
need to store the number of seconds for the next 50 years?
86400 sec/day * 365 (days a year) * 50 (years) => 1.6B
We would need 31 bits to store this number. Since on average we are expecting 1150 new tweets per
second, we can allocate 17 bits to store auto incremented sequence; this will make our TweetID 48 bits
long. So, every second we can store (2^17 => 130K) new tweets. We can reset our auto incrementing
sequence every second. For fault tolerance and better performance, we can have two database servers
to generate auto-incrementing keys for us, one generating even numbered keys and the other
generating odd numbered keys.
If we assume our current epoch seconds are “1483228800,” our TweetID will look like this:
1483228800 000001
1483228800 000002
1483228800 000003

## Examples & Scenarios

- The problem here is that the traffic load will not be distributed, e.g., while writing, all new tweets will
be going to one server and the remaining servers will be sitting idle. Similarly, while reading, the server
holding the latest data will have a very high load as compared to servers holding old data.
What if we can combine sharding by TweetID and Tweet creation time?  If we don’t store
tweet creation time separately and use TweetID to reflect that, we can get benefits of both the
approaches. This way it will be quite quick to find the latest Tweets. For this, we must make each
TweetID universally unique in our system and each TweetID should contain a timestamp too.
We can use epoch time for this. Let’s say our TweetID will have two parts: the first part will be
representing epoch seconds and the second part will be an auto-incrementing sequence. So, to make a
new TweetID, we can take the current epoch time and append an auto-incrementing number to it. We

## Tables & Comparisons

| Tweet |  | User UserFollow Favorite
PK UserID: int PK U Us se er rI ID D1 2: : i in nt t PK T inw teetID:
Name: varchar(20) UserID: int
CreationDate: datetime
Email: varchar(32)
DateOfBirth: datetime
CreationDate: datetime
LastLogin: datatime | Favorite |  |
| --- | --- | --- | --- | --- |
| PK | TweetID: int |  | PK | TweetID:
int |
|  | UserID: int
Content: varchar(140)
TweetLatitude: int
TweetLongitude: int
UserLatitude: int
UserLongitude: int
CreationDate: datetime
NumFavorites: int |  |  |  |
|  |  |  |  | UserID: int
CreationDate: datetime |

| User |  |
| --- | --- |
| PK | UserID: int |
|  | Name: varchar(20)
Email: varchar(32)
DateOfBirth: datetime
CreationDate: datetime
LastLogin: datatime |

| UserFollow |  |
| --- | --- |
| PK | UserID1: int
UserID2: int |

