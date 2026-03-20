# Chapter 12: Designing a Service Like Instagram

> Source: System Design Guide for Software Professionals, Chapter 16, Pages 271-295

## Key Concepts

- 12
Designing a Service Like Instagram
In the era of social media, photo-sharing platforms have taken the world by storm, and Instagram
stands out as one of the most popular and influential services. W
- Users should be able to create new accounts by providing the necessary information such as a username, email,
and password
The system should securely store user credentials and authenticate users upon

## Content

12
Designing a Service Like Instagram
In the era of social media, photo-sharing platforms have taken the world by storm, and Instagram
stands out as one of the most popular and influential services. With over a billion active users,
Instagram has revolutionized the way people capture, share, and engage with visual content.
Designing a service similar to Instagram presents a unique set of challenges and opportunities. It
requires a robust and scalable architecture that can handle the immense volume of user-generated
content while providing a seamless and engaging user experience. In this chapter, we will
explore the system design of an Instagram-like service, delving into the key components, design
decisions, and best practices involved in building a scalable and efficient photo-sharing platform.
By the end of this chapter, you will have a comprehensive understanding of the system design
principles and techniques involved in building a service similar to Instagram.
In this chapter, we will cover the following topics:
Functional requirements
Non-functional requirements
Designing the data model
Scale calculations
High-level design
Low-level design
Additional considerations
Let us start with the functional requirements of a service similar to Instagram.
Functional requirements
Before diving into the system design, it is crucial to define the functional requirements that
specify what the Instagram-like service should be capable of doing. These requirements lay the
foundation for the entire design process and ensure that the system meets the needs of its users.
Let’s explore the key functional requirements:
User registration and authentication:


Users should be able to create new accounts by providing the necessary information such as a username, email,
and password
The system should securely store user credentials and authenticate users upon login
User sessions should be managed efficiently to allow seamless access to the service
Photo upload and sharing:
Users should be able to upload photos from their devices or capture photos directly within the app
The system should support various photo formats (e.g., JPEG and PNG) and perform necessary processing and
compression
Users should have the ability to apply filters, add captions, and tag other users in their photos
The uploaded photos should be associated with the user’s profile and stored in a scalable and reliable storage
system
News feed:
The news feed is a crucial feature that displays a personalized stream of photos from the users a person follows
The system should generate and serve the news feed in real-time, considering factors such as photo timestamps,
user preferences, and engagement metrics
The news feed should support infinite scrolling, allowing users to load more photos as they scroll down
User interactions:
Users should be able to like and comment on photos shared by other users
The system should store and display the count of likes and comments for each photo
Users should have the ability to mention other users in comments using the @ symbol followed by the username
Direct messaging:
The service should support direct messaging functionality, allowing users to privately send photos and messages
to other users or groups
Users should be able to initiate conversations, view message history, and receive real-time notifications for new
messages
Search and discovery:
Users should be able to search for other users, photos, and hashtags within the platform
The search functionality should provide relevant and accurate results based on keywords, usernames, and
hashtags
The system should also support discovery features, such as exploring popular photos, trending hashtags, and
personalized recommendations


Notifications:
The service should send real-time notifications to users for various events, such as new followers, likes,
comments, and direct messages
Notifications should be delivered through push notifications on mobile devices and in-app notifications
Users should have control over their notification preferences, allowing them to customize the types of
notifications they receive
These functional requirements provide a comprehensive overview of the core features that an
Instagram-like service should offer. By fulfilling these requirements, the system will enable users
to seamlessly share photos, connect with others, and engage with visual content.
In the next section, we will explore the non-functional requirements that ensure the service
remains scalable, reliable, and performant while meeting the functional requirements discussed
so far.
Non-functional requirements
While functional requirements define what the system should do, non-functional requirements
specify how the system should perform and behave. These requirements are critical to ensuring
that the Instagram-like service remains scalable, available, and reliable under various conditions.
Let’s discuss the key non-functional requirements:
Scalability:
The system should be designed to handle a large number of users and photos, accommodating growth and peak
traffic loads
Horizontal scalability should be achieved by adding more servers and distributing the load across them
The architecture should allow for easy scaling of individual components, such as the Photo Upload Service or
News Feed Service , independently
Performance:
The service should provide a fast and responsive user experience, with minimal latency for key operations such
as photo uploads, news feed loading, and interactions
The system should optimize resource utilization and employ caching mechanisms to reduce the load on backend
services and improve performance
Asynchronous processing should be utilized for resource-intensive tasks, such as photo compression and
thumbnail generation, to ensure quick response times


Availability:
The service should be highly available, minimizing downtime and ensuring that users can access their photos and
engage with the platform at all times
The system should be designed with redundancy and fault tolerance in mind, employing techniques including
data replication, load balancing, and automatic failover
Regular backups and disaster recovery mechanisms should be in place to protect against data loss and ensure
quick recovery in the case of failure
Reliability:
The system should be reliable, ensuring data integrity and consistency across all components
Mechanisms should be implemented to handle and recover from errors gracefully, preventing data corruption or
inconsistencies
Transactions and data consistency models should be chosen carefully to maintain the accuracy and reliability of
user data, likes, comments, and other interactions
Usability:
The system should provide features such as search, filters, and recommendations to enhance user engagement
and content discovery
By addressing these non-functional requirements, the Instagram-like service can ensure a
reliable, scalable, and performant user experience. It is essential to consider these requirements
throughout the design process and make architectural decisions that align with these goals.
In the next section, we will explore the data model that forms the foundation of the Instagramlike service, defining the entities and relationships necessary to support the functional
requirements.
Designing the data model
The data model is a crucial component of the Instagram-like service, as it defines the structure
and relationships of the data entities involved. A well-designed data model ensures efficient
storage, retrieval, and manipulation of data while supporting the functional requirements of the
system. Let’s dive into the key entities and their relationships:
The User entity represents the users of the Instagram-like service, storing their profile information such as username, email,
password hash, profile picture, bio, and website. Each user is uniquely identified by their user_id. The Photo entity
represents the photos uploaded by users. It contains the photo details such as the user_id of the uploader, caption, image
URL, creation timestamp, location, and tags. The photo_id serves as the primary key.


The Comment entity represents the comments posted on photos. It contains the comment text, user_id of the commenter,
photo_id of the associated photo, and creation timestamp. The comment_id is the primary key. The Like entity
represents the likes on photos. It contains the user_id of the user who liked the photo and the photo_id of the liked
photo. The created_at timestamp records when the like occurred.
The Follow entity represents the follow relationships between users. It contains the follower_id and followee_id,
indicating which user is following whom. The created_at timestamp captures when the follow relationship was
established. The Hashtag entity represents the hashtags used in photos. It contains the hashtag_id and the name of the
hashtag. The PhotoHashtag entity represents the many-to-many relationship between photos and hashtags. It contains the
photo_id and hashtag_id, indicating which photos are associated with which hashtags. The DirectMessage entity
represents private conversations between users. It contains the message_id, sender_id, recipient_id, content,
and created_at timestamp.
Figure 12.1 illustrates the key entities (User, Photo, Comment, Like, Follow, Hashtag,
PhotoHashtag, and DirectMessage) in the Instagram-like service, their attributes, and the
relationships between them, providing a comprehensive visual representation of the data
structure that supports the service’s core functionalities.


Figure 12.1: An overview of the entity relationship diagram for Instagram-like service data model
This diagram effectively captures the complex relationships between the various entities in the
Instagram-like service, including one-to-many and many-to-many relationships. It visually
represents how users interact with photos, comments, likes, follows, hashtags, and direct
messages, which is crucial for understanding the data structure of the system.
By designing the data model with these entities and relationships, the Instagram-like service can
efficiently store and retrieve data related to users, photos, comments, likes, follows, hashtags,
and direct messages. The data model supports the functional requirements and enables the
system to handle the complex interactions between users and their shared content.
After we have evaluated the data model design, we will perform scale calculations to estimate
the storage, bandwidth, and processing requirements of the Instagram-like service based on the
anticipated user base and usage patterns.
Scale calculations
To design a scalable Instagram-like service, it is essential to estimate the storage, bandwidth, and
processing requirements based on the expected user base and usage patterns. These calculations
help in making informed decisions about the infrastructure and resources needed to support the
service. Let’s perform some scale calculations:
Assumptions:
Total number of users: 100 million
Daily active users: 10 million
Average number of photos uploaded per user per day: 2
Average photo size: 5 MB
Retention period for photos: 5 years
Average number of followers per user: 500
Average number of likes per photo: 100
Average number of comments per photo: 10
Storage requirements:
Daily photo storage: 10 million users × 2 photos/user/day × 5 MB/photo = 100
TB/day
Yearly photo storage: 100 TB/day × 365 days = 36.5 PB/year


Total photo storage for 5 years: 36.5 PB/year × 5 years = 182.5 PB
User data storage: Assuming 1 MB of storage per user for profile information
Total user data storage: 100 million users × 1 MB/user = 100 GB
Metadata storage (likes, comments, hashtags): Assuming 1 KB of metadata per photo
Daily metadata storage: 10 million users × 2 photos/user/day × 1 KB/photo = 20
GB/day
Yearly metadata storage: 20 GB/day × 365 days = 7.3 TB/year
Total metadata storage for 5 years: 7.3 TB/year × 5 years = 36.5 TB
Total storage: 182.5 PB (photos) + 100 GB (user data) + 36.5 TB (metadata) ≈
182.5 PB
Bandwidth requirements:
Daily bandwidth for photo uploads: 10 million users × 2 photos/user/day × 5 MB/photo =
100 TB/day
Daily bandwidth for photo delivery: 10 million users × 500 followers/user × 2
photos/user/day × 5 MB/photo = 50 PB/day
Total daily bandwidth: 100 TB (uploads) + 50 PB (delivery) ≈ 50 PB/day
Processing requirements:
Peak photo uploads per second: 10 million users × 2 photos/user/day ÷ 86400
seconds/day ≈ 230 photos/second
Likes per second: 230 photos/second × 100 likes/photo = 23,000 likes/second
Comments per second: 230 photos/second × 10 comments/photo = 2,300
comments/second
These calculations provide a rough estimate of the storage, bandwidth, and processing
requirements for the Instagram-like service. It’s important to note that these numbers can vary
based on the actual usage patterns and growth of the user base. The infrastructure should be
designed to handle peak loads and should be easily scalable to accommodate future growth.
In the next section, we will propose a high-level design architecture that takes into account these
scale requirements and leverages various building blocks to create a scalable and efficient
system.


High-level design
Now that we have a clear understanding of the functional and non-functional requirements, as
well as the scale calculations, let’s dive into the high-level design of the Instagram-like service.
The goal is to create an architecture that is scalable, reliable, and efficient in handling the
massive volume of photos, users, and interactions. Figure 12.2 shows the high-level design of
the Instagram-like system. This diagram illustrates the comprehensive architecture of an
Instagram-like service, showcasing the flow of data and interactions between various
components including client applications, load balancer, API gateway, microservices, databases,
caching systems, object storage, CDN, and message queues, all working together to provide a
scalable and efficient photo-sharing platform.
Figure 12.2: High-level system design of our Instagram-like service
Components and modules in the high-level
architecture
Let's go through the following software components and modules:


Client-server architecture: The Instagram-like service will follow a client-server architecture, where clients (such as
mobile apps or web browsers) communicate with the server-side components through APIs. The server-side components
will handle the core functionality, data storage, and processing.
Load balancer: To distribute the incoming traffic evenly across multiple servers, a load balancer will be placed in front of
the server-side components. The load balancer will ensure that requests are efficiently routed to the appropriate servers
based on factors such as server load, request type, and geographic location.
API gateway: An API gateway will act as the entry point for all client requests. It will handle request routing,
authentication, rate limiting, and request/response transformation. The API gateway will expose well-defined APIs for
various functionalities, such as photo uploads, news feed retrieval, user interactions, and direct messaging.
Microservices architecture: To promote modularity, scalability, and maintainability, the server-side components will be
designed as microservices. Each microservice will be responsible for a specific domain or functionality. The main
microservices in the Instagram-like service will be the following:
Photo Upload Service :
Handles photo uploads, processing, and storage
Performs image compression, resizing, and thumbnail generation
Stores photos in an object storage system (e.g., Amazon S3)
News Feed Service :
Generates and serves personalized news feeds for users
Aggregates photos from followed users and applies ranking algorithms
Utilizes caching to improve performance and reduce latency
User Service:
Manages user profiles, authentication, and authorization
Handles user-related operations such as sign-up, login, and profile updates
Stores user data in a database (e.g., MySQL or PostgreSQL)
Interaction service:
Handles user interactions such as likes, comments, and hashtags
Stores interaction data in a database and updates relevant counts
Sends notifications to users for new interactions
Direct Messaging service:
Enables private communication between users
Handles message delivery, storage, and real-time updates
Utilizes a message queue (e.g., Apache Kafka) for asynchronous processing


Database and caching: The Instagram-like service will employ a combination of databases and caching to store and retrieve
data efficiently:
Relational database (e.g., MySQL or PostgreSQL):
Stores structured data such as user profiles, photo metadata, comments, likes, and hashtags
Provides ACID properties and supports complex queries
NoSQL database (e.g., Apache Cassandra or MongoDB):
Handles high-volume write operations for user interactions and real-time data
Offers scalability and eventual consistency
Caching (e.g., Redis or Memcached):
Caches frequently accessed data such as news feed photos, user profiles, and trending hashtags
Reduces the load on databases and improves response times
Object storage: Photos and videos will be stored in an object storage system (e.g., Amazon S3) that provides scalable and
durable storage. Object storage allows for efficient retrieval and delivery of media files to users.
Content Delivery Network (CDN): To optimize the delivery of photos and videos to users across different geographic
locations, a CDN (e.g., Amazon CloudFront) will be utilized. The CDN caches and serves content from edge locations
closer to the users, reducing latency and improving the overall user experience.
Asynchronous processing: Resource-intensive tasks, such as photo processing and notifications, will be handled
asynchronously using message queues (e.g., Apache Kafka) and background workers. This ensures that the main application
remains responsive and can handle a high volume of requests.
Security and privacy: Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords, will be hashed and
stored securely. Data encryption will be applied to protect user information both in transit and at rest. Rate limiting and
throttling mechanisms will be put in place to prevent abuse and ensure fair usage of the service.
This high-level design provides an overview of the key components and their interactions in the
Instagram-like service. It takes into account the scale requirements and employs various building
blocks to create a scalable and efficient architecture.
In the next sections, we will explore the low-level design of key components, including the
Photo Upload Service , News Feed Service , and User Service, diving deeper into their specific
functionalities and design considerations.
Low-level design


In this section, we will cover the low-level design of a subset of services in our system, namely
the Photo Upload Service , News Feed Service, and the User Service. Let us first discuss the
Photo Upload Service .
Designing the Photo Upload Service
The Photo Upload Service is a critical component of the Instagram-like service, responsible for
handling the upload, processing, and storage of photos. Let’s explore the low-level design of the
Photo Upload Service in detail. Figure 12.3 illustrates the architecture of the Photo Upload
Service showing its interactions with the database, object storage, message queue, background
workers, and CDN for efficient photo handling and delivery.
Figure 12.3: Low-level design of the Photo Upload Service
Let us now look into the API endpoint exposed by the service and the photo upload and retrieval
flow.
The Photo Upload Service will expose the following API endpoints:
POST /photos: Upload a new photo
Request body: Photo file, user ID, caption, location, and other metadata
Response: Uploaded photo details, including photo ID and URL
Let us look at the photo upload flow and photo retrieval flow in detail.
Photo upload flow
The following sequence diagram depicts the flow of uploading a photo, from the initial client
request through metadata storage, photo upload, and asynchronous processing.


Figure 12.4: Flowchart for the photo upload flow
When a user uploads a photo through the client application, the following happens:
1. The Client sends a POST request to the /photos endpoint with the photo file and associated metadata.
2. The API gateway receives the request and routes it to the Photo Upload Service.
3. The Photo Upload Service performs the following steps:
I. Validates the request, ensuring the presence of required fields and the authenticity of the user.
II. Generates a unique photo ID and stores the metadata in the database.
III. Uploads the photo file to the object storage system (e.g., Amazon S3).
IV. Initiates asynchronous processing tasks for photo compression, resizing, and thumbnail generation.
V. Returns the uploaded photo details, including the photo ID and URL, to the client.
The client receives the response and updates the user interface accordingly.
To optimize the photo upload process and ensure a responsive user experience, photo processing
tasks are performed asynchronously:
1. After the photo is uploaded to the object storage, the Photo Upload Service sends a message to a message queue (e.g.,
Apache Kafka) containing the photo ID and processing instructions.
2. Background workers consume the messages from the message queue and perform the following tasks:
I. Compress the photo to optimize storage and network usage.
II. Generate multiple resized versions of the photo for different device resolutions.
III. Create thumbnail images for preview purposes.


IV. Update the photo metadata in the database with the processed file locations.
3. The processed photo files are stored in the object storage system, and their URLs are updated in the database.
We have looked at the flow for photo upload, now let us understand what happens when a user
requests to view the photo.
Photo retrieval
The following sequence diagram shows the photo retrieval process, including metadata caching
and content delivery through the CDN, illustrating how the system optimizes photo access for
users.
Figure 12.5: Photo retrieval flow
When a user requests to view a photo, the following occurs:
1. The client sends a GET request to the /photos/{photoId} endpoint.
2. The API Gateway receives the request and routes it to the Photo Upload Service .
3. The Photo Upload Service retrieves the photo metadata from the database, including the photo URL.
4. If the photo is not cached in the CDN, the Photo Upload Service fetches the photo file from the object storage system.


5. The photo file is returned to the client, along with the necessary metadata.
6. The client renders the photo on the user interface.
Caching and content delivery
To improve photo retrieval performance and reduce the load on the backend services, caching
and content delivery mechanisms are employed:
CDN: Frequently accessed photos are cached in the CDN, which serves them from edge locations closer to the users. The
CDN reduces the latency and improves the photo-loading speed for users across different geographic regions.
Application-level caching: The Photo Upload Service can utilize an in-memory caching system (e.g., Redis) to store
frequently accessed photo metadata. Caching photo metadata reduces the number of database queries and improves response
times.
By following this low-level design, the Photo Upload Service ensures efficient and reliable
handling of photo uploads, processing, and retrieval. It leverages asynchronous processing,
caching, and content delivery techniques to provide a seamless and performant user experience.
In the next section, we will explore the low-level design of the News Feed Service, which is
responsible for generating and serving personalized photo feeds to users.
News Feed Service
The News Feed Service is responsible for generating and serving personalized photo feeds to
users based on their follow relationships and engagement activities. Let’s dive into the low-level
design of the News Feed Service . Figure 12.6 illustrates the architecture of the News Feed
Service, showing its interactions with the database, cache, notification service, and WebSocket
Service for efficient feed generation and real-time updates.


Figure 12.6: Low-level design of the News Feed Service
Let us look at the API endpoints exposed by the News Feed Service and the generation process.
The News Feed Service exposes the following API endpoint:
GET /newsfeed/{userId}: Retrieve the personalized news feed for a user:
Request parameters: User ID, pagination token, and limit
Response: List of photo objects in the user’s news feed
Let us dive into the news feed generation process in detail.
Generating news feeds
The News Feed Service generates personalized news feeds for users based on the following
steps:
Follower-followee relationship: The News Feed Service retrieves the list of users that the current user follows from the
database. This information is stored in the Follow table, which contains the follower-followee relationships.
Photo aggregation: For each followed user, the News Feed Service retrieves their recently uploaded photos from the
database. The photo metadata, including the photo ID, user ID, timestamp, and engagement metrics (likes and comments), is
fetched.
Ranking and ordering: The retrieved photos are ranked and ordered based on relevance and freshness. Various ranking
algorithms can be applied, such as chronological ordering, engagement-based ranking, or a combination of factors. The
ranking algorithm takes into account the photo’s timestamp, the user’s affinity with the photo owner, and the overall
engagement received by the photo.


Pagination: To optimize performance and network usage, the news feed is paginated. The API endpoint accepts a
pagination token and a limit to retrieve a subset of the news feed photos. The pagination token represents the last photo ID
or timestamp from the previous page, allowing efficient retrieval of the next set of photos.
Caching: To improve the response time and reduce the load on the backend services, the generated news feed is cached. The
News Feed Service utilizes a distributed caching system (e.g., Redis) to store the news feed data. The cache is updated
whenever new photos are uploaded or engagement activities occur.
Photo deduplication: To prevent duplicate photos from appearing in the news feed, the News Feed Service performs
deduplication. Deduplication can be achieved by maintaining a set of photo IDs that have already been included in the user’s
news feed. Before adding a photo to the news feed, the service checks if the photo ID exists in the deduplication set.
Real-time updates
To provide real-time updates to the news feed, the News Feed Service employs the following
mechanisms:
WebSocket or long polling: The client establishes a persistent connection with the server using WebSocket or long polling
techniques. Whenever a new photo is uploaded by a followed user or significant engagement occurs on a photo in the user’s
news feed, the server pushes the update to the client in real-time. The client receives the update and dynamically updates the
news feed on the user interface.
Notification service integration: The News Feed Service integrates with the Notification service to send push notifications
to users for important updates. When a followed user uploads a new photo or when a photo in the user’s news feed receives
significant engagement, a notification is triggered. The Notification service sends the notification to the user’s device,
prompting them to view the updated news feed.
Feed synchronization
To ensure a consistent news feed experience across multiple devices, the News Feed Service
implements feed synchronization:
Timestamp-based synchronization: Each photo in the news feed is associated with a timestamp indicating when it was
added to the feed. When a user accesses their news feed from a different device, the client sends the timestamp of the last
viewed photo. The News Feed Service uses this timestamp to retrieve and return the photos that have been added to the feed
since the last viewed timestamp.
Incremental updates: Instead of retrieving the entire news feed each time, the client can request incremental updates. The
client sends the last viewed photo ID or timestamp, and the News Feed Service returns only the new or updated photos since
that point. This approach reduces the amount of data transferred and improves the efficiency of feed synchronization.
By following this low-level design, the News Feed Service generates personalized and engaging
photo feeds for users. It leverages ranking algorithms, caching, real-time updates, and feed
synchronization techniques to provide a seamless and up-to-date news feed experience.


In the next section, we will explore the low-level design of the User Service , which manages
user profiles, authentication, and social interactions within the Instagram-like service.
User Service
The User Service is responsible for managing user profiles, authentication, and social
interactions within the Instagram-like service. It handles user registration, login, profile updates,
and follow/unfollow functionality. Let’s explore the low-level design of the User Service. Figure
12.7 illustrates the architecture of the User Service, showing its interactions with the database,
cache, and authentication service for managing user profiles and authentication.
Figure 12.7: Low-level design of the User Service
Let us look at the API endpoints exposed by the User Service, next.
The User Service exposes the following API endpoints:
POST /users: Create a new user account:
Request body: User information, such as username, email, password, and profile picture
Response: User ID and authentication token
POST /users/login: Authenticate the user and generate an authentication token:
Request body: User credentials (email/username and password)
Response: Authentication token
GET /users/{userId}: Retrieve user profile information:


Request parameters: User ID
Response: User profile data, including username, profile picture, bio, and follower/following counts
PUT /users/{userId}: Update user profile information:
Request parameters: User ID
Request body: Updated user profile data
Response: Success status
POST /users/{userId}/follow: Follow a user:
Request parameters: User ID of the user to follow
Response: Success status
DELETE /users/{userId}/follow: Unfollow a user:
Request parameters: User ID of the user to unfollow
Response: Success status
Now that we have looked at the different APIs exposed by the service, let us understand the user
registration and authentication flow.
User registration and authentication
The following sequence diagram depicts the process of user registration and authentication,
showing the steps involved in creating a new account and logging in to an existing account.


Figure 12.8: User registration and authentication flow sequence diagram
Let us understand what is happening in the preceding sequence diagram. When a user registers
for the Instagram-like service or logs in, the following occurs:
1. The client sends a POST request to the /users or /users/login endpoints with the user’s information or credentials.
2. The User Service receives the request and performs the following steps:
For registration, it does the following:
Validates the user input data
Checks whether the username or email is already taken
Hashes the password securely
Generates a unique user ID
Stores the user information in the database


For login, it does the following:
Verifies the provided credentials against the stored user data
If the credentials are valid, generate an authentication token (e.g., JWT)
3. The User Service returns the user ID and authentication token to the client.
4. The client stores the authentication token securely and includes it in subsequent requests to authenticate the user.
When a user updates their profile information, the client sends a PUT request to the
/users/{userId} endpoint with the updated profile data. The User Service validates the request
and updates the user’s profile in the database and the updated profile information is returned to
the client.
Let us look at the flow of events when users follow/unfollow each other in our service.
Follow/unfollow functionality
The following sequence diagram illustrates the step-by-step process and interactions between
system components during the follow and unfollow operations, including request validation,
database checks, and updates.




Figure 12.9: The flow of events for user follow/unfollow interactions
When a user follows or unfollows another user, the following takes place:
1. The client sends a POST or DELETE request to the /users/{userId}/follow endpoint with the user ID of the user to
follow/unfollow.
2. The User Service validates the request and checks whether the user is authorized to perform the action.
3. For a follow request: The User Service creates a new entry in the Follow table, establishing the follower-followee
relationship. The follower and following counts of both users are incremented.
4. For an unfollow request: The User Service removes the corresponding entry from the Follow table. The follower and
following counts of both users are decremented.
5. The User Service returns a success status to the client.
We have explored the different flows of user interaction in our service, above. Now, let us
understand the different modules that can help our User Service become performant and more
useful:
Caching and optimization: To improve the performance of the User Service and reduce the load on the database, user
profile data is cached using a distributed caching system (e.g., Redis). Frequently accessed user profiles, such as those of
popular users or users with a high number of followers, are cached to reduce the number of database queries. The cache is
updated whenever a user’s profile is modified or when the follower/following counts change.
Notifications and feed updates: The User Service integrates with the Notification service and News Feed Service to handle
relevant updates. When a user is followed by another user, the User Service sends a message to the Notification service to
generate a notification for the followed user. The User Service also publishes an event to the News Feed Service to update
the follower’s news feed with the newly followed user’s photos.
Security and privacy: The User Service implements security and privacy measures to protect user data. User passwords are
hashed securely using a strong hashing algorithm (e.g., bcrypt) before storing them in the database. Authentication tokens
are generated using secure methods (e.g., JWT) and have an expiration time to prevent unauthorized access. User data is
encrypted at rest and in transit to ensure confidentiality. Access controls are enforced to ensure that users can only modify
their own profiles and follow/unfollow other users within the defined permissions.
By following this low-level design, the User Service provides a secure and efficient way to
manage user profiles, authentication, and social interactions within the Instagram-like service. It
leverages caching, event-driven architecture, and security best practices to ensure a seamless user
experience.
We will now discuss some additional considerations to further enhance our service.
Additional considerations


When designing and implementing the Instagram-like service, there are several additional
considerations and best practices to keep in mind. These considerations ensure the system is
scalable, maintainable, and aligned with business requirements.
Let’s explore some of these key aspects.
Hashtag functionality:
Implement a hashtag system to allow users to categorize and discover photos based on specific topics or themes
Store hashtags as separate entities in the database, with a many-to-many relationship with photos
Provide API endpoints to search for photos based on hashtags and retrieve trending hashtags
Update the Photo Upload Service to extract hashtags from photo captions and associate them with the
corresponding photos
Explore and discover features:
Implement explore and discover features to help users find new and interesting content
Develop algorithms to suggest personalized recommendations based on user preferences, interests, and
engagement history
Create curated collections or featured content showcasing popular or trending photos
Provide a search functionality to allow users to find photos, users, and hashtags based on keywords
Spam and abuse prevention:
Implement measures to detect and prevent spam, abuse, and inappropriate content
Develop algorithms to identify and flag suspicious activities, such as automated likes, comments, or
follow/unfollow patterns
Employ content moderation techniques, such as machine learning-based image classification, to detect and
remove offensive or explicit content
Provide users with options to report and block abusive accounts or content
Internationalization and localization:
Design the system to support internationalization and localization
Allow users to select their preferred language and locale settings
Store user-generated content, such as captions and comments, in the original language and provide translation
options if required
Monetization and business model:
Develop a monetization strategy and business model for the Instagram-like service


Implement features for sponsored content, promoted posts, or advertising to generate revenue
Provide tools for businesses to create and manage their profiles, track metrics, and engage with their audience
Explore partnerships and integrations with e-commerce platforms to enable product tagging and in-app
purchases
Monitoring, metrics, and observability:
Implement a comprehensive logging system using a centralized log aggregator (e.g., ELK stack or Splunk) to
collect and analyze logs from all microservices and components
Set up a metrics collection and visualization system (e.g., Prometheus and Grafana) to track key performance
indicators (KPIs), system health, and business metrics across the entire Instagram-like service
Utilize distributed tracing (e.g., Jaeger or Zipkin) to monitor and analyze request flows across microservices,
helping to identify performance bottlenecks and optimize system interactions
Establish an alerting system with defined thresholds for critical metrics, and implement automated notifications
(e.g., PagerDuty or OpsGenie) to ensure timely responses to potential issues or anomalies in the system
By considering these additional aspects and best practices, the Instagram-like service can be
designed and implemented to be feature-rich, user-friendly, and aligned with business goals. It
ensures a scalable and engaging platform that meets the evolving needs of users and
stakeholders.
Summary
In this chapter, we have explored the system design of an Instagram-like service, covering
various aspects such as functional and non-functional requirements, data modeling, scalability
considerations, and architectural components. We have delved into the high-level design, laying
out the overall architecture and the interaction between different services and components.
Furthermore, we have examined the low-level design of key services, including the Photo
Upload Service, News Feed Service, and User Service. Each service has been designed to handle
specific functionalities and work together to deliver a seamless user experience. We have
discussed data storage, caching mechanisms, real-time updates, and performance optimization
techniques to ensure scalability and efficiency.
Throughout the chapter, we have emphasized the importance of scalability, performance, and
user engagement. The system has been designed to handle a large number of users, photos, and
interactions by leveraging horizontal scaling, data partitioning, and distributed processing.


Caching and content delivery networks have been employed to improve response times and
reduce latency.
Some potential future considerations and enhancements for the Instagram-like service could
include the following:
Implementing advanced features such as stories, live streaming, and augmented reality filters to enhance user engagement
and creativity
Exploring machine learning and computer vision techniques to improve content recommendations, facial recognition, and
object detection
Integrating with social commerce platforms to enable seamless product tagging, in-app purchases, and influencer marketing
We can thus say that designing an Instagram-like service requires careful consideration of
various aspects, from functional requirements to scalability and performance. By following the
principles and best practices outlined in this chapter, developers and system architects can create
a robust and scalable platform that meets the needs of users and stands the test of time.
In the next chapter, we will look at the system design of another popular service: Google Docs.

## Examples & Scenarios

- The system should support various photo formats (e.g., JPEG and PNG) and perform necessary processing and
compression
Users should have the ability to apply filters, add captions, and tag other users in their photos
The uploaded photos should be associated with the user’s profile and stored in a scalable and reliable storage
system
News feed:
The news feed is a crucial feature that displays a personalized stream of photos from the users a person follows
The system should generate and serve the news feed in real-time, considering factors such as photo timestamps,
user preferences, and engagement metrics
The news feed should support infinite scrolling, allowing users to load more photos as they scroll down

- Stores photos in an object storage system (e.g., Amazon S3)
News Feed Service :
Generates and serves personalized news feeds for users
Aggregates photos from followed users and applies ranking algorithms
Utilizes caching to improve performance and reduce latency
User Service:
Manages user profiles, authentication, and authorization
Handles user-related operations such as sign-up, login, and profile updates
Stores user data in a database (e.g., MySQL or PostgreSQL)
Interaction service:

- Utilizes a message queue (e.g., Apache Kafka) for asynchronous processing

- Relational database (e.g., MySQL or PostgreSQL):
Stores structured data such as user profiles, photo metadata, comments, likes, and hashtags
Provides ACID properties and supports complex queries
NoSQL database (e.g., Apache Cassandra or MongoDB):
Handles high-volume write operations for user interactions and real-time data
Offers scalability and eventual consistency
Caching (e.g., Redis or Memcached):
Caches frequently accessed data such as news feed photos, user profiles, and trending hashtags
Reduces the load on databases and improves response times
Object storage: Photos and videos will be stored in an object storage system (e.g., Amazon S3) that provides scalable and

- locations, a CDN (e.g., Amazon CloudFront) will be utilized. The CDN caches and serves content from edge locations
closer to the users, reducing latency and improving the overall user experience.
Asynchronous processing: Resource-intensive tasks, such as photo processing and notifications, will be handled
asynchronously using message queues (e.g., Apache Kafka) and background workers. This ensures that the main application
remains responsive and can handle a high volume of requests.
Security and privacy: Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords, will be hashed and
stored securely. Data encryption will be applied to protect user information both in transit and at rest. Rate limiting and
throttling mechanisms will be put in place to prevent abuse and ensure fair usage of the service.
This high-level design provides an overview of the key components and their interactions in the

- III. Uploads the photo file to the object storage system (e.g., Amazon S3).
IV. Initiates asynchronous processing tasks for photo compression, resizing, and thumbnail generation.
V. Returns the uploaded photo details, including the photo ID and URL, to the client.
The client receives the response and updates the user interface accordingly.
To optimize the photo upload process and ensure a responsive user experience, photo processing
tasks are performed asynchronously:
1. After the photo is uploaded to the object storage, the Photo Upload Service sends a message to a message queue (e.g.,
Apache Kafka) containing the photo ID and processing instructions.
2. Background workers consume the messages from the message queue and perform the following tasks:
I. Compress the photo to optimize storage and network usage.

- Application-level caching: The Photo Upload Service can utilize an in-memory caching system (e.g., Redis) to store
frequently accessed photo metadata. Caching photo metadata reduces the number of database queries and improves response
times.
By following this low-level design, the Photo Upload Service ensures efficient and reliable
handling of photo uploads, processing, and retrieval. It leverages asynchronous processing,
caching, and content delivery techniques to provide a seamless and performant user experience.
In the next section, we will explore the low-level design of the News Feed Service, which is
responsible for generating and serving personalized photo feeds to users.
News Feed Service
The News Feed Service is responsible for generating and serving personalized photo feeds to

- News Feed Service utilizes a distributed caching system (e.g., Redis) to store the news feed data. The cache is updated
whenever new photos are uploaded or engagement activities occur.
Photo deduplication: To prevent duplicate photos from appearing in the news feed, the News Feed Service performs
deduplication. Deduplication can be achieved by maintaining a set of photo IDs that have already been included in the user’s
news feed. Before adding a photo to the news feed, the service checks if the photo ID exists in the deduplication set.
Real-time updates
To provide real-time updates to the news feed, the News Feed Service employs the following
mechanisms:
WebSocket or long polling: The client establishes a persistent connection with the server using WebSocket or long polling
techniques. Whenever a new photo is uploaded by a followed user or significant engagement occurs on a photo in the user’s

- If the credentials are valid, generate an authentication token (e.g., JWT)
3. The User Service returns the user ID and authentication token to the client.
4. The client stores the authentication token securely and includes it in subsequent requests to authenticate the user.
When a user updates their profile information, the client sends a PUT request to the
/users/{userId} endpoint with the updated profile data. The User Service validates the request
and updates the user’s profile in the database and the updated profile information is returned to
the client.
Let us look at the flow of events when users follow/unfollow each other in our service.
Follow/unfollow functionality
The following sequence diagram illustrates the step-by-step process and interactions between

- profile data is cached using a distributed caching system (e.g., Redis). Frequently accessed user profiles, such as those of
popular users or users with a high number of followers, are cached to reduce the number of database queries. The cache is
updated whenever a user’s profile is modified or when the follower/following counts change.
Notifications and feed updates: The User Service integrates with the Notification service and News Feed Service to handle
relevant updates. When a user is followed by another user, the User Service sends a message to the Notification service to
generate a notification for the followed user. The User Service also publishes an event to the News Feed Service to update
the follower’s news feed with the newly followed user’s photos.
Security and privacy: The User Service implements security and privacy measures to protect user data. User passwords are
hashed securely using a strong hashing algorithm (e.g., bcrypt) before storing them in the database. Authentication tokens
are generated using secure methods (e.g., JWT) and have an expiration time to prevent unauthorized access. User data is

- Implement a comprehensive logging system using a centralized log aggregator (e.g., ELK stack or Splunk) to
collect and analyze logs from all microservices and components
Set up a metrics collection and visualization system (e.g., Prometheus and Grafana) to track key performance
indicators (KPIs), system health, and business metrics across the entire Instagram-like service
Utilize distributed tracing (e.g., Jaeger or Zipkin) to monitor and analyze request flows across microservices,
helping to identify performance bottlenecks and optimize system interactions
Establish an alerting system with defined thresholds for critical metrics, and implement automated notifications
(e.g., PagerDuty or OpsGenie) to ensure timely responses to potential issues or anomalies in the system
By considering these additional aspects and best practices, the Instagram-like service can be
designed and implemented to be feature-rich, user-friendly, and aligned with business goals. It

