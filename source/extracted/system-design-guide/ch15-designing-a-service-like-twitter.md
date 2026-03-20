# Chapter 11: Designing a Service Like Twitter

> Source: System Design Guide for Software Professionals, Chapter 15, Pages 240-270

## Key Concepts

- 11
Designing a Service Like Twitter
In today’s digital landscape, social media platforms have revolutionized communication and
information sharing. Twitter, currently know as X, is a microblogging ser
- Let’s explore the key functional requirements.
Functional requirements
Here are the functional requirements for our system:
User registration and authentication:
Users should be able to create new acc

## Content

11
Designing a Service Like Twitter
In today’s digital landscape, social media platforms have revolutionized communication and
information sharing. Twitter, currently know as X, is a microblogging service allowing users to
share short messages called tweets, has emerged as a global phenomenon with millions of active
users and billions of tweets generated daily. Designing a service like Twitter presents unique
challenges in scalability, reliability, and user experience.
This chapter explores the system design of a Twitter-like service, applying our learnings from
basic system design blocks to create a scalable and efficient platform. We will examine the core
features, non-functional requirements, data models, and scale calculations that form the
foundation of the system. Based on these, we’ll propose a high-level design architecture
leveraging various components, such as load balancers, API gateways, caches, databases, and
storage systems. We’ll also delve into the low-level design of key services, emphasizing
scalability, reliability, and performance throughout.
We will cover the following topics in this chapter:
Functional requirements
Non-functional requirements
Data model
Scale calculations
Designing Tweet Service
Designing User Service
Low-level design –Timeline Service
Designing Search Service
Additional considerations
Low-level design of key components (Tweet Service, User Service, Timeline Service, and Search Service)
Scalability techniques (caching, sharding, and asynchronous processing)
By the end of this chapter, you will have a comprehensive understanding of the principles and
practices involved in designing a scalable and robust social media platform like Twitter.


Let’s explore the key functional requirements.
Functional requirements
Here are the functional requirements for our system:
User registration and authentication:
Users should be able to create new accounts by providing the necessary information, such as username, email,
and password
The system should securely store user credentials and authenticate users upon login
User sessions should be managed efficiently to allow seamless access to the service
Tweeting:
Users should be able to post tweets, which are short messages limited to a specific character count (e.g., 280
characters)
Tweets can contain text, hashtags, mentions of other users, and media attachments such as images or videos
The system should enforce the character limit and handle the storage and retrieval of tweets efficiently
Follow/unfollow:
Users should be able to follow other users to receive their tweets in their timeline
The system should maintain a follow graph that represents the relationships between users
Users should also have the ability to unfollow other users, removing their tweets from the timeline
Timeline:
The timeline is a crucial feature that displays a chronological feed of tweets from the users a person follows
The system should efficiently generate and serve personalized timelines for each user, considering factors such
as tweet timestamps and user preferences
The timeline should support real-time updates, ensuring that users see the latest tweets as they are posted
Searching:
Users should be able to search for tweets and other users based on keywords, hashtags, or usernames
The search functionality should provide relevant and accurate results, considering factors such as relevance,
popularity, and recency
The system should efficiently index and store tweet and user data to enable fast and scalable searching
Retweeting and liking:


Users should have the ability to retweet, which means sharing another user’s tweet with their own followers
The system should handle retweets efficiently, maintaining the original tweet’s metadata and attribution
Users should also be able to like tweets, indicating their appreciation or agreement with the content
Direct messaging:
The service should support direct messaging functionality, allowing users to privately communicate with each
other
Users should be able to send and receive direct messages, which are separate from the public tweet stream
The system should ensure the privacy and security of direct messages, implementing proper access controls and
encryption
These functional requirements provide a comprehensive overview of the core features that a
Twitter-like service should offer. By fulfilling these requirements, the system will enable users to
engage in microblogging, connect with others, and consume relevant content in real-time.
In the next section, we will explore the non-functional requirements that ensure the service
remains scalable, reliable, and performant while meeting the functional requirements discussed
previously.
Non-functional requirements
While functional requirements define what the system should do, non-functional requirements
specify how the system should perform and behave. These requirements are critical to ensuring
that the Twitter-like service remains scalable, available, and reliable under various conditions.
Let’s discuss the key non-functional requirements:
Scalability:
The system should be designed to handle a large number of users and tweets, accommodating growth and peak
traffic loads
Horizontal scalability should be achieved by adding more servers and distributing the load across them
The architecture should allow for easy scaling of individual components, such as Tweet Service or Timeline
Service, independently
Availability:
The service should be highly available, ensuring minimal downtime and quick recovery from failures
Redundancy should be implemented at various levels, including server redundancy, database replication, and
geo-redundancy


The system should be designed to handle server failures, network outages, and data center disasters without
significant impact on user experience
Reliability:
The system should be reliable, ensuring data integrity and consistency across all components
Mechanisms should be in place to prevent data loss, such as regular backups and data replication
Consistency models should be chosen carefully to balance data accuracy and performance, considering factors
such as eventual consistency or strong consistency
Latency:
The service should provide real-time updates and fast response times to ensure a smooth user experience
Latency should be minimized for critical operations, such as posting tweets, viewing timelines, and receiving
notifications
Techniques such as caching, content delivery networks (CDNs), and efficient data retrieval should be
employed to reduce latency
By addressing these non-functional requirements, the Twitter-like service can ensure a reliable,
scalable, and performant user experience. It is essential to consider these requirements
throughout the design process and make architectural decisions that align with these goals.
Let us now learn about the data model that forms the foundation of the Twitter-like service,
defining the entities and relationships necessary to support the functional requirements.
Data model
The data model is a crucial component of the Twitter-like service, as it defines the structure and
relationships of the data entities involved. A well-designed data model ensures efficient storage,
retrieval, and manipulation of data while supporting the functional requirements of the system.
Let’s dive into the key entities and their relationships. Figure 11.1 captures the UML-style class
diagram for the different data models and how they interact with each other.


Figure 11.1: UML-style class diagram for different data models
Figure 11.1’s UML-style class diagram provides a comprehensive visual representation of the
data model for our Twitter-like service. It illustrates the key entities (User, Tweet, Follow, Like,
Retweet, and DirectMessage) along with their attributes and the relationships between them. The
diagram clearly depicts the one-to-many and many-to-many relationships, such as users posting


multiple tweets or following multiple users, offering a clear overview of the system’s data
structure and relationships at a glance.
At a high level, in our system, we need to represent users, their tweets, and their relationships
with other users. Our data models will be designed to speed up the common queries and will
support the uncommon ones. Let’s summarize the different entities and relationships between
them:
The User entity represents the users of the Twitter-like service, storing their profile information such as username, email,
password hash, profile picture, bio, location, and website. Each user is uniquely identified by their user_id.
The Tweet entity represents the tweets posted by users. It contains the tweet content, user ID of the author, creation
timestamp, media URL (if applicable), location, and counts for retweets and likes. tweet_id serves as the primary key.
The Follow entity represents the follow relationships between users. It contains follower_id and followee_id,
indicating which user is following whom. The created_at timestamp captures when the follow relationship was
established.
The Like entity represents the likes on tweets. It contains the user ID of the user who liked the tweet and the tweet ID of
the liked tweet. The created_at timestamp records when the like occurred.
The Retweet entity represents the retweets of tweets. It contains the tweet ID of the original tweet and
retweeted_by_user_id, which is the ID of the user who retweeted the tweet. The created_at timestamp indicates
when the retweet happened.
The Direct Message entity represents private conversations between users. It contains message_id, sender_id,
recipient_id, content, and the created_at timestamp.
By designing the data model with these entities and relationships, the Twitter-like service can
efficiently store and retrieve data related to users, tweets, follows, likes, retweets, and direct
messages. The data model supports the functional requirements and enables the system to handle
the complex interactions between users and their activities.
To build a usable system, it is important to understand the scale at which it will operate. Now,
we will perform scale calculations to estimate the storage, bandwidth, and processing
requirements of the Twitter-like service based on the anticipated user base and usage patterns.
Scale calculations
To design a scalable Twitter-like service, it is essential to estimate the storage, bandwidth, and
processing requirements based on the expected user base and usage patterns. These calculations


help in making informed decisions about the infrastructure and resources needed to support the
service. Let’s perform some scale calculations:
Assumptions:
Total number of users: 100 million
Daily active users: 20 million
Average number of tweets per user per day: 5
Average tweet size: 200 bytes
Average media size per tweet: 1 MB
Percentage of tweets with media: 20%
Retention period for tweets: Five years
Storage requirements:
Tweet storage:
Daily tweet storage: 20 million users × 5 tweets/user/day × 200
bytes/tweet = 20 GB/day
Yearly tweet storage: 20 GB/day × 365 days = 7.3 TB/year
Total tweet storage for five years: 7.3 TB/year × 5 years = 36.5 TB
Media storage:
Daily media storage: 20 million users × 5 tweets/user/day × 20% media tweets × 1
MB/media = 200 TB/day
Yearly media storage: 200 TB/day × 365 days = 73 PB/year
Total media storage for five years: 73 PB/year × 5 years = 365 PB
User storage – assuming 1 MB of storage per user (profile picture, bio, etc.):
Total user storage: 100 million users × 1 MB/user = 100 TB
Total storage: 36.5 TB (tweets) + 365 PB (media) + 100 TB (users) ≈ 365 PB
Bandwidth considerations:
Daily bandwidth for tweet delivery: Assuming an average of 100 followers per user:
Daily tweet deliveries: 20 million users × 5 tweets/user/day × 100 followers/user =
10 billion tweet deliveries/day
Daily bandwidth: 10 billion tweet deliveries/day × 200 bytes/tweet = 2 TB/day


Daily bandwidth for media delivery:
Daily media deliveries: 20 million users × 5 tweets/user/day × 20% media tweets ×
100 followers/user = 2 billion media deliveries/day
Daily bandwidth: 2 billion media deliveries/day × 1 MB/media = 2 PB/day
Total daily bandwidth: 2 TB (tweets) + 2 PB (media) ≈ 2 PB/day
Processing requirements:
Peak tweets per second: 20 million users × 5 tweets/user/day ÷ 86400 seconds/day ≈
1,200 tweets/second
Peak media uploads per second: 1,200 tweets/second × 20% media tweets ≈ 240 media
uploads/second
Fanout requests for timeline generation: 100 followers/user × 1200 tweets/second ≈
120,000 requests/second
Cache sizing:
Assuming 80% of the daily tweet views can be served from the cache
Daily tweet views: 20 million users × 100 timeline views/user/day = 2 billion tweet
views/day
Cache size: 2 billion tweet views/day × 80% cache hit rate × 200 bytes/tweet ≈
320 GB
These calculations provide a rough estimate of the storage, bandwidth, and processing
requirements for the Twitter-like service. It’s important to note that these numbers can vary
based on the actual usage patterns and growth of the user base. The infrastructure should be
designed to handle peak loads and should be easily scalable to accommodate future growth.
Before we dive into developing services and features, a good step is to get a high-level design in
order so we can understand different modules and how they interact. The subsequent section will
focus on designing various building blocks to create a scalable and efficient system.
Exploring high-level design
Now that we have a clear understanding of the functional and non-functional requirements, as
well as the scale calculations, let’s dive into the high-level design of the Twitter-like service. The
goal is to create an architecture that is scalable, reliable, and efficient in handling the massive


volume of tweets, users, and interactions. Figure 11.2 shows the high-level design of the Twitterlike system, which includes a load balancer, API gateway, microservices such as User Service
and Tweet Service, database tables, the caching layer, Kafka, and an object store. We will
discuss these components at a high level in this section and in the next section do a deep dive
into some of them.


Figure 11.2: High-level system design of Twitter
Figure 11.2 shows different modules and microservices that need to be developed to build a
system like Twitter. These are listed as follows, along with a brief explanation for each:
Client-server architecture: The Twitter-like service will follow a client-server architecture, where clients (such as web
browsers or mobile apps) communicate with the server-side components through APIs. The server-side components will
handle the core functionality, data storage, and processing.
Load balancer: To distribute the incoming traffic evenly across multiple servers, a load balancer will be placed in front of
the server-side components. The load balancer will ensure that requests are efficiently routed to the appropriate servers
based on factors such as server load, request type, and geographic location.
API gateway: An API gateway will act as the entry point for all client requests. It will handle
request routing, authentication, rate limiting, and request/response transformation. The API
gateway will expose well-defined APIs for various functionalities, such as tweeting, following,
liking, and searching.
Microservices architecture
To promote modularity, scalability, and maintainability, the server-side components will be
designed as microservices. Each microservice will be responsible for a specific domain or
functionality. The main microservices in the Twitter-like service will be the following:
Tweet Service:
Handles tweet creation, retrieval, and deletion
Stores tweet data in the database and media files in the object storage
Publishes new tweets to the message queue for processing by other services
User Service:
Manages user registration, authentication, and profile information
Stores user data in the database
Handles the follow/unfollow functionality and maintains the follower-followee relationships
Timeline Service:
Generates and serves user timelines by aggregating tweets from followed users
Consumes new tweets from the message queue and updates user timelines accordingly
Stores timeline data in the cache for fast retrieval


Search Service:
Enables searching for tweets and users based on keywords, hashtags, and other criteria
Indexes tweet and user data for efficient searching
Provides search results ranked by relevance and popularity
In order to support performance, scale, and reliability, we need to develop a bunch of common
software modules and themes that can be reused across different microservices. These cover
caching, data models, the use of message queues, handling updates, monitoring and logging, and
security and privacy, which we cover next:
Caching: To improve performance and reduce the load on the backend services, a distributed caching layer (e.g., Redis) will
be employed. The caching layer will store frequently accessed data, such as user profiles, popular tweets, and timeline data.
Caching will help in serving data quickly and reducing the number of requests to the database.
Database: The Twitter-like service will use a distributed database (e.g., Apache Cassandra or Amazon DynamoDB) to store
structured data, such as tweets, users, follows, likes, and retweets. The database will be designed to handle high write
throughput and provide low-latency reads. Techniques such as sharding and replication will be used to distribute the data
across multiple nodes and ensure availability.
Object storage: Media files, such as images and videos, will be stored in an object storage system (e.g., Amazon S3).
Object storage provides scalable and durable storage for large files, allowing for efficient retrieval and delivery to users.
Message queue: A message queue (e.g., Apache Kafka) will be used for asynchronous communication between
microservices. When a new tweet is created, it will be published to the message queue. Timeline Service and Search Service
will consume these messages and update their respective data stores accordingly. The message queue ensures loose coupling
between services and enables scalable processing of tweets.
Real-time updates: To provide real-time updates to users, WebSocket connections can be established between the clients
and the server. When a new tweet is posted or an event occurs (e.g., a new follower), the server can push the updates to the
relevant clients through the WebSocket connection, ensuring instant notification.
Monitoring and logging: Comprehensive monitoring and logging mechanisms will be implemented to track the health and
performance of the system. Metrics such as request latency, error rates, and resource utilization will be collected and
visualized using tools such as Prometheus and Grafana. Centralized logging solutions (e.g., ELK stack) will be used to
aggregate and analyze logs from all components.
Security and privacy: Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords, will be hashed and
stored securely. Data encryption will be applied to protect user information both in transit and at rest. Rate limiting and
throttling mechanisms will be put in place to prevent abuse and ensure fair usage of the service.
This high-level design provides an overview of the key components and their interactions in the
Twitter-like service. It takes into account the scale requirements and employs various building
blocks to create a scalable and efficient architecture.


Now that we have a good idea about the different high-level components our system will contain,
the next thing to do is to dive deeper into the low-level design of each microservice, exploring
their specific functionalities, APIs, and data flow.
Designing Tweet Service
Tweet Service is responsible for handling the creation, retrieval, and deletion of tweets. It plays
a crucial role in the Twitter-like service by managing the core functionality related to tweets.
Let’s explore the low-level design of Tweet Service. Figure 11.3 shows the architecture of Tweet
Service where we have the appropriate requests flow in from the load balancer, through the API
gateway to Tweet Service, which interacts with the Tweet Database table, the object store, and
the message queue to power Timeline Service and Search Service (discussed in the next
sections).
Figure 11.3: High-level architecture of Tweet Service
Each service will expose API endpoints that can be used to communicate with it. Here are the
API endpoints for Tweet Service:
POST /tweets – create a new tweet:
Request body: Tweet content, user ID, and optional media attachment
Response: Created tweet object with assigned tweet ID and timestamp
GET /tweets/{tweetId} – retrieve a specific tweet by its ID:
Response: Tweet object containing content, user details, timestamp, and engagement metrics (e.g., likes,
retweets)


DELETE /tweets/{tweetId} – delete a tweet by its ID:
Request: User authentication token to ensure only the tweet owner can delete it
Response: Success or error message
GET /users/{userId}/tweets – retrieve tweets posted by a specific user:
Request: User ID and optional pagination parameters
Response: List of tweet objects posted by the user
These APIs are sufficient for any Tweet Service client to interact with the service. Let us now
understand the data model and storage aspects of this service.
Data storage
Tweet Service will utilize a combination of database and object storage for storing tweet data:
Database (e.g., Apache Cassandra or Amazon DynamoDB): Structured tweet data such as tweetId, userId,
content, and timestamp can be stored in a relational database. The partition key could be based on tweetId to ensure
an even distribution of data across nodes, and the clustering key could be a timestamp for the efficient retrieval of tweets in
chronological order.
Object storage (e.g., Amazon S3): Tweets are sometimes posted with media attachments that can be stored as separate
objects in object storage. Each such file will be assigned a unique identifier and tweets in the database will contain a
reference to the media file’s unique identifier.
Given that we have discussed the APIs and the data storage aspects of the service, let us discuss
the tweet creation and retrieval flows.
Tweet creation flow
Figure 11.4 shows the flow of data/API calls invoked in the tweet creation flow.


Figure 11.4: Tweet creation flow
When a user creates a new tweet through the client application, the following occurs:
1. The client sends a POST request to the /tweets endpoint with the tweet content, user ID, and optional media attachment.
2. Tweet Service receives the request and performs the necessary validations (e.g., tweet length and user authentication).
3. If the tweet contains a media attachment, Tweet Service uploads the media file to the object storage and obtains the unique
identifier.
4. Tweet Service generates a unique tweet ID and stores the tweet data (content, user ID, timestamp, and media reference) in
the database.
5. The created tweet object is returned to the client as the response.
6. Tweet Service publishes a message to the message queue (e.g., Apache Kafka) containing the newly created tweet ID. This
message will be consumed by other services, such as Timeline Service and Search Service, for further processing.
Tweet retrieval flow
Figure 11.5 shows the data flow/API calls invoked in the tweet retrieval flow.


Figure 11.5: Tweet retrieval flow
When a user requests to view a specific tweet or a user’s tweet timeline, the following steps are
carried out:
1. The client sends a GET request to the appropriate endpoint (/tweets/{tweetId} or /users/{userId}/tweets)
with the necessary parameters.
2. Tweet Service receives the request and validates the user authentication and authorization.
3. Tweet Service queries the database to retrieve the requested tweet(s) based on the provided tweet ID or user ID.
4. If the tweet(s) contain media references, Tweet Service fetches the corresponding media files from the object storage.
5. The retrieved tweet(s) and media files are combined and returned to the client as a response.
For any system designed to be used by a large number of users and services, it is important to
build a layer of caching to improve performance, which we will cover next.
Caching
To improve the performance of tweet retrieval, Tweet Service can utilize a distributed caching
layer (e.g., Redis). Frequently accessed tweets, such as popular or trending tweets, can be cached
in the cache layer. When a tweet is requested, Tweet Service first checks the cache. If the tweet


is found in the cache, it is served directly from there, reducing the load on the database. If the
tweet is not found in the cache, Tweet Service retrieves it from the database, stores it in the cache
for future requests, and returns it to the client.
The following are some of the caching strategies for new and popular tweets:
Time-based sliding window cache:
Maintain a cache of tweets posted within the last N hours (e.g., 24 hours)
As new tweets are posted, add them to the cache and remove tweets older than the time window
This ensures that the newest tweets are always available in the cache
Popularity-based caching:
Implement a scoring system based on engagement metrics (likes, retweets, and replies)
Cache tweets with scores above a certain threshold
Periodically recalculate scores and update the cache accordingly
Hybrid approach:
Combine time-based and popularity-based strategies
Cache all tweets from the last few hours (e.g., two hours) regardless of popularity
For older tweets, only cache those that meet a popularity threshold
Predictive caching:
Use machine learning models to predict which tweets are likely to become popular
Proactively cache tweets that the model predicts will have high engagement
User-based caching:
Cache recent tweets from users with high follower counts or verified status
This strategy assumes that tweets from popular users are more likely to be requested
The following are the eviction strategies:
Least Recently Used (LRU):
Evict the least recently accessed tweets when the cache reaches capacity
This strategy works well for maintaining a cache of currently popular content
Time to Live (TTL):


Assign an expiration time to each cached tweet
Evict tweets that have exceeded their TTL
Use shorter TTLs for regular tweets and longer TTLs for highly popular tweets
Least Frequently Used (LFU):
Track the access frequency of cached tweets
Evict the least frequently accessed tweets when the cache is full
This can be combined with a decay factor to favor more recent popularity
Size-based eviction:
Implement a maximum cache size (e.g., 10 GB)
When the cache reaches this limit, evict tweets based on a combination of size and another factor (such as LRU
or LFU)
Priority-based eviction:
Assign priorities to tweets based on factors such as user popularity, tweet engagement, and recency
Evict lower-priority tweets first when the cache is full
The following are the implementation considerations:
Use a multi-tiered caching strategy, such as hot cache for extremely popular tweets, warm cache for moderately popular
tweets, and cold storage for less accessed tweets
Implement cache warming techniques to preload the cache with likely-to-be-accessed tweets after a system restart
Use cache versioning or generation numbers to handle cache invalidation when tweets are modified or deleted
Consider using separate caches for different types of data (e.g., tweet content, user profiles, and timelines) to optimize
performance and eviction strategies for each
Implement monitoring and analytics to continuously evaluate and refine caching strategies based on actual usage patterns
By implementing these caching and eviction strategies, the Twitter-like service can efficiently
manage its cache to keep the most relevant and frequently accessed tweets readily available,
significantly improving response times and reducing the load on backend databases.
By following this low-level design, Tweet Service can efficiently handle the creation, retrieval,
and deletion of tweets while ensuring scalability, performance, and data integrity. The service
integrates with other components, such as the object storage and message queue, to provide a
seamless tweet management experience.


In the subsequent sections, we will explore the low-level design of other critical services, such as
User Service, Timeline Service, and Search Service, which work in conjunction with Tweet
Service to power the Twitter-like platform.
Designing User Service
User Service is responsible for managing user-related functionalities in the Twitter-like service.
It handles user registration, authentication, profile management, and follower-followee
relationships. Let’s dive into the low-level design of User Service. Figure 11.6 shows the User
Service high-level architecture, where we have the client request flowing through the load
balancer, API gateway, and User Service and interacting with the user and follow tables.
Figure 11.6: High-level architecture of User Service
Each service is defined by the set of API endpoints it exposes to its clients and how it stores the
data. We will cover both these aspects next.
User Service will expose the following API endpoints:
POST /users – create a new user account:
Request body: User information, such as username, email, and password
Response: Created user object with assigned user ID


GET /users/{userId} – retrieve user profile information:
Response: User object containing profile details, such as username, bio, profile picture URL, and
follower/followee counts
PUT /users/{userId} – update user profile information:
Request body: Updated user information, such as bio, profile picture URL, or location
Response: Updated user object
POST /users/{userId}/follow – follow another user:
Request: User authentication token and target user ID
Response: Success or error message
DELETE /users/{userId}/follow – unfollow another user:
Request: User authentication token and target user ID
Response: Success or error message
GET /users/{userId}/followers – retrieve a user’s followers:
Response: List of user objects representing the followers
GET /users/{userId}/following – retrieve the users a user is following:
Response: List of user objects representing the followees
Next, we will cover how and where the data for User Service will be stored.
Data storage
User Service will store user-related data in a database (e.g., PostgreSQL or MySQL):
User table: This table is used to store user information, such as user ID, username, email, password hash, bio, profile picture
URL, location, and registration timestamp, and will use the user ID as the primary key for efficient lookup
Follow table: This table will store the follower-followee relationships. It will contain the follower user ID, followee user ID,
and timestamp columns. This table will use a composite primary key of the follower user ID and followee user ID to ensure
uniqueness and efficient querying.
Now that we have covered the API endpoints and the data storage, let us look at the flow for user
registration, authentication, follows, and retrieving followers.


User registration flow
Figure 11.7’s sequence diagram shows the process of registering a new user, including
validation, user ID generation, password hashing, and data storage.
Figure 11.7: User registration flow
When a new user registers for the Twitter-like service:
1. The client sends a POST request to the /users endpoint with the user’s information, such as username, email, and
password.
2. User Service receives the request and performs the necessary validations (e.g., has a unique username and email been
provided?).
3. If the validations pass, User Service generates a unique user ID and stores the user information in the user table, hashing the
password for security.
4. The created user object is returned to the client as the response.


User authentication flow
Figure 11.8’s diagram illustrates the process of user authentication, including credential
verification and token generation.
Figure 11.8: Authentication flow
When a user logs in to the Twitter-like service:
1. The client sends a POST request to the authentication endpoint (e.g., /auth/login) with the user’s credentials (e.g.,
username and password).
2. User Service receives the request and verifies the provided credentials against the stored user information in the user table.
3. If the credentials are valid, User Service generates an authentication token (e.g., JSON Web Token, or JWT) containing
the user ID and other relevant information.
4. The authentication token is returned to the client, which includes it in subsequent requests to authenticate and authorize the
user.
Follow/unfollow flow


Figure 11.9’s sequence diagram shows the process of following or unfollowing a user, including
token verification and database updates.
Figure 11.9: Follow/unfollow flow sequence diagram
When a user follows or unfollows another user:
1. The client sends a POST or DELETE request to the /users/{userId}/follow endpoint with the user authentication
token and target user ID.
2. User Service verifies the authentication token to ensure the request is made by a valid user.
3. For a follow request, User Service inserts a new entry into the follow table with the follower user ID and followee user ID.
4. For an unfollow request, User Service removes the corresponding entry from the follow table.
5. User Service returns a success or error message to the client.
Retrieving followers/followees
Figure 11.10 illustrates the process of retrieving a user’s followers or followees, including
database queries and profile fetching.


Figure 11.10: Retrieving followers/followees sequence diagram
When a user requests their followers or the users they are following, the following occurs:
1. The client sends a GET request to the /users/{userId}/followers or /users/{userId}/following
endpoint.
2. User Service queries the follow table to retrieve the user IDs of the followers or followees.
3. User Service then fetches the user profile information for each follower or followee from the user table.
4. The list of user objects representing the followers or followees is returned to the client.
By following this low-level design, User Service can efficiently handle user registration,
authentication, profile management, and follower-followee relationships. It integrates with the
database and caching layer to provide a seamless user experience and support the social
networking aspects of the Twitter-like service.
In the next section, we will explore the low-level design of Timeline Service, which is
responsible for generating and serving user timelines based on the tweets from the users they
follow.
Low-level design – Timeline Service
Timeline Service is responsible for generating and serving user timelines in the Twitter-like
service. It aggregates tweets from the users a person follows and presents them in chronological
order. Let’s explore the low-level design of Timeline Service. We have already seen in Figure


11.2 how Tweet Service posts the incoming tweet to Timeline Service via a message queue
(Kafka).
Timeline Service will expose the following API endpoints:
GET /timeline/{userId} – retrieve the user’s home timeline:
Request: User authentication token
Response: List of tweet objects representing the user’s timeline
GET /timeline/{userId}/mentions – retrieve the user’s mentions timeline:
Request: User authentication token
Response: List of tweet objects mentioning the user
Given that we have the API endpoints listed, we will now check the data flow.
Data flow
Timeline Service relies on Tweet Service and User Service to generate user timelines. Figure
11.11 shows the data flow for creating a new tweet.
Figure 11.11: The data flow for creating a new tweet and updating followers’ timelines
Here is the flow:
1. When a new tweet is created, Tweet Service publishes a message to the message queue (e.g., Apache Kafka) containing the
tweet ID and the user ID of the tweet author.
2. Timeline Service consumes the message from the message queue.
3. Timeline Service retrieves the follower IDs of the tweet author from User Service.


4. For each follower, Timeline Service appends the tweet ID to their timeline data structure (e.g., a list or a sorted set) stored
in the cache (e.g., Redis).
5. The timeline data structure maintains a limited number of recent tweet IDs for each user, typically based on a time window
or a maximum count.
Timeline retrieval flow
Figure 11.12 shows the timeline retrieval flow.
Figure 11.12: The timeline retrieval flow when a user requests their home timeline
When a user requests their home timeline, the following occurs:
The client sends a GET request to the /timeline/{userId} endpoint with the user authentication token.
Timeline Service verifies the authentication token to ensure the request is made by a valid user.
Timeline Service retrieves the user’s timeline data structure from the cache.
If the timeline data structure is not found in the cache or is incomplete, Timeline Service fetches the missing tweet IDs from
the database and updates the cache accordingly.
Timeline Service retrieves the actual tweet objects corresponding to the tweet IDs from Tweet Service.


The retrieved tweets are sorted based on their timestamps to ensure chronological order.
The sorted list of tweet objects is returned to the client as the user’s home timeline.
Mentions timeline
The mentions timeline is generated similarly to the home timeline but with a different data flow.
Figure 11.13 shows the mentions timeline process for handling and retrieving mentions.
Figure 11.13: The mentions timeline process for handling and retrieving mentions
Here is the flow:
1. When a new tweet is created, Tweet Service checks whether the tweet contains any mentions of other users.
2. If mentions are found, Tweet Service publishes a separate message to the message queue for each mentioned user,
containing the tweet ID and the mentioned user ID.
3. Timeline Service consumes these messages and appends the tweet ID to the mentions timeline data structure of each
mentioned user in the cache.
4. The mentions timeline retrieval process is similar to the home timeline retrieval, but uses the mentions timeline data
structure instead.
Push-based updates
To provide real-time updates to user timelines, Timeline Service can utilize push-based
mechanisms. When a new tweet is created, Timeline Service can send a real-time notification to
the relevant users’ clients using WebSocket connections. The clients can update their timelines
instantly upon receiving the notification, providing a real-time user experience.


By following this low-level design, Timeline Service can efficiently generate and serve user
timelines by aggregating tweets from followed users. It leverages caching and push-based
updates to provide a real-time and responsive user experience. The service integrates with Tweet
Service, User Service, and the message queue to ensure data consistency and scalability.
In the next section, we will explore the low-level design of Search Service, which enables users
to search for tweets and user profiles based on keywords and other criteria.
Designing Search Service
Search Service is responsible for enabling users to search for tweets and user profiles based on
keywords, hashtags, and other criteria in the Twitter-like service. It provides a powerful and
efficient search functionality to help users discover relevant content. Let’s dive into the low-level
design of Search Service. We have already seen in Figure 11.3 how Tweet Service posts the
incoming tweets to the message queue, which forwards it to Search Service for index searching.
Figure 11.14 illustrates how Search Service interacts with the API gateway, message queue, and
Elasticsearch. It also shows how Tweet Service and User Service feed data into the message
queue for indexing.
Figure 11.14: Search Service low-level design
Let us look at the API endpoints exposed by Search Service and the data flow.
The Search Service will expose the following API endpoints:
GET/search/tweets?q={query}&limit={limit}&offset={offset} – search for tweets based on a given
query:
Request: Search query; optional limit and offset parameters for pagination
Response: List of tweet objects matching the search query


GET/search/users?q={query}&limit={limit}&offset={offset} – search for user profiles based on a
given query:
Request: Search query; optional limit and offset parameters for pagination
Response: List of user objects matching the search query
We have covered the API endpoints. Let us now look at the data flow and indexing next.
Data flow and indexing
To enable efficient searching, Search Service relies on a search engine such as Elasticsearch to
index and store the tweet and user data. Figure 11.15’s sequence diagram shows the process of
indexing new tweets and user profiles in Elasticsearch, including data extraction and processing
by Search Service.
Figure 11.15: Data flow and indexing sequence diagram
Here is the flow:


1. When a new tweet is created, Tweet Service sends the tweet data to Search Service.
2. Search Service extracts relevant information from the tweet, such as the text content, hashtags, mentions, and user details.
3. The extracted data is then indexed in Elasticsearch, creating an inverted index that maps terms to tweet IDs.
4. Similarly, when a new user is created or their profile is updated, User Service sends the user data to Search Service for
indexing.
5. The user data, including the username, bio, location, and other relevant information, is indexed in Elasticsearch.
We have covered the indexing of data into our Search Service. Let us now learn how to process
search queries.
Search query processing
Figure 11.16 illustrates the process of handling a search query, from the initial client request
through query parsing, Elasticsearch searching, and result processing.
Figure 11.16: Search query processing sequence diagram


When a user performs a search query, the following occurs:
1. The client sends a GET request to the /search/tweets or /search/users endpoint with the search query and
optional pagination parameters.
2. Search Service receives the request and parses the search query.
3. The parsed query is transformed into an Elasticsearch query using appropriate query builders and filters.
4. Search Service sends the query to Elasticsearch, which performs the search operation on the indexed data.
5. Elasticsearch retrieves the matching tweet or user documents based on the query criteria.
6. Search Service processes the search results, applying any additional filtering, sorting, or pagination as needed.
7. The final list of tweets or user objects is returned to the client as the search results.
Relevance scoring and ranking
To provide the most relevant search results, Search Service utilizes Elasticsearch’s relevance
scoring and ranking capabilities. Elasticsearch uses a combination of factors, such as term
frequency, inverse document frequency (TF-IDF) and field-level boosting, to calculate the
relevance score of each document. The relevance score determines the order in which the search
results are presented to the user. Search Service can customize the relevance scoring by defining
custom scoring functions or boosting certain fields based on specific requirements.
By following this low-level design, Search Service can provide a powerful and efficient search
functionality for the Twitter-like service. It leverages Elasticsearch for indexing and searching,
applies relevance scoring and ranking techniques, and utilizes caching to optimize performance.
The service integrates with Tweet Service and User Service to ensure data consistency and realtime updates.
In the next section, we will discuss additional considerations and best practices for designing and
implementing the Twitter-like service.
Additional considerations
When designing and implementing the Twitter-like service, there are several additional
considerations and best practices to keep in mind. These considerations ensure the system is
scalable, maintainable, and aligned with business requirements. Let’s explore some of these key
aspects:


Handling trending topics and hashtags: We can implement a mechanism to track and identify trending topics and hashtags
based on their popularity and frequency of use. To do so, we can utilize real-time stream processing frameworks such as
Apache Storm or Apache Flink to analyze the incoming tweet data and update the trending topics in real-time. For
performance, we can store the trending topics and hashtags in a cache or database for quick retrieval and display to users.
Finally, we can provide API endpoints to retrieve the current trending topics and allow users to explore tweets related to
those topics.
Implementing rate limiting and throttling: One of the core requirements for any large-scale system with millions of users
is to implement rate limiting and throttling mechanisms to protect the system from abuse and ensure fair usage of resources.
We can set appropriate rate limits for different API endpoints based on the expected usage patterns and system capacity and
use techniques such as token buckets or leaky buckets to enforce rate limits and throttle requests that exceed the defined
thresholds.
By considering these additional aspects and best practices, the Twitter-like service can be
designed and implemented to be scalable, maintainable, and extensible. It ensures a robust and
user-friendly platform that can handle the demands of a growing user base and evolving business
requirements.
In the final section, we will summarize the key takeaways from this chapter and discuss future
considerations and potential enhancements for the Twitter-like service.
Summary
In this chapter, we have explored the system design of a Twitter-like service, covering functional
and non-functional requirements, data modeling, scalability considerations, and architectural
components. We examined both high-level and low-level designs, focusing on key services such
as Tweet Service, User Service, Timeline Service, and Search Service. The system architecture
leverages horizontal scaling, data partitioning, and distributed processing to handle a large
number of users and interactions efficiently.
Throughout our discussion, we emphasized scalability, reliability, and performance,
incorporating techniques such as caching and asynchronous processing to improve response
times and handle high throughput. As we conclude, it’s important to note that designing such a
service is an ongoing process, requiring flexibility and adaptability to evolving user needs and
technological advancements. By following the principles and best practices outlined here,
developers and system architects can create a robust and scalable platform that meets user needs
and stands the test of time. In the next chapter, we will see how we can design a service like
Instagram for millions of users. Stay tuned.

## Examples & Scenarios

- Users should be able to post tweets, which are short messages limited to a specific character count (e.g., 280
characters)
Tweets can contain text, hashtags, mentions of other users, and media attachments such as images or videos
The system should enforce the character limit and handle the storage and retrieval of tweets efficiently
Follow/unfollow:
Users should be able to follow other users to receive their tweets in their timeline
The system should maintain a follow graph that represents the relationships between users
Users should also have the ability to unfollow other users, removing their tweets from the timeline
Timeline:
The timeline is a crucial feature that displays a chronological feed of tweets from the users a person follows

- Caching: To improve performance and reduce the load on the backend services, a distributed caching layer (e.g., Redis) will
be employed. The caching layer will store frequently accessed data, such as user profiles, popular tweets, and timeline data.
Caching will help in serving data quickly and reducing the number of requests to the database.
Database: The Twitter-like service will use a distributed database (e.g., Apache Cassandra or Amazon DynamoDB) to store
structured data, such as tweets, users, follows, likes, and retweets. The database will be designed to handle high write
throughput and provide low-latency reads. Techniques such as sharding and replication will be used to distribute the data
across multiple nodes and ensure availability.
Object storage: Media files, such as images and videos, will be stored in an object storage system (e.g., Amazon S3).
Object storage provides scalable and durable storage for large files, allowing for efficient retrieval and delivery to users.
Message queue: A message queue (e.g., Apache Kafka) will be used for asynchronous communication between

- and the server. When a new tweet is posted or an event occurs (e.g., a new follower), the server can push the updates to the
relevant clients through the WebSocket connection, ensuring instant notification.
Monitoring and logging: Comprehensive monitoring and logging mechanisms will be implemented to track the health and
performance of the system. Metrics such as request latency, error rates, and resource utilization will be collected and
visualized using tools such as Prometheus and Grafana. Centralized logging solutions (e.g., ELK stack) will be used to
aggregate and analyze logs from all components.
Security and privacy: Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords, will be hashed and
stored securely. Data encryption will be applied to protect user information both in transit and at rest. Rate limiting and
throttling mechanisms will be put in place to prevent abuse and ensure fair usage of the service.

- Response: Tweet object containing content, user details, timestamp, and engagement metrics (e.g., likes,
retweets)

- Database (e.g., Apache Cassandra or Amazon DynamoDB): Structured tweet data such as tweetId, userId,
content, and timestamp can be stored in a relational database. The partition key could be based on tweetId to ensure
an even distribution of data across nodes, and the clustering key could be a timestamp for the efficient retrieval of tweets in
chronological order.
Object storage (e.g., Amazon S3): Tweets are sometimes posted with media attachments that can be stored as separate
objects in object storage. Each such file will be assigned a unique identifier and tweets in the database will contain a
reference to the media file’s unique identifier.
Given that we have discussed the APIs and the data storage aspects of the service, let us discuss
the tweet creation and retrieval flows.
Tweet creation flow

- 2. Tweet Service receives the request and performs the necessary validations (e.g., tweet length and user authentication).
3. If the tweet contains a media attachment, Tweet Service uploads the media file to the object storage and obtains the unique
identifier.
4. Tweet Service generates a unique tweet ID and stores the tweet data (content, user ID, timestamp, and media reference) in
the database.
5. The created tweet object is returned to the client as the response.
6. Tweet Service publishes a message to the message queue (e.g., Apache Kafka) containing the newly created tweet ID. This
message will be consumed by other services, such as Timeline Service and Search Service, for further processing.
Tweet retrieval flow
Figure 11.5 shows the data flow/API calls invoked in the tweet retrieval flow.

- layer (e.g., Redis). Frequently accessed tweets, such as popular or trending tweets, can be cached
in the cache layer. When a tweet is requested, Tweet Service first checks the cache. If the tweet

- Maintain a cache of tweets posted within the last N hours (e.g., 24 hours)
As new tweets are posted, add them to the cache and remove tweets older than the time window
This ensures that the newest tweets are always available in the cache
Popularity-based caching:
Implement a scoring system based on engagement metrics (likes, retweets, and replies)
Cache tweets with scores above a certain threshold
Periodically recalculate scores and update the cache accordingly
Hybrid approach:
Combine time-based and popularity-based strategies
Cache all tweets from the last few hours (e.g., two hours) regardless of popularity

- Implement a maximum cache size (e.g., 10 GB)
When the cache reaches this limit, evict tweets based on a combination of size and another factor (such as LRU
or LFU)
Priority-based eviction:
Assign priorities to tweets based on factors such as user popularity, tweet engagement, and recency
Evict lower-priority tweets first when the cache is full
The following are the implementation considerations:
Use a multi-tiered caching strategy, such as hot cache for extremely popular tweets, warm cache for moderately popular
tweets, and cold storage for less accessed tweets
Implement cache warming techniques to preload the cache with likely-to-be-accessed tweets after a system restart

- Consider using separate caches for different types of data (e.g., tweet content, user profiles, and timelines) to optimize
performance and eviction strategies for each
Implement monitoring and analytics to continuously evaluate and refine caching strategies based on actual usage patterns
By implementing these caching and eviction strategies, the Twitter-like service can efficiently
manage its cache to keep the most relevant and frequently accessed tweets readily available,
significantly improving response times and reducing the load on backend databases.
By following this low-level design, Tweet Service can efficiently handle the creation, retrieval,
and deletion of tweets while ensuring scalability, performance, and data integrity. The service
integrates with other components, such as the object storage and message queue, to provide a
seamless tweet management experience.

- User Service will store user-related data in a database (e.g., PostgreSQL or MySQL):
User table: This table is used to store user information, such as user ID, username, email, password hash, bio, profile picture
URL, location, and registration timestamp, and will use the user ID as the primary key for efficient lookup
Follow table: This table will store the follower-followee relationships. It will contain the follower user ID, followee user ID,
and timestamp columns. This table will use a composite primary key of the follower user ID and followee user ID to ensure
uniqueness and efficient querying.
Now that we have covered the API endpoints and the data storage, let us look at the flow for user
registration, authentication, follows, and retrieving followers.

- 2. User Service receives the request and performs the necessary validations (e.g., has a unique username and email been
provided?).
3. If the validations pass, User Service generates a unique user ID and stores the user information in the user table, hashing the
password for security.
4. The created user object is returned to the client as the response.

- 1. The client sends a POST request to the authentication endpoint (e.g., /auth/login) with the user’s credentials (e.g.,
username and password).
2. User Service receives the request and verifies the provided credentials against the stored user information in the user table.
3. If the credentials are valid, User Service generates an authentication token (e.g., JSON Web Token, or JWT) containing
the user ID and other relevant information.
4. The authentication token is returned to the client, which includes it in subsequent requests to authenticate and authorize the
user.
Follow/unfollow flow

- 1. When a new tweet is created, Tweet Service publishes a message to the message queue (e.g., Apache Kafka) containing the
tweet ID and the user ID of the tweet author.
2. Timeline Service consumes the message from the message queue.
3. Timeline Service retrieves the follower IDs of the tweet author from User Service.

- 4. For each follower, Timeline Service appends the tweet ID to their timeline data structure (e.g., a list or a sorted set) stored
in the cache (e.g., Redis).
5. The timeline data structure maintains a limited number of recent tweet IDs for each user, typically based on a time window
or a maximum count.
Timeline retrieval flow
Figure 11.12 shows the timeline retrieval flow.
Figure 11.12: The timeline retrieval flow when a user requests their home timeline
When a user requests their home timeline, the following occurs:
The client sends a GET request to the /timeline/{userId} endpoint with the user authentication token.
Timeline Service verifies the authentication token to ensure the request is made by a valid user.

