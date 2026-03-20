# 5. High Level System Design

> Source: System Design - Grokking (Notes), Chapter 106, Pages 26-26

## Key Concepts

- 3. Capacity Estimation and Constraints
Let’s assume we have one billion total users with 200 million daily active users (DAU). Also assume we
have 100 million new tweets every day and on average each 

## Content

3. Capacity Estimation and Constraints
Let’s assume we have one billion total users with 200 million daily active users (DAU). Also assume we
have 100 million new tweets every day and on average each user follows 200 people.
How many favorites per day? If, on average, each user favorites five tweets per day we will have:
200M users * 5 favorites => 1B favorites
How many total tweet-views will our system generate?  Let’s assume on average a user visits
their timeline two times a day and visits five other people’s pages. On each page if a user sees 20
tweets, then our system will generate 28B/day total tweet-views:
200M DAU * ((2 + 5) * 20 tweets) => 28B/day
Storage Estimates Let’s say each tweet has 140 characters and we need two bytes to store a
character without compression. Let’s assume we need 30 bytes to store metadata with each tweet (like
ID, timestamp, user ID, etc.). Total storage we would need:
100M * (280 + 30) bytes => 30GB/day
What would our storage needs be for five years? How much storage we would need for users’ data,
follows, favorites? We will leave this for the exercise.
Not all tweets will have media, let’s assume that on average every fifth tweet has a photo and every
tenth has a video. Let’s also assume on average a photo is 200KB and a video is 2MB. This will lead us
to have 24TB of new media every day.
(100M/5 photos * 200KB) + (100M/10 videos * 2MB) ~= 24TB/day
Bandwidth Estimates Since total ingress is 24TB per day, this would translate into 290MB/sec.
Remember that we have 28B tweet views per day. We must show the photo of every tweet (if it has a
photo), but let’s assume that the users watch every 3rd video they see in their timeline. So, total egress
will be:
(28B * 280 bytes) / 86400s of text => 93MB/s 
+ (28B/5 * 200KB ) / 86400s of photos => 13GB/S 
+ (28B/10/3 * 2MB ) / 86400s of Videos => 22GB/s
Total ~= 35GB/s
4. System APIs
��      Once we've finalized the requirements, it's always a good idea to define the
system APIs. This should explicitly state what is expected from the system.
We can have SOAP or REST APIs to expose the functionality of our service. Following could be the
definition of the API for posting a new tweet:
tweet(api_dev_key, tweet_data, tweet_location, user_location, media_ids)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
tweet_data (string): The text of the tweet, typically up to 140 characters.
tweet_location (string): Optional location (longitude, latitude) this Tweet refers to.
user_location (string): Optional location (longitude, latitude) of the user adding the tweet.
media_ids (number[]): Optional list of media_ids to be associated with the Tweet. (all the media
photo, video, etc. need to be uploaded separately).
Returns: (string)
A successful post will return the URL to access that tweet. Otherwise, an appropriate HTTP error is
returned.
5. High Level System Design
We need a system that can efficiently store all the new tweets, 100M/86400s => 1150 tweets per
second and read 28B/86400s => 325K tweets per second. It is clear from the requirements that this
will be a read-heavy system.
At a high level, we need multiple application servers to serve all these requests with load balancers in
front of them for traffic distributions. On the backend, we need an efficient database that can store all
the new tweets and can support a huge number of reads. We also need some file storage to store photos
and videos.
Although our expected daily write load is 100 million and read load is 28 billion tweets. This means on
average our system will receive around 1160 new tweets and 325K read requests per second. This
traffic will be distributed unevenly throughout the day, though, at peak time we should expect at least a
few thousand write requests and around 1M read requests per second. We should keep this in mind
while designing the architecture of our system.

