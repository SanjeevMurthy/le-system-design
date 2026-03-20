# Source Traceability Map

This document maps each canonical topic file in the knowledge base to the source files that contain relevant content for that topic.

---

## 01-fundamentals/

### 01-system-design-framework.md
- source/youtube-video-reports/3.md (requirements framework: functional vs. non-functional requirements, the "five-minute rule")
- source/youtube-video-reports/6.md (Hello Interview delivery framework: requirement clarification, core entities, HLD vs. deep dives, strategic estimates)
- source/youtube-video-reports/8.md (networking fundamentals as prerequisite; API design and inter-service architectures)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (system design interview overview, tradeoffs discussion, scaling walkthrough)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (interview flow: clarify requirements, draft API spec, design data model, discuss failure)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (NFR taxonomy: scalability, availability, fault-tolerance, latency, consistency, cost)
- source/extracted/system-design-guide/ch01-system-design-guide-for-software-professionals.md (overview of system design for professionals)
- source/extracted/system-design-guide/ch03-basics-of-system-design.md (system design process: requirements analysis, HLD, detailed design, API design, DB design)
- source/extracted/system-design-guide/ch11-system-design-in-practice.md (practical system design methodology)
- source/extracted/grokking/ch01-system-design-interviews-a-step-by-step-guide.md (step-by-step interview guide)
- source/extracted/grokking/ch06-step-5-high-level-design.md (high-level design approach)
- source/extracted/ddia/ch01-part-i-foundations-of-data-systems.md (foundations of data systems)
- source/extracted/ddia/ch02-reliable-scalable-and-maintainable-applications.md (reliability, scalability, maintainability foundations)

### 03-scaling-overview.md
- source/youtube-video-reports/2.md (scaling paradigm: vertical vs. horizontal scaling, microservices, 3-stage infrastructure maturity model)
- source/youtube-video-reports/3.md (scaling from startup to enterprise, complexity budget)
- source/youtube-video-reports/5.md (foundational metrics, scalability/reliability/availability pillars, "nines" of availability)
- source/youtube-video-reports/7.md (scaling paradigms, vertical vs. horizontal, auto scaling in Kubernetes)
- source/youtube-video-reports/8.md (vertical vs. horizontal scaling, consistent hashing, fault tolerance)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (scaling a service: GeoDNS, caching, CDN, horizontal scalability, functional partitioning)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (scalability as NFR, stateless vs. stateful services)
- source/extracted/system-design-guide/ch02-foundations-of-system-design.md (foundations of scaling)
- source/extracted/system-design-guide/ch03-basics-of-system-design.md (system design basics including scaling considerations)
- source/extracted/ddia/ch02-reliable-scalable-and-maintainable-applications.md (describing load, describing performance, approaches for coping with load)

### 04-availability-reliability.md
- source/youtube-video-reports/2.md (system reliability, monitoring, blast radius)
- source/youtube-video-reports/5.md ("nines" of availability table, P99 latency, reliability vs. availability distinction)
- source/youtube-video-reports/7.md (availability levels table, reliability vs. availability analogy, MTTR/MTBF)
- source/youtube-video-reports/8.md (fault tolerance, SPOF, redundancy, circuit breaker pattern)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (availability benchmarks table, fault-tolerance mechanisms: replication, circuit breaker, exponential backoff, bulkhead, fallback)
- source/extracted/system-design-guide/ch04-distributed-system-attributes.md (distributed system attributes including availability)
- source/extracted/grokking/ch59-reliability-and-redundancy.md (reliability and redundancy)
- source/extracted/grokking/ch128-fault-tolerance.md (fault tolerance mechanisms)
- source/extracted/grokking/ch164-fault-tolerance.md (fault tolerance continued)
- source/extracted/ddia/ch02-reliable-scalable-and-maintainable-applications.md (reliability: hardware/software/human faults)

### 05-cap-theorem.md
- source/youtube-video-reports/3.md (CAP theorem and consistency models: CP vs. AP, use-case based evaluation)
- source/youtube-video-reports/5.md (CAP theorem dictating availability vs. consistency during partitions)
- source/youtube-video-reports/7.md (strong vs. eventual consistency, BASE philosophy, gossip protocol)
- source/youtube-video-reports/8.md (strong, eventual, causal, read-your-own-writes consistency)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (ACID vs. CAP consistency, linearizability vs. eventual consistency, PACELC theorem)
- source/extracted/system-design-guide/ch05-distributed-systems-theorems-and-data-structures.md (distributed systems theorems including CAP)
- source/extracted/grokking/ch267-05-cap-theorem.md (CAP theorem definition: consistency, availability, partition tolerance)
- source/extracted/ddia/ch11-consistency-and-consensus.md (consistency and consensus deep dive)

### 06-networking-fundamentals.md
- source/youtube-video-reports/1.md (client-server model, peer-to-peer, HTTP request/response cycle)
- source/youtube-video-reports/5.md (network infrastructure: IGW, NAT gateway, subnets, route tables, security groups, bastion hosts, OSI model layers 3/4/7)
- source/youtube-video-reports/8.md (IP addresses, DNS, TCP vs. UDP, HTTP, WebSockets, forward vs. reverse proxies, OSI model)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (OSI model table, WebSocket protocol)
- source/extracted/system-design-guide/ch07-distributed-systems-building-blocks-dns-load-balancers-and-a.md (DNS, load balancers, networking building blocks)
- source/extracted/grokking/ch274-websockets.md (WebSockets protocol)
- source/extracted/grokking/ch275-server-sent-events-sses.md (Server-Sent Events)

### 07-back-of-envelope-estimation.md
- source/youtube-video-reports/6.md (strategic estimates: math as design tool, Facebook post search 3.6PB calculation, web crawler bandwidth estimation)
- source/youtube-video-reports/8.md (QPS calculation: 10^8 DAU / 10^5 seconds = 1000 QPS, availability nines)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (estimating daily/hourly request rates from DAU)
- source/extracted/grokking/ch15-500m-50b.md (capacity estimation)
- source/extracted/grokking/ch87-capacity-estimation-and-constraints.md (capacity estimation and constraints)
- source/extracted/grokking/ch183-capacity-estimation-and-constraints.md (capacity estimation continued)

---

## 02-scalability/

### 01-load-balancing.md
- source/youtube-video-reports/1.md (load balancer algorithms: IP hashing, round robin, least connections; forward vs. reverse proxy)
- source/youtube-video-reports/2.md (3-stage infrastructure maturity model, L4 vs. L7 load balancing, proxy specialization)
- source/youtube-video-reports/3.md (L4 vs. L7 load balancers, round robin, least connections, IP hash)
- source/youtube-video-reports/5.md (L4 vs. L7 load balancing, external vs. internal LBs, reverse proxy as NAT)
- source/youtube-video-reports/8.md (L4 vs. L7 comparison, load balancer placement)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (L4 vs. L7 load balancers, sticky sessions, session replication, load balancing vs. reverse proxy)
- source/extracted/system-design-guide/ch07-distributed-systems-building-blocks-dns-load-balancers-and-a.md (DNS, load balancers, algorithms)
- source/extracted/grokking/ch63-cache-and-01-load-balancing.md (cache and load balancing)
- source/extracted/grokking/ch137-replication-and-load-balancer.md (replication and load balancer)
- source/extracted/grokking/ch243-benefits-of-01-load-balancing.md (benefits of load balancing)
- source/extracted/grokking/ch245-redundant-load-balancers.md (redundant load balancers)

### 02-autoscaling.md
- source/youtube-video-reports/1.md (Kubernetes HPA and resource baselining, 80% threshold strategy)
- source/youtube-video-reports/4.md (traffic patterns: predictable/unpredictable/interconnected spikes, serverless trap)
- source/youtube-video-reports/5.md (auto scaling in Kubernetes: HPA, metrics server, CPU/memory thresholds)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (horizontal scalability, cluster management, CI/CD)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (horizontal scaling, auto-scaling services)

### 03-consistent-hashing.md
- source/youtube-video-reports/5.md (consistent hashing: hash ring, adding/removing nodes, K/N key redistribution)
- source/youtube-video-reports/8.md (consistent hashing: mapping keys to circular ring, adding/removing nodes)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (consistent hashing mentioned in context of library vs. service)
- source/extracted/system-design-guide/ch05-distributed-systems-theorems-and-data-structures.md (consistent hashing and distributed data structures)
- source/extracted/grokking/ch270-how-does-it-work.md (how consistent hashing works)
- source/extracted/ddia/ch08-partitioning.md (partitioning and hash-based distribution)

### 04-sharding.md
- source/youtube-video-reports/4.md (shard key anatomy: high cardinality, even distribution, query alignment; range/hash/directory strategies; celebrity hotspot; cross-shard transactions: 2PC and saga)
- source/youtube-video-reports/5.md (vertical/horizontal partitioning, sharding across nodes, consistent hashing for distribution)
- source/youtube-video-reports/8.md (consistent hashing, virtual nodes for even distribution)
- source/extracted/acing-system-design/ch06-scaling-databases.md (sharding: distributing replicas, scaling storage capacity, sharded RDBMS, partitioning)
- source/extracted/system-design-guide/ch08-design-and-implementation-of-system-components-databases-and.md (database design and sharding)
- source/extracted/grokking/ch60-data-04-sharding.md (data sharding)
- source/extracted/grokking/ch108-data-04-sharding.md (data sharding continued)
- source/extracted/grokking/ch190-data-partitioning.md (data partitioning)
- source/extracted/grokking/ch233-data-partitioning.md (data partitioning continued)
- source/extracted/grokking/ch252-partitioning-methods.md (partitioning methods)
- source/extracted/grokking/ch254-common-problems-of-data-partitioning.md (common partitioning problems)
- source/extracted/ddia/ch08-partitioning.md (partitioning deep dive)

---

## 03-storage/

### 01-sql-databases.md
- source/youtube-video-reports/2.md (SQL for ACID transactions, Postgres for structured data)
- source/youtube-video-reports/3.md (SQL mandatory for ACID, Postgres/MySQL for profile services and seat inventories)
- source/youtube-video-reports/4.md (relational vs. NoSQL decision matrix: structure, storage, scale, access)
- source/youtube-video-reports/5.md (SQL for ACID compliance, vertical scaling, Postgres)
- source/youtube-video-reports/8.md (SQL vs. NoSQL comparison: structure, scaling, complexity)
- source/extracted/acing-system-design/ch06-scaling-databases.md (SQL storage, replication techniques, single-leader replication, HDFS)
- source/extracted/system-design-guide/ch08-design-and-implementation-of-system-components-databases-and.md (database design)
- source/extracted/grokking/ch263-high-level-differences-between-sql-and-nosql.md (SQL vs. NoSQL differences)
- source/extracted/ddia/ch03-data-models-and-query-languages.md (data models and query languages)
- source/extracted/ddia/ch09-transactions.md (transactions and ACID)

### 02-nosql-databases.md
- source/youtube-video-reports/2.md (Cassandra for high-write throughput, document stores for unstructured JSON)
- source/youtube-video-reports/3.md (NoSQL types: document stores, Cassandra for swipes, graph DBs)
- source/youtube-video-reports/4.md (NoSQL decision matrix, Cassandra append-only architecture, DynamoDB)
- source/youtube-video-reports/5.md (NoSQL types: key-value, document, wide-column, graph)
- source/youtube-video-reports/8.md (NoSQL: flexible schema, horizontal scaling, key-value/document/wide-column/graph types)
- source/extracted/acing-system-design/ch06-scaling-databases.md (NoSQL storage: column-oriented, key-value, document, graph)
- source/extracted/grokking/ch263-high-level-differences-between-sql-and-nosql.md (SQL vs. NoSQL differences)
- source/extracted/grokking/ch266-reasons-to-use-nosql-database.md (reasons to use NoSQL)
- source/extracted/ddia/ch03-data-models-and-query-languages.md (document model, graph model)

### 03-object-storage.md
- source/youtube-video-reports/2.md (S3 for unstructured media, CDN for edge caching)
- source/youtube-video-reports/4.md (object storage: flat namespaces, immutable writes, 11 9s durability, metadata/data split, pre-signed URLs, multipart uploads)
- source/youtube-video-reports/8.md (Amazon S3 for unstructured media)
- source/extracted/acing-system-design/ch06-scaling-databases.md (object storage: flatter hierarchy, HTTP APIs, suited for static data, AWS S3)
- source/extracted/alex-xu-vol2/ch10-s3-like-03-object-storage.md (S3-like object storage design)
- source/extracted/grokking/ch77-e-cloudblock-storage.md (cloud/block storage)

### 04-database-indexing.md
- source/youtube-video-reports/5.md (indexing for read performance: primary, secondary, composite; write penalty of indexes)
- source/youtube-video-reports/8.md (B-Tree vs. hash index, full table scan bottleneck, specialized indexing: geospatial, inverted index)
- source/extracted/system-design-guide/ch08-design-and-implementation-of-system-components-databases-and.md (database indexing)
- source/extracted/grokking/ch258-how-do-indexes-decrease-write-performance.md (indexes and write performance)
- source/extracted/ddia/ch04-storage-and-retrieval.md (storage engines, B-trees, LSM-trees, indexing)

### 05-database-replication.md
- source/youtube-video-reports/7.md (strong vs. eventual consistency, synchronous vs. asynchronous replication)
- source/extracted/acing-system-design/ch06-scaling-databases.md (single-leader, multi-leader, leaderless replication; primary-secondary failover; multi-level replication; HDFS replication; consistency problems)
- source/extracted/system-design-guide/ch06-core-components-of-distributed-systems.md (core components including replication)
- source/extracted/grokking/ch205-replication-and-fault-tolerance.md (replication and fault tolerance)
- source/extracted/ddia/ch07-replication.md (leader-based replication, synchronous vs. asynchronous, replication lag, multi-leader, leaderless)

### 06-time-series-databases.md
- source/youtube-video-reports/7.md (TSDB: LSM trees, append-only storage, WAL, MemTable, Gorilla compression, delta encoding, downsampling)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (TSDB for logging time series data, downsampling, Graphite, Prometheus, OpenTSDB, InfluxDB)
- source/extracted/alex-xu-vol2/ch06-metrics-monitoring-and-alerting-system.md (metrics monitoring using time-series data)

### 07-cassandra.md
- source/youtube-video-reports/2.md (Cassandra for 1M writes/sec at Netflix, high-write throughput)
- source/youtube-video-reports/3.md (Cassandra for 100K+ writes/sec on Tinder, append-only architecture, compaction)
- source/youtube-video-reports/8.md (Cassandra deep dive: keyspaces, tables, partition key, clustering key, leaderless architecture, gossip protocol, tunable consistency levels: ANY/ONE/QUORUM/ALL, write path: commit log -> MemTable -> SSTable, read path with Bloom filters, compaction)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (Cassandra as eventual consistency favoring availability)
- source/extracted/acing-system-design/ch06-scaling-databases.md (Cassandra as column-oriented NoSQL)

### 08-dynamodb.md
- source/youtube-video-reports/6.md (DynamoDB deep dive: primary key architecture with partition key and sort key, GSI vs. LSI, DAX accelerator, DynamoDB Streams for CDC, ACID transactions)
- source/extracted/alex-xu-vol2/ch05-distributed-message-queue.md (DynamoDB in distributed system context)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (DynamoDB gossip protocol with vector clocks)

---

## 04-caching/

### 01-caching.md
- source/youtube-video-reports/5.md (caching strategies: write-through, write-around, write-back; cache stampede/thundering herd; consistency/stale data; hot keys "Taylor Swift problem")
- source/youtube-video-reports/8.md (caching layers: external, in-process, CDN, client-side; cache-aside vs. read-through patterns; cache hit/miss)
- source/extracted/acing-system-design/ch06-scaling-databases.md (caching: read strategies: cache-aside, read-through; write strategies: write-through, write-back, write-around; cache invalidation; cache warming; request coalescing)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (caching for fault-tolerance: caching responses of other services)
- source/extracted/system-design-guide/ch09-distributed-cache.md (distributed cache design)
- source/extracted/grokking/ch24-cache.md (cache concepts)
- source/extracted/grokking/ch81-01-caching.md (caching strategies)
- source/extracted/grokking/ch250-cache-eviction-policies.md (cache eviction policies: LRU, FIFO, LIFO)

### 02-redis.md
- source/youtube-video-reports/4.md (Redis deep dive: single-threaded model, hot key and sharding with CRC mod 16384, rate limiters with atomic INCR/TTL, leaderboards with sorted sets, async job queues with streams, geospatial API with geohashing, PubSub)
- source/youtube-video-reports/6.md (Redis Pub/Sub for WhatsApp routing, at-least-once delivery with inbox pattern)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (Redis as distributed cache, in-memory store, consistency implications)
- source/extracted/acing-system-design/ch06-scaling-databases.md (Redis for aggregation fault-tolerance)
- source/extracted/alex-xu-vol2/ch11-real-time-gaming-leaderboard.md (Redis sorted sets for leaderboards)

### 03-cdn.md
- source/youtube-video-reports/2.md (CDN for reducing global latency by caching at edge)
- source/youtube-video-reports/3.md (CDN caching for TicketMaster search during surges)
- source/youtube-video-reports/5.md (CDN edge locations for static media)
- source/youtube-video-reports/8.md (CDN as edge caching layer)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (CDN: CloudFlare, Rackspace, CloudFront; improved latency/throughput/reliability)
- source/extracted/acing-system-design/ch16-design-a-content-distribution-network.md (CDN design)

---

## 05-messaging/

### 01-message-queues.md
- source/youtube-video-reports/5.md (Kafka architecture: append-only log, sequential I/O, consumer groups, hot partition problem, back pressure)
- source/youtube-video-reports/8.md (message queues as "checklist": producer/consumer decoupling)
- source/extracted/acing-system-design/ch06-scaling-databases.md (messaging terminology: message queue, producer/consumer, message broker, event streaming; Kafka vs. RabbitMQ comparison; pull vs. push)
- source/extracted/alex-xu-vol2/ch05-distributed-message-queue.md (distributed message queue design: decoupling, scalability, availability, performance)
- source/extracted/system-design-guide/ch10-pubsub-and-distributed-queues.md (pub/sub and distributed queues)

### 02-event-driven-architecture.md
- source/youtube-video-reports/7.md (request-response vs. event-driven: choreography vs. orchestration, Kafka/SNS/SQS, loose coupling)
- source/extracted/acing-system-design/ch07-03-distributed-transactions.md (Event Driven Architecture: asynchronous, non-blocking, loose coupling, scalability)
- source/extracted/ddia/ch14-stream-processing.md (stream processing concepts)

### 03-event-sourcing.md
- source/youtube-video-reports/4.md (event sourcing: append-only log, hydration/replay, immutable audit trail, "time machine" for data)
- source/youtube-video-reports/8.md (event sourcing: append-only log in Kafka/Kinesis, state via hydration, perfect audit trail)
- source/extracted/acing-system-design/ch07-03-distributed-transactions.md (event sourcing: log as source of truth, publishers/subscribers, audit trail, replay; comparison with CDC)

### 04-cqrs.md
- source/youtube-video-reports/8.md (CQRS: separating commands from queries, write side with SQL, read side with NoSQL denormalized views)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (CQRS: command/write and query/read on separate services, message brokers and ETL as examples)

---

## 06-architecture/

### 01-api-gateway.md
- source/youtube-video-reports/2.md (API gateway as strategic entry point: routing, authentication, rate limiting; 3-stage infrastructure maturity)
- source/youtube-video-reports/3.md (API gateway: central entry point for microservices, AuthN/AuthZ, rate limiting, routing)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (API gateway: reverse proxy for routing, authorization, authentication, rate limiting, billing, analytics)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (API gateway functionalities: security, error-checking, performance/availability, logging)
- source/extracted/system-design-guide/ch12-design-and-implementation-of-system-components-api-security-.md (API security and gateway)

### 02-microservices.md
- source/youtube-video-reports/2.md (microservices and API gateway mandate, cross-service latency tradeoffs)
- source/youtube-video-reports/7.md (Kubernetes five pillars: computation, networking, storage, security, custom resources)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (functional partitioning, service mesh/sidecar pattern with Istio, sidecarless mesh)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (service mesh, sidecar pattern, metadata service, service discovery)
- source/extracted/ddia/ch05-encoding-and-evolution.md (encoding and evolution for microservices)

### 03-serverless.md
- source/youtube-video-reports/4.md (serverless/Lambda trap: vendor lock-in ecosystem bind with SQS/API Gateway/Route 53/S3/CloudWatch)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (FaaS: AWS Lambda, Azure Functions, cold start, OpenFaaS, Knative, Spring Cloud Function)

---

## 08-resilience/

### 01-rate-limiting.md
- source/youtube-video-reports/1.md (rate limiting: protection against DDoS, server stability, cost control; fixed window algorithm, token bucket algorithm with burst/sustain; exponential backoff and jitter)
- source/youtube-video-reports/3.md (strategic rate limiting at API gateway level)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (rate limiting as security and availability measure)
- source/extracted/acing-system-design/ch11-design-a-rate-limiting-service.md (rate limiting service design)
- source/extracted/grokking/ch146-what-are-different-types-of-throttling.md (throttling types)
- source/extracted/grokking/ch149-basic-system-design-and-algorithm.md (rate limiting algorithm design)
- source/extracted/grokking/ch150-sliding-window-algorithm.md (sliding window algorithm)
- source/extracted/grokking/ch151-sliding-window-with-counters.md (sliding window with counters)
- source/extracted/grokking/ch153-should-we-rate-limit-by-ip-or-by-user.md (rate limiting by IP vs. user)

### 02-circuit-breaker.md
- source/youtube-video-reports/5.md (circuit breaker: detects downstream failure, trips to fail fast, half-open state for testing recovery)
- source/youtube-video-reports/8.md (circuit breaker pattern: open state fails fast, half-open tests system)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (circuit breaker: error threshold, timers, Resilience4j, Netflix Hystrix, adaptive concurrency limits)

### 03-distributed-transactions.md
- source/youtube-video-reports/4.md (cross-shard transactions: two-phase commit with coordinator as SPOF; saga pattern with compensating actions)
- source/youtube-video-reports/7.md (saga pattern: e-commerce fulfillment case study; choreographed vs. orchestrated)
- source/extracted/acing-system-design/ch07-03-distributed-transactions.md (distributed transactions: event sourcing, CDC, transaction supervisor, saga with choreography and orchestration; comparison table)
- source/extracted/ddia/ch09-transactions.md (transactions: ACID, isolation levels, serializability)
- source/extracted/ddia/ch11-consistency-and-consensus.md (consensus algorithms)

### 04-feature-flags.md
- source/youtube-video-reports/1.md (feature flags: programmatic if-statement from external config; database migrations, allow lists, operational levers; feature flags vs. canary releases; audit trail requirement)
- source/extracted/acing-system-design/ch03-a-walkthrough-of-system-design-concepts.md (gradual rollouts, rollbacks, experimentation, A/B testing)

---

## 09-security/

### 01-authentication-authorization.md
- source/youtube-video-reports/2.md (AuthN/AuthZ as security pillar)
- source/youtube-video-reports/3.md (authentication at API gateway level)
- source/youtube-video-reports/5.md (security: custom binary pattern, RBAC, service accounts, least privilege)
- source/youtube-video-reports/8.md (JWTs, session tokens in headers, security protocols)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (security: TLS termination, encryption in transit/at rest, OAuth 2.0, OpenID Connect)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (API gateway security: authentication, authorization, SSL termination, data encryption)
- source/extracted/system-design-guide/ch12-design-and-implementation-of-system-components-api-security-.md (API security)
- source/extracted/grokking/ch28-security-and-permissions.md (security and permissions)
- source/extracted/grokking/ch46-security-and-permissions.md (security and permissions continued)

### 02-encryption.md
- source/youtube-video-reports/2.md (mandatory encryption at rest, TLS 1.3 for data in transit)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (encryption in transit vs. at rest, TLS termination, hashing algorithms SHA-2/SHA-3 for PII)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (server-side data encryption, SSL termination)

### 03-api-security.md
- source/youtube-video-reports/2.md (ingress security: IP-based rate limiting, input validation against DDoS/injection)
- source/youtube-video-reports/5.md (DevSecOps, custom binary with embedded service accounts, least privilege)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (privacy: PII, GDPR, CCPA, LDAP, access control, data retention policies)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (request validation, request deduplication, rate limiting at gateway)
- source/extracted/system-design-guide/ch12-design-and-implementation-of-system-components-api-security-.md (API security components)

---

## 10-observability/

### 01-monitoring.md
- source/youtube-video-reports/2.md (Prometheus/Grafana for real-time health, ELK stack for post-mortem)
- source/youtube-video-reports/3.md (ELK stack for log analysis, Prometheus/Grafana for real-time metrics)
- source/youtube-video-reports/7.md (monitoring vs. logging distinction, Prometheus service monitoring object, four golden signals)
- source/youtube-video-reports/8.md (four golden signals: metrics, logs, traces, events)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (observability: four golden signals of monitoring, metrics/dashboards/alerts, TSDB, anomaly detection)
- source/extracted/alex-xu-vol2/ch06-metrics-monitoring-and-alerting-system.md (metrics monitoring and alerting system design)
- source/extracted/grokking/ch113-01-monitoring.md (monitoring concepts)

### 02-logging.md
- source/youtube-video-reports/2.md (ELK stack: Elasticsearch, Logstash, Kibana for centralized logging)
- source/youtube-video-reports/7.md (logging as reactive bookkeeping tool, ELK stack)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (ELK suite: Elasticsearch, Logstash, Beats, Kibana; structured logging best practices; Splunk; distributed tracing with Zipkin/Jaeger)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (logging and periodic auditing for silent errors)

---

## 07-api-design/

### 01-rest-api.md
- source/youtube-video-reports/5.md (REST as resource-based industry standard, JSON parsing overhead)
- source/youtube-video-reports/8.md (REST: GET, POST, PUT, PATCH, DELETE; stateless; path/query params, headers, body)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (REST: hypermedia/HATEOAS, caching headers: Expires/Cache-Control/ETag/Last-Modified, disadvantages, OpenAPI)

### 02-grpc.md
- source/youtube-video-reports/5.md (gRPC: up to 10x faster than REST, binary serialization with Protobufs)
- source/youtube-video-reports/8.md (gRPC: Protocol Buffers, 5-10x faster than JSON, internal microservice standard)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (RPC: gRPC, Thrift, Protocol Buffers; resource optimization; schema-based documentation; binary protocol tradeoffs)

### 03-graphql.md
- source/youtube-video-reports/5.md (GraphQL: solves under-fetching/over-fetching, frontend defines response shape)
- source/youtube-video-reports/8.md (GraphQL: custom queries, N+1 problem, data loaders)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (GraphQL: declarative data fetching, pinpoint requests, tradeoffs: complexity, security, learning curve, JSON-only)

### 04-real-time-protocols.md
- source/youtube-video-reports/2.md (SSE vs. WebSockets: unidirectional vs. bidirectional; long polling; Pub/Sub fan-out)
- source/youtube-video-reports/3.md (SSE vs. WebSockets: firewall considerations, 1000:1 read-write ratio)
- source/youtube-video-reports/4.md (short polling, long polling, WebSockets; video conferencing: WebRTC mesh, MCU, SFU)
- source/youtube-video-reports/8.md (WebSockets for bidirectional, SSE for unidirectional, WebRTC for P2P)
- source/extracted/acing-system-design/ch08-common-services-for-functional-partitioning.md (WebSocket: full-duplex, persistent TCP, HTTP upgrade handshake, stateful, P2P)
- source/extracted/grokking/ch274-websockets.md (WebSockets)
- source/extracted/grokking/ch275-server-sent-events-sses.md (Server-Sent Events)

---

## 11-patterns/

### 01-fan-out.md
- source/youtube-video-reports/2.md (fan-out on write vs. fan-out on read; celebrity problem; hybrid approach)
- source/youtube-video-reports/3.md (fan-out on write for average users, fan-out on read for celebrities)
- source/youtube-video-reports/6.md (fanout problem: read vs. write comparison table; hot shard/celebrity problem; N-cache strategy)
- source/extracted/acing-system-design/ch19-design-a-02-news-feed.md (news feed fan-out strategies)

### 02-probabilistic-data-structures.md
- source/youtube-video-reports/6.md (Bloom filters for crawled URLs, count-min sketch for viral search terms, logarithmic counting for likes)
- source/youtube-video-reports/8.md (Bloom filter: likely in / definitely not in; count-min sketch: heavy hitters frequency estimation; HyperLogLog: cardinality estimation with constant memory)
- source/extracted/acing-system-design/ch05-non-functional-requirements.md (HyperLogLog for cardinality, count-min sketch for frequency estimation)

### 03-recommendation-engines.md
- source/youtube-video-reports/4.md (three-stage pipeline: candidate generation, ranking with ML, reranking; vector search with embeddings; HNSW algorithm; approximate nearest neighbor)

### 04-video-streaming.md
- source/youtube-video-reports/7.md (video delivery evolution: progressive download, RTMP/RTSP, adaptive bitrate streaming via HLS/MPEG-DASH; index file M3U8; chunking for fast start)
- source/extracted/system-design-guide/ch18-designing-a-service-like-12-netflix.md (Netflix-like video streaming service)
- source/extracted/grokking/ch119-system-apis.md (video system APIs)
- source/extracted/grokking/ch122-detailed-component-design.md (video system component design)
- source/extracted/grokking/ch124-video-deduplication.md (video deduplication)

### 05-search-and-indexing.md
- source/youtube-video-reports/2.md (Elasticsearch for inverted indices, CDC for syncing with primary DB)
- source/youtube-video-reports/6.md (inverted index for post search, count-min sketch for hot terms)
- source/youtube-video-reports/8.md (B-Tree for disk-based, inverted index for full-text search via Elasticsearch)
- source/extracted/acing-system-design/ch04-a-typical-system-design-interview-flow.md (search with Elasticsearch: index/ingestion, fuzzy matching, SQL-to-ES terminology mapping)
- source/extracted/acing-system-design/ch14-autocompletetypeahead.md (autocomplete/typeahead)
- source/extracted/grokking/ch132-basic-system-design-and-algorithm.md (typeahead algorithm design)
- source/extracted/grokking/ch133-permanent-storage-of-the-trie.md (trie storage for autocomplete)

### 06-geospatial-indexing.md
- source/youtube-video-reports/2.md (geospatial indexes: quad-trees in Elasticsearch, PostGIS)
- source/youtube-video-reports/4.md (Redis geospatial API with geohashing, sorted sets for radius search)
- source/youtube-video-reports/8.md (geohashing: recursive grid splitting with prefix matching; quad-trees: recursive 4-child splitting; R-trees: dynamic clustering with bounding boxes in PostGIS)
- source/extracted/alex-xu-vol2/ch02-proximity-service.md (proximity service design with geospatial indexing)
- source/extracted/alex-xu-vol2/ch04-14-google-maps.md (Google Maps with geospatial data)
- source/extracted/grokking/ch199-b-grids.md (grid-based geospatial approaches)
- source/extracted/grokking/ch201-c-dynamic-size-grids.md (dynamic size grids)
- source/extracted/system-design-guide/ch14-system-design-proximity-service.md (proximity service design)

---

## 12-case-studies/

### 01-twitter.md
- source/youtube-video-reports/2.md (Twitter case study: massive read-to-write ratio, hybrid timeline: fan-out on write for average users, fan-out on read for celebrities, hybrid merge)
- source/youtube-video-reports/3.md (Twitter hybrid fan-out: pre-computed timelines for normal users, on-demand for mega-accounts)
- source/youtube-video-reports/1.md (Twitter API operational case study: endpoint, method, parameters, response, idempotency)
- source/extracted/system-design-guide/ch15-designing-a-service-like-01-twitter.md (designing a Twitter-like service)

### 06-ticketmaster.md
- source/youtube-video-reports/2.md (Ticketmaster case study: strong consistency, two-phase booking with Redis TTL lock, virtual waiting room)
- source/youtube-video-reports/3.md (TicketMaster: two-phase booking, CDN caching for search, virtual waiting queue)
- source/youtube-video-reports/8.md (consistent hashing for TicketMaster event database example)
- source/extracted/alex-xu-vol2/ch08-hotel-reservation-system.md (hotel reservation system with similar booking patterns)

### 07-tinder.md
- source/youtube-video-reports/2.md (Tinder case study: geospatial with quad-trees/PostGIS, atomic swipe logic in Redis, Bloom filters vs. 30-90 day cache reset)
- source/youtube-video-reports/3.md (Tinder: atomic swiping in Redis, Bloom filters for repeat profiles, 30-day cache clear)

### 10-upi-payments.md
- source/youtube-video-reports/2.md (UPI case study: NPCI closed-loop ecosystem, VPA, push/pull transactions, acknowledgment and rollback)
- source/youtube-video-reports/3.md (UPI: PSP model, partner bank requirement, App -> Partner Bank -> NPCI -> Payee's Bank flow)
- source/extracted/alex-xu-vol2/ch12-payment-system.md (payment system design)
- source/extracted/alex-xu-vol2/ch13-digital-wallet.md (digital wallet design)

### 04-facebook-live-comments.md
- source/youtube-video-reports/2.md (Facebook Live Comments: sub-200ms sync, SSE connections, in-memory user-to-video mapping, Redis Pub/Sub partitioning with hash mod N)

### 03-whatsapp.md
- source/youtube-video-reports/6.md (WhatsApp/Messenger: persistent WebSockets, Redis Pub/Sub for routing, inbox pattern for at-least-once delivery with ACK)
- source/extracted/acing-system-design/ch17-design-a-text-messaging-app.md (text messaging app design)
- source/extracted/grokking/ch87-capacity-estimation-and-constraints.md (WhatsApp capacity estimation)
- source/extracted/grokking/ch90-a-messages-handling.md (message handling)
- source/extracted/grokking/ch92-c-managing-users-status.md (managing user status)
- source/extracted/grokking/ch98-a-group-chat.md (group chat design)

### 05-dropbox.md
- source/youtube-video-reports/8.md (Dropbox/Google Drive: chunking with fingerprinting, pre-signed URL flow, delta sync, adaptive polling, trust but verify, reconciliation)
- source/extracted/grokking/ch67-you-should-always-clarify-requirements-at-the-beginning-of-t.md (Dropbox requirements)
- source/extracted/grokking/ch72-component-design.md (Dropbox component design)
- source/extracted/grokking/ch74-b-metadata-database.md (metadata database)
- source/extracted/grokking/ch77-e-cloudblock-storage.md (cloud/block storage)

### 08-web-crawler.md
- source/youtube-video-reports/6.md (web crawler: 10B pages in 5 days bandwidth calculation, SQS with visibility timeouts and exponential backoff, DLQ, Bloom filters for URL dedup, robots.txt politeness)
- source/extracted/grokking/ch171-some-design-considerations.md (web crawler design considerations)
- source/extracted/grokking/ch175-difficulties-in-implementing-efficient-08-web-crawler.md (web crawler difficulties)
- source/extracted/grokking/ch176-detailed-component-design.md (web crawler component design)
- source/extracted/grokking/ch179-crawler-traps.md (crawler traps)

### 09-ad-click-aggregator.md
- source/youtube-video-reports/6.md (ad click aggregator: Kappa/Lambda architecture, Flink for 1-minute windows, Spark for reconciliation, logarithmic counting for write reduction)
- source/extracted/alex-xu-vol2/ch07-aggregate-ad-click-events.md (ad click event aggregation design)

### 02-news-feed.md
- source/youtube-video-reports/6.md (Facebook News Feed: hybrid approach with pre-computed flag, fan-out on write for normal users, fan-out on read for mega-accounts)
- source/extracted/acing-system-design/ch19-design-a-02-news-feed.md (news feed design)
- source/extracted/grokking/ch37-system-apis.md (news feed system APIs)
- source/extracted/grokking/ch42-b-datastore-layer.md (news feed datastore layer)
