# Source Inventory

## YouTube Video Reports

### 1.md
Covers foundational distributed systems principles including client-server vs. peer-to-peer models, API contracts, traffic management, and container orchestration in Kubernetes.

- Client-server model vs. peer-to-peer (P2P) architecture
- API design as a technical contract (Twitter API case study)
- Load balancing algorithms (IP hashing, round robin, least connections)
- Forward proxies vs. reverse proxies
- Rate limiting and throttling (fixed window, token bucket)
- Feature flags and progressive releases (canary vs. flag-based)
- ACID transactions and database integrity
- Container runtimes (OCI, runc, containerd, CRI-O) and Docker Shim deprecation
- Kubernetes cost management (spot instances, affinity rules, HPA)

### 2.md
Comprehensive system design handbook covering scalability foundations, networking, data storage strategies, real-time communication, and multiple real-world case studies at scale.

- Vertical vs. horizontal scaling trade-offs
- Microservices and API gateway architecture
- 3-stage infrastructure maturity model (startup, growth, enterprise)
- SQL vs. NoSQL database selection (Postgres, Cassandra, MongoDB)
- CDN and media persistence with S3
- Full-text search with Elasticsearch and Change Data Capture (CDC)
- SSE vs. WebSockets for real-time communication
- Fan-out on write vs. fan-out on read
- Case studies: Twitter (hybrid timeline), Facebook Live Comments, Ticketmaster (two-phase booking, distributed locking), Tinder (geospatial indexing, atomic swiping), UPI payments
- Observability stack (Prometheus, Grafana, ELK)

### 3.md
Focuses on the requirement framework for system design, the CAP theorem, traffic management layers, data architecture, real-time messaging, and detailed case studies with an emphasis on consistency trade-offs.

- Functional vs. non-functional requirements
- CAP theorem: consistency vs. availability trade-offs by use case
- Layer 4 vs. Layer 7 load balancing
- API gateway vs. reverse proxy roles and the complexity budget
- SQL vs. NoSQL storage engines by use case
- Cassandra append-only architecture and compaction
- SSE vs. WebSockets and Pub/Sub fan-out patterns
- Case studies: Twitter (hybrid fan-out), Ticketmaster (edge caching, Redis TTL locks), Tinder (Bloom filters, atomic Redis operations), UPI (PSP model), virtual waiting queues
- Security pillars: AuthN/AuthZ, encryption, rate limiting, input validation

### 4.md
Deep dive into data storage paradigms (relational, NoSQL, object storage), Redis as a distributed performance layer, sharding strategies, recommendation engines, communication protocols, and serverless trade-offs.

- Relational vs. NoSQL decision matrix (structure, storage, scale, access)
- Object storage mechanics (S3/GCS): flat namespaces, immutable writes, 11 nines durability
- Metadata/data split pattern and pre-signed URLs
- Multipart uploads for large files
- Redis: single-threaded model, hot key mitigation, CRC hash slot distribution
- Redis patterns: rate limiters, sorted set leaderboards, async job queues (streams), geospatial API, PubSub
- Sharding: shard key selection (cardinality, distribution, query alignment)
- Range-based, hash-based, and directory-based distribution strategies
- Celebrity hotspot mitigation (compound keys, dedicated shards)
- Two-phase commit (2PC) vs. Saga pattern for cross-shard transactions
- Recommendation engine pipeline (candidate generation, ranking, reranking)
- Vector search and HNSW algorithms
- Video conferencing: WebRTC mesh, MCU, SFU
- Traffic patterns (predictable, unpredictable, interconnected spikes)
- Serverless (Lambda) vendor lock-in risks
- Event sourcing as append-only audit trail

### 5.md
Covers foundational system metrics, network infrastructure (VPCs, subnets, gateways), load balancing, caching strategies, data storage with partitioning, Kubernetes pillars, auto-scaling, and video streaming architecture.

- Latency, throughput, and the "nines" of availability (99.9% to 99.999%)
- P99 tail latency as the key metric
- CAP theorem and network partition handling
- Network infrastructure: Internet Gateway vs. NAT Gateway, bastion hosts, security groups
- Layer 4 vs. Layer 7 load balancing with algorithm selection
- Caching strategies: write-through, write-around, write-back
- CDN edge locations and database indexing (primary, secondary, composite)
- SQL vs. NoSQL: polyglot persistence approach
- Horizontal partitioning (sharding) and consistent hashing
- Auto-scaling with Horizontal Pod Autoscaler (HPA)
- Exponential backoff with jitter and circuit breaker pattern
- Kafka architecture: partitions as append-only logs, consumer groups, hot partition mitigation
- Communication protocols: REST, gRPC (10x faster with protobufs), GraphQL
- WebSockets, SSE, WebRTC for real-time communication
- Idempotency in API design
- Kubernetes five pillars (computation, networking, storage, security, custom resources)
- Adaptive bitrate streaming (HLS/MPEG-DASH) and index files (M3U8)
- Five-point methodology for architectural analysis

### 6.md
Interview-focused system design framework covering the Hello Interview delivery methodology, fanout problem, DynamoDB deep dive, real-world scenario breakdowns, and probabilistic data structures for approximation.

- Hello Interview delivery framework (requirements, entities, APIs, HLD, deep dives)
- Back-of-the-envelope estimation as a design tool
- Fanout on read vs. fanout on write (pull vs. push models)
- Hot shard / celebrity problem: random suffixes, N-cache strategy
- SQS vs. Kafka for reliability (visibility timeouts, DLQ, exponential backoff)
- Consistency models: eventual vs. strong
- DynamoDB: partition key + sort key architecture, GSI vs. LSI
- DAX (DynamoDB Accelerator) and DynamoDB Streams (CDC)
- DynamoDB ACID transactions (up to 100 items)
- Case studies: Facebook News Feed (hybrid fanout), Facebook Post Search (inverted index, Count-Min Sketch), WhatsApp/Messenger (inbox pattern, WebSocket + Redis PubSub), Web Crawler (bandwidth math, politeness via robots.txt), Ad Click Aggregator (Kappa/Lambda, logarithmic counting)
- Probabilistic data structures: Bloom filters, Count-Min Sketch, HyperLogLog
- Memory vs. disk trade-offs (Redis vs. S3)

### 7.md
Comprehensive guide to distributed systems foundations including scaling paradigms, consistency models, database internals (ACID, TSDB, LSM trees), communication patterns (event-driven vs. request-response), and Kubernetes observability.

- Vertical vs. horizontal scaling and availability "nines"
- Reliability vs. availability distinction
- Strong consistency (synchronous replication) vs. eventual consistency (BASE philosophy)
- Gossip protocol for P2P state management (epidemic protocol)
- ACID compliance in relational databases
- Partitioning: vertical, horizontal, and sharding across nodes
- Time series databases (TSDB): LSM trees, write-ahead log, memtable
- Delta encoding and delta-of-deltas compression (Facebook Gorilla paper)
- Downsampling for storage cost management
- Request-response vs. event-driven (choreography vs. orchestration)
- Saga pattern for distributed transactions
- Orchestrator pattern (AWS Step Functions) with e-commerce fulfillment case study
- Kubernetes five pillars and custom resources
- Observability: logging (ELK) vs. monitoring (Prometheus/Grafana)
- Service monitoring objects for Prometheus scraping
- Video streaming evolution: progressive download, RTMP/RTSP, adaptive bitrate streaming
- HLS/MPEG-DASH chunking and M3U8 index files

### 8.md
Focuses on strategic data modeling, database indexing mechanics (B-tree, hash, geospatial, inverted), consistent hashing with virtual nodes, Cassandra deep dive, caching architectures, and probabilistic data structures.

- Five database types compared: relational, document, key-value, wide-column, graph
- Normalization (entity-driven) vs. denormalization (query-driven) schema design
- B-tree vs. hash index trade-offs
- Geospatial indexing: geohashing, quad-trees, R-trees (PostGIS)
- Inverted index for full-text search (Elasticsearch)
- Consistent hashing and the hash ring with virtual nodes
- Cassandra deep dive: keyspaces, partition keys, clustering keys, leaderless architecture
- Gossip protocol for peer-to-peer coordination
- Cassandra tunable consistency (ANY, ONE, QUORUM, ALL)
- Cassandra persistence path: commit log, memtable, SSTable, Bloom filter, compaction
- Caching layers: external (Redis/Memcached), in-process, CDN, client-side
- Cache patterns: cache-aside, read-through, write-through, write-behind
- Cache stampede (thundering herd), stale data, and hot key mitigations
- Probabilistic data structures: Bloom filter, Count-Min Sketch, HyperLogLog
- Case study: Dropbox/Google Drive (chunking, fingerprinting, pre-signed URLs, delta sync)

### 9.md
Covers networking fundamentals, communication protocols (TCP/UDP, WebSockets), API design (REST, GraphQL, gRPC), data management (SQL vs. NoSQL, caching, CAP theorem), scalability patterns, CQRS, event sourcing, and observability.

- IP addressing, DNS, and the evolution from on-premise to cloud (CAPEX vs. OPEX)
- Client-server relationship fundamentals
- TCP vs. UDP transport protocols
- WebSockets for bidirectional communication
- Forward vs. reverse proxy roles
- REST vs. GraphQL vs. gRPC API design
- HTTP methods and idempotency (GET, POST, PUT, PATCH, DELETE)
- Request anatomy: path params, query params, headers, body
- SQL vs. NoSQL selection criteria
- Object storage (S3) for unstructured media
- Caching with Redis: cache-aside and read-through patterns
- CAP theorem: strong, eventual, causal, and read-your-own-writes consistency
- Vertical vs. horizontal scaling
- Consistent hashing for data distribution
- Circuit breaker pattern and message queues for fault tolerance
- CQRS (Command Query Responsibility Segregation)
- Event sourcing with append-only logs and hydration
- Four golden signals of observability (metrics, logs, traces, events)
- Back-of-the-envelope QPS calculations and availability "nines"

---

## PDF Books (Extracted)

### Designing Data-Intensive Applications (Martin Kleppmann)
**Chapters extracted:** 15

#### ch01-part-i-foundations-of-data-systems.md
Introduction to Part I of the book, providing an overview of the four foundational chapters covering data systems on single and distributed machines.

- Overview of reliability, scalability, and maintainability
- Data models and query languages
- Storage and retrieval engines
- Encoding and evolution

#### ch02-reliable-scalable-and-maintainable-applications.md
Defines the core goals of data-intensive applications: reliability, scalability, and maintainability, and explores what each means in practice.

- Data-intensive vs. compute-intensive applications
- Reliability: hardware faults, software errors, human errors
- Scalability: describing load and performance
- Maintainability: operability, simplicity, evolvability

#### ch03-data-models-and-query-languages.md
Examines data models as layers of abstraction and compares relational, document, and graph models with their respective query languages.

- Relational model vs. document model
- Schema-on-read vs. schema-on-write
- Graph data models (property graphs, triple stores)
- Query languages: SQL, MapReduce, Cypher, SPARQL

#### ch04-storage-and-retrieval.md
Explores how databases internally store and retrieve data, covering log-structured and page-oriented storage engines.

- Hash indexes and SSTables
- LSM-trees and B-trees
- Column-oriented storage
- OLTP vs. OLAP workloads

#### ch05-encoding-and-evolution.md
Covers data encoding formats and their role in enabling system evolution through schema changes and rolling upgrades.

- JSON, XML, and binary encoding formats
- Thrift, Protocol Buffers, Avro
- Schema evolution and compatibility (forward/backward)
- Dataflow through databases, services (REST/RPC), and message passing

#### ch06-part-ii-distributed-data.md
Introduction to Part II covering distributed data: reasons for distributing data (scalability, fault tolerance, latency) and shared-nothing architectures.

- Reasons for distributing databases across machines
- Scalability, fault tolerance, and latency requirements
- Shared-nothing architecture
- Replication vs. partitioning overview

#### ch07-replication.md
Covers data replication across multiple machines for latency reduction, fault tolerance, and read throughput scaling.

- Leader-based replication (single-leader, multi-leader)
- Synchronous vs. asynchronous replication
- Handling node outages and replication lag
- Leaderless replication (Dynamo-style)

#### ch08-partitioning.md
Discusses strategies for breaking large datasets into partitions (shards) distributed across multiple nodes.

- Partitioning by key range vs. hash of key
- Secondary indexes and partitioning
- Rebalancing partitions
- Request routing and service discovery

#### ch09-transactions.md
Examines database transactions as a mechanism for grouping reads and writes into logical units to simplify error handling.

- ACID properties (atomicity, consistency, isolation, durability)
- Single-object and multi-object transactions
- Weak isolation levels (read committed, snapshot isolation)
- Serializability (two-phase locking, SSI)

#### ch10-the-trouble-with-distributed-systems.md
Explores the many ways things can go wrong in distributed systems: unreliable networks, clocks, and process pauses.

- Unreliable networks and network partitions
- Unreliable clocks and clock synchronization
- Process pauses (GC, virtualization)
- Knowledge, truth, and lies in distributed systems

#### ch11-consistency-and-consensus.md
Covers consistency guarantees and consensus algorithms for building fault-tolerant distributed systems.

- Linearizability and ordering guarantees
- Sequence number ordering and total order broadcast
- Distributed transactions and consensus
- Paxos, Raft, Zab algorithms

#### ch12-part-iii-derived-data.md
Introduction to Part III on derived data: systems of record vs. derived data, and the need for multiple datastores in large applications.

- Systems of record vs. derived data
- Combining multiple datastores (indexes, caches, analytics)
- Batch processing vs. stream processing overview

#### ch13-batch-processing.md
Explores batch processing systems (offline) that take large input datasets, process them, and produce output, with focus on MapReduce and beyond.

- Unix philosophy and composability
- MapReduce and distributed filesystems
- Dataflow engines (Spark, Flink)
- Joins in batch processing (sort-merge, broadcast)

#### ch14-stream-processing.md
Covers stream processing for handling unbounded, continuously arriving data, bridging batch and real-time processing.

- Transmitting event streams (messaging, logs)
- Databases and streams (CDC, event sourcing)
- Processing streams: uses, time handling, joins
- Fault tolerance in stream processing

#### ch15-the-future-of-data-systems.md
Forward-looking chapter on how data systems should evolve, proposing ideas for improved application design and data integration.

- Data integration challenges and total ordering
- Unbundling databases
- Aiming for correctness (end-to-end argument)
- Ethics and responsibility in data systems

---

### System Design Interview -- An Insider's Guide: Volume 2 (Alex Xu)
**Chapters extracted:** 14

#### ch01-acknowledgments.md
Acknowledgments page listing contributors and reviewers for each chapter of the book.

- Credits for chapter contributors from major tech companies

#### ch02-proximity-service.md
Designs a proximity service for discovering nearby places (restaurants, hotels) similar to Yelp or Google Maps nearby search.

- Geohashing and quad-tree spatial indexing
- Location-based service (LBS) architecture
- Read-heavy system design with caching
- Geospatial database design

#### ch03-nearby-friends.md
Designs a real-time "Nearby Friends" feature similar to Facebook's, showing friends who are geographically close.

- Real-time location tracking
- WebSocket connections for location updates
- Redis Pub/Sub for location broadcasting
- Geohashing for proximity calculation

#### ch04-google-maps.md
Designs a simplified version of Google Maps covering map rendering, routing, and real-time navigation.

- Map tile serving and rendering
- Routing algorithms (Dijkstra, A*)
- Real-time traffic conditions
- Tile-based map architecture and caching

#### ch05-distributed-message-queue.md
Designs a distributed message queue system, covering both traditional message queues and event streaming platforms.

- Message queue vs. event streaming platforms
- Producer/consumer model and consumer groups
- Message ordering and delivery guarantees
- Replication, partitioning, and fault tolerance

#### ch06-metrics-monitoring-and-alerting-system.md
Designs a scalable metrics monitoring and alerting system for large-scale infrastructure health visibility.

- Time-series data storage and retrieval
- Data collection, processing, and alerting pipelines
- Pull vs. push models for metric collection
- Visualization and dashboard design

#### ch07-aggregate-ad-click-events.md
Designs an ad click event aggregation system for real-time digital advertising analytics at Facebook/Google scale.

- Real-time bidding (RTB) process
- Stream processing for click aggregation
- Exactly-once processing semantics
- Lambda/Kappa architecture for dual stream/batch

#### ch08-hotel-reservation-system.md
Designs a hotel reservation system similar to Marriott, covering booking flow, concurrency control, and overbooking.

- Reservation flow and concurrency control
- Database schema for hotel/room inventory
- Idempotency in booking operations
- Overbooking strategy and race condition handling

#### ch09-distributed-email-service.md
Designs a large-scale email service (Gmail/Outlook scale) supporting billions of users with reliability and availability.

- Email protocols (SMTP, IMAP, POP3)
- Email sending and receiving flows
- Distributed storage for email data
- Search functionality and attachment handling

#### ch10-s3-like-object-storage.md
Designs an object storage system similar to Amazon S3 with RESTful API, versioning, and high durability.

- Object storage architecture (data store vs. metadata store)
- Erasure coding for durability
- Multipart upload and versioning
- Garbage collection and data compaction

#### ch11-real-time-gaming-leaderboard.md
Designs a real-time leaderboard for an online mobile game with ranking and score tracking.

- Redis sorted sets for real-time ranking
- Leaderboard pagination and relative ranking
- Score update and retrieval at scale
- Sharding strategies for large player bases

#### ch12-payment-system.md
Designs a payment system for e-commerce covering the full payment lifecycle from checkout to settlement.

- Payment service provider (PSP) integration
- Exactly-once payment processing and idempotency
- Reconciliation and ledger design
- Handling payment failures and retries

#### ch13-digital-wallet.md
Designs a digital wallet backend supporting cross-wallet balance transfers with strong consistency requirements.

- Distributed transaction handling for balance transfers
- Event sourcing for audit trails and consistency
- CQRS pattern for read/write separation
- Reproducibility and correctness verification

#### ch14-stock-exchange.md
Designs an electronic stock exchange system for matching buyers and sellers with stringent latency and throughput requirements.

- Order matching engine design
- Sequencer for deterministic ordering
- Market data and candlestick chart generation
- Low-latency architecture and hot path optimization

---

### Acing the System Design Interview (Zhiyong Tan, 2024)
**Chapters extracted:** 20

#### ch01-acknowledgments.md
Acknowledgments page crediting contributors, reviewers, and the Manning publishing team.

- Credits for reviewers and editorial staff

#### ch02-part-1.md
Introduction to Part 1 covering foundational system design concepts that set the stage for the interview question walkthroughs in Part 2.

- Overview of system design concepts
- Scaling, cloud hosting, databases, distributed transactions
- Common services and functional partitioning

#### ch03-a-walkthrough-of-system-design-concepts.md
Walks through a sample system, introducing core system design concepts including trade-offs, scaling, and cloud vs. bare metal hosting.

- Importance of system design interviews
- Trade-off analysis in architecture
- Scaling a service from single server to distributed
- Cloud hosting vs. bare metal infrastructure

#### ch04-a-typical-system-design-interview-flow.md
Describes the step-by-step flow of a typical system design interview from requirement clarification through API design and data modeling.

- Clarifying requirements and optimizing trade-offs
- Drafting API specifications
- Designing data models
- High-level design and deep dives

#### ch05-non-functional-requirements.md
Covers non-functional requirements in depth, including techniques and technologies for fulfilling performance, availability, and scalability goals.

- Performance, latency, P99, and throughput
- Availability and fault tolerance
- Scalability techniques
- Consistency levels and trade-offs

#### ch06-scaling-databases.md
Discusses database scaling strategies including replication, partitioning, normalization vs. denormalization, and various storage service types.

- Types of storage services
- Database replication strategies
- Event aggregation to reduce writes
- Normalization vs. denormalization
- Partitioning and sharding

#### ch07-distributed-transactions.md
Covers maintaining data consistency across multiple services using distributed transaction patterns.

- Two-phase commit (2PC)
- Saga pattern for distributed workflows
- Event sourcing for scalability and consistency
- Change Data Capture (CDC)

#### ch08-common-services-for-functional-partitioning.md
Discusses cross-cutting concerns and common services used in functional partitioning of large systems.

- API gateway and service mesh/sidecar patterns
- Metadata service for reducing network traffic
- Notification and messaging services
- Frameworks for developing system components

#### ch09-part-2.md
Introduction to Part 2 containing sample system design interview questions that apply the concepts from Part 1.

- Overview of design questions (Craigslist, rate limiting, notifications, autocomplete, Flickr, CDN, messaging, Airbnb, news feed, top-K dashboard)

#### ch10-design-craigslist.md
Designs a Craigslist-like classified ads platform with two distinct user types, geolocation routing, and read-heavy vs. write-heavy patterns.

- Two user types: viewer and poster
- Geolocation-based partitioning
- Read-heavy vs. write-heavy design trade-offs
- Search and listing architecture

#### ch11-design-a-rate-limiting-service.md
Designs a rate-limiting service covering various algorithms and implementation strategies.

- Rate limiting use cases and threat mitigation
- Fixed window, sliding window, token bucket algorithms
- Distributed rate limiting with Redis
- Rate limiting at different system layers

#### ch12-design-a-notificationalerting-service.md
Designs a notification and alerting service that delegates to platform-specific channels (push, SMS, email).

- Feature scope definition for notifications
- Platform-specific channel delegation
- Priority and throttling of notifications
- Reliability and delivery guarantees

#### ch13-design-a-database-batch-auditing-service.md
Designs a service for auditing database tables to find invalid data, focusing on scalability and accuracy.

- Data quality dimensions: validity, uniqueness, timeliness
- Scalable batch auditing solutions
- MapReduce and distributed processing approaches
- Audit rule configuration and scheduling

#### ch14-autocompletetypeahead.md
Designs an autocomplete/typeahead suggestion service with data collection, processing, and real-time querying.

- Autocomplete vs. search distinction
- Trie data structure for prefix matching
- Data collection and processing pipeline
- Ranking and personalization of suggestions

#### ch15-design-flickr.md
Designs a photo-sharing service like Flickr with storage selection based on non-functional requirements and async workflows.

- Storage service selection for photos
- Saga pattern for asynchronous upload workflows
- Image processing and thumbnail generation
- Photo feed and sharing architecture

#### ch16-design-a-content-distribution-network.md
Designs a CDN with frontend metadata storage architecture and edge server management.

- CDN advantages, disadvantages, and failure scenarios
- Push vs. pull CDN strategies
- Edge server placement and routing
- Cache invalidation and consistency

#### ch17-design-a-text-messaging-app.md
Designs a messaging app for billions of users supporting real-time short message delivery with latency vs. cost trade-offs.

- Real-time vs. eventually-consistent delivery
- WebSocket-based message delivery
- Message storage and retrieval at scale
- Group chat design and presence tracking

#### ch18-design-airbnb.md
Designs a reservation system like Airbnb with features for guests and operations staff managing listings and bookings.

- Reservation system design with dual user roles
- Search and listing management
- Booking flow with concurrency control
- Payment integration and availability management

#### ch19-design-a-news-feed.md
Designs a personalized, scalable news feed system serving images and text with filtering capabilities.

- Personalized content ranking
- Fan-out strategies for feed generation
- Content filtering and moderation
- Image and text serving optimization

#### ch20-design-a-dashboard-of-top-10-products-on-amazon-by-sales-vol.md
Designs a real-time dashboard showing the top 10 products on Amazon by sales volume using large-scale data stream aggregation.

- Top-K problem formulation
- Lambda architecture for fast approximate + accurate batch results
- Stream processing for real-time aggregation
- Count-Min Sketch and approximate counting

---

### System Design Guide for Software Professionals
**Chapters extracted:** 20

#### ch01-system-design-guide-for-software-professionals.md
Title page and copyright information for the book, published by Packt Publishing in 2024.

- Publication metadata and copyright

#### ch02-foundations-of-system-design.md
Introduction to Part 1 covering foundational system design concepts: distributed system principles, theorems, and data structures.

- Overview of consistency, availability, partition tolerance
- CAP theorem, PACELC theorem, Paxos, Raft
- Consistent hashing, Bloom filters, HyperLogLog

#### ch03-basics-of-system-design.md
Introduces software system design, its types, and its significance in software development and maintenance.

- What is system design
- Types of system design
- Importance in software development
- Impact on performance and maintenance

#### ch04-distributed-system-attributes.md
Covers the key attributes of distributed systems and the trade-offs required when designing for consistency, availability, and partition tolerance.

- Consistency, availability, and partition tolerance
- Latency, durability, reliability, fault tolerance
- Trade-offs among distributed system attributes
- Hotel booking example for consistency illustration

#### ch05-distributed-systems-theorems-and-data-structures.md
Explores foundational theorems and data structures used in distributed systems design and implementation.

- CAP theorem and PACELC theorem
- FLP impossibility result
- Byzantine Generals Problem (BGP)
- Consistent hashing, Bloom filters, HyperLogLog
- Paxos and Raft consensus algorithms

#### ch06-core-components-of-distributed-systems.md
Introduction to Part 2 covering core building blocks: DNS, load balancers, databases, caches, and message queues.

- Overview of distributed systems building blocks
- DNS, load balancers, application gateways
- Databases, storage, distributed cache
- Pub/Sub and distributed queues

#### ch07-distributed-systems-building-blocks-dns-load-balancers-and-a.md
Covers the essential infrastructure building blocks: DNS architecture, load balancer types and algorithms, and application gateways.

- DNS architecture and resolution workflow
- Load balancer types (L4, L7) and algorithms
- Application gateways and reverse proxies
- SSL/TLS termination and health checks

#### ch08-design-and-implementation-of-system-components-databases-and.md
Deep dive into database and storage system design, covering relational and NoSQL databases, storage engines, and popular database internals.

- Relational vs. NoSQL database selection
- Database internals and storage engines
- Data organization: tables, rows, columns
- Popular databases: design and architecture

#### ch09-distributed-cache.md
Covers distributed caching principles, strategies, and implementation for high-performance systems.

- Caching fundamentals and use cases
- Distributed caching architecture
- Cache eviction policies (LRU, LFU, FIFO)
- Cache consistency and invalidation strategies

#### ch10-pubsub-and-distributed-queues.md
Explores Publish-Subscribe systems and distributed queues as primary messaging patterns in distributed architectures.

- Pub/Sub systems vs. distributed queues
- Message ordering and delivery guarantees
- Designing distributed queues
- Scalability and fault tolerance in messaging

#### ch11-system-design-in-practice.md
Introduction to Part 3 bridging theory and practice with real-world system design case studies and interview preparation.

- Overview of practical design chapters
- API design, security, and metrics
- Case studies: URL shortener, proximity service, Twitter, Instagram, Google Docs, Netflix

#### ch12-design-and-implementation-of-system-components-api-security-.md
Covers API design (REST, gRPC), security practices, and observability (logging, metrics, alerting, tracing) in distributed systems.

- REST and gRPC API design principles
- API security: authentication, authorization, rate limiting
- Logging, metrics, alerting, and tracing
- Distributed system observability

#### ch13-system-design-url-shortener.md
Designs a URL shortener service covering algorithm selection, database design, and scalability considerations.

- URL shortening algorithms and hash functions
- Key generation strategies
- Database design for short URL mappings
- Read-heavy optimization and caching

#### ch14-system-design-proximity-service.md
Designs a proximity service for location-based features like nearby restaurant search and ride-hailing.

- Functional and non-functional requirements
- Geospatial indexing (geohash, quad-tree)
- Read and write path design
- Location-based marketing and dynamic pricing use cases

#### ch15-designing-a-service-like-twitter.md
Designs a Twitter-like microblogging service covering feed generation, data modeling, and scale calculations.

- User registration, authentication, tweet creation
- Timeline/feed generation strategies
- Data model design and scale calculations
- Load balancers, API gateways, caches, databases

#### ch16-designing-a-service-like-instagram.md
Designs an Instagram-like photo-sharing platform covering media storage, feeds, and user engagement features.

- Photo upload and storage architecture
- User feed generation and content delivery
- Media processing pipelines
- Scalable architecture for user-generated content

#### ch17-designing-a-service-like-google-docs.md
Designs a collaborative document editing service like Google Docs with real-time synchronization.

- Real-time collaboration architecture
- Operational Transform (OT) or CRDT for conflict resolution
- Document storage and versioning
- User presence and cursor tracking

#### ch18-designing-a-service-like-netflix.md
Designs a video streaming service like Netflix covering content delivery, encoding, and personalization.

- Video encoding and transcoding pipeline
- Content delivery network (CDN) architecture
- Recommendation engine and personalization
- Adaptive bitrate streaming

#### ch19-tips-for-interviewees.md
Practical tips and strategies for excelling in system design interviews, from preparation to presentation.

- Preparation strategies for system design interviews
- Tips for the interview session
- How to communicate trade-offs effectively
- Leveling considerations based on interview performance

#### ch20-system-design-cheat-sheet.md
Quick-reference cheat sheet covering structured approaches, data store selection, component choices, and protocols for system design interviews.

- Structured approach to problem clarification
- Data store selection by use case
- Component and protocol selection guide
- High-level architectural diagram patterns

---

### System Design - Grokking (Notes)
**Chapters extracted:** 81

This source consists of condensed notes from the Grokking the System Design Interview course. The 81 chapters are fragmented sections covering interview methodology, system design case studies, and foundational concepts. They are organized below by topic grouping.

#### Interview Methodology (ch01, ch06, ch09)
Step-by-step guide for system design interviews covering the structured approach from requirements to detailed design.

- Unstructured nature of SDIs and preparation strategies
- Step-by-step framework: requirements, capacity estimation, high-level design, detailed design
- Trade-off analysis and interviewer-guided deep dives

#### Designing a URL Shortening Service / TinyURL (ch15, ch19, ch22, ch24, ch28)
Designs a URL shortening service like TinyURL covering capacity estimation, database schema, key generation, caching, and security.

- Capacity estimation (500M new URLs/month, 50B redirects)
- Database schema design and data partitioning
- Key Generation Service (KGS) for offline key generation
- Caching strategies and load balancing
- Security and permissions

#### Designing Pastebin (ch32, ch37, ch42, ch46)
Designs a text storage and sharing service like Pastebin with API design, data storage layers, and access controls.

- Design considerations and size limits
- System APIs for create/retrieve/delete
- Datastore layer design
- Security and permissions

#### Designing Instagram (ch55, ch59, ch60, ch63)
Designs a photo-sharing service with focus on reliability, redundancy, data sharding, and caching strategies.

- Database schema and data flow
- Reliability and redundancy patterns
- Data sharding strategies
- Cache and load balancing

#### Designing Dropbox / Google Drive (ch67, ch72, ch74, ch77, ch81)
Designs a cloud file storage service with component-level design, metadata management, and caching.

- Requirements clarification and cloud storage motivation
- Component design for sync and storage
- Metadata database design
- Cloud/block storage architecture
- Caching strategies

#### Designing Facebook Messenger / Chat (ch87, ch90, ch92, ch98)
Designs a real-time messaging system with capacity estimation, message handling, user status management, and group chat.

- Capacity estimation (20B messages/day, 3.6PB for 5 years)
- Message handling and delivery
- Managing user online/offline status
- Group chat architecture

#### Designing Twitter (ch102, ch106, ch108, ch113, ch114)
Designs a Twitter-like service with capacity estimation, high-level architecture, data sharding, monitoring, and extended requirements.

- 1B users, 200M DAU, 100M tweets/day
- High-level system design and feed generation
- Data sharding strategies
- Monitoring and health checks
- Extended requirements (search, trending, notifications)

#### Designing YouTube / Netflix (ch119, ch122, ch124, ch128)
Designs a video sharing/streaming service covering APIs, component design, video deduplication, and fault tolerance.

- System APIs for upload, view, and search
- Detailed component design for video processing
- Video deduplication strategies
- Fault tolerance and reliability

#### Designing Typeahead Suggestion (ch132, ch133, ch137, ch140)
Designs a real-time autocomplete service with trie-based algorithms, persistent storage, replication, and personalization.

- Trie data structure for prefix matching
- Permanent storage of the trie
- Replication and load balancer design
- Personalization of suggestions

#### Designing API Rate Limiter (ch146, ch149, ch150, ch151, ch153)
Designs a rate limiting system covering throttling types, algorithms, and client identification strategies.

- Types of throttling (hard, soft, elastic)
- Fixed window algorithm
- Sliding window algorithm and sliding window with counters
- Rate limiting by IP vs. by user

#### Designing Twitter Search (ch160, ch164)
Designs a search service for tweets with detailed component design and fault tolerance.

- Inverted index for tweet search
- Detailed component design
- Fault tolerance and replication

#### Designing Web Crawler (ch171, ch175, ch176, ch179)
Designs a web crawler covering design considerations, implementation challenges, component design, and trap detection.

- Design considerations for large-scale crawling
- Difficulties: scale, content freshness, duplicates
- Detailed component design (URL frontier, DNS resolver, content parser)
- Crawler traps detection and avoidance

#### Designing Facebook News Feed (ch183, ch187, ch188, ch190)
Designs a news feed system with capacity estimation, high-level and detailed design, and data partitioning.

- Capacity estimation for feed generation
- High-level system design
- Feed generation and ranking algorithms
- Data partitioning strategies

#### Designing Yelp / Nearby Friends (ch195, ch199, ch201, ch205, ch208)
Designs a location-based service with database schema, grid-based indexing, dynamic grids, replication, and ranking.

- Database schema for places and reviews
- Grid-based spatial indexing
- Dynamic-size grids for variable density
- Replication and fault tolerance
- Ranking by proximity and popularity

#### Designing Uber Backend (ch213, ch216)
Designs a ride-sharing service backend covering driver/rider matching algorithms and fault tolerance.

- Geospatial matching of drivers and riders
- Basic system design and matching algorithm
- Fault tolerance and replication
- Real-time location tracking

#### Designing Ticketmaster (ch221, ch224, ch227, ch230, ch233, ch234)
Designs an online ticketing system with requirements, APIs, component design, transaction handling, and data partitioning.

- Requirements and goals for event ticketing
- System APIs for search and booking
- Detailed component design
- Transaction handling (BEGIN TRANSACTION)
- Data partitioning strategies

#### System Design Basics (ch237, ch241, ch243, ch245)
Covers fundamental system design concepts: scalability, manageability, load balancing benefits, and redundancy.

- Scalability principles
- Serviceability and manageability
- Benefits of load balancing
- Redundant load balancers

#### Caching (ch250)
Covers cache eviction policies used in distributed systems.

- LRU, LFU, FIFO eviction policies
- Cache sizing and management

#### Data Partitioning (ch252, ch254)
Covers partitioning methods and common challenges in data partitioning.

- Horizontal, vertical, and directory-based partitioning
- Common problems: joins, referential integrity, rebalancing

#### Indexes, Proxies, SQL vs. NoSQL (ch258, ch260, ch263, ch266)
Covers database indexing trade-offs, proxy types, SQL vs. NoSQL comparison, and NoSQL use cases.

- How indexes decrease write performance
- Forward and reverse proxy server types
- High-level SQL vs. NoSQL differences
- Reasons to use NoSQL databases

#### CAP Theorem (ch267)
Explains the CAP theorem and its implications for distributed system design trade-offs.

- Consistency, availability, and partition tolerance
- Trade-offs in distributed systems
- CP vs. AP system design choices

#### Communication Protocols (ch270, ch274, ch275)
Covers long-polling, WebSockets, and Server-Sent Events as real-time communication protocols.

- How long-polling works
- WebSocket protocol for bidirectional communication
- Server-Sent Events (SSE) for unidirectional streams
