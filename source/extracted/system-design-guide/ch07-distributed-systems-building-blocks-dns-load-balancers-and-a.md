# Chapter 4: Distributed Systems Building Blocks: DNS, Load Balancers, and Application Gateways

> Source: System Design Guide for Software Professionals, Chapter 7, Pages 91-112

## Key Concepts

- 4
Distributed Systems Building Blocks: DNS, Load
Balancers, and Application Gateways
In this chapter, we shift our focus to the essential building blocks that are instrumental in crafting
robust, scal
- performed seamlessly, allowing users to access websites using easy-to-remember names. This is
shown in Figure 4.1.
Figure 4.1: Basic architecture of DNS
The DNS is comprised of architectural

## Content

4
Distributed Systems Building Blocks: DNS, Load
Balancers, and Application Gateways
In this chapter, we shift our focus to the essential building blocks that are instrumental in crafting
robust, scalable, and efficient systems. Mastering the intricacies of the Domain Name System
(DNS), load balancers, and application gateways allows for a granular, bottom-up approach to
system design, a complement to the theoretical principles discussed in previous chapters.
The knowledge gained here will not only deepen your understanding of system architecture but
will also provide you with practical skills that are useful in real-world applications. From
ensuring global connectivity with DNS to optimizing server performance with load balancers,
and further securing your applications through application gateways, this chapter equips you to
tackle complex design challenges head-on.
We will cover the following topics in this chapter:
Exploring DNS
Load balancers
Application gateways
Let us first understand what a DNS is.
Exploring DNS
The DNS maps human-friendly domain names to machine-readable IP addresses. It provides the
translation service between domain names and IP addresses. When a user enters a domain name
in the browser, the browser needs to find the corresponding IP address to complete the request. It
does this by querying the DNS infrastructure. The DNS works transparently in the background.
Users are unaware of the domain name to IP mapping performed by DNS. When the browser
obtains the IP address from DNS, it forwards the user’s request to the destination web server at
that IP address.
In short, DNS performs the crucial function of translating domain names that users type into their
browsers to IP addresses that computers use to locate websites and resources. This translation is


performed seamlessly, allowing users to access websites using easy-to-remember names. This is
shown in Figure 4.1.
Figure 4.1: Basic architecture of DNS
The DNS is comprised of architectural concepts such as name servers, resource records, caching,
and hierarchical arrangement of DNS servers. Let us now look at each of these concepts:
Name servers: The DNS is not a single server, but a network of numerous servers. DNS servers that respond to user queries
are called name servers.
Resource records (RRs): The DNS database stores mappings in units called RRs. There are different RR types that store
different kinds of information.
Some common RR types are as follows:
A records: These map hostnames to IP addresses
NS records: These map domain names to authoritative name servers
CNAME records: These map alias hostnames to canonical hostnames
MX records: These map domains to mail servers
Caching: The DNS uses caching at multiple levels to reduce latency. Caching reduces the load on the DNS infrastructure
since it handles queries for the entire internet.
Hierarchy: DNS name servers are arranged hierarchically, allowing DNS to scale to its enormous size and query load. The
hierarchical structure manages the entire DNS database.


In short, DNS performs its function through a network of distributed name servers, a database of
resource records, caching at multiple levels, and a hierarchical structure. These details, as shown
in Figure 4.2, allow DNS to provide fast, scalable translation of domain names to IP addresses
for the entire internet.
Figure 4.2: DNS name server hierarchy
As seen in the figure, there are different types of DNS name servers. Name servers at different
hierarchies are a critical aspect of the DNS infrastructure. Let us understand the different types of
server hierarchy:
Root-level name servers: These servers receive queries from local resolvers. They maintain name servers for top-level
domains such as .com, .edu, and .us. For example, for google.com, root servers will return servers for the .com toplevel domain.
Top-level domain (TLD) name servers: These servers hold the IP addresses of authoritative name servers for their domain.
For the .com TLD, they would return the authoritative servers for google.com.
Authoritative name servers: These are the organization’s actual DNS servers that provide the IP addresses of their web and
application servers.


To summarize, we can say that the DNS resolver starts the query process. Root servers point to
TLD servers, which point to authoritative servers that finally resolve domain names to IP
addresses. This hierarchy allows DNS to scale for the entire internet.
Here are the steps:
1. Resolvers initiate user queries.
2. Root servers point to TLD servers.
3. TLD servers point to authoritative servers.
4. Authoritative servers provide final IP addresses.
5. The hierarchy enables DNS to scale for the internet.
Let us now understand how DNS querying works.
DNS querying
DNS queries basically come in two flavors: iterative and recursive. These are the main ways a
computer finds out what IP address corresponds to a website name such as www.google.com.
Let’s dig into what each type is all about.
Iterative queries
In an Iterative query, your computer, through its local DNS resolver, does all the legwork. It goes
from asking the root name servers at the top of the DNS chain, down to the TLD servers (e.g.,
.com, .org), and then directly asks the authoritative name servers for the website you want to
visit.
Your computer directly talks to the following:
Root servers
TLD servers
Website’s authoritative name servers
Your computer walks through these steps one by one.
Figure 4.3 shows how an iterative query works.


Figure 4.3: Iterative DNS queries
Next, let us understand how the DNS recursive queries work.
Recursive queries
Recursive queries are a bit different. Your computer asks its local DNS resolver for the website’s
IP address. The local resolver then takes over and does all the asking, moving from the root
servers to the TLD servers, and finally to the authoritative servers for the website.
You ask your local resolver for the IP. The local resolver then talks to the following:
Root servers
TLD servers


Website’s authoritative name servers
The resolver then gives you back the IP address you need.
Figure 4.4 shows how recursive queries work.
Figure 4.4: Recursive DNS queries
In summary, with iterative queries, the local resolver goes through the DNS hierarchy itself.
With recursive queries, the local resolver recursively asks higher-level servers that forward the
query down the hierarchy until the final IP address is obtained.
CAN YOU GUESS WHICH MECHANISM IS PREFERRED TO
REDUCE THE LOAD ON THE DNS INFRASTRUCTURE?
Hint: it is not recursive. Recursive DNS queries will require an increase in memory to maintain the recursion structure,
whereas iterative does not need that. This implies that recursion will get slower over time as more state needs to be


maintained.
When you type a website name, you almost instantaneously get the results of the web page. This
slick interface is made possible due to DNS caching, which we will discuss in the next section.
Caching
Caching means temporarily storing frequently accessed RRs. An RR is a unit of data that binds a
name to a value in the DNS database.
Caching provides two main benefits:
It reduces response time for users by providing answers locally instead of querying the DNS hierarchy
It decreases network traffic by avoiding unnecessary queries up the DNS hierarchy
Caching at multiple levels can significantly reduce the load on the DNS infrastructure since it
handles queries for the entire internet.
There are many places where caching can be implemented:
In the user’s browser
In the operating system
In the local name server within the user’s network
In the internet service provider (ISP) resolvers
Therefore, caching DNS resource records at different levels allows answers to be provided
locally. This reduces response times for users and decreases traffic in the DNS system, especially
when caching is implemented at multiple levels.
DNS is a distributed system and like any other distributed system, it implements some form of
scalability, reliability, and consistency, which we will learn in the next section.
Scalability, reliability, and consistency in DNS
When we talk about any large-scale system, especially something as vast as DNS, there are three
buzzwords that often come up: scalability, reliability, and consistency. These are like the three
pillars that hold up any robust system. Let’s dive into how DNS checks off these crucial boxes.
Scalability


The DNS achieves high scalability through its hierarchical design with root, top-level domain,
and authoritative name servers distributed worldwide. Roughly 1,000 replicated instances of 13
root-level servers handle the initial user queries. They point to TLD servers, which, in turn, point
to authoritative servers managed by individual organizations. This hierarchical structure divides
the load between different levels, allowing DNS to scale to serve billions of daily queries for the
entire internet.
The distributed nature of DNS also contributes to its scalability. Redundant replicated DNS
servers are located strategically around the globe to serve user requests with low latency. If a
DNS server becomes overloaded or unavailable, other servers can respond to queries, further
enhancing the scalability of the system.
Reliability
The DNS demonstrates high reliability through various mechanisms. Caching at multiple levels –
in browsers, operating systems, local networks, and ISP resolvers – provides answers to users
even if some DNS servers are temporarily unavailable.
The redundant replicated DNS servers distributed worldwide also improve reliability by serving
requests with low latency.
While DNS uses the User Datagram Protocol (UDP) for most queries and responses, which is
inherently unreliable, it compensates through techniques such as resending requests if no
response is received. This allows DNS to achieve acceptable levels of reliability for its core
function.
Consistency
Though DNS achieves high performance by sacrificing strong consistency, it does provide
eventual consistency through techniques such as time-to-live for cached records and lazy
propagation of updates across the DNS infrastructure. Updates within the DNS system can take
from seconds to days to be reflected across all servers.
However, performance remains the higher priority in DNS design. Even though there are
techniques to ensure consistency, the acceptable level of consistency is one that does not degrade
performance significantly.


This covers the basics of DNS and we will now explore the second basic building block (i.e.,
load balancers).
Load balancers
Load balancing distributes workload across multiple computing resources, such as servers,
CPUs, hard drives, and network links, to achieve optimal resource utilization, maximize
throughput, minimize response time, and avoid overload. Figure 4.5 shows a load balancer
connected to clients on one end and a pool of server machines on the other end.
Figure 4.5: Load balancer
The following are some key points about load balancing:
It allows the spread of a huge amount of traffic across multiple servers so that no single server gets overloaded.
It improves fault tolerance by failing over (i.e., retrying the failed requests from failed or slowed-down servers to
functioning servers).
It increases overall service availability since requests can still be serviced by the functioning servers even if some servers
fail.
It can enable a graceful degradation of performance during periods of high load instead of a complete failure of the system.
As load increases, response time may increase but the system remains operational.
It enables horizontal scaling by adding more servers into the pool to handle higher loads.


Load balancing is achieved through dedicated hardware devices called load balancers or software
solutions that distribute incoming traffic among multiple servers. A load balancer sits in front of
the servers and monitors the load on each server, forwarding incoming requests to the server that
is least busy.
Placing load balancers
Load balancers can be placed at various points in a system’s architecture, as seen in Figure 4.6,
to distribute load and achieve scalability. This includes placing them between clients and
frontend servers, between different tiers of a multi-tier system, and potentially between any two
services with multiple instances.
Figure 4.6: Placing load balancers
Placing load balancers between clients and servers allows incoming client requests to be
distributed to multiple server instances, which is common for scaling web servers. Load
balancers can also be used between layers of a multi-tier system, such as between web servers
and application servers, and between application servers and database servers. This enables each
layer to be scaled independently, based on its needs.
Distributing traffic at different points in the system also isolates layers from each other,
protecting upper layers if a lower layer becomes overloaded or has an outage. The load balancers
can detect faults and failures at one layer and redirect traffic around them, keeping the overall
system operational.


In summary, the flexibility of load balancers allows them to be strategically placed at critical
points in a system’s architecture to distribute load, improve scalability, and provide high
availability. Load balancers sit at the intersection of where traffic enters and exits different
system tiers, serving as a control point for optimizing resource utilization across the system.
Advantages of load balancers
Load balancers are not just leveraged for distributing load and requests, but can improve the
availability and health of the systems:
Load balancers can implement health checks to determine whether backend servers are available or not. This prevents
clients from sending requests to unavailable servers.
Load balancers can terminate TLS (Transport Layer Security)connections to improve the reliability of backend servers. This
prevents attackers from using TLS connections to overload backend servers. When a load balancer terminates TLS
connections, it acts as a secure gateway for the incoming traffic. Instead of sending encrypted data directly to the backend
servers, the load balancer decrypts the data first. This means the backend servers receive unencrypted traffic, which is easier
for them to handle because they don’t have to spend resources on decryption. As a result, the servers can focus on their
primary tasks, such as processing requests and delivering content, without being bogged down by the additional workload of
decrypting TLS traffic. This leads to more efficient server performance and reduces the risk of servers being overloaded,
especially during high-traffic periods.
Load balancers can analyze traffic patterns and perform intelligent load-balancing algorithms to distribute requests to servers
in a way that maximizes resource utilization.
Overall, health checking, TLS termination, and analytics help improve the reliability and
availability of backend servers.
Global and local load balancing
Load balancing is required at both a global and local scale. As shown in Figure 4.7, global
server load balancing (GSLB) distributes traffic across data centers in different geographical
regions, while local load balancing focuses on improving resource utilization within a single data
center.


Figure 4.7: Global and local load balancing
GSLB intelligently forwards incoming global traffic to the appropriate data center based on
factors such as users’ locations, data center health, and the number of hosting servers. It enables
automatic failover to alternate data centers during power or network failures. GSLB can be
deployed on-premises or obtained as a service (load balancing as a service (LBaaS)).
Each data center uses local load balancers to distribute traffic to servers within that region. The
local load balancers report health and capacity information to the GSLB, which uses this data to
determine how to route incoming traffic to the different data centers.
DNS and GSLB
DNS can also perform GSLB to some extent by returning multiple IP addresses for a DNS query.
Different clients will receive those IP addresses in a rotated order, distributing traffic to the
different data centers in a round-robin fashion.
However, round-robin DNS load balancing has limitations. It cannot account for uneven demand
from different ISPs or detect crashed servers. DNS uses short time-to-live durations for cache


entries to enable more effective load balancing.
Overall, both global and local load balancing layers work together to achieve the optimal
distribution of incoming traffic across a system with multiple data centers and servers.
While DNS load balancing provides some level of global load distribution, it has limitations that
necessitate local load balancers within data centers:
The small 512-byte size of DNS packets means DNS cannot include all possible server IP addresses in its responses to
clients. This limits its load-balancing capabilities.
Clients can arbitrarily select from the set of IP addresses returned by DNS, potentially choosing addresses for busy data
centers. DNS has limited control over client behavior.
DNS cannot determine the closest server for a given client to connect to, though geolocation and anycasting techniques
could help. However, these are not trivial solutions.
During failures, recovery through DNS can be slow due to caching, especially when time-to-live values are long.
To address some of these limitations, local load balancers within data centers are needed.
Client applications can connect to local load balancers using virtual IP addresses and these local
load balancers distribute the incoming requests from clients to all the available servers.
In summary, while DNS load balancing provides a basic level of global load distribution, local
load balancers provide more intelligent and effective load balancing within data centers. They
can implement sophisticated techniques to distribute load optimally among backend servers. So,
both layers – global and local load balancing – are required to achieve high performance and
scalability at both the data center and global levels.
Load balancer algorithms
Load balancers use various algorithms to determine how to distribute incoming client requests to
backend servers. Common algorithms include the following:
Round-robin scheduling: This simply assigns each new request to the next server in the list, cycling through the servers in
order. This is the simplest algorithm but does not account for differences in server capabilities or load.
Weighted round-robin: This assigns weights to each server based on its capacity. Servers with higher weights receive a
proportionally higher number of requests. This accounts for differences in server capabilities.
The least connections algorithm: This assigns new requests to the server with the fewest existing connections. This helps
distribute load more evenly among servers, especially when some requests take longer to serve. The load balancer must
track the number of connections to each server.


The least response time algorithm: This assigns new requests to the server with the shortest response time, prioritizing
performance-sensitive services.
IP hash, URL hash, and consistent hashing algorithms: These assign requests based on hashing the client’s IP address or
request URL, respectively. This is useful when different clients or URLs need to be routed to specific servers.
In general, load balancers choose algorithms that consider relevant factors such as server
capacity and load, request characteristics, and application requirements to achieve their goals of
optimizing resource utilization, throughput, response times, and fault tolerance. The simplest
algorithms may not distribute the load optimally, while more sophisticated algorithms can
require additional state tracking.
Static versus dynamic algorithms
Load balancing algorithms can be classified as either static or dynamic based on whether they
consider the state of the servers.
Forwarding decisions are made based on server configuration alone by static algorithms, which
are often used in simple load balancing.
Dynamic algorithms do consider the current or recent state of the servers, such as their load
levels and health. They maintain state by communicating with the servers, which adds
communication overhead and complexity. Dynamic algorithms require load balancers to
exchange information to make decisions, making the system more modular. They also only
forward requests to active servers.
While dynamic algorithms are more complex than static algorithms, they provide better load
balancing results by making more informed decisions based on up-to-date server state. They can
adapt to changes over time, unlike static algorithms.
In practice, dynamic algorithms are preferred because the improved load balancing they provide
outweighs their additional complexity. However, for simple use cases with few servers, static
algorithms may be sufficient and easier to implement. The choice of static versus dynamic
algorithms involves trade-offs between simplicity, performance, and adaptability.
Overall, maintaining an accurate state of the backend servers – whether their load levels,
response times, or health status – allows load balancers to make the most effective forwarding
decisions to optimize resource utilization and meet performance goals.
Stateful versus stateless


Load balancers can be classified as stateful or stateless based on whether they maintain session
information for clients.
Stateful load balancers maintain state information that maps incoming clients to backend servers.
They incorporate this state into their load-balancing algorithms to make forwarding decisions.
However, stateful load balancers require all load balancers to share state information, which
increases complexity and limits scalability.
Stateful load balancers maintain a data structure that tracks the session information for all clients
connected to the backend servers. When new requests come in for existing sessions, the load
balancer can route them to the correct backend server based on the stored session information.
In comparison, stateless load balancers do not maintain any client session state. They use
consistent hashing algorithms to map requests to servers. While this makes them faster and more
scalable, they may not be as resilient during infrastructure changes since consistent hashing alone
is not enough to route requests to the correct server. Local state is still required along with
consistent hashing in some cases.
In general, maintaining state information across multiple load balancers is considered stateful
load balancing, while maintaining a local internal state within a single load balancer is stateless
load balancing.
The choice between stateful and stateless load balancing involves trade-offs between resilience,
scalability, and complexity. Stateful approaches can provide higher availability and reliability,
while stateless approaches tend to be faster, more scalable, and simpler to implement. Most
production systems employ a hybrid approach.
Overall, both stateful and stateless load balancing techniques are useful depending on the
requirements and architecture of the system they are balancing. Let us now discuss the types of
load balancers.
Load balancing at different layers of the Open
Systems Interconnection (OSI) model
Load balancers can operate at different layers of the OSI model, impacting their capabilities and
performance. The OSI model is a conceptual framework used to understand and standardize the
functions of a computing system without regard to its underlying internal structure and


technology. It is divided into seven layers, each specifying particular network functions such as
physical transmission, data link, network routing, transport, session management, presentation
formatting, and application services. This layered approach helps in the development,
troubleshooting, and management of network protocols and communication between different
systems and devices, promoting interoperability and flexibility in network architecture.
Layer 4 load balancers distribute load based on the transport layer protocols, TCP and UDP.
These load balancers provide stability for connection-oriented protocols since they maintain the
TCP/UDP connection and forward requests from a client to the same server on the backend.
Moreover, some load balancers help with TLS termination, too. Layer 7 load balancers
distribute the load based on the application layer data from protocols such as HTTP. They can
make more intelligent forwarding decisions based on HTTP headers, URLs, cookies, and other
application-specific information such as user IDs. In addition to TLS termination, Layer 7 load
balancers can perform functions such as rate limiting, HTTP routing, and header rewriting.
While Layer 7 load balancers can take into account more context from the application to
optimize load distribution, Layer 4 load balancers tend to be faster since they operate at a lower
level.
In practice, most load-balancing solutions employ a combination of both Layer 4 and Layer 7
techniques to balance performance requirements, application needs, and protocol support. Layer
4 load balancers provide a basic level of load distribution and stability for TCP-based
applications, while Layer 7 load balancers enable more intelligent and customized load
distribution for application-specific use cases.
The choice of Layer 4 versus Layer 7 load balancing depends on factors such as the application
architecture and protocols used, performance requirements, and the level of control and
optimization needed over load distribution. Both approaches have benefits for achieving the
goals of high availability, scalability, and resource utilization. We will now look at the
deployment of load balancers.
Deployment of load balancers
In a typical data center, load balancing usually involves different layers, each with its own role:
Tier 0 uses the DNS system to switch between multiple IP addresses for a certain website or service.


Tier 1 uses special routers to split internet traffic based on things such as IP address or simple rules, such as taking turns
(round-robin). These routers make it easier to add more load balancers as needed.
Tier 2 uses Layer 4 load balancers to make sure that all pieces of data related to a single online activity go to the same nextlevel load balancer. They use techniques such as consistent hashing and keep track of changes in the network setup.
Tier 3 uses Layer 7 load balancers that are in direct touch with the main servers. These balancers check how well the servers
are working and share the work between servers that are up and running well. They also take on some tasks to make the
servers work more efficiently. Sometimes, these balancers work closely with the main servers themselves.
This layered setup offers benefits such as being able to scale up easily, staying available, being
resilient, and making smart use of resources at each layer. The first few layers handle basic
traffic splitting, while the higher layers use more information to distribute the load in a smarter
way. Together, this makes the entire system work better, faster, and more reliably.
Implementing load balancers
Load balancers can be implemented in various ways to meet the needs of different organizations
and applications:
Hardware load balancers were the first type of load balancers, introduced in the 1990s. They work as standalone devices and
can handle many concurrent users due to their performance. However, they are expensive and have some drawbacks. They
are difficult to configure, have high maintenance costs, and vendor lock-in issues. While availability is important, additional
hardware is needed for failover.
Software load balancers have become more popular due to their flexibility, programmability, and lower cost. They scale
well as requirements grow and availability is easier to achieve by adding additional commodity hardware. They can also
provide predictive analytics to prepare for future traffic.
Cloud load balancers, known as LBaaS, are offered by cloud providers. Users pay based on usage or service-level
agreements. They can perform global traffic management between cloud regions in addition to local load balancing. Their
advantages include ease of use, scalability, metered costs, and advanced monitoring capabilities.
In general, software and cloud load balancers are gaining popularity due to their benefits over
hardware load balancers. They provide a more cost-effective and manageable solution for most
organizations today.
However, hardware load balancers still offer the best performance for extremely high throughput
requirements. A hybrid approach employing different load balancer types can optimize
performance, availability, and cost for complex systems.
The ideal load balancer implementation depends on factors such as the system architecture,
throughput needs, management requirements, costs, and resource availability. Each type has pros


and cons, so the solution needs to be chosen based on an organization’s unique needs and goals.
Let us now discuss our last building block, the application gateway/API gateway.
Application gateways
While load balancers provide basic traffic distribution services, application gateways offer more
advanced intermediary proxy functionality tailored for modern cloud-based environments.
An application gateway sits between clients and backend services, intercepting traffic to provide
routing, security, acceleration, analytics, and adaptability capabilities. Application gateways are
especially beneficial for architectures based on microservices, where numerous independent
services must be aggregated into unified APIs.
We will cover the key features and benefits of application gateways, their importance for
microservices, real-world implementation options, and critical design considerations when
integrating them into cloud architectures. Figure 4.8 shows a typical API gateway, which is the
first point of contact for incoming API traffic and covers different aspects of security, AuthN,
AuthZ, caching, and even load balancing.


Figure 4.8: A typical API gateway
Let us now explore the features and capabilities of the application gateways (also referred to as
API gateways in many cases) in more detail.
Features and capabilities
Application gateways differ from basic load balancers in the more specialized proxy services
they provide:
Advanced request routing: Application gateways route incoming requests to the appropriate backend service through rules
matching on factors such as hostname, path, headers, and source IP. This advanced routing is crucial in microservices
environments comprised of diverse dynamic services that require more logic to map requests.
Security: Gateways centralize shared security services, protecting all backend applications and services. These include
authentication, access controls, TLS termination, DDoS (Distributed Denial of Service) protection, and integrating web


application firewalls (WAFs) to guard against OWASP (Open Web Application Security Project) threats.
Acceleration and offloading: To improve performance, gateways implement features such as caching, compression, TCP
connection management, and TLS termination so that backend services are not burdened by CPU-intensive tasks.
Application gateways absorb these tasks at the edge.
Observability: As a centralized intermediary, gateways aggregate logging, metrics, and traces providing valuable
application visibility. Unified insights into all traffic facilitate monitoring, analytics, and debugging.
Adaptability: Gateways enable adapting requests and responses to gracefully handle changing backend service capabilities.
For example, protocol translation and request shaping for legacy services.
These capabilities make application gateways well suited for the demands of organizing logic,
security, and reliability in modern service-oriented architectures. Many organizations such as
Netflix are known for their microservices-based architectures. There are thousands of
microservices deployed in production at Netflix. API gateways help with these microservices as
well, as we will see in the next section.
Microservices architectures
Microservices approaches decompose monoliths into collections of independent, reusable
services. These loosely coupled services communicate through well-defined interfaces using
lightweight protocols such as REST/HTTP.
Microservices environments involve numerous discrete services developed and deployed
independently. This dynamic system presents challenges in exposing cohesive APIs to clients,
handling cross-cutting concerns, and coordinating services.
Application gateways are crucial for microservices to do the following:
Aggregate numerous microservices into unified logical APIs exposed to clients. This decouples clients from volatile
backend implementations.
Implement service discovery and dynamic request routing to backend services, load balancing across instances.
Handle cross-cutting concerns such as security, monitoring, and reliability in a centralized place, avoiding code duplication
across services.
Enable releasing updated gateway versions independently of backend services.
Accelerate development by allowing services to be developed and scaled independently.
In short, application gateways provide the abstraction layer to coordinate microservices into
cohesive systems and handle common integration needs. Different cloud providers have different


approaches to application gateway implementation, and we will briefly talk about some of them
in the next section.
Cloud-native implementations
Leading cloud providers offer fully managed application gateway services that integrate tightly
with their technology stacks:
AWS: Amazon API Gateway handles API creation, deployment, management, and security. Application Load Balancer
routes traffic to AWS services and containers.
Microsoft Azure: Azure Application Gateway provides advanced Layer 7 load balancing along with WAF, SSL (Secure
Sockets Layer) offload, end-to-end TLS encryption, and autoscaling capabilities.
Google Cloud Platform: Cloud Armor provides DDoS protection and a WAF that integrates with Google’s network
infrastructure. Cloud CDN (Content Distribution Network) offers caching and acceleration.
Kubernetes environments: Ingress controllers such as Istio, Kong, Traefik, and Ambassador act as API gateways for
Kubernetes clusters, handling ingress HTTP/HTTPS traffic.
These serverless, auto-scaling gateways simplify operational overhead for organizations
leveraging cloud-native architectures. Along with cloud-native implementations, many
enterprises also choose on-premise options.
On-premises options
Application gateways or API gateways are not only present in cloud environments. For many
enterprises, especially in the financial domain, a lot of services and applications are hosted in
their own data centers. These enterprises prefer leveraging open-source software that can be
seamlessly deployed in on-premise environments. Some popular application gateway platforms
for on-premises environments are outlined in the following list:
Kong: Kong Gateway and Kong Mesh offer API gateway and service mesh capabilities using lightweight proxy servers.
Plugins support authentication, security, analytics, and more.
Tyk: Tyk API Gateway provides an open-source gateway with robust access control, developer portal capabilities, and
REST API-driven configuration.
NGINX: NGINX can be configured as an API gateway and load balancer, with rate limiting, access control, and service
discovery integrations.
HAProxy: HAProxy is a fast, lightweight load balancer and proxy that can be configured for Layer 7 application delivery.


These open-source options run on commodity infrastructure, providing flexibility for onpremises gateway implementations. With their advanced routing, security, acceleration, and
coordination capabilities, application gateways are integral components for implementing
reliable, scalable microservices architectures.
Summary
This chapter provided a comprehensive overview of three fundamental building blocks used in
distributed system design – DNS, load balancers, and application gateways. We learned how
DNS provides a directory service translating domain names to IP addresses through a globally
distributed hierarchy of name servers. Load balancers distribute requests across backend servers
using algorithms that optimize performance and reliability. Application gateways act as
specialized proxies providing advanced routing, security, acceleration, and coordination logic
tailored for modern cloud architectures, especially critical for microservices. In this chapter, we
also covered some nuances of these basic building blocks, for example, the DNS caching for
lower latency and traffic, some load balancer algorithms and implementations in different layers
of the OSI model, and application gateway support for providing a unified front to distributed
services on the backend. These are the basic building blocks of modern enterprise systems
deployed at scale. Almost every system design interview would require you to describe these
systems and how they work.
In the next chapter, we will study another cornerstone of any modern system – databases and
storage.

## Examples & Scenarios

- domains such as .com, .edu, and .us. For example, for google.com, root servers will return servers for the .com toplevel domain.
Top-level domain (TLD) name servers: These servers hold the IP addresses of authoritative name servers for their domain.
For the .com TLD, they would return the authoritative servers for google.com.
Authoritative name servers: These are the organization’s actual DNS servers that provide the IP addresses of their web and
application servers.

- from asking the root name servers at the top of the DNS chain, down to the TLD servers (e.g.,
.com, .org), and then directly asks the authoritative name servers for the website you want to
visit.
Your computer directly talks to the following:
Root servers
TLD servers
Website’s authoritative name servers
Your computer walks through these steps one by one.
Figure 4.3 shows how an iterative query works.

- For example, protocol translation and request shaping for legacy services.
These capabilities make application gateways well suited for the demands of organizing logic,
security, and reliability in modern service-oriented architectures. Many organizations such as
Netflix are known for their microservices-based architectures. There are thousands of
microservices deployed in production at Netflix. API gateways help with these microservices as
well, as we will see in the next section.
Microservices architectures
Microservices approaches decompose monoliths into collections of independent, reusable
services. These loosely coupled services communicate through well-defined interfaces using
lightweight protocols such as REST/HTTP.

- also covered some nuances of these basic building blocks, for example, the DNS caching for
lower latency and traffic, some load balancer algorithms and implementations in different layers
of the OSI model, and application gateway support for providing a unified front to distributed
services on the backend. These are the basic building blocks of modern enterprise systems
deployed at scale. Almost every system design interview would require you to describe these
systems and how they work.
In the next chapter, we will study another cornerstone of any modern system – databases and
storage.

