# Chapter 6: Distributed Cache

> Source: System Design Guide for Software Professionals, Chapter 9, Pages 159-177

## Key Concepts

- 6
Distributed Cache
In the rapidly evolving landscape of modern computing, the demand for scalable, highperformance systems has become paramount. As applications grow in complexity and user bases
expa
- Before we start digging deeper into distributed caching, let’s understand caching. Caching is a
technique used in computing to store and manage copies of data or resources in a location that
allows fo

## Content

6
Distributed Cache
In the rapidly evolving landscape of modern computing, the demand for scalable, highperformance systems has become paramount. As applications grow in complexity and user bases
expand, traditional approaches to data retrieval and storage may encounter bottlenecks that
hinder overall performance. One of the most effective strategies to enhance performance is the
implementation of caching. Caching involves temporarily storing copies of data in locations
closer to the user or application, thereby reducing access time and improving efficiency. At its
core, caching is a technique used to store frequently accessed data in a high-speed data storage
layer. This storage layer, or cache, can be located in various places, such as in memory (RAM),
on a disk, or even in a network. By keeping a subset of data in these faster access locations,
systems can significantly reduce the latency experienced when fetching data, leading to
improved application performance and user experience.
As applications scale and distribute across multiple servers or data centers, a single cache may no
longer suffice. This is where distributed caching comes into play. Distributed caching involves
using a network of cache nodes that work together to provide a cohesive caching layer across
multiple servers or locations.
This chapter delves into the principles of caching and the more advanced concept of distributed
caching, exploring their importance, mechanisms, and applications in modern computing.
We will be covering the following concepts in detail in this chapter:
What is caching?
What is distributed caching?
Designing a distributed cache
Popular distributed cache solutions
Let's start by looking at caching.
What is caching?


Before we start digging deeper into distributed caching, let’s understand caching. Caching is a
technique used in computing to store and manage copies of data or resources in a location that
allows for faster access. The primary purpose of caching is to reduce the time and resources
required to retrieve data by keeping a copy of frequently accessed or expensive-to-compute
information in a readily accessible location. This location is typically faster to access than the
original source of the data.
Here are the key concepts associated with caching:
Cache: A cache is a temporary storage area that holds copies of frequently accessed data or resources. This can be in the
form of a hardware cache (for example, a CPU cache) or a software-based cache (for example, an in-memory cache).
Cached data: This refers to the copies of data that are stored in the cache. The data is usually obtained from a slower, more
permanent storage location (such as a database or disk) and is kept in the cache for faster retrieval.
Cache hit: A cache hit occurs when the requested data is found in the cache. This results in a faster retrieval process since
the data is readily available without the need to go to the original data source.
Cache miss: A cache miss happens when the requested data is not found in the cache. In this case, the system needs to fetch
the data from the original source and store a copy in the cache for future access.
Eviction: In situations where the cache has limited space, eviction may occur when the cache is full and needs to make room
for new data. The system may remove less frequently accessed, less recently used, or older data to accommodate new
entries.
Caching plays a crucial role in optimizing system performance, reducing latency, and improving
the overall user experience in a wide range of computing environments.
What is distributed caching?
Distributed caching is a technique employed to optimize data access by strategically storing
frequently accessed information in memory across multiple interconnected servers or nodes.
Rather than repeatedly fetching the same data from the primary data source, a distributed cache
ensures that a copy of this data is readily available in the cache, significantly reducing latency
and enhancing system responsiveness.
The primary objective of distributed caching is to mitigate the performance challenges associated
with accessing data from slower, disk-based storage systems. By maintaining a cache in the main
memory of multiple nodes, the system can quickly retrieve frequently accessed data without
incurring the delays associated with disk I/O operations. This caching strategy proves


particularly effective in scenarios where rapid access to data is critical, such as in web
applications, databases, and other data-intensive environments.
How is it different from regular caching?
Distributed caching and regular (non-distributed, local, single node) caching both involve the
storage and retrieval of frequently accessed data to improve system performance. However, they
differ in terms of their scope and architecture, as well as the scale at which they operate. Here are
the key distinctions between distributed caching and regular caching:
Regular caching
Distributed caching
Scope
Caching typically
refers to the practice of
storing and retrieving
frequently accessed
data within a single
local cache. This cache
could be a part of the
application or system
and may exist on a
single machine or
server.
Distributed caching extends
the concept of caching to a
network of interconnected
nodes or servers. In a
distributed caching system, the
cache is spread across multiple
machines, enabling the sharing
of cached data among these
nodes.
Architecture In a traditional caching
setup, data is stored in
a local cache, which is
often located in
memory. The cache is
directly accessible by
the application running
on a single machine.
Distributed caching involves a
network of cache nodes, where
each node may have its local
cache. These nodes
communicate and collaborate
to share cached data. The
architecture is designed to
scale horizontally by adding
more nodes to the distributed
environment.


Scale
Caching is suitable for
smaller-scale
scenarios, such as a
single server or a
standalone application.
It is effective when the
performance
improvement gained
from caching on a
local machine is
sufficient.
Distributed caching is
designed to address the
challenges of larger-scale
systems and applications. It is
particularly beneficial in
scenarios where data needs to
be shared and accessed across
multiple nodes to achieve
improved performance and
scalability.
Use cases
Common use cases for
caching include
improving the
performance of local
applications, reducing
database access times,
and speeding up the
retrieval of frequently
accessed resources
within a single server
or application.
Distributed caching is applied
in scenarios where the scale
and distribution of data access
require a more coordinated
approach. It is commonly used
in large-scale web
applications, distributed
databases, and microservices
architectures.
Consistency
and
coordination
In the regular caching
(single-node) scenario,
maintaining cache
consistency is
relatively
straightforward.
However, cache
invalidation and
ensuring data
coherence in a
distributed
Distributed caching systems
implement mechanisms for
maintaining consistency across
nodes, ensuring that all nodes
have access to the most up-todate and synchronized data.
Coordination protocols and
distributed cache management
strategies are employed to
handle potential challenges.


environment can be
more complex.
Table 6.1: Regular caching versus distributed caching
While both regular and distributed caching aim to improve system performance by storing
frequently accessed data, distributed caching extends the concept to a network of interconnected
nodes, addressing the challenges of larger-scale and distributed computing environments. The
choice between regular caching and distributed caching depends on the specific requirements and
scale of the application or system being designed.
Use cases
Let’s look at some of the use cases of distributed caching
Web applications: Distributed caching is extensively used in web applications to store frequently accessed data such as user
sessions, page fragments, and database query results
Database query results: Caching frequently executed database queries or query results helps reduce the need for repeated
database access
Content Delivery Networks (CDNs): CDNs leverage distributed caching to store and serve static content (images, videos,
stylesheets) at strategically located edge servers
Session management: Storing session data in a distributed cache allows for efficient and scalable session management in
web applications
API response caching: Caching API responses helps reduce the load on backend servers and speeds up the delivery of
frequently requested data
Real-time analytics: Caching aggregated or frequently queried analytics data enables faster retrieval for real-time reporting
and dashboard generation
Message queues: Caching message queues can improve the efficiency of message processing systems by storing
intermediate results
Benefits of using a distributed cache
Here are some of the benefits of using the distributed cache:
Performance improvement: Distributed caching significantly reduces data access times by keeping frequently accessed
data in memory. This results in faster response times and improved system performance.
Scalability: As system demands grow, distributed caching allows for easy scaling by adding more cache nodes. This ensures
that the cache can accommodate increased loads and maintain optimal performance.


Reduced load on backend systems: By serving frequently accessed data from the cache, distributed caching minimizes the
load on backend storage systems (such as databases and file systems), leading to more efficient resource utilization. The
number of requests going to the backend is reduced. This can immensely help mitigate the risks of origin servers going
down by an overwhelming margin in the event of a DDoS attack.
Fault tolerance: Distributed caching systems often provide redundancy and fault tolerance. In the event of a node failure,
other nodes can continue serving cached data, ensuring system reliability and continuity.
Consistent access times: Caching ensures consistent and predictable access times for frequently requested data, regardless
of the size or complexity of the overall data set.
Cost savings: Improved performance and reduced load on backend systems can lead to cost savings in terms of
infrastructure resources, as the need for additional servers or resources may be minimized.
Enhanced user experience: Faster response times and improved system performance contribute to a more responsive and
seamless user experience, which is crucial in applications and services where user satisfaction is paramount.
In summary, distributed caching proves invaluable in addressing performance bottlenecks,
enhancing scalability and security, and optimizing resource utilization in a variety of computing
scenarios. The specific benefits and use cases may vary based on the requirements of the
application or system that is being designed.
Challenges of using distributed caching
While distributed caching provides numerous benefits, it also comes with certain potential
drawbacks and challenges. It’s important to be aware of these considerations when implementing
distributed caching solutions.
Here are some potential drawbacks:
Consistency challenges: Maintaining data consistency across multiple cache nodes can be challenging. Ensuring that all
nodes have the most up-to-date information requires coordination mechanisms, and achieving perfect consistency may
introduce latency or trade-offs.
Cache invalidation complexity: Cache invalidation, the process of removing or updating cached data when the underlying
data changes, can be complex in a distributed environment. Ensuring that all nodes are aware of changes and update their
caches accordingly can introduce additional overhead.
Increased complexity and configuration: Setting up and configuring a distributed caching system can be more complex
than using a single-node caching solution. The need for coordination, partitioning strategies, and proper configuration
settings adds complexity to the deployment and maintenance of the system.
Network overhead: The communication between cache nodes introduces network overhead. In situations where nodes need
to coordinate and share updates, network latency and bandwidth can become limiting factors, especially in geographically
distributed systems.


Potential for cache staleness: Due to the distributed nature of caching, there’s a risk of cache staleness, where a node might
serve outdated data if it hasn’t received updates from other nodes. This issue can occur during cache expiration periods or
when the cache is not properly synchronized.
Data partitioning challenges: Distributing data across multiple cache nodes requires effective partitioning strategies. Poor
partitioning decisions can lead to uneven distribution of data, resulting in some nodes being overloaded while others are
underutilized.
High memory usage: In scenarios where the cache needs to store large amounts of data, distributed caching systems may
consume a significant amount of memory across multiple nodes. This can impact the overall system’s resource usage and
scalability.
Cost: Implementing and managing a distributed caching solution may incur additional costs, both in terms of infrastructure
(hardware or cloud resources) and the complexity of maintenance. The benefits should be carefully weighed against the
associated costs.
Data access patterns: Certain access patterns, such as random or infrequent access, might not benefit as much from
distributed caching. In such cases, the overhead of maintaining a distributed cache may outweigh the performance gains.
Limited utility for write-intensive workloads: Distributed caching is typically more beneficial for read-intensive
workloads. Write-intensive workloads, where data is frequently updated, may face challenges in maintaining consistency
and coordination across cache nodes.
It’s essential to carefully evaluate the specific requirements of your application and consider
these drawbacks when deciding whether to implement distributed caching. Additionally,
choosing the right distributed caching solution, configuring it properly, and monitoring its
performance can help mitigate some of these challenges.
In the subsequent sections, we will delve deeper into the intricacies of designing and
implementing distributed caching solutions, exploring key considerations, architectures, and best
practices that contribute to the successful integration of distributed caching into diverse
computing environments.
Designing a distributed cache
We will now design a distributed cache. Let’s start by noting down the requirements and then
creating a high-level diagram with all the components. We will then go into a detailed design
hashing out the inner workings of the components.
Requirements
Thinking about the requirements for the distributed cache, we can categorize them into two
areas: functional and non-functional requirements.


The following are the functional requirements:
put(key, value): We should be able to add a key and value pair to the cache
get(key): Given the key, we should be able to fetch the corresponding value
The following are the non-functional requirements:
Highly performant: The system should deliver fast and efficient access to cached data, providing low-latency responses
and high throughput. Performance is a critical aspect of distributed caching, especially in scenarios where quick access to
frequently used data is essential for improving overall system responsiveness.
Highly scalable: The system should be capable of efficiently handling increased workloads and growing demands by adding
more resources or nodes. This is important so that the system can handle a higher volume of data, requests, or users without
a significant degradation in performance.
Highly available: We should minimize downtime and ensure that the service remains accessible and operational even in the
presence of failures or disruptions. This is a critical attribute for systems that require continuous accessibility to support
mission-critical applications and services.
Design journey
Now that we have listed the requirements, let’s build the solution iteratively by enhancing the
design in each iteration. First, we will think about what is an appropriate data structure for the
cache. Then we will look into the most suitable system arrangements and deployment strategies,
and then we will evaluate whether the design satisfies the functional and non-functional
requirements.
Data structure for a cache
What are our options for the underlying data structure that we will use to store and retrieve the
cache entries? A very simple solution would be to use a HashMap (or a HashTable) that can
store a key and corresponding value. HashMap data structure has constant time put and get
operations and therefore is a good choice.
What if the HashMap size becomes more than the capacity of the server memory? This can be
mitigated by adopting an eviction policy. Let’s take a look at the various options we have.
Cache eviction policies
Cache eviction refers to the process of deciding which entries to remove from the cache when it
reaches its capacity or when certain conditions are met. Let’s explore some of the cache eviction


policies.
Insertion based, not accounting for access time:
First in, First out (FIFO): Consider a restaurant reservation system that holds a limited number of reservations
in a cache. When the cache is full and a new reservation is made, the oldest reservation (the one made first) is
evicted to accommodate the new one. This ensures that reservations are managed in the order in which they were
received, adhering to the FIFO principle.
Last in, First out (LIFO): Social media story suggestions are an example of the LIFO principle. The news
suggestion that was just shown to the user can be evicted when the cache is full to give a chance to stories that
were not suggested recently.
Access based:
MRU: The idea here is to evict the most recently used entry. Document editing software is an example. Imagine
a piece of document editing software that keeps a cache of recently opened documents for quick access. If the
cache size is limited and a new document is opened, the most recently used document (the one that was just
accessed or edited) might be evicted to make room for the new one. This approach is useful in scenarios where
the most recent items are considered the least likely to be needed again immediately, following the MRU
eviction policy.
Least Recently Used (LRU): This policy is very common. It evicts the least recently used entry and keeps the
most recently used entries. A web browser cache is an example. Web browsers often use LRU cache policies for
storing web pages. When a user visits a website, the page is cached. If the browser cache is full and a new page
needs to be cached, the page that has not been accessed for the longest time is evicted. This ensures that
frequently accessed pages are kept in the cache, improving browsing speed and performance.
LFU: This policy involves evicting the least frequently used entry. In a music streaming service, for example, a
cache might be used to store the most frequently played songs for quicker access. If the cache becomes full, the
song that has been played the least number of times is evicted to make room for a new song. This ensures that
the cache holds the songs that users listen to most often, improving the efficiency and user experience of the
service.
Eviction triggers can be size-based or days-based. If the cache has reached its capacity 'C', or if
the entries are more than 'N' days old, the entries will be evicted based on one of the preceding
logic policies.
Designing an LRU cache
As we see, there are many cache eviction policies out there, but a simple and popular eviction
policy is to evict the LRU cache entry. Let’s note down the high-level requirements for an LRU
cache:
There is a limited number of entries in the cache (let’s call it N)


We need to be able to add an entry to the cache in O(1)
We need to be able to remove an entry to the cache in O(1)
Let’s consider a doubly linked list and a HashMap combination data structure as shown in
Figure 6.1 and see whether this works well:
Figure 6.1: A doubly linked list and a HashMap
There are two flows here – a read flow and a write flow. For simplicity, let’s assume that writes
would go to the database directly. Only in the read time, if there is a cache miss, will the cache


be populated.
Let us consider the different cases based on the key being present in the cache and not present in
the cache.
So, the primary flow is a read flow – given a key, we need to find its corresponding valueObject
(we will be referring to it as valueObject to differentiate between this “value” and the HashMap’s
value field). The valueObject is the actual data we are trying to cache here. This could be the
profile of a user, for example, which would look like this:
    valueObject: {
        "name": "John Doe",
        "city": "San Jose",
        "state": "California"
}
So, the first step is to check the HashMap to see whether the key is present. Here are a few
possible scenarios:
Case 1: The key is not present in the HashMap; it’s a cache miss. So, it’s a new entry. The number of entries in the cache is
less than N. In this instance, follow these steps:
Fetch the valueObject for the key from the actual database
Create a node with the valueObject and add it in front of this linked list.
Add the corresponding entry in the HashMap with the key and value as the pointer to the node in the linked list.
Case 2: The key is not present in the HashMap; it’s a cache miss. So, it’s a new entry, and the number of entries in the
cache is equal to N. In this instance, you can follow these steps:
Since the cache is full, we need to create space.
Go to the end of the LinekdList and fetch the entry at the end, which is the least recently used entry.
Remove this entry from the LinkedList as well as from the HashMap
Now, the number of entries is less than N. This case is exactly like in the first case, so follow
those steps.
Fetch the valueObject for the key from the actual database.
Create a node with the valueObject and add it in front of this linked list.
Add the corresponding entry in the HashMap with the key and value as the pointer to the node in the linked list.
Case 3: The key is present in the HashMap, so It’s an existing entry:


Locate the node in the LinkedList with this key by doing a lookup in the hashMap and following the
pointer stored in the value field of the HashMap.
We need to move this node to the front of the LinkedList.
All of these operations can be done in O(1) time.
Putting the system together
Now that we have designed the data structure, let’s go into the various arrangements for
deploying the cache.
Solution 1 – a co-located cache solution
As shown in Figure 6.2, we can run the cache as a process and co-locate it in the same machine
as the app server. To scale up, we would have as many cache instances as the app servers, since
they are co-located. This approach is scalable too. Some details on the solution are as follows:
Advantage: It will be quicker to do a cache lookup since it will be an interprocess call in the same machine.
Challenge: What happens if the machine goes down? The new request would be handled by a new app server, but the cache
would be empty. We may need to think about a cache solution where the cache is not co-located with the AppServer
machine. There are trade-offs to be made here, but let’s think about a standalone cache solution in the next section.
Figure 6.2: A co-located cache solution
Solution 2 – a standalone cache solution
As shown in Figure 6.3, we can deploy the cache on an independently scalable cluster of hosts.
The details for this solution are as follows:


Advantage: It can support the scale to any frequency and concurrency of requests. This can also scale independently of the
number of app servers.
Challenge: We may need to share the cache entries based on the cache key and put some sort of load balancer or lookup
map to find which host contains the appropriate key. We can use a simple modulo approach to shard the keys, but a better
strategy would be using a consistent hashing approach we discussed earlier in this book (in Chapter 3).
Figure 6.3: A standalone cache solution
Next, let us explore how can we choose between the two cache solutions.
How to choose between the two cache arrangements
Choosing between a co-located cache with the app server and a standalone cache involves
considering various factors related to your application’s requirements, architecture, and
priorities. Table 6.2 shows some key considerations to help you make an informed decision:
Co-located cache
Standalone cache


Performance
requirements
If low-latency access to
cached data is crucial and
the application demands fast
response times, a co-located
cache may be preferred due
to direct access without
network overhead.
If scalability and high
throughput are more
critical than minimal
latency, a standalone
cache that can be
independently scaled
might be a better
choice.
Scalability
It is suitable for scenarios
where the application and
cache can scale together,
and the scalability demands
are not extremely high.
It offers better
scalability as the cache
can be scaled
independently, allowing
for more granular
control over resource
allocation.
Resource
sharing
Shared resources with the
app server can be efficient
in terms of memory and
CPU utilization.
It provides isolation,
avoiding resource
contention between the
app server and cache,
which can be beneficial
for large-scale systems.
Flexibility
It comes with a simpler
configuration and
integration process but may
have limitations in terms of
technology choices and
configurations.
It comes with more
flexibility in choosing
caching solutions based
on specific
requirements and the
ability to select
technologies
independently.
Dependency
and isolation
It is tightly coupled with the
app server; changes or
It offers independence
and isolation, reducing


issues in one may impact the
other.
the risk of system-wide
disruptions due to
changes in one
component.
Operational
complexity
It offers simpler deployment
and management but may
lack the flexibility to
address specific caching
needs.
It may involve more
complex configuration
and management but
allows for tailored
solutions and updates
without affecting the
app server.
Infrastructure
and cost
It may be more costeffective in terms of
infrastructure, as it shares
resources with the app
server.
It requires additional
infrastructure,
potentially leading to
higher operational
costs.
Network
latency
tolerance
It is well-suited for
applications where
minimizing network latency
is a top priority.
It is acceptable if the
application can tolerate
slightly higher network
latency for cache
access.
Table 6.2: Key considerations to choose between a co-located or standalone cache
Ultimately, the choice between co-located and standalone caching depends on the specific needs
of your application, and a careful evaluation of the trade-offs in terms of performance,
scalability, flexibility, and operational considerations is essential. Additionally, considering
future growth and changes in requirements can help ensure that the chosen caching architecture
aligns with the long-term goals of your system.
Evaluate the design against the requirements
This seems like a good point to evaluate if we have met our functional and non-functional
requirements. Functional requirements seem to be satisfied with the put and get functions


working fine.
Let’s look at the non-functional requirements.
Highly performant: The operations are all O(1), so it’s very efficient.
Highly scalable: This seems to be fine since we can scale it to any number of requests and concurrency by scaling the
number of hosts where this cache is deployed and sharding them properly.
Highly available: This criterion seems to still not be fully satisfied. If one host goes down, then we lose the entire shard.
Let’s dig in a bit more and think about a strategy to address the high availability requirement. We
can achieve this via data replication – keeping multiple copies with each copy deployed into
different hosts. So, if one host goes down, there will still be additional copies in different hosts
that can serve the request. Typically, we would keep two additional copies, so there are three
copies on three different hosts. One of them is a primary copy and the other two are secondary
copies. The secondary copies can also be used to serve higher read traffic. Writes would go to
the primary host first and then be replicated to secondary hosts.
This data replication arrangement introduces another challenge – consistency. There is a tradeoff here as to whether to choose availability or consistency. We have discussed this trade-off in
earlier chapters. So, we will not go into a lot of detail.
Popular distributed cache solutions
There are two very popular distributed cache solutions out there in the market – Redis and
Memcached. Redis and Memcached are two widely used distributed cache solutions, prized for
their speed and simplicity in efficiently storing and retrieving data. Understanding the strengths
of Redis and Memcached is crucial for developers looking to optimize data access in distributed
environments. Let’s explore each one of them a bit more.
Redis
Redis is a versatile in-memory data store that supports a range of data structures such as strings,
lists, sets, and hashes. Offering persistence options for durability, it goes beyond basic storage
capabilities with advanced features including pub/sub messaging, transactions, and Lua scripting.
This flexibility allows Redis to serve multiple purposes, functioning as a cache, message broker,
or even a full-fledged database. Let’s explore its common use cases, scalability, and community
support.


Use cases
Caching in web applications
Real-time analytics
Session storage
Leaderboards and counting systems
Scalability
Redis is horizontally scalable through sharding, allowing you to distribute data across multiple nodes.
Community and support
Active open-source community with widespread adoption
Robust documentation and community support
Memcached
Memcached stands out as a straightforward key-value store, functioning seamlessly as an inmemory caching solution. Known for its lightweight and user-friendly design, it efficiently
supports simple data types while leveraging a distributed architecture to enhance its scalability.
Let’s see what use cases Memcached is good for, its scalability and the community support it
has.
Use cases
Caching in web applications.
Session storage.
Database result caching.
Distributed systems where a simple key-value store is sufficient.
Scalability
Memcached is designed to scale horizontally by adding more nodes to the cache cluster.
Data is distributed across nodes using consistent hashing.
Community and support
Well-established and widely adopted, with a mature code base


Simple and easy to integrate, suitable for various programming languages
How to choose between Redis and Memcached
Here are some considerations for choosing between the two options:
Use case specificity: The choice between Redis and Memcached often depends on specific use case requirements. Redis,
with its versatile data structures, is suitable for a broader range of scenarios, while Memcached excels in simplicity and
speed for basic key-value caching.
Persistence: Redis provides options for persistence, making it more suitable for use cases requiring data durability.
Memcached, being an in-memory cache, does not inherently provide persistent storage.
Data structure support: Redis supports a wider range of data structures and features, making it more versatile in certain
scenarios where complex data manipulation is required.
Ease of use: Memcached is known for its simplicity and straightforward design, making it easy to integrate and operate.
Redis, despite being more feature-rich, might have a steeper learning curve for some users.
Ultimately, the choice between Redis and Memcached depends on the specific requirements of
your application, the complexity of data manipulation needed, and considerations such as ease of
use and community support.
Summary
In this chapter, we started by defining caching as a computing technique to store and manage
copies of data for faster access. The primary goal is to reduce the time and resources needed to
retrieve frequently accessed or computationally expensive information. We then covered some
other key concepts including cached data, cache hit, cache miss, and eviction policies
Then we delved into distributed caching. Distributed caching optimizes data access by
strategically storing frequently accessed information across multiple interconnected servers or
nodes. We learned that it aims to mitigate performance challenges related to slower, disk-based
storage systems. This is effective in scenarios where rapid access to data is crucial, such as in
web applications and databases. We explored the differences between caching and distributed
caching in terms of the following dimensions: scope, architecture, scale, and use cases.
We talked about the benefits of distributed caching such as performance improvement,
scalability, reduced load on backend systems, and fault tolerance. We discussed the drawbacks
and challenges of distributed caching, such as consistency challenges, cache invalidation
complexity, increased complexity and configuration, and network overhead.


Then we started tackling the problem of actually designing a distributed cache, starting with
documenting the functional and non-functional requirements and then thinking about the core
data structure for caches. We iteratively enhanced the solution by tackling the challenges faced.
We then evaluated our design against the functional and non-functional requirements.
Lastly, we looked at two of the most popular distributed cache solutions and discussed their key
features, as well as their use cases. We also discussed how scalable they are. We also discussed
which considerations to look into to choose one over the other.
In the next chapter, we will explore pub/sub and distributed queues.

## Examples & Scenarios

- form of a hardware cache (for example, a CPU cache) or a software-based cache (for example, an in-memory cache).
Cached data: This refers to the copies of data that are stored in the cache. The data is usually obtained from a slower, more
permanent storage location (such as a database or disk) and is kept in the cache for faster retrieval.
Cache hit: A cache hit occurs when the requested data is found in the cache. This results in a faster retrieval process since
the data is readily available without the need to go to the original data source.
Cache miss: A cache miss happens when the requested data is not found in the cache. In this case, the system needs to fetch
the data from the original source and store a copy in the cache for future access.
Eviction: In situations where the cache has limited space, eviction may occur when the cache is full and needs to make room
for new data. The system may remove less frequently accessed, less recently used, or older data to accommodate new
entries.

- LFU: This policy involves evicting the least frequently used entry. In a music streaming service, for example, a
cache might be used to store the most frequently played songs for quicker access. If the cache becomes full, the
song that has been played the least number of times is evicted to make room for a new song. This ensures that
the cache holds the songs that users listen to most often, improving the efficiency and user experience of the
service.
Eviction triggers can be size-based or days-based. If the cache has reached its capacity 'C', or if
the entries are more than 'N' days old, the entries will be evicted based on one of the preceding
logic policies.
Designing an LRU cache
As we see, there are many cache eviction policies out there, but a simple and popular eviction

- profile of a user, for example, which would look like this:
valueObject: {
"name": "John Doe",
"city": "San Jose",
"state": "California"
}
So, the first step is to check the HashMap to see whether the key is present. Here are a few
possible scenarios:
Case 1: The key is not present in the HashMap; it’s a cache miss. So, it’s a new entry. The number of entries in the cache is
less than N. In this instance, follow these steps:

## Tables & Comparisons

|  | Regular caching | Distributed caching |
| --- | --- | --- |
| Scope | Caching typically
refers to the practice of
storing and retrieving
frequently accessed
data within a single
local cache. This cache
could be a part of the
application or system
and may exist on a
single machine or
server. | Distributed caching extends
the concept of caching to a
network of interconnected
nodes or servers. In a
distributed caching system, the
cache is spread across multiple
machines, enabling the sharing
of cached data among these
nodes. |
| Architecture | In a traditional caching
setup, data is stored in
a local cache, which is
often located in
memory. The cache is
directly accessible by
the application running
on a single machine. | Distributed caching involves a
network of cache nodes, where
each node may have its local
cache. These nodes
communicate and collaborate
to share cached data. The
architecture is designed to
scale horizontally by adding
more nodes to the distributed
environment. |

| Scale | Caching is suitable for
smaller-scale
scenarios, such as a
single server or a
standalone application.
It is effective when the
performance
improvement gained
from caching on a
local machine is
sufficient. | Distributed caching is
designed to address the
challenges of larger-scale
systems and applications. It is
particularly beneficial in
scenarios where data needs to
be shared and accessed across
multiple nodes to achieve
improved performance and
scalability. |
| --- | --- | --- |
| Use cases | Common use cases for
caching include
improving the
performance of local
applications, reducing
database access times,
and speeding up the
retrieval of frequently
accessed resources
within a single server
or application. | Distributed caching is applied
in scenarios where the scale
and distribution of data access
require a more coordinated
approach. It is commonly used
in large-scale web
applications, distributed
databases, and microservices
architectures. |
| Consistency
and
coordination | In the regular caching
(single-node) scenario,
maintaining cache
consistency is
relatively
straightforward.
However, cache
invalidation and
ensuring data
coherence in a
distributed | Distributed caching systems
implement mechanisms for
maintaining consistency across
nodes, ensuring that all nodes
have access to the most up-to-
date and synchronized data.
Coordination protocols and
distributed cache management
strategies are employed to
handle potential challenges. |

| Performance
requirements | If low-latency access to
cached data is crucial and
the application demands fast
response times, a co-located
cache may be preferred due
to direct access without
network overhead. | If scalability and high
throughput are more
critical than minimal
latency, a standalone
cache that can be
independently scaled
might be a better
choice. |
| --- | --- | --- |
| Scalability | It is suitable for scenarios
where the application and
cache can scale together,
and the scalability demands
are not extremely high. | It offers better
scalability as the cache
can be scaled
independently, allowing
for more granular
control over resource
allocation. |
| Resource
sharing | Shared resources with the
app server can be efficient
in terms of memory and
CPU utilization. | It provides isolation,
avoiding resource
contention between the
app server and cache,
which can be beneficial
for large-scale systems. |
| Flexibility | It comes with a simpler
configuration and
integration process but may
have limitations in terms of
technology choices and
configurations. | It comes with more
flexibility in choosing
caching solutions based
on specific
requirements and the
ability to select
technologies
independently. |

|  | issues in one may impact the
other. | the risk of system-wide
disruptions due to
changes in one
component. |
| --- | --- | --- |
| Operational
complexity | It offers simpler deployment
and management but may
lack the flexibility to
address specific caching
needs. | It may involve more
complex configuration
and management but
allows for tailored
solutions and updates
without affecting the
app server. |
| Infrastructure
and cost | It may be more cost-
effective in terms of
infrastructure, as it shares
resources with the app
server. | It requires additional
infrastructure,
potentially leading to
higher operational
costs. |
| Network
latency
tolerance | It is well-suited for
applications where
minimizing network latency
is a top priority. | It is acceptable if the
application can tolerate
slightly higher network
latency for cache
access. |

