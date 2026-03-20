# Chapter 14: Designing a Service Like Netflix

> Source: System Design Guide for Software Professionals, Chapter 18, Pages 331-364

## Key Concepts

- 14
Designing a Service Like Netflix
In today’s digital age, video streaming services have revolutionized the way we consume
entertainment. Netflix, one of the pioneers in this industry, has set a high
- Users should be able to create new accounts by providing necessary information, such as email, password, and
profile details
The system should securely store user credentials and authenticate users up

## Content

14
Designing a Service Like Netflix
In today’s digital age, video streaming services have revolutionized the way we consume
entertainment. Netflix, one of the pioneers in this industry, has set a high bar for delivering a
seamless and personalized video streaming experience to millions of users worldwide. Designing
a service such as Netflix requires careful consideration of various aspects, including scalability,
performance, user experience, and reliability.
In this chapter, we will delve into the system design principles and components necessary to
build a robust and scalable video streaming service such as Netflix. To understand how to design
a service such as Netflix, we will cover the following topics:
Functional requirements
Non-functional requirements
Designing the data model
Scale calculations
High-level design
Low-level design
By the end of this chapter, you will have a comprehensive understanding of the building blocks
and design decisions involved in creating a service such as Netflix. Let’s begin by examining the
functional requirements that define the core features and capabilities of a Netflix-like service.
Functional requirements
Before we embark on designing our Netflix-like service, it’s crucial to define the functional
requirements that specify what our system should be capable of doing. These requirements will
guide our design decisions and ensure that we build a platform that meets the needs and
expectations of our users.
Let’s outline the key functional requirements:
User registration and authentication:


Users should be able to create new accounts by providing necessary information, such as email, password, and
profile details
The system should securely store user credentials and authenticate users upon login
User sessions should be managed efficiently to allow seamless access to the service across different devices
Content browsing and search:
Users should be able to browse and explore a vast catalog of movies, TV shows, and other video content
The system should provide a user-friendly interface to navigate through different categories, genres, and
recommendations
Users should be able to search for specific titles, actors, directors, or keywords to find desired content quickly
Video playback and streaming:
Users should be able to play videos seamlessly, with minimal buffering and high-quality streaming
The system should support various video resolutions and adapt to the user’s network bandwidth for an optimal
playback experience
Users should have control over video playback, including play, pause, seek, and resume functionalities
User profiles and preferences:
Each user should have a personalized profile that captures their viewing preferences, watch history, and ratings
There should be multiple profiles supported per account so that each profile can be personalized separately
Users should be able to update their profile information, manage their viewing preferences, and set parental
controls
Recommendations and personalization:
Based on a user’s preferences, their history of watched content, and the viewing history of similar users, the
system should provide content recommendations
Recommendations should be generated using sophisticated algorithms that analyze user data and identify similar
content
The system should continuously learn and adapt to user feedback to refine and improve the accuracy of
recommendations over time
Watchlist and viewing history:
Users should be able to add titles to their watchlist for future viewing and easily access their viewing history
The system should sync the watchlist and viewing history across different devices, allowing users to seamlessly
continue watching from where they left off


Offline viewing:
The system should support offline viewing functionality, allowing users to download selected titles and watch
them without an internet connection.
Downloaded content should be securely stored on the user’s device and have an expiration mechanism to comply
with licensing agreements.
These functional requirements lay the foundation for our Netflix-like service, defining the core
features and capabilities that our system must deliver to provide an immersive and personalized
video streaming experience to our users.
In the next section, we’ll explore the non-functional requirements that ensure our service remains
scalable, reliable, and performant while handling a large user base and streaming massive
amounts of video content.
Non-functional requirements
While functional requirements define what our Netflix-like service should do, non-functional
requirements specify how the system should perform and behave under various conditions.
These requirements are crucial for ensuring a smooth, reliable, and efficient streaming
experience for our users. Let’s discuss the key non-functional requirements:
Scalability and performance:
The system should be designed to handle a large number of concurrent users and a growing library of video
content
It should be able to scale horizontally by adding more servers to handle increased traffic and storage needs
The architecture should allow the efficient distribution of content across multiple servers and data centers to
ensure fast and reliable streaming
Caching mechanisms should be employed at various levels to reduce latency and improve performance
Availability and reliability:
The system should be highly available, ensuring minimal downtime and quick recovery from failures
It should be designed with redundancy and fault tolerance in mind, using techniques such as data replication,
load balancing, and automatic failover
The system should be able to handle server failures, network outages, and data center disasters without
significant impact on user experience
Regular data backups and disaster recovery mechanisms should be in place to prevent data loss and ensure
business continuity


Content delivery and streaming quality:
The system should leverage a Content Delivery Network (CDN) to efficiently deliver video content to users
across different geographical locations
Depending on the user’s device and its location, our system should dynamically adjust video quality by
supporting adaptive bitrate streaming
The streaming infrastructure should be optimized to minimize buffering, reduce latency, and provide a seamless
playback experience
The system should handle a large number of concurrent streams and support various video formats and codecs
By addressing these non-functional requirements, our Netflix-like service will be able to deliver
a high-quality, reliable, and scalable streaming experience to our users. These requirements will
shape our architectural decisions and guide us in designing a robust and efficient system.
Let’s now examine the data model that will serve as the backbone of our service, defining the
entities and relationships necessary to support the functionality of our Netflix-like platform.
Designing the data model
Designing an efficient and scalable data model is essential for our Netflix-like service. The data
model defines the structure and relationships of the entities involved in the system, ensuring that
data is stored and retrieved effectively. Let’s explore the key entities and their relationships:
User: The central entity, representing a customer, which can have multiple profiles associated with it, allowing for
personalized experiences within a single account
Profile: Linked to a user, this entity represents individual viewing preferences and settings and is associated with the
WatchHistory, Watchlist, and Rating entities to track personalized interactions with content
Movie: A standalone content entity that has its own metadata, and it can be part of a user’s WatchHistory and
Watchlist and receive Ratings from Profiles
TVShow: Represents a series that contains multiple Episodes, has its own metadata, and, like Movies, can be part of
WatchHistory, Watchlist, and receive Ratings
Episode: Belongs to a TVShow and has its own metadata, allowing for granular tracking of viewing progress within a series
through the WatchHistory entity
WatchHistory: Tracks the viewing activity of a Profile, linking to either a Movie, TVShow, or specific Episode,
enabling features such as resuming playback and viewing statistics
Watchlist: Allows Profiles to save Movies or TVShows for future viewing, supporting content discovery and
personalized recommendations


Rating: Enables Profiles to provide feedback on Movies or TVShows, which can be used for personalized
recommendations and overall content quality assessment
ContentMetadata: Stores technical details about the content (Movie, TVShow, or Episode), such as video quality and
file size, supporting adaptive streaming and content delivery optimization
These entities and their relationships form a comprehensive data model that supports the core
functionalities of a Netflix-like streaming service, enabling personalized user experiences,
content management, and interaction tracking.
Figure 14.1’s entity relationship diagram illustrates the comprehensive data model for a Netflixlike streaming service, showcasing the key entities such as User, Profile, Movie, TVShow, Episode,
WatchHistory, Watchlist, Rating, and ContentMetadata, along with their attributes and the
relationships between them.
Figure 14.1: An overview of the entity relationship diagram for Netflix


Let’s now discuss the many-many, one-many, and many-one relationships between the different
entities in this data model design.
Relationships
Lets us highlight the different one-to-many relationships in our data model.
OnetoMany:
User to Profile: A user can have multiple profiles
Movie to ContentMetadata: A movie can have multiple versions of metadata (e.g., different video qualities
or languages)
TVShow to Episode: A TV show can have multiple episodes
TVShow to ContentMetadata: A TV show can have multiple versions of metadata
Episode to ContentMetadata: An episode can have multiple versions of metadata
Profile to WatchHistory: A profile can have multiple watch history entries
Profile to Watchlist: A profile can have multiple watchlist entries
Profile to Rating: A profile can have multiple ratings
The preceding data model captures the essential entities and relationships required for our
Netflix-like service. It allows us to store and manage user information, profiles, movies, TV
shows, episodes, watch history, watchlists, ratings, and content metadata.
By designing the data model in a structured and efficient manner, we can ensure that our system
can handle the storage and retrieval of large amounts of data while supporting the key
functionalities of our streaming platform.
In the next section, we’ll perform capacity estimation and scaling calculations to determine the
storage, bandwidth, and processing requirements of our Netflix-like service, based on the
expected user base and usage patterns.
Scale calculations
To design a scalable Netflix-like service, it’s crucial to estimate the storage, bandwidth, and
processing requirements, based on the expected user base and usage patterns. These estimations
will help us determine the necessary infrastructure and resources needed to support the service.


Let’s perform some capacity estimation and scaling calculations by making some basic
assumptions.
Here are some of the assumptions we will make while designing our Netflix-like service.
Assumptions
The total number of users: 50 million
The average number of active users per day: 10 million
The average number of videos watched per user per day: 3
The average video duration: 1.5 hours
The average video file size (HD quality): 3 GB
Next, based on these assumptions, let’s estimate the storage for our service
Storage estimation
Storage will typically include both data and metadata storage. In our case, we have videos,
thumbnails, users, and so on, so let’s try to estimate, based on the preceding assumptions, how
much storage we will need to make our service functional:
Video storage:
The total number of movies: 10,000
The total number of TV shows: 5,000
The average number of episodes per TV show: 30
The total number of episodes: 5,000 × 30 = 150,000
The total video files: 10,000 (movies) + 150,000 (episodes) = 160,000
The total video storage: 160,000 × 3 GB = 480 PB
User and metadata storage:
User data: 50 million × 1 KB = 50 GB
Profile data: 50 million × 5 profiles × 1 KB = 250 GB
Watch history and ratings data: 50 million × 5 profiles × 1 MB = 250 TB
Content metadata: 160,000 × 10 KB = 1.6 GB
Total storage: 480 PB (video) + 250 TB (user and metadata) ≈ 480 PB


We now have a good estimate of the storage needs, so we will move on to bandwidth
estimations.
Bandwidth estimation
One of the ways Netflix stands out from the competition is its seamless user experience, made
possible due to accurate bandwidth estimation and management. We will attempt to estimate our
bandwidth needs to support our users.
The daily video streaming bandwidth:
The average video file size: 3 GB
The average number of videos streamed per day: 10 million users × 3 videos = 30 million
The daily streaming bandwidth: 30 million × 3 GB = 90 PB/day
Peak bandwidth requirements:
Peak concurrent users: 1 million
Peak bandwidth: 1 million × 3 GB / 1.5 hours = 2 TB/s
Processing estimation
Netflix is run on different systems that range from smartphones and tablets to browsers and
television sets. For each of these systems, the same movie or content is rendered, stored, and
transferred differently to make the experience compelling. Therefore, we need to perform some
pre- and post-processing of content, which is very typical for video streaming services such as
Netflix. Let’s estimate the scale for these:
Video encoding and transcoding:
The number of new videos added per day: 100
The average video duration: 1.5 hours
The encoding time: 1.5 hours × 5 (multiple bitrates) = 7.5 hours per video
Daily encoding processing: 100 videos × 7.5 hours = 750 hours
Recommendation processing:
The number of active users per day: 10 million
The recommendation requests per user per day: 10


The total recommendation requests per day: 10 million × 10 = 100 million
The processing time per request: 100 ms
Daily recommendation processing: 100 million × 100 ms = 2.7 hours
So far, we have discussed different scale calculations for our service, but there are some inherent
scaling considerations that we would like to explicitly spell out. The following are some of the
scaling considerations:
Horizontal scaling:
Use load balancers to distribute traffic across multiple application servers
Scale the number of application servers, based on the incoming traffic and processing requirements
Utilize auto-scaling techniques to dynamically adjust the number of servers, based on demand
Caching:
Implement caching at various levels (e.g., CDN, application server, and database) to reduce the load on backend
systems and improve performance
Cache frequently accessed data such as popular videos, user profiles, and recommendations
CDN:
Utilize a CDN to distribute video content globally and reduce latency for users.
Store video files on CDN servers located closer to the users for faster streaming.
Database sharding and replication:
Shard the database to distribute data across multiple servers and handle increased storage and traffic
Replicate data to ensure high availability and fault tolerance
These estimations provide a starting point for designing the infrastructure and scaling our
Netflix-like service. It’s important to note that these numbers can vary, based on actual usage
patterns, video quality, and the growth of the user base. Regular monitoring, performance
analysis, and capacity planning should be conducted to adapt to changing requirements.
In the next section, we’ll propose a high-level architecture that takes into account these capacity
estimations and incorporates the necessary components and services to build a scalable and
efficient video streaming platform.


High-level design
Now that we have a clear understanding of the functional and non-functional requirements, data
model, and capacity estimations, let’s design a high-level architecture for our Netflix-like
service. The architecture should be scalable, reliable, and efficient in handling the massive
amount of video content and user traffic. Figure 14.2 shows the high-level architecture of our
service. Let’s dive into the flow and understand this architecture in detail.
Figure 14.2: The Netflix architecture diagram
This diagram illustrates the comprehensive architecture of a Netflix-like streaming service,
showcasing the flow from client applications through various components, including the API
gateway, application servers, specialized services, CDN, storage systems, and supporting
infrastructure such as a Message Queue and Monitoring and Logging.
At the heart of our architecture are the client applications. These include the web application,
mobile applications (iOS and Android), smart TV applications, and gaming console applications.
These client applications serve as the primary interface for users to interact with our streaming
service.
When a user makes a request through one of the client applications, it first reaches the API
gateway. The API gateway acts as the entry point for all client requests and plays a crucial role
in the system. It handles request routing, authentication, and rate limiting, ensuring that only
authorized requests are forwarded to the appropriate backend services. The API gateway also
provides a unified API interface, making it easier for the front-end applications to communicate
with the various backend components.


Behind the API gateway, we have the application servers. These servers handle the business
logic and processing of client requests. They communicate with various backend services and
databases to retrieve and manipulate data as needed. The application servers are designed to scale
horizontally, based on traffic and processing requirements, ensuring that the system can handle a
growing user base and increasing demands.
One of the critical components of our architecture is the Video Service. This service is
responsible for handling video storage, encoding, and streaming. When a user uploads a video or
when new content is added to the platform, the Video Service stores the video files in a
distributed storage system. It then encodes the videos into multiple formats and bitrates to
support adaptive streaming. Adaptive streaming allows the video quality to adjust dynamically,
based on the user’s network conditions, providing a smooth and uninterrupted viewing
experience.
To efficiently deliver video content to users, the Video Service integrates with a CDN. The CDN
distributes video content globally, bringing it closer to the users and reducing latency. It caches
video files on servers located strategically around the world, allowing users to stream videos
from a server that is geographically close to them. This significantly improves streaming
performance and ensures a high-quality user experience.
Next, let’s explore the User Service. This service manages user authentication, authorization,
and profile data. When a user signs up or logs in to the platform, the User Service handles the
authentication process. It securely stores user information, such as credentials and profile data, in
a database. The User Service also manages user permissions and access controls, ensuring that
users can only access the content and features they are authorized to use.
To provide personalized video recommendations to users, we have the Recommendation
Service. This service is responsible for generating tailored suggestions based on a user’s viewing
history, preferences, and behavior. It analyzes various data points, such as the videos a user has
watched, their ratings, and their interactions with the platform. By leveraging machine learning
algorithms, the Recommendation Service can identify patterns and make accurate
recommendations, enhancing the user experience and encouraging user engagement.
Another essential component of our architecture is the Search Service. With a vast library of
video content, it’s crucial to provide users with a powerful search functionality. The Search
Service indexes video metadata, including titles, descriptions, genres, and tags, making it easy
for users to find the content they are looking for. It supports features such as autocomplete and


fuzzy matching, ensuring that users can quickly discover relevant videos even if they don’t
remember the exact title or spelling.
To handle user subscriptions, billing, and payments, we have the Billing and Subscription
Service. This service integrates with payment gateways and manages recurring billing for users
who have subscribed to our platform. It provides APIs for subscription management, allowing
users to upgrade, downgrade, or cancel their subscriptions. The Billing and Subscription Service
also generates invoices and handles payment processing securely.
Monitoring and analyzing user behavior and system performance is crucial for making datadriven decisions and ensuring a smooth user experience. The Analytics and Reporting Service
takes care of collecting and analyzing various metrics and user behavior data. It generates
insights and reports that help a business make informed decisions, such as identifying popular
content, optimizing recommendations, and improving the overall service.
To support the communication and coordination between different services, we utilize a
Message Queue. The Message Queue facilitates asynchronous communication and enables an
event-driven architecture. It decouples services, allowing them to communicate and exchange
data without direct dependencies. For example, when a new video is uploaded, the Video Service
can send an encoding job to the Message Queue, which can then be picked up and processed by a
separate encoding service. This ensures that tasks are processed efficiently and reliably, even
under a high load.
Lastly, to ensure the reliability and stability of our system, we implement comprehensive
Monitoring and Logging. We collect logs and metrics from all components of the architecture
and centralize them for analysis and troubleshooting. This allows us to quickly identify and
resolve any issues that may arise. We also set up dashboards and alerts to provide real-time
visibility into the system’s health and performance.
In summary, our high-level architecture is designed to handle the scale and complexity of a
Netflix-like streaming service. The client applications interact with the API gateway, which
routes requests to the appropriate backend services. The Video Service handles video storage,
encoding, and streaming, while the User Service manages user authentication and profile data.
The Recommendation Service provides personalized video suggestions, and the Search Service
enables users to find content easily. The Billing and Subscription Service handles payments and
subscriptions, and the Analytics and Reporting Service provides valuable insights. The Message


Queue facilitates communication between services, and Monitoring and Logging ensure the
system’s reliability and performance.
In the next sections, we’ll dive deeper into the design and implementation details of low-level
system design and focus on some key components, such as the Video Service, User Service,
Recommendation Service, and CDN.
Low-level system design
In this section, we will pick some of the main microservices in our system and try to delve into
their APIs and design. Note that we are not going to cover each part of our system, just some of
the main services to give you a feel for the design and implementation details.
Video Service
The Video Service is a critical component of our Netflix-like architecture, responsible for
handling video storage, encoding, and streaming. Let’s dive into the design and implementation
details of the Video Service.
Figure 14.3 shows the high-level architecture of the service.
Figure 14.3: The Video Service architecture
Let’s first discuss the API endpoints exposed by the service:


POST /videos: Upload a new video file:
Request body: The video file and metadata (title, description, duration, etc.).
Response: The video ID and status.
GET /videos/{videoId}: Retrieve video metadata:
Response: Video metadata (title, description, duration, etc.).
GET /videos/{videoId}/stream: Stream the video content:
Request parameters: Video ID, quality/bitrate, offset.
Response: Video chunk or segment.
Now that we have discussed the API endpoints, let’s look at the different workflows for this
service. We will use sequence diagrams to explain these.
Video upload and storage
Figure 14.4 shows the video upload and storage workflow sequence diagram.
Figure 14.4: Video upload and storage
Here is the flow:
1. When a new video is uploaded, the Video Service receives the video file and metadata through the API endpoint.


2. The video file is stored in a distributed storage system, such as Amazon S3 or Hadoop Distributed File System (HDFS),
for scalable and durable storage.
3. The video metadata is stored in a database, such as PostgreSQL or Cassandra, along with a reference to the video file
location in the distributed storage.
Let’s now look at video encoding and transcoding workflows.
Video encoding and transcoding
Figure 14.5 shows the video encoding and transcoding sequence diagram.
Figure 14.5: Video encoding and transcoding
Here is the flow:
1. After a video is uploaded, the Video Service triggers a video encoding job to convert the video into multiple formats and
bitrates.
2. The encoding job can be handled by a separate encoding service or a cluster of encoding workers.


3. The video is transcoded into different formats (e.g., MP4, HLS, and DASH) and bitrates to support adaptive streaming and
various client devices.
4. The encoded video files are stored in the distributed storage system, and their locations are updated in the video metadata
database.
Next, let’s look at the flow for the video streaming aspect of our service.
Video streaming
Figure 14.6 shows the video streaming sequence diagram.
Figure 14.6: The video streaming sequence diagram
Here is the flow:
1. When a user requests to stream a video, the client application sends a request to the Video Service API endpoint.
2. The Video Service retrieves the video metadata from the database and determines the appropriate video format and bitrate,
based on the client’s capabilities and network conditions.
3. The Video Service generates a streaming URL or manifest file (e.g., an HLS playlist or DASH manifest) that contains the
information needed by the client to stream the video.
4. The client application uses the streaming URL or manifest file to request video chunks or segments from the CDN, or
directly from the Video Service.


5. The CDN or Video Service serves the video chunks or segments to the client application, which plays them in the correct
order to provide a continuous streaming experience.
Next, let’s look at the flow for content delivery and appropriate caching.
Caching and content delivery
Figure 14.7 shows the sequence diagram for content delivery and appropriate caching.
Figure 14.7: The content delivery sequence diagram


Here is the flow:
1. To improve streaming performance and reduce latency, the Video Service integrates with a CDN.
2. The CDN caches video chunks or segments at edge locations closer to the users, reducing the distance between the user and
the video content.
3. The Video Service can also implement caching mechanisms, such as Redis or Memcached, to store frequently accessed
video metadata and reduce the load on the database.
The Video Service plays a vital role in the Netflix-like architecture, enabling efficient video
storage, encoding, and streaming. By leveraging distributed storage, encoding workflows, and
CDNs, the Video Service ensures a seamless and high-quality video streaming experience for
users.
In the next section, we’ll explore the User Service, which handles user authentication, profile
management, and personalization aspects of our Netflix-like platform.
User Service
The User Service is responsible for managing user authentication, authorization, and profile data
in our Netflix-like platform. It handles user registration, login, and profile management
functionalities. Figure 14.8 shows the User service at a very high level.
Figure 14.8: The User service
Let’s explore the design and implementation details of the User Service. We’ll begin by checking
the API endpoints of the User service:
POST /users: Create a new user account:
Request body: User information (email, password, name, etc.)


Response: User ID and authentication token
POST /users/login: User login:
Request body: User credentials (email and password)
Response: An authentication token
GET /users/{userId}: Retrieve user profile information:
Response: User profile data (name, email, profile picture, etc.)
PUT /users/{userId}: Update user profile information:
Request body: Updated user profile data
Response: Updated user profile
POST /users/{userId}/profiles: Create a new profile for a user:
Request body: Profile information (name, avatar, preferences, etc.)
Response: A profile ID
GET /users/{userId}/profiles: Retrieve all profiles of a user:
Response: A list of user profiles
PUT /users/{userId}/profiles/{profileId}: Update a user profile:
Request body: Updated profile information
Response: An updated profile
Let’s next look at how we can design several workflows for this service, starting with the user
authentication and authorization flow.
User authentication and authorization
Figure 14.9 shows the user authentication and authorization flow for Netflix.


Figure 14.9: Authentication and authorization flow
Here is the flow:
1. When a user registers or logs in, the User Service verifies the provided credentials against the user database.
2. Upon successful authentication, the User Service generates an authentication token (e.g., JWT) that contains the user ID and
other relevant information.


3. The authentication token is returned to the client application, which includes it in subsequent requests to authenticate and
authorize the user.
4. The User Service validates the authentication token for each incoming request to ensure that the user is authenticated and
authorized to access the requested resources.
Next, let’s look at the profile management workflow.
User profile management
Figure 14.10 shows the user profile management sequence diagram.


Figure 14.10: The user profile management sequence diagram
Here is the flow:
1. The User Service allows users to create and manage multiple profiles within their account.
2. Each profile represents a separate viewing experience, with its own preferences, watch history, and recommendations.
3. The User Service provides APIs to create, retrieve, update, and delete user profiles.
4. Profile information, such as name, avatar, and preferences, is stored in the user database.
Now that we have looked at some workflows, we should also look at what other services will the
user service integrate with.
The User Service integrates with other services in the Netflix-like architecture to provide
personalized experiences. It communicates with the Recommendation Service to retrieve
personalized video recommendations, based on user preferences and viewing history. The User
Service interacts with the Video Service to retrieve user-specific video metadata, such as watch
history and favorites. It collaborates with the Billing and Subscription Service to manage user
subscriptions and payment information.
Next, we will cover what database, caching, and security are needed for our service.
Database and caching
The User Service uses a relational database, such as PostgreSQL or MySQL, to store user and
profile information. The database schema includes tables for users, profiles, preferences, and
authentication tokens. To improve performance and reduce database load, the User Service can
employ caching mechanisms, such as Redis or Memcached, to store frequently accessed user and
profile data.
Let’s look at the security and privacy requirements for our service.
Security and privacy
The User Service implements secure authentication and authorization mechanisms to protect user
data and prevent unauthorized access. User passwords are hashed and salted before storing them
in the database to ensure their confidentiality. Sensitive user information, such as payment
details, is encrypted and stored securely. The User Service adheres to data protection regulations


and privacy laws, such as GDPR (General Data Protection Regulation) or CCPA (California
Consumer Privacy Act), to ensure user privacy and data security.
The User Service plays a crucial role in managing user authentication, authorization, and profile
data in our Netflix-like platform. By providing secure and scalable APIs for user and profile
management, it enables personalized experiences and seamless integration with other services.
In the next section, we’ll explore the Recommendation Service, which generates personalized
video recommendations for users, based on their preferences and viewing history.
Recommendation Service
The Recommendation Service is a key component of our Netflix-like platform, responsible for
generating personalized video recommendations for users. It analyzes user behavior, preferences,
and viewing history to provide relevant and engaging content suggestions. Figure 14.11 shows at
a very high level what services the Recommendation Service interacts with.
Figure 14.11: The Recommendation service high-level diagram
Let’s dive into the design and implementation details of the Recommendation Service. The
following are the API endpoints:
GET /recommendations/{userId}: Retrieve personalized video recommendations for a user:
Request parameters: The user ID, number of recommendations, and filters (e.g., genre or language)
Response: A list of recommended videos with metadata
POST /events: Record user events for recommendation purposes:


Request body: The user ID, event type (e.g., the video watched, rated, and searched), and event data
Response: Success status
Let’s now see how the recommendations are generated for a user.
The recommendation generation flow
Figure 14.12 shows the sequence diagram for the recommendation generation flow.
Figure 14.12: The recommendation generation flow
Here is the flow:
1. When a user requests recommendations, the client sends a GET request to the /recommendations/{userId}
endpoint.
2. The API layer forwards the request to the Recommendation Manager.
3. The Recommendation Manager first checks the cache for existing recommendations:
If they are found in the cache, it returns the cached recommendations
If they are not found, it proceeds to generate new recommendations
4. For new recommendations, the following occurs:
I. The Recommendation Manager fetches user data from the User Behavior Database.


II. It then requests the Recommendation Generator to create personalized recommendations.
III. The Recommendation Generator loads the appropriate model from the Model Repository.
IV. It then fetches relevant video data from the User Behavior Database.
V. The generator applies the model to create a list of recommendations.
5. The Recommendation Manager stores the new recommendations in the cache for future quick access.
Finally, the list of recommended videos is returned to the client through the API Layer.
Next, let’s see how user events get recorded.
The user event recording flow
Figure 14.13 shows the sequence diagram for the user event recording flow.
Figure 14.13: The user event recording flow
Here is the flow:
1. When a user performs an action (e.g., watching a video), the client sends a POST request to the /events endpoint with the
event data.
2. The API layer forwards the event to the data collection and processing component.
3. The event data is validated and preprocessed.
4. The processed event data is then stored in the User Behavior Database.


A success status is returned to the client via the API layer.
Next, let’s cover the flow for the model training and deployment process.
The model training and deployment process
Figure 14.14 shows the flow for the model training and deployment process.


Figure 14.14: The model training and deployment process
Here is the flow:


1. The process begins with collecting user behavior data from the User Behavior Database.
2. The data is preprocessed and cleaned to remove any inconsistencies or errors.
3. Relevant features are extracted from the cleaned data.
4. The dataset is split into training and validation sets.
5. Various recommendation models are trained using the training data.
6. The models’ performance is evaluated using the validation set.
7. If the performance is satisfactory, the best-performing model is deployed to production.
8. The Model Repository is updated with the new model.
9. If the performance is not satisfactory, the process returns to the model training step with adjusted parameters.
Now, let’s look at the Recommendation Service’s integration with other services:
The Recommendation Service integrates closely with the User Service to retrieve user profiles and viewing history
It communicates with the Video Service to fetch up-to-date video metadata, ensuring accurate recommendations
The service also interacts with the Analytics and Reporting Service, providing performance
metrics and insights about the recommendation system
These flows and processes work together to create a robust and efficient Recommendation
Service. Let’s now cover the scalability and performance aspects of this service.
Scalability and performance
The Recommendation Service is designed to handle a large number of concurrent
recommendation requests. It can be scaled horizontally by deploying multiple instances of the
service behind a load balancer, distributing the incoming traffic. Caching mechanisms, such as
Redis or Memcached, can be employed to store frequently accessed recommendation results and
improve response times. The recommendation models can be deployed on scalable
infrastructure, such as Apache Spark or TensorFlow Serving, to handle high-volume requests
efficiently.
Next, let’s look at monitoring and evaluation.
Monitoring and evaluation
The Recommendation Service integrates with monitoring systems to track key metrics and
performance indicators. Metrics such as recommendation request latency, cache hit rate, and
model accuracy are monitored to ensure the health and effectiveness of the service. A/B testing


and online evaluation techniques can be employed to assess the impact of different
recommendation algorithms and configurations on user engagement and satisfaction. User
feedback and explicit ratings can be collected to evaluate and improve the quality of
recommendations over time.
The Recommendation Service is a critical component of our Netflix-like platform, enabling
personalized and engaging video recommendations for users. By leveraging advanced
recommendation algorithms, data collection, and real-time processing, it enhances user
satisfaction and retention.
In the next section, we’ll explore the CDN, which plays a vital role in efficiently delivering video
content to users across the globe.
The CDN
The CDN is a crucial component of our Netflix-like platform, responsible for efficiently
delivering video content to users across the globe. It ensures high performance, scalability, and
reliability by distributing video content across a network of geographically dispersed servers.
Figure 14.15 covers the CDN architecture.
Figure 14.15: The CDN architecture
Let’s explore the design and implementation details of the CDN.
CDN architecture and content distribution
Figure 14.16 covers the flow for the content distribution sequence diagram


Figure 14.16: The content distribution sequence diagram
Here is the flow:
1. The CDN consists of a network of edge servers located in various regions around the world, connected to an origin server
that holds the master copy of all content.
2. When new video content is uploaded to the platform via the Video Service, it triggers the following process:
The origin server transcodes the video into multiple formats and bitrates to support different devices and network
conditions
The CDN manager is notified of the new content availability
The CDN manager initiates content propagation to the edge servers
Each edge server requests and caches the content chunks from the origin server
3. This distribution ensures that content is readily available, closer to the users, reducing latency and improving streaming
performance.
Next, let’s look at the request routing and video streaming workflow.
Request routing and video streaming


Figure 14.17 shows the sequence diagram for request routing and video streaming.
Figure 14.17: The request routing and video streaming workflow
Here is the flow:
1. When a user requests to stream a video, the client application initiates the following sequence:
2. The client sends a request to the DNS Load Balancer.
3. The DNS Load Balancer redirects the client to the nearest CDN entry point.
4. The client then contacts the Request Router.
5. The Request Router analyzes factors such as user location, server availability, network latency, and server load to
determine the optimal edge server.
6. The client is redirected to the selected edge server.


The edge server then serves the video content to the user:
If the content is cached, it’s served directly from the edge server
If not cached, the edge server retrieves the content from the origin server, caches it, and then serves it
to the client
This intelligent routing ensures a fast and reliable streaming experience for users worldwide.
In order to support compelling user experiences, our Netflix-like system must support adaptive
bitrate streaming, which we will discuss next.
Adaptive bitrate streaming
The CDN supports adaptive bitrate streaming to provide optimal video quality:
Video content is encoded into multiple bitrates and segmented into small chunks.
During playback, the client continuously monitors network conditions.
The client requests subsequent video segments from the edge server, adjusting the bitrate as needed, based on network
performance.
The edge server serves the requested segments, allowing for seamless quality adjustments during playback.
This adaptive approach ensures a smooth streaming experience across varying network conditions and device capabilities.
Let’s now talk about how our CDN design deals with content security.
Content security and DRM
The CDN integrates with a (Digital Rights Management) DRM Service to implement content
security measures:
Video content is encrypted using DRM systems, such as Microsoft PlayReady or Google Widevine
The CDN collaborates with the DRM Service for secure content delivery and license management
Only authorized users with valid DRM licenses can access and play the protected video content
This integration ensures content protection against unauthorized access and piracy while
complying with licensing agreements and regional restrictions
The CDN seamlessly integrates with other components of our Netflix-like platform:
Video Service: Facilitates content propagation and retrieval, ensuring efficient video transcoding, storage, and distribution


Recommendation Service: Enables personalized content delivery, allowing for dynamic and personalized playlists or
recommendations
Analytics Service: Provides comprehensive insights and metrics on content delivery performance, helping to optimize the
CDN’s operations
DRM Service: Ensures secure content delivery through encryption and license management
This integrated approach allows the CDN to not only deliver content efficiently but also
contribute to a personalized and secure user experience. By leveraging this sophisticated CDN
architecture and its integrations, our Netflix-like platform can deliver high-quality video content
to users worldwide with minimal latency, adaptive quality, and robust security, ensuring an
excellent streaming experience for our global audience.
Summary
In this chapter, we explored the system design of a Netflix-like platform, covering various
aspects such as functional and non-functional requirements, data modeling, capacity estimation,
high-level architecture, and the design of key components, such as the Video Service, User
Service, Recommendation Service, and CDN.
We started by defining the core features and functionalities that our platform should support,
ensuring a comprehensive and user-centric streaming experience. We then discussed the nonfunctional requirements, emphasizing the importance of scalability, performance, reliability, and
security.
To handle the massive amount of data and traffic generated by millions of users, we delved into
data modeling and capacity estimation. We designed a data model that captures the essential
entities and relationships, and we performed calculations to estimate the storage, bandwidth, and
processing requirements of our platform.
Based on these requirements and estimations, we proposed a high-level architecture that
incorporates various components and services, ensuring a modular and scalable design. We
explored the responsibilities and interactions of each component, focusing on efficient video
storage, encoding, streaming, recommendation generation, and content delivery.
Throughout the chapter, we emphasized the importance of scalability, fault tolerance, and
performance optimization. We discussed techniques such as data sharding, caching, content
distribution, and adaptive bitrate streaming to ensure a seamless and reliable streaming
experience for users. We have discussed many different services that present different learnings


of designing scalable systems. In the next chapter, we will focus on some tips to interview for
System Design based on our experience interviewing candidates and talking to Senior Engineers
at several Fortune 100 companies..

## Examples & Scenarios

- Movie to ContentMetadata: A movie can have multiple versions of metadata (e.g., different video qualities
or languages)
TVShow to Episode: A TV show can have multiple episodes
TVShow to ContentMetadata: A TV show can have multiple versions of metadata
Episode to ContentMetadata: An episode can have multiple versions of metadata
Profile to WatchHistory: A profile can have multiple watch history entries
Profile to Watchlist: A profile can have multiple watchlist entries
Profile to Rating: A profile can have multiple ratings
The preceding data model captures the essential entities and relationships required for our
Netflix-like service. It allows us to store and manage user information, profiles, movies, TV

- Implement caching at various levels (e.g., CDN, application server, and database) to reduce the load on backend
systems and improve performance
Cache frequently accessed data such as popular videos, user profiles, and recommendations
CDN:
Utilize a CDN to distribute video content globally and reduce latency for users.
Store video files on CDN servers located closer to the users for faster streaming.
Database sharding and replication:
Shard the database to distribute data across multiple servers and handle increased storage and traffic
Replicate data to ensure high availability and fault tolerance
These estimations provide a starting point for designing the infrastructure and scaling our

- data without direct dependencies. For example, when a new video is uploaded, the Video Service
can send an encoding job to the Message Queue, which can then be picked up and processed by a
separate encoding service. This ensures that tasks are processed efficiently and reliably, even
under a high load.
Lastly, to ensure the reliability and stability of our system, we implement comprehensive
Monitoring and Logging. We collect logs and metrics from all components of the architecture
and centralize them for analysis and troubleshooting. This allows us to quickly identify and
resolve any issues that may arise. We also set up dashboards and alerts to provide real-time
visibility into the system’s health and performance.
In summary, our high-level architecture is designed to handle the scale and complexity of a

- 3. The video is transcoded into different formats (e.g., MP4, HLS, and DASH) and bitrates to support adaptive streaming and
various client devices.
4. The encoded video files are stored in the distributed storage system, and their locations are updated in the video metadata
database.
Next, let’s look at the flow for the video streaming aspect of our service.
Video streaming
Figure 14.6 shows the video streaming sequence diagram.
Figure 14.6: The video streaming sequence diagram
Here is the flow:
1. When a user requests to stream a video, the client application sends a request to the Video Service API endpoint.

- 3. The Video Service generates a streaming URL or manifest file (e.g., an HLS playlist or DASH manifest) that contains the
information needed by the client to stream the video.
4. The client application uses the streaming URL or manifest file to request video chunks or segments from the CDN, or
directly from the Video Service.

- 2. Upon successful authentication, the User Service generates an authentication token (e.g., JWT) that contains the user ID and
other relevant information.

- Request parameters: The user ID, number of recommendations, and filters (e.g., genre or language)
Response: A list of recommended videos with metadata
POST /events: Record user events for recommendation purposes:

- Request body: The user ID, event type (e.g., the video watched, rated, and searched), and event data
Response: Success status
Let’s now see how the recommendations are generated for a user.
The recommendation generation flow
Figure 14.12 shows the sequence diagram for the recommendation generation flow.
Figure 14.12: The recommendation generation flow
Here is the flow:
1. When a user requests recommendations, the client sends a GET request to the /recommendations/{userId}
endpoint.
2. The API layer forwards the request to the Recommendation Manager.

- 1. When a user performs an action (e.g., watching a video), the client sends a POST request to the /events endpoint with the
event data.
2. The API layer forwards the event to the data collection and processing component.
3. The event data is validated and preprocessed.
4. The processed event data is then stored in the User Behavior Database.

