# System Design Glossary

An alphabetical reference of key terms and concepts found across the system design knowledge base sources.

---

## A

- **ACID**: Atomicity, Consistency, Isolation, Durability -- the four properties that guarantee database transactions are processed reliably, ensuring all-or-nothing completion, valid state transitions, independent concurrent execution, and data permanence.
- **Adaptive Bitrate Streaming (ABS)**: A video delivery technique (via HLS or MPEG-DASH) where the source video is encoded into multiple resolutions and segmented into small chunks, allowing the client to dynamically switch quality based on network bandwidth.
- **API (Application Programming Interface)**: A formal contract between software intermediaries that defines endpoints, methods, parameters, and response formats, enabling systems to interact predictably regardless of underlying implementation.
- **API Gateway**: A centralized entry point for microservices that handles cross-cutting concerns such as request routing, authentication, authorization, rate limiting, SSL termination, and logging.
- **Append-Only Log**: An immutable, sequential data structure where new entries are only added to the end, used in event sourcing, Kafka topics, LSM trees, and write-ahead logs for durability and auditability.
- **Autoscaling**: The automatic adjustment of compute resources (e.g., adding or removing server instances) in response to changing traffic loads, commonly implemented via Horizontal Pod Autoscaler (HPA) in Kubernetes.
- **Availability**: The percentage of time a system can accept requests and return desired responses, measured in "nines" (e.g., 99.99% or "four nines" allows 52.6 minutes of downtime per year).

## B

- **Back-of-the-Envelope Estimation**: Quick, order-of-magnitude calculations used during system design to validate feasibility -- for example, computing storage needs (3.6 trillion posts x 1 KB = 3.6 PB) or QPS (10^8 DAU / 10^5 seconds = 1,000 QPS).
- **Back Pressure**: A flow control mechanism where a downstream system signals an upstream producer to slow down when it cannot keep up with the incoming message rate.
- **BASE (Basically Available, Soft state, Eventual consistency)**: An alternative to ACID for distributed systems that prioritizes availability over immediate consistency, accepting that replicas will eventually converge.
- **Bastion Host / Jump Host**: A hardened server in a public subnet that serves as the single audited entry point for SSH access to instances in private subnets.
- **Batch Processing**: Periodically processing accumulated data in bulk, as opposed to real-time stream processing; tools include Airflow, Spark, and Hive with MapReduce.
- **Bloom Filter**: A space-efficient probabilistic data structure that tests set membership, returning "definitely not in the set" or "possibly in the set," used for URL deduplication in web crawlers and avoiding redundant database lookups.
- **B-Tree**: The industry-standard disk-based index structure that maintains sorted data across root nodes, child pointers, and leaf pages, supporting both exact-match and range queries efficiently.
- **Bulkhead Pattern**: A fault-tolerance mechanism that isolates a system into independent pools (e.g., separate thread pools per endpoint) so that failure in one pool does not cascade to the entire system.

## C

- **Cache-Aside (Lazy Loading)**: A caching strategy where the application checks the cache first; on a miss, it fetches from the database and populates the cache for subsequent requests.
- **Cache Stampede (Thundering Herd)**: A failure scenario where a hot cache key expires and millions of simultaneous requests hit the database; mitigated by request coalescing or cache warming.
- **Cache Warming**: Pre-populating a cache with anticipated data before the first user request to eliminate cold-start misses.
- **Canary Release**: A deployment strategy that routes a small percentage of traffic (e.g., 5%) to a new software version to detect issues before full rollout.
- **CAP Theorem**: States that during a network partition in a distributed system, you must choose between Consistency (all nodes see the same data) and Availability (every request receives a response); Partition tolerance is assumed.
- **Cassandra**: A distributed NoSQL wide-column database designed for massive write throughput with no single point of failure, using a leaderless architecture, gossip protocol, tunable consistency (ANY/ONE/QUORUM/ALL), and an append-only storage model (commit log, MemTable, SSTable, compaction).
- **CDC (Change Data Capture)**: A pattern for logging data change events from a source database to an event stream, enabling downstream services to stay synchronized without polluting application logic.
- **CDN (Content Delivery Network)**: A geographically distributed network of edge servers that caches and serves static assets (images, CSS, JS, video) from locations proximate to end users, reducing latency.
- **Checkpointing**: Writing progress markers during data processing so that if a worker fails, the replacement can resume from the last checkpoint rather than reprocessing everything.
- **Circuit Breaker**: A resilience pattern that monitors downstream service failures and "trips" to fail fast when an error threshold is exceeded, preventing cascading failures and allowing the failing service to recover.
- **Client-Server Model**: The primary communication paradigm where a client initiates requests and a centralized server processes them and returns responses, following the HTTP request/response cycle.
- **Compaction**: A background process in append-only storage systems (e.g., Cassandra, LSM trees) that merges immutable SSTables, resolving duplicates and cleaning up deleted data (tombstones).
- **Compensating Transaction**: A reverse operation executed to undo the effects of a previously completed transaction step in a saga, restoring eventual consistency after a failure.
- **Consistent Hashing**: A distribution technique that maps both data keys and server nodes onto a virtual ring (0 to 2^32), so adding or removing a node only affects a small fraction of keys rather than triggering massive redistribution.
- **Consumer Group**: A Kafka concept where multiple consumers share a topic's partitions, ensuring each message is processed by exactly one consumer within the group, enabling horizontal scaling.
- **Count-Min Sketch**: A probabilistic data structure that estimates the frequency of items in a data stream using sub-linear memory, useful for identifying heavy hitters in real-time monitoring.
- **CQRS (Command Query Responsibility Segregation)**: An architectural pattern that separates write operations (commands) from read operations (queries) into different services or data stores, allowing independent optimization and scaling.

## D

- **DAX (DynamoDB Accelerator)**: An in-memory, write-through cache for DynamoDB that provides microsecond read latency.
- **Dead Letter Queue (DLQ)**: A queue that stores messages that could not be processed successfully after multiple retry attempts, enabling later inspection and reprocessing.
- **Delta Encoding**: A compression technique used in time-series databases that stores only the difference between consecutive values rather than absolute values, dramatically reducing storage.
- **Denormalization**: The deliberate duplication of data across tables to eliminate expensive JOIN operations and optimize read latency, at the cost of increased storage and write complexity.
- **DNS (Domain Name System)**: The internet's hierarchical naming system that translates human-readable domain names into machine-identifiable IP addresses.
- **DynamoDB**: AWS's fully managed NoSQL key-value and document database supporting horizontal scaling with consistent hashing, partition keys, sort keys, GSI/LSI, DynamoDB Streams for CDC, and ACID transactions across up to 100 items.

## E

- **ELK Stack**: A combination of Elasticsearch (search and indexing), Logstash (log collection and transformation), and Kibana (visualization and dashboarding) used for centralized logging and log analysis; Beats was later added as a lightweight data shipper.
- **Elasticsearch**: A distributed search and analytics engine that builds inverted indices for full-text search, supporting fuzzy matching, relevance scoring, and near-real-time indexing.
- **Encryption at Rest**: Securing stored data by encrypting it on disk, protecting against unauthorized access to physical storage media.
- **Encryption in Transit**: Protecting data as it moves between systems using protocols like TLS/SSL to prevent interception and tampering.
- **Eventual Consistency**: A consistency model where replicas will converge to the same state given sufficient time, but stale reads are temporarily possible; favored for high-availability systems like social media.
- **Event Driven Architecture (EDA)**: An architectural style where components communicate by announcing events that have already happened rather than requesting work, promoting loose coupling, scalability, and responsiveness.
- **Event Sourcing**: A pattern where all state changes are stored as an immutable, append-only sequence of events (the source of truth), and the current state is reconstructed by replaying ("hydrating") the event log.
- **Exponential Backoff with Jitter**: A retry strategy where wait time between retries increases exponentially, with a random component (jitter) added to prevent synchronized retry storms from multiple clients.

## F

- **Failover**: The process of automatically switching to a standby system component (e.g., promoting a secondary database leader to primary) when the active component fails.
- **Fan-Out on Read (Pull)**: A news feed strategy where feeds are assembled at request time by querying all followed accounts; avoids write amplification but increases read latency.
- **Fan-Out on Write (Push)**: A news feed strategy where a new post is immediately pushed to all followers' pre-computed inboxes; provides ultra-low read latency but causes high write amplification.
- **Feature Flag**: A configuration-driven mechanism (an "if-statement" backed by external config) that allows enabling or disabling features at runtime without a full code deployment, decoupling deployment from release.
- **Forward Proxy**: An intermediary that acts on behalf of the client, concealing the client's identity from the destination server (e.g., for accessing geo-restricted content).

## G

- **GeoDNS**: A DNS service that returns different IP addresses based on the geographic location of the requesting client, routing users to the nearest data center.
- **Geohashing**: A technique that recursively splits the world into a grid and encodes locations as strings where nearby points share common prefixes, enabling efficient proximity queries using standard B-Tree range lookups.
- **Gossip Protocol**: A peer-to-peer communication protocol (also called epidemic protocol) where nodes periodically share state information with randomly selected peers, used by Cassandra and Redis for node discovery and liveness monitoring.
- **Grafana**: An open-source visualization and dashboarding tool commonly paired with Prometheus for real-time system health monitoring.
- **GraphQL**: A query language for APIs that allows clients to specify exactly what data they need in a single request, solving the over-fetching and under-fetching problems of REST.
- **gRPC**: A high-performance RPC framework using Protocol Buffers for binary serialization, achieving 5-10x faster communication than JSON-based REST, widely used for internal microservice communication.
- **GSI (Global Secondary Index)**: A DynamoDB index with a completely different partition key and sort key from the base table, enabling alternative query patterns.

## H

- **Hash Index**: An in-memory index structure providing O(1) key lookups but unable to support range queries or sorting; used in key-value stores like Redis.
- **HDFS (Hadoop Distributed File System)**: A distributed, append-only file system that stores data across DataNodes with configurable replication factors, managed by a NameNode for metadata.
- **HLS (HTTP Live Streaming)**: An adaptive bitrate streaming protocol developed by Apple that segments video into small chunks referenced by an M3U8 manifest file.
- **HNSW (Hierarchical Navigable Small Worlds)**: An algorithm for approximate nearest neighbor search in high-dimensional vector spaces, used in recommendation engines and vector databases.
- **Horizontal Pod Autoscaler (HPA)**: A Kubernetes controller that automatically scales the number of pods based on observed CPU, memory, or custom metrics.
- **Horizontal Scaling (Scaling Out)**: Adding more machines to a system to distribute load, providing theoretically unlimited capacity and fault isolation; the standard approach for internet-scale systems.
- **Hot Key / Hot Shard**: A data key or partition that receives disproportionately high traffic (e.g., a viral celebrity's profile), overwhelming a single node; mitigated by key salting, dedicated shards, or N-cache strategies.
- **HyperLogLog**: A probabilistic algorithm for cardinality estimation (counting distinct elements) that uses constant/bounded memory (approximately 1.5 KB) regardless of the number of unique items.

## I

- **Idempotency**: The property that an operation produces the same result whether executed once or multiple times, critical for safe retries in distributed systems to prevent issues like double-charging.
- **Inverted Index**: A data structure that maps tokens (words, terms) to the documents or records containing them, enabling fast full-text search; the foundation of Elasticsearch.
- **IP Address**: A unique numerical identifier assigned to every device on a network, serving as its digital coordinate for routing (IPv4: 32-bit, IPv6: 128-bit).

## J

- **Jitter**: Random variation added to retry intervals in exponential backoff to prevent multiple clients from retrying simultaneously and causing a secondary overload ("retry storm").
- **JWT (JSON Web Token)**: A compact, URL-safe token format used for securely transmitting authentication and authorization claims between parties, commonly passed in HTTP headers.

## K

- **Kafka**: A distributed event streaming platform that treats partitions as append-only log files with sequential I/O, providing high-throughput messaging with configurable retention periods, consumer groups, and replication via ZooKeeper.
- **Kappa Architecture**: A simplified alternative to Lambda architecture that uses a single streaming pipeline (e.g., Kafka + Flink) for both real-time and batch processing, avoiding the complexity of maintaining two separate pipelines.

## L

- **Lambda Architecture**: A data processing architecture that runs parallel batch (slow, accurate) and streaming (fast, approximate) pipelines against the same data, combining their outputs for both speed and correctness.
- **Latency**: The time between a client sending a request and receiving a response; P99 latency measures the worst-case experience for the bottom 1% of requests, considered the most important metric for user retention.
- **Layer 4 Load Balancing**: Transport-layer load balancing that routes based on IP addresses and TCP/UDP ports without inspecting packet contents; exceptionally fast but unable to make content-aware decisions.
- **Layer 7 Load Balancing**: Application-layer load balancing that inspects HTTP headers, URLs, and cookies for intelligent routing decisions; supports SSL termination and feature-based routing but adds processing overhead.
- **Leaderless Replication**: A database replication strategy where all nodes are equal and accept both reads and writes, using quorum-based consensus (e.g., Cassandra, DynamoDB).
- **Least Connections**: A load balancing algorithm that routes traffic to the server with the fewest active connections, providing load-aware distribution for requests with variable processing times.
- **Linearizability**: The strongest consistency guarantee where all operations appear to execute atomically and in real-time order, as if there were only one copy of the data.
- **Long Polling**: A communication technique where the client sends a request that the server holds open until new data is available, then responds and the cycle repeats; simpler than WebSockets but ties up connections.
- **LSI (Local Secondary Index)**: A DynamoDB index sharing the same partition key as the base table but with a different sort key, providing alternative sorting views on the same partition.
- **LSM Tree (Log-Structured Merge Tree)**: A write-optimized storage structure that performs sequential writes to a Write-Ahead Log and MemTable, then flushes to immutable on-disk segments (SSTables), avoiding random disk seeks.

## M

- **MCU (Multipoint Control Unit)**: A video conferencing architecture where the server mixes all participant streams into one; CPU-intensive and inflexible, as users cannot individually select or pin speakers.
- **MemTable**: An in-memory, sorted data structure (typically a red-black tree or skip list) that buffers writes before they are flushed to disk as immutable SSTables in LSM-tree-based storage engines.
- **Message Broker**: A program that translates messages between the formal messaging protocols of senders and receivers, decoupling producers from consumers; examples include Kafka and RabbitMQ.
- **Metadata Service**: A shared service that stores information (e.g., IDs, configurations) used by multiple components, reducing message sizes by allowing systems to pass IDs instead of full data payloads.
- **Microservices**: An architectural style where an application is composed of small, independently deployable services with well-defined interfaces, enabling isolated fault domains and independent scaling at the cost of operational complexity.
- **MTBF (Mean Time Between Failures)**: The average time elapsed between system failures, used as a reliability metric.
- **MTTR (Mean Time to Recovery)**: The average time required to restore a system after a failure, used as an availability metric.
- **Multipart Upload**: A technique for uploading large files by splitting them into smaller chunks (typically 5 MB) that are uploaded in parallel and reassembled by the storage provider, improving throughput and resilience.

## N

- **NAT Gateway**: A managed network component that allows instances in private subnets to initiate outbound internet connections while preventing inbound connections from the external internet.
- **Normalization**: A database design philosophy where each piece of information exists in exactly one location, enforced through primary and foreign keys, ensuring referential integrity at the cost of requiring JOIN operations for reads.
- **NoSQL**: A broad category of non-relational databases that sacrifice some ACID properties for horizontal scalability and flexible schemas; includes key-value (Redis), document (MongoDB), wide-column (Cassandra), and graph (Neo4j) types.

## O

- **Object Storage**: A flat-namespace storage system (e.g., AWS S3, GCS) designed for large binary objects with immutable writes, achieving 11 nines of durability through erasure coding across multiple facilities.
- **Observability**: The degree to which a system's internal state can be understood from its external outputs (metrics, logs, traces), enabling engineers to diagnose issues and measure performance.
- **Orchestration**: A saga coordination pattern where a central orchestrator manages the sequence of steps in a distributed transaction, issuing commands and handling compensating transactions on failure.
- **OSI Model**: The 7-layer Open Systems Interconnection conceptual framework (Physical, Data Link, Network, Transport, Session, Presentation, Application) that characterizes networking functions.

## P

- **P99 Latency**: The response time at the 99th percentile, meaning 99% of requests complete faster; reveals worst-case "tail latency" that averages conveniently hide and is critical for user experience.
- **PACELC Theorem**: An extension of CAP stating that even when no partition exists (Else), a system must choose between Latency and Consistency.
- **Partition Key**: In distributed databases (e.g., Cassandra, DynamoDB), the key component that determines which physical node stores the data via consistent hashing.
- **Peer-to-Peer (P2P)**: A decentralized communication model where every node acts as both client and server, offering superior resilience but lacking centralized authority; exemplified by BitTorrent and WebRTC.
- **PII (Personally Identifiable Information)**: Data that can uniquely identify a person (e.g., name, government ID, email), subject to regulations like GDPR and CCPA.
- **Polyglot Persistence**: The practice of using different storage technologies for different data needs within the same system, choosing each engine based on specific access patterns and consistency requirements.
- **Pre-Signed URL**: A temporary, time-limited URL generated by the application server that allows a client to upload or download directly to/from object storage (e.g., S3), bypassing the application server as a bandwidth bottleneck.
- **Prometheus**: An open-source monitoring system built around a time-series database that pulls metrics from HTTP endpoints, supports PromQL for querying, and integrates with Alertmanager for notifications.
- **Protocol Buffers (Protobuf)**: Google's language-neutral binary serialization format used by gRPC that is significantly more compact and faster to parse than JSON.
- **Pub/Sub (Publish/Subscribe)**: An asynchronous messaging pattern where publishers emit events to topics without knowing the subscribers, and subscribers receive all messages on topics they have registered interest in.

## Q

- **QPS (Queries Per Second)**: A throughput metric representing the number of requests a system processes per second; a fundamental capacity planning number.
- **Quad-Tree**: A spatial index structure where each node has four children, recursively splitting space into quadrants with finer grids in areas of high data density, used for geospatial queries.
- **Quorum**: The minimum number of nodes that must agree for a read or write operation to be considered successful in a distributed system; typically set to N/2 + 1 for consistency guarantees.

## R

- **R-Tree**: The production standard spatial index (used in PostGIS) that groups nearby objects using overlapping bounding rectangles, handling multi-dimensional spatial queries more efficiently than quad-trees.
- **Rate Limiting**: A defense mechanism that caps the number of requests a client can make within a time window, protecting against DDoS attacks, maintaining SLAs, and controlling infrastructure costs.
- **RBAC (Role-Based Access Control)**: A security model where permissions are assigned to roles rather than individual users, and users are assigned roles, simplifying access management.
- **Read-Through Cache**: A caching pattern where the cache itself fetches data from the database on a miss, simplifying application logic by making the cache act as a proxy.
- **Redis**: A single-threaded, in-memory data structure server providing sub-millisecond latency for caching, rate limiting, leaderboards (sorted sets), pub/sub messaging, geospatial queries, and distributed locking with TTL.
- **Redundancy**: The duplication of critical system components (servers, databases, network paths) so that if one fails, another can take over, eliminating single points of failure.
- **Replication**: Creating and maintaining copies of data on multiple machines to increase availability, reduce latency (geo-proximity), and scale read throughput.
- **Reverse Proxy**: An intermediary that sits in front of backend servers, receiving client requests and forwarding them to appropriate servers while concealing the backend's identity; handles SSL termination, caching, and IP masking.
- **Round Robin**: A simple load balancing algorithm that distributes requests sequentially across servers in rotation; easy to implement but load-agnostic.

## S

- **Saga Pattern**: A distributed transaction pattern consisting of a sequence of local transactions, each with a compensating transaction that can undo its effects if a subsequent step fails, coordinated via choreography (parallel) or orchestration (linear).
- **SFU (Selective Forwarding Unit)**: The modern standard for video conferencing (used by Zoom, Google Meet) where the server forwards individual streams to clients without mixing, allowing client-side layout control with minimal server CPU.
- **Sharding**: Horizontal partitioning of data across multiple distributed nodes, where each shard holds a subset of the data, enabling storage and throughput beyond single-machine limits.
- **Single Point of Failure (SPOF)**: Any component whose failure would cause the entire system to become unavailable; eliminated through redundancy, replication, and failover mechanisms.
- **SLA (Service Level Agreement)**: A formal contract specifying performance guarantees (e.g., response time under 100ms, 99.99% uptime) between a service provider and its consumers.
- **Sort Key (Clustering Key)**: In DynamoDB or Cassandra, the secondary key component that determines the sorted order of items within a partition, enabling efficient range queries.
- **Spot Instance**: Discounted cloud compute capacity (up to 80-90% savings) that can be reclaimed by the provider with short notice, suitable for fault-tolerant workloads when combined with soft affinity rules.
- **SQS (Simple Queue Service)**: AWS's managed message queue service with built-in features like visibility timeouts, exponential backoff, and dead letter queues, often preferred over Kafka for simpler retry use cases.
- **SSE (Server-Sent Events)**: A unidirectional streaming protocol from server to client over standard HTTP, lightweight and firewall-friendly, preferred for broadcast scenarios (e.g., live comments) where bidirectional communication is unnecessary.
- **SSTable (Sorted String Table)**: An immutable, on-disk data structure containing sorted key-value pairs, produced when a MemTable is flushed; the foundation of LSM-tree storage engines.
- **Sticky Session**: A load balancer configuration that routes all requests from a particular client to the same backend server, necessary for stateful applications using session data.
- **Stream Processing**: Continuously processing data events as they arrive in real time, using tools like Flink, Kafka Streams, or Spark Streaming, as opposed to periodic batch processing.
- **Strong Consistency**: A guarantee that every read reflects the most recent write, requiring synchronous replication and consensus among nodes; mandatory for financial, inventory, and booking systems.

## T

- **TCP (Transmission Control Protocol)**: A reliable, connection-oriented transport protocol that guarantees ordered delivery of all packets, retransmitting lost data; used for web traffic, file transfers, and databases.
- **Throughput**: The rate at which a system processes requests or transactions, typically measured in QPS or TPS (transactions per second).
- **TLS (Transport Layer Security)**: The cryptographic protocol (successor to SSL) that provides encrypted communication between clients and servers; TLS termination at a load balancer offloads encryption overhead from application servers.
- **Token Bucket Algorithm**: A rate limiting algorithm defined by bucket size (burst capacity) and refill rate (sustained throughput), allowing temporary traffic spikes while enforcing a steady-state rate.
- **Tombstone**: A marker in append-only databases (e.g., Cassandra, HDFS) indicating that a record has been logically deleted, resolved during compaction.
- **TTL (Time to Live)**: An expiration duration assigned to data in caches, DNS records, or distributed locks, after which the entry is automatically removed or refreshed.
- **Two-Phase Commit (2PC)**: A distributed transaction protocol where a coordinator asks all participants to prepare, then issues a commit or abort; provides atomicity but introduces a single point of failure at the coordinator.

## U

- **UDP (User Datagram Protocol)**: A connectionless transport protocol that prioritizes speed over reliability by not guaranteeing packet delivery or ordering; used for live streaming, gaming, and DNS lookups.

## V

- **Vector Database**: A specialized database (e.g., Pinecone, FAISS) that stores high-dimensional vector embeddings and supports approximate nearest neighbor search using algorithms like HNSW, essential for recommendation engines and semantic search.
- **Vertical Partitioning**: Splitting a database table by columns, moving infrequently accessed or large columns (e.g., blobs) to separate tables to improve query performance on the remaining columns.
- **Vertical Scaling (Scaling Up)**: Increasing the CPU, RAM, or storage of a single machine; simpler but has a hard ceiling defined by hardware limits and creates a catastrophic single point of failure.
- **Virtual Node (vNode)**: In consistent hashing, mapping a single physical server to multiple points on the hash ring to ensure even data distribution and minimize redistribution when nodes are added or removed.
- **Virtual Waiting Room**: A traffic management pattern (e.g., Ticketmaster) that queues users during extreme surges and admits them at a controlled rate, protecting backend services from being overwhelmed.
- **VPA (Virtual Payment Address)**: A memorable identifier (e.g., name@bank) used in UPI systems that replaces cumbersome bank account and routing numbers for peer-to-peer payments.

## W

- **WAL (Write-Ahead Log)**: A durability mechanism where changes are first written to a sequential log before being applied to the main data structure, ensuring recovery after crashes.
- **WebRTC**: A peer-to-peer protocol for real-time audio and video communication directly between browsers, used in video calling but unscalable for large groups without an SFU or MCU.
- **WebSocket**: A full-duplex communication protocol over a persistent TCP connection, enabling bidirectional real-time data exchange between client and server; essential for chat applications but stateful and less scalable than HTTP.
- **Write-Back / Write-Behind Cache**: A caching strategy where writes go to the cache first and are asynchronously flushed to the database in batches, offering high throughput but risking data loss if the cache fails.
- **Write-Through Cache**: A caching strategy where every write simultaneously updates both the cache and the database, guaranteeing consistency at the cost of increased write latency.

## Z

- **ZooKeeper**: A distributed coordination service that provides leader election, configuration management, distributed locking, and service discovery using consensus algorithms (Zab protocol), used by Kafka and other distributed systems.
