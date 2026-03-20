# Chapter 16: System Design Cheat Sheet

> Source: System Design Guide for Software Professionals, Chapter 20, Pages 373-385

## Key Concepts

- 16
System Design Cheat Sheet
Welcome to this final chapter, a cheat sheet designed to equip you with the essential strategies to
ace your technical interviews. This chapter is meticulously crafted to 
- 1. Ask and clarify the p

## Content

16
System Design Cheat Sheet
Welcome to this final chapter, a cheat sheet designed to equip you with the essential strategies to
ace your technical interviews. This chapter is meticulously crafted to provide structured insights
into key aspects crucial for mastering system design assessments. Whether you’re gearing up for
your next interview or seeking to enhance your system architecture skills, this chapter offers
practical solutions to common questions that arise during system design interviews.
Throughout this chapter, we will explore the structured approach necessary to excel in system
design interviews. From understanding how to effectively clarify problem statements and outline
functional and non-functional requirements to creating high-level architectural diagrams, each
step is designed to ensure you approach interviews with confidence and clarity.
Additionally, we will delve into critical decisions such as selecting the optimal data store based
on use case requirements, choosing the right data structures to maximize efficiency, and
identifying the most suitable components and protocols for various system challenges. By the
end of this chapter, you’ll be equipped with a comprehensive toolkit to navigate and excel in any
system design interview scenario.
The chapter covers the following core questions:
What structure should we follow in a system design interview?
Which data store should we use for a use case?
Which data structures should we use for a use case?
Which components should we use for which use case?
What protocol should we use for which use case?
Which solution should we use for which core challenge?
Let’s jump right in.
What structure should we follow in a system design interview?
A system design interview is a comprehensive evaluation of your ability to architect scalable,
reliable, and maintainable systems. Here’s a structured approach to follow during a system
design interview to ensure you cover all essential aspects:


1. Ask and clarify the problem
2. List out the functional requirements
3. List out the non-functional requirements
4. Write down the APIs
5. Do high-level estimates and calculations
6. Draw a high-level system design diagram addressing the functional requirements without focusing too much on an
optimized solution
7. Identify core challenges and address them by brainstorming various options and making the right trade-offs
8. Put together a final high-level system design and architecture
9. Verify the functional and non-functional requirements
Now that we know the high-level steps to be followed in an interview, let’s explore some core
questions and their answers.
Which data store should we use for a use case?
Choosing the right data store for a specific use case depends on various factors, including the
nature of the data, access patterns, scalability requirements, consistency, latency, and the overall
architecture of the application. Here are some guidelines and examples to help you select the
most appropriate data store for different scenarios:
Use case
Data store
Structured data
Require ACID properties
Not sparse and not a huge number of rows
Not a lot of joins else reads will be slow
Relational database
(MySQL,
PostgreSQL, or
Oracle)
Shard to support
scale
Non-structured, very high scale
Wide variety of documents, such as Amazon items (sparse data)
Data is finite
Document database
(MongoDB or
Couchbase)
Non-structured, very high scale
Ever-increasing data
Columnar databases


Large volume of data with thousands of columns
Most of the time just queries only a few columns
Hbase (consistency
over availability)
Cassandra
(availability over
consistency,
tunable
consistency)
Scalable and fast key-value store
Redis or
Memcached
Fast free-text search
Lucene,
Elasticsearch, or
Solr
Fast writes
WAL
Fast reads
Caching,
replications, in
memory, CDNs
Blob store video and images
S3/CDNs
Complex relations such as in a graph
Graph db (Neo4j)
Hot data
In memory,
SSDs
Cold data
Disk, Amazon
Glacier
Find "highly similar" data in a set of unstructured
data (such as images, text blobs, and videos). This
is particularly needed in AI applications.
Vector database
Time-series metrics data
Time series
(OpenTSDB)


Proximity or nearby entity search
Geo-spatial index
(quadtrees or
geohashing)
Table 17.1: Choosing the right data store for different use cases
The preceding table lists the use cases for data store mapping. Now, let’s go over the data
structures to be used for different use cases in the next section.
Which data structures should we use for a use case?
Choosing the right data structure for a use case depends on the specific requirements and
constraints of the problem you are trying to solve. Here is a guide on choosing the right data
structure for different use cases:
Example use cases
Data
structure
Find whether an element is a member of a set when the space efficiency and
speed of query operations are critical, even at the expense of a small
probability of false positives.
Ensure that a web cache does not store duplicate URLs.
Check whether a key might be in a database table before performing a costly
disk access.
Filter out known spam emails efficiently and check whether an incoming
email matches any email in a database of known spam addresses
Bloom
filter
Estimate the frequency of elements in a data stream in a space-efficient way,
handling large-scale data streams with fixed memory usage.
Monitor and analyze network traffic to detect heavy hitters or frequent items
by keeping track of the frequency of packets or flows.
Monitor large-scale social media activity or website traffic by tracking the
frequency of events in real time, such as clicks, views, or transactions.
Suggest popular or trending items to users by maintaining approximate
counts of item views, purchases, or ratings.
Count
min
sketch
Approximate the cardinality (i.e., the number of distinct elements) of a
multiset with high accuracy and low memory usage.
Hyper
log log


Measure the reach and effectiveness of advertising campaigns without
storing detailed logs by estimating the number of unique users who have
seen or clicked on an ad.
Understand network usage patterns and detect anomalies such as DDoS
attacks by counting unique IP addresses, sessions, or flows in network traffic
data.
Measure the reach and impact of social media campaigns by estimating the
number of unique users liking, sharing, or commenting on posts.
Efficiently verify data integrity with fingerprinting data, allowing you to
confirm whether the data has been tampered with without needing to
download the entire dataset.
Git version control system: Track changes to code efficiently. Each commit
in Git history has a unique Merkle root representing the state of the code
base at that point. This allows developers to verify the integrity of specific
versions and identify changes made over time.
P2P file sharing: Ensure downloaded files are complete and unaltered. The
file is divided into chunks, and each chunk is hashed. The complete file’s
Merkle root is distributed along with the chunks. Anyone downloading the
file can verify its integrity by checking the hashes of the downloaded chunks
against the Merkle root.
Software updates: Merkle trees can be used to ensure the downloaded file is
complete and hasn’t been corrupted during transmission. The update
provider can publish the Merkle root of the file beforehand, and users can
verify the downloaded file’s integrity by calculating its Merkle root and
comparing it to the published one.
Merkle
tree
Table 17.2: Choosing the right data structure for different use cases
In the next section, let’s go through the components to be selected for different use cases.
Which components should we use for which use
case?
In system design, choosing the right components is crucial to building a scalable, reliable, and
maintainable system. The following is a guide to help you decide which components to use for
various use cases:
A traffic director for the network or application distributing
incoming traffic evenly across multiple servers in a pool.
Load
balancer


Web applications: Distributing traffic across multiple web servers to handle
high user volumes for e-commerce sites, social media platforms, or any web
application with fluctuating traffic.
Database clusters: Balancing read/write requests across multiple database
servers in a cluster for improved performance and redundancy.
An intermediary between your device and the internet to
protect your device.
Privacy and anonymity: Proxies can hide your IP address, making it seem
like you’re browsing from a different location. This is useful for accessing
content restricted by geography (content blocked in your region) or for
maintaining a level of anonymity online.
Security: Some proxy servers offer additional security features, such as
filtering out malicious content or encrypting your traffic. This can be helpful
when using public Wi-Fi networks where your connection might be less
secure.
Content filtering: Organizations or schools might use proxies to restrict
access to certain websites or types of content (e.g., gambling sites or social
media).
Proxy
A middleman between the internet and your web
application to protect servers.
E-commerce websites: Reverse proxies can handle high volumes of traffic
during sales or peak seasons, distributing load and ensuring a smooth
shopping experience.
Content Delivery Networks (CDNs): CDNs often use reverse proxies to
cache content at geographically dispersed edge locations, bringing content
closer to users for faster loading times.
Microservices architectures: Reverse proxies can route requests to the
appropriate microservice based on specific criteria, simplifying traffic
management in complex systems.
Reverse
proxy
Manage traffic and protect systems in software design to
prevent overload and ensure fair access for everyone.
API protection: Limiting the number of API calls an application can make
per minute prevents abuse and protects against Denial-of-Service (DoS)
attacks.
Rate
limiter


Login attempts: Limiting login attempts deters brute-force attacks where
someone tries to guess a password repeatedly.
E-commerce transactions: Rate-limiting purchase attempts can prevent
fraudulent activity or overwhelm payment processing systems during sales.
Automatic switch that monitors the health of a service or
resource, protecting the system from cascading failures.
Microservices architecture: In a system with multiple interconnected
services, a circuit breaker can isolate a failing service and prevent it from
bringing down the entire system.
External APIs: If an external API you rely on is experiencing problems, a
circuit breaker can prevent your system from constantly retrying failed
requests.
Third-party integrations: When integrating with a third-party service, a
circuit breaker can prevent your system from crashing due to temporary
outages with the external service.
Circuit
breaker
A central hub for managing all incoming API requests in a
microservices architecture.
Single entry point: The gateway acts as a single point of entry for all API
requests, simplifying client interactions and reducing the need for clients to
know the specifics of each backend service.
Request routing: The gateway receives requests and routes them to the
appropriate backend service based on predefined rules (such as path, headers,
or parameters).
Security: The gateway can enforce authentication and authorization policies,
ensuring only authorized users can access specific functionalities. It can also
handle tasks such as encryption and rate limiting to protect backend services.
Monitoring and analytics: The gateway can monitor API traffic, track usage
patterns, and provide valuable insights into how APIs are being used.
API
gateway
A communication channel between systems, making them
decoupled so that they don’t have to wait for each other to
complete tasks:
E-commerce order processing: When a customer places an order, a
message can be sent to a queue. A separate worker service can then consume
the message, process the order (payment, inventory check, and shipping), and
Message
queues


update relevant systems asynchronously. This avoids blocking the user
interface while order processing happens in the background.
Task queues: Long-running tasks, such as video encoding or image
processing, can be added to a message queue. Worker services can then pick
up these tasks and complete them asynchronously, freeing up the main
application to handle other user requests.
Social media feeds: When a user follows someone on a social media
platform, a message queue can be used to notify them about new posts. The
queue stores updates and a separate service can deliver them to the user’s
feed asynchronously, improving performance and scalability to handle large
user bases.
Geographically distributed network of servers that work
together to deliver content to users with faster loading times
and improved user experience.
Websites and web applications: Most popular websites and web
applications leverage CDNs to ensure fast loading times for users worldwide.
This is especially crucial for e-commerce sites where slow loading times can
lead to lost sales.
Streaming services: Video and music streaming services rely heavily on
CDNs to deliver high-quality content with minimal buffering, even during
peak usage periods.
Social media platforms: Social media platforms with massive user bases
utilize CDNs to deliver images, videos, and other content efficiently,
ensuring a smooth user experience.
CDNs
Table 17.3: Choosing the right component for different use cases
In the next section, we will learn about various protocols and compare them with each other.
Also, we will list several use cases and the applicable protocols to be used for them.
What protocol should we use for which use case?
Before we jump into the different use cases and which protocol to use, let’s understand the
differences between the different protocols and compare them along the following dimensions:
Feature
HTTP
SSE
WebSockets
Bidirectional


Communication
model
Requestresponse
Unidirectional
(server to
client)
Connection
type
Short-lived
Long-lived
Long-lived
Data format
Text (HTML,
JSON, etc.)
Text (eventstream)
Text and binary
Use case
examples
Web pages,
REST APIs
Live updates,
notifications
Real-time chat,
games, financial
tickers
Latency
High
Low
Very low
Scalability
High (for
stateless
requests)
Moderate
Moderate (requires
careful
management)
Automatic
reconnection
No
Yes
Application
managed
Protocol
overhead
High
(repeated
handshakes)
Low
Low
Browser
support
Universal
Modern
browsers
Modern browsers
Table 17.4: Different protocols and their comparison table
In the following table, let’s explore different use cases and the right protocol to be used along
with the rationale for the choice:
Use Case
Recommended
Protocol
Rationale


Static content
delivery
HTTP
Simple request-response model,
well supported
RESTful APIs
HTTP
Stateless, widely used for backend
communication
Form
submissions
HTTP
Standard way to handle form data
File transfers
HTTP
Efficient for large file
uploads/downloads
Real-time
notifications
SSE
Simple, automatic reconnection,
server-to-client updates
Live feeds
SSE
Efficient for streaming live
updates
Monitoring
dashboards
SSE
Continuous updates from server to
client
Chat and
messaging
(simple)
SSE
Simple unidirectional message
updates
Online gaming
WebSockets
Low-latency, bidirectional
communication
Real-time chat
WebSockets
Fast, continuous message
exchange
Collaborative
tools
WebSockets
Real-time, bidirectional data
exchange
Financial
applications
WebSockets
Real-time updates, low latency


IoT applications
WebSockets
Continuous data exchange
between devices and servers
Table 17.5: Choosing the right protocol for different use cases
In the next section, let’s explore various solutions for different use cases.
Which solution should we use for which core
challenge?
Identifying the right solution for specific core challenges is essential to building robust, scalable
systems. Each challenge requires tailored strategies and technologies. This section delves into the
best solutions for various core challenges, helping you make informed decisions to optimize your
system’s performance and reliability:
Core
Challenge
Description
Potential
Solutions
Handling
high write
throughput
Managing systems with very high
write rates (e.g., logging, real-time
analytics)
Write-Ahead Logging
(WAL)
Sharding
NoSQL databases
Ensuring
data
consistency
Maintaining consistency in a
distributed system
Distributed
transactions (e.g.,
two-phase commit)
Eventual consistency
Conflict resolution
Low-latency
requirements
Providing responses with minimal
delay
In-memory databases
(e.g., Redis)
Caching (e.g.,
Memcached)
Edge computing


Scalability
Scaling the system to handle
increased load
Horizontal scaling
Load balancing
Microservices
architecture
Fault
tolerance
Ensuring the system continues to
operate despite failures
Replication
Failover mechanisms
Circuit breakers
Data
partitioning
Distributing data across multiple
nodes
Hash partitioning
Range partitioning
Consistent hashing
Search
performance
Providing fast and relevant search
results
Inverted index<br>
Search engines (e.g.,
Elasticsearch)
Caching
Handling
spiky traffic
Managing sudden spikes in traffic
(e.g., sales or events)
Autoscaling
Load smoothing (e.g.,
request queuing or
rate limiting)
CDNs
Distributed
locking
Coordinating access to shared
resources in a distributed system
Distributed Lock
Managers (DLMs)
ZooKeeper
Redis
Table 16.6: Choosing the right solution idea for different use cases
Summary
In this chapter, we explored a structured approach to excel in system design interviews, focusing
on problem clarification, requirement listing, API design, and architectural diagramming. We’ve


also delved into critical decisions such as selecting appropriate data stores, choosing optimal data
structures, and identifying suitable components and protocols to tackle core system challenges.
By providing practical insights and guidelines, this chapter equips you with the necessary tools
to confidently navigate system design interviews and build scalable, reliable, and maintainable
systems.
This concludes the last chapter of this book. We hope that this system design book serves as a
comprehensive guide to mastering the art of architecting scalable, reliable, and maintainable
systems. Covering essential topics and deep dives, it equips you with the knowledge and skills
needed not only for successful system design but also to excel at interviews.
As you move forward, remember that practical experience is crucial. Regularly practice
designing systems for different scenarios, analyze real-world case studies, and engage in mock
interviews. Stay updated with the latest trends and best practices by leveraging online resources
and honing your communication skills.
Embrace the journey of continuous learning and improvement, and approach each challenge with
confidence and curiosity. We wish you all the very best!

## Examples & Scenarios

- access to certain websites or types of content (e.g., gambling sites or social
media).
Proxy
A middleman between the internet and your web
application to protect servers.
E-commerce websites: Reverse proxies can handle high volumes of traffic
during sales or peak seasons, distributing load and ensuring a smooth
shopping experience.
Content Delivery Networks (CDNs): CDNs often use reverse proxies to
cache content at geographically dispersed edge locations, bringing content

- write rates (e.g., logging, real-time
analytics)
Write-Ahead Logging
(WAL)
Sharding
NoSQL databases
Ensuring
data
consistency
Maintaining consistency in a

- transactions (e.g.,
two-phase commit)
Eventual consistency
Conflict resolution
Low-latency
requirements
Providing responses with minimal
delay
In-memory databases
(e.g., Redis)

- Caching (e.g.,
Memcached)
Edge computing

- Search engines (e.g.,
Elasticsearch)
Caching
Handling
spiky traffic
Managing sudden spikes in traffic
(e.g., sales or events)
Autoscaling
Load smoothing (e.g.,
request queuing or

## Tables & Comparisons

| Use case | Data store |
| --- | --- |
| Structured data
Require ACID properties
Not sparse and not a huge number of rows
Not a lot of joins else reads will be slow | Relational database
(MySQL,
PostgreSQL, or
Oracle)
Shard to support
scale |
| Non-structured, very high scale
Wide variety of documents, such as Amazon items (sparse data)
Data is finite | Document database
(MongoDB or
Couchbase) |

| Large volume of data with thousands of columns
Most of the time just queries only a few columns | Hbase (consistency
over availability)
Cassandra
(availability over
consistency,
tunable
consistency) |
| --- | --- |
| Scalable and fast key-value store | Redis or
Memcached |
| Fast free-text search | Lucene,
Elasticsearch, or
Solr |
| Fast writes | WAL |
| Fast reads | Caching,
replications, in
memory, CDNs |
| Blob store video and images | S3/CDNs |
| Complex relations such as in a graph | Graph db (Neo4j) |
| Hot data | In memory,
SSDs |
| Cold data | Disk, Amazon
Glacier |
| Find "highly similar" data in a set of unstructured
data (such as images, text blobs, and videos). This
is particularly needed in AI applications. | Vector database |
| Time-series metrics data | Time series
(OpenTSDB) |
|  |  |

| Example use cases | Data
structure |
| --- | --- |
| Find whether an element is a member of a set when the space efficiency and
speed of query operations are critical, even at the expense of a small
probability of false positives.
Ensure that a web cache does not store duplicate URLs.
Check whether a key might be in a database table before performing a costly
disk access.
Filter out known spam emails efficiently and check whether an incoming
email matches any email in a database of known spam addresses | Bloom
filter |
| Estimate the frequency of elements in a data stream in a space-efficient way,
handling large-scale data streams with fixed memory usage.
Monitor and analyze network traffic to detect heavy hitters or frequent items
by keeping track of the frequency of packets or flows.
Monitor large-scale social media activity or website traffic by tracking the
frequency of events in real time, such as clicks, views, or transactions.
Suggest popular or trending items to users by maintaining approximate
counts of item views, purchases, or ratings. | Count
min
sketch |

| Measure the reach and effectiveness of advertising campaigns without
storing detailed logs by estimating the number of unique users who have
seen or clicked on an ad.
Understand network usage patterns and detect anomalies such as DDoS
attacks by counting unique IP addresses, sessions, or flows in network traffic
data.
Measure the reach and impact of social media campaigns by estimating the
number of unique users liking, sharing, or commenting on posts. |  |
| --- | --- |
| Efficiently verify data integrity with fingerprinting data, allowing you to
confirm whether the data has been tampered with without needing to
download the entire dataset.
Git version control system: Track changes to code efficiently. Each commit
in Git history has a unique Merkle root representing the state of the code
base at that point. This allows developers to verify the integrity of specific
versions and identify changes made over time.
P2P file sharing: Ensure downloaded files are complete and unaltered. The
file is divided into chunks, and each chunk is hashed. The complete file’s
Merkle root is distributed along with the chunks. Anyone downloading the
file can verify its integrity by checking the hashes of the downloaded chunks
against the Merkle root.
Software updates: Merkle trees can be used to ensure the downloaded file is
complete and hasn’t been corrupted during transmission. The update
provider can publish the Merkle root of the file beforehand, and users can
verify the downloaded file’s integrity by calculating its Merkle root and
comparing it to the published one. | Merkle
tree |

| Web applications: Distributing traffic across multiple web servers to handle
high user volumes for e-commerce sites, social media platforms, or any web
application with fluctuating traffic.
Database clusters: Balancing read/write requests across multiple database
servers in a cluster for improved performance and redundancy. |  |
| --- | --- |
| An intermediary between your device and the internet to
protect your device.
Privacy and anonymity: Proxies can hide your IP address, making it seem
like you’re browsing from a different location. This is useful for accessing
content restricted by geography (content blocked in your region) or for
maintaining a level of anonymity online.
Security: Some proxy servers offer additional security features, such as
filtering out malicious content or encrypting your traffic. This can be helpful
when using public Wi-Fi networks where your connection might be less
secure.
Content filtering: Organizations or schools might use proxies to restrict
access to certain websites or types of content (e.g., gambling sites or social
media). | Proxy |
| A middleman between the internet and your web
application to protect servers.
E-commerce websites: Reverse proxies can handle high volumes of traffic
during sales or peak seasons, distributing load and ensuring a smooth
shopping experience.
Content Delivery Networks (CDNs): CDNs often use reverse proxies to
cache content at geographically dispersed edge locations, bringing content
closer to users for faster loading times.
Microservices architectures: Reverse proxies can route requests to the
appropriate microservice based on specific criteria, simplifying traffic
management in complex systems. | Reverse
proxy |

| Login attempts: Limiting login attempts deters brute-force attacks where
someone tries to guess a password repeatedly.
E-commerce transactions: Rate-limiting purchase attempts can prevent
fraudulent activity or overwhelm payment processing systems during sales. |  |
| --- | --- |
| Automatic switch that monitors the health of a service or
resource, protecting the system from cascading failures.
Microservices architecture: In a system with multiple interconnected
services, a circuit breaker can isolate a failing service and prevent it from
bringing down the entire system.
External APIs: If an external API you rely on is experiencing problems, a
circuit breaker can prevent your system from constantly retrying failed
requests.
Third-party integrations: When integrating with a third-party service, a
circuit breaker can prevent your system from crashing due to temporary
outages with the external service. | Circuit
breaker |
| A central hub for managing all incoming API requests in a
microservices architecture.
Single entry point: The gateway acts as a single point of entry for all API
requests, simplifying client interactions and reducing the need for clients to
know the specifics of each backend service.
Request routing: The gateway receives requests and routes them to the
appropriate backend service based on predefined rules (such as path, headers,
or parameters).
Security: The gateway can enforce authentication and authorization policies,
ensuring only authorized users can access specific functionalities. It can also
handle tasks such as encryption and rate limiting to protect backend services.
Monitoring and analytics: The gateway can monitor API traffic, track usage
patterns, and provide valuable insights into how APIs are being used. | API
gateway |

| update relevant systems asynchronously. This avoids blocking the user
interface while order processing happens in the background.
Task queues: Long-running tasks, such as video encoding or image
processing, can be added to a message queue. Worker services can then pick
up these tasks and complete them asynchronously, freeing up the main
application to handle other user requests.
Social media feeds: When a user follows someone on a social media
platform, a message queue can be used to notify them about new posts. The
queue stores updates and a separate service can deliver them to the user’s
feed asynchronously, improving performance and scalability to handle large
user bases. |  |
| --- | --- |
| Geographically distributed network of servers that work
together to deliver content to users with faster loading times
and improved user experience.
Websites and web applications: Most popular websites and web
applications leverage CDNs to ensure fast loading times for users worldwide.
This is especially crucial for e-commerce sites where slow loading times can
lead to lost sales.
Streaming services: Video and music streaming services rely heavily on
CDNs to deliver high-quality content with minimal buffering, even during
peak usage periods.
Social media platforms: Social media platforms with massive user bases
utilize CDNs to deliver images, videos, and other content efficiently,
ensuring a smooth user experience. | CDNs |

| Feature | HTTP | SSE | WebSockets |
| --- | --- | --- | --- |
|  |  |  | Bidirectional |

| Communication
model | Request-
response | Unidirectional
(server to
client) |  |
| --- | --- | --- | --- |
| Connection
type | Short-lived | Long-lived | Long-lived |
| Data format | Text (HTML,
JSON, etc.) | Text (event-
stream) | Text and binary |
| Use case
examples | Web pages,
REST APIs | Live updates,
notifications | Real-time chat,
games, financial
tickers |
| Latency | High | Low | Very low |
| Scalability | High (for
stateless
requests) | Moderate | Moderate (requires
careful
management) |
| Automatic
reconnection | No | Yes | Application
managed |
| Protocol
overhead | High
(repeated
handshakes) | Low | Low |
| Browser
support | Universal | Modern
browsers | Modern browsers |

| Use Case | Recommended
Protocol | Rationale |
| --- | --- | --- |
|  |  |  |

| Static content
delivery | HTTP | Simple request-response model,
well supported |
| --- | --- | --- |
| RESTful APIs | HTTP | Stateless, widely used for backend
communication |
| Form
submissions | HTTP | Standard way to handle form data |
| File transfers | HTTP | Efficient for large file
uploads/downloads |
| Real-time
notifications | SSE | Simple, automatic reconnection,
server-to-client updates |
| Live feeds | SSE | Efficient for streaming live
updates |
| Monitoring
dashboards | SSE | Continuous updates from server to
client |
| Chat and
messaging
(simple) | SSE | Simple unidirectional message
updates |
| Online gaming | WebSockets | Low-latency, bidirectional
communication |
| Real-time chat | WebSockets | Fast, continuous message
exchange |
| Collaborative
tools | WebSockets | Real-time, bidirectional data
exchange |
| Financial
applications | WebSockets | Real-time updates, low latency |

| Core
Challenge | Description | Potential
Solutions |
| --- | --- | --- |
| Handling
high write
throughput | Managing systems with very high
write rates (e.g., logging, real-time
analytics) | Write-Ahead Logging
(WAL)
Sharding
NoSQL databases |
| Ensuring
data
consistency | Maintaining consistency in a
distributed system | Distributed
transactions (e.g.,
two-phase commit)
Eventual consistency
Conflict resolution |
| Low-latency
requirements | Providing responses with minimal
delay | In-memory databases
(e.g., Redis)
Caching (e.g.,
Memcached)
Edge computing |

| Scalability | Scaling the system to handle
increased load | Horizontal scaling
Load balancing
Microservices
architecture |
| --- | --- | --- |
| Fault
tolerance | Ensuring the system continues to
operate despite failures | Replication
Failover mechanisms
Circuit breakers |
| Data
partitioning | Distributing data across multiple
nodes | Hash partitioning
Range partitioning
Consistent hashing |
| Search
performance | Providing fast and relevant search
results | Inverted index<br>
Search engines (e.g.,
Elasticsearch)
Caching |
| Handling
spiky traffic | Managing sudden spikes in traffic
(e.g., sales or events) | Autoscaling
Load smoothing (e.g.,
request queuing or
rate limiting)
CDNs |
| Distributed
locking | Coordinating access to shared
resources in a distributed system | Distributed Lock
Managers (DLMs)
ZooKeeper
Redis |

