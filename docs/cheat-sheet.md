# System Design Cheat Sheet

A quick-reference guide for system design interviews. Every section links to the canonical deep-dive file where the concept is fully explored.

---

## Interview Framework (5 Steps)

Follow this sequence in every design session. The phases are sequential -- each produces artifacts that feed the next. See [System Design Framework](./fundamentals/system-design-framework.md) for the full methodology.

| Step | Time | What You Do | Output |
|---|---|---|---|
| **1. Requirements** | 5 min | Clarify functional requirements (the "verbs": create, read, search, notify). Quantify non-functional requirements (DAU, QPS, latency SLA, availability target). Declare the CAP trade-off. Agree on scope. | FR list, NFR numbers, in/out of scope |
| **2. Core Entities and API** | 5 min | Identify entities ("nouns": User, Post, Order). Define the API contract (REST endpoints, request/response shapes). This is where the [data model](./fundamentals/data-modeling.md) begins. | Entity list, API sketch |
| **3. High-Level Design** | 15 min | Draw the end-to-end architecture: client, API gateway, services, databases, caches, queues. Prove the concept works -- it can have "warts." | Architecture diagram |
| **4. Deep Dives** | 20 min | Proactively identify bottlenecks and address them: hot shards, fan-out problems, consistency challenges, failure modes. This is where you show senior-level depth. | Refined architecture with specific solutions |
| **5. Wrap-Up** | 5 min | Summarize trade-offs, state what you would do next (monitoring, security, multi-region), and acknowledge limitations. | Concise summary |

**Critical reminders:**
- Do NOT start drawing boxes before requirements are clear.
- State non-functional numbers early: "100M DAU, 1000 QPS write, 10K QPS read, P99 < 200ms, 99.99% availability."
- Always do back-of-envelope math. See [Back-of-Envelope Estimation](./fundamentals/back-of-envelope-estimation.md).

---

## Data Store Selection Guide

Choose based on the data shape, access pattern, and consistency requirement. See [Data Modeling](./fundamentals/data-modeling.md) for the full framework.

| Use Case | Recommended Store | Why | Canonical File |
|---|---|---|---|
| User profiles, orders, payments (ACID required) | **PostgreSQL / MySQL** | Rigid schema, transactions, referential integrity, flexible ad-hoc queries | [SQL Databases](./storage/sql-databases.md) |
| High-velocity writes (telemetry, swipes, logs) | **Cassandra** | Append-only LSM storage, linear horizontal scaling, 100K+ writes/sec | [Cassandra](./storage/cassandra.md) |
| Flexible-schema documents (product catalog, tweets) | **MongoDB / DynamoDB** | Schema-on-read, nested JSON, no join needed | [NoSQL Databases](./storage/nosql-databases.md) |
| Session data, cache, rate limiting | **Redis** | Sub-millisecond in-memory reads, TTL support, atomic operations | [Redis](./caching/redis.md) |
| Full-text search, log search | **Elasticsearch** | Inverted index, relevance scoring, aggregation | [Search and Indexing](./patterns/search-and-indexing.md) |
| Social graph, recommendation edges | **Neo4j / Amazon Neptune** | Native graph traversal, O(1) edge lookups | [NoSQL Databases](./storage/nosql-databases.md) |
| Images, videos, large files | **S3 / GCS / Azure Blob** | Flat namespace, 11 nines durability, cheap at scale | [Object Storage](./storage/object-storage.md) |
| Time-series metrics (CPU, temperature, stock) | **InfluxDB / TimescaleDB** | LSM trees, compression (delta-of-deltas), downsampling | [Time-Series Databases](./storage/time-series-databases.md) |
| Pre-computed feed, leaderboard | **Redis Sorted Sets** | O(log N) insert/rank, in-memory speed | [Redis](./caching/redis.md) |
| Serverless API with known access patterns | **DynamoDB** | Single-digit ms latency, auto-scaling, GSIs for secondary patterns | [DynamoDB](./storage/dynamodb.md) |

**Polyglot persistence rule**: Most real systems use 3-5 different stores. SQL for transactions, Redis for cache, S3 for media, Elasticsearch for search, Cassandra or DynamoDB for high-volume writes.

---

## Protocol Selection Guide

Choose the communication protocol based on the interaction pattern. See [REST API](./api-design/rest-api.md), [gRPC](./api-design/grpc.md), [GraphQL](./api-design/graphql.md), and [Real-Time Protocols](./api-design/real-time-protocols.md).

| Use Case | Protocol | Why |
|---|---|---|
| Public API, CRUD operations, browser clients | **REST** | Universal, cacheable, human-readable, well-tooled |
| Internal microservice-to-microservice calls | **gRPC** | Binary protobuf (5-10x faster than JSON), streaming, strong typing |
| Mobile/web client needing flexible queries | **GraphQL** | Client specifies exact fields, solves over-fetching/under-fetching, single endpoint |
| Real-time bidirectional (chat, gaming) | **WebSocket** | Persistent full-duplex connection, sub-50ms push |
| Real-time unidirectional (live feed, notifications) | **SSE** | Server push over standard HTTP, simpler than WebSocket, survives corporate firewalls |
| Long-running request, infrequent updates | **Long Polling** | Client holds request open until server has data, simpler than WebSocket for low-frequency updates |
| File upload > 100 MB | **Pre-signed URL (S3)** | Client uploads directly to object storage, bypasses app server bottleneck |
| Event-driven async communication | **Message Queue (SQS/Kafka)** | Decouples producer/consumer, retry semantics, dead-letter queues |

---

## Scaling Decision Tree

Use this to navigate scaling decisions systematically. See [Scaling Overview](./fundamentals/scaling-overview.md), [Sharding](./scalability/sharding.md), and [Autoscaling](./scalability/autoscaling.md).

| If You See This... | Then Do This... | Why |
|---|---|---|
| Single server CPU > 80% sustained | Scale vertically (bigger instance) | Cheapest fix, zero architectural changes |
| Vertical limit reached (~96 cores, 768 GB RAM) | Scale horizontally (add nodes + load balancer) | Physical ceiling of single machine |
| Read throughput is the bottleneck | Add read replicas | Replicas serve reads, leader handles writes. See [Database Replication](./storage/database-replication.md) |
| Write throughput is the bottleneck | Shard the database | Distribute writes across partitions. See [Sharding](./scalability/sharding.md) |
| Same data read repeatedly | Add a caching layer (Redis) | Cache hit avoids DB round-trip. See [Caching](./caching/caching.md) |
| Global users, high latency | Deploy CDN for static assets | Serve from edge locations. See [CDN](./caching/cdn.md) |
| Traffic is bursty/unpredictable | Use autoscaling (HPA or serverless) | Scale to demand, scale to zero. See [Serverless](./architecture/serverless.md) |
| Single point of failure | Add redundancy (replicas, multi-AZ) | See [Availability and Reliability](./fundamentals/availability-reliability.md) |
| Downstream service overwhelmed | Add rate limiting + circuit breaker | Protect dependencies. See [Rate Limiting](./resilience/rate-limiting.md), [Circuit Breaker](./resilience/circuit-breaker.md) |
| Database table > 1 TB or > 50K writes/sec | Shard with consistent hashing | See [Consistent Hashing](./scalability/consistent-hashing.md) |
| Synchronous service chain too slow | Decouple with message queues | Async processing, independent scaling. See [Message Queues](./messaging/message-queues.md) |
| Need exactly-once processing across services | Use saga pattern or 2PC | See [Distributed Transactions](./resilience/distributed-transactions.md) |

---

## Key Numbers Every Architect Should Know

### Latency Reference

| Operation | Time | Notes |
|---|---|---|
| L1 cache reference | 1 ns | |
| L2 cache reference | 4 ns | |
| RAM access | 100 ns | 0.1 microseconds |
| SSD random read | 150 microseconds | 1,500x slower than RAM |
| HDD random read | 10 ms | 100,000x slower than RAM |
| Network round-trip (same data center) | 0.5 ms | |
| Network round-trip (cross-region) | 50-150 ms | US East to US West ~70ms |
| Redis GET | 0.1-0.5 ms | In-memory, network hop |
| PostgreSQL simple query (indexed) | 1-5 ms | B-tree lookup + disk |
| Elasticsearch query | 5-50 ms | Depends on index size |
| S3 GET | 50-200 ms | Network + storage |

### Throughput Reference

| System | Typical Throughput | Notes |
|---|---|---|
| Single PostgreSQL (writes) | 5,000-10,000 TPS | Depends on row size, indexes |
| Single PostgreSQL (reads) | 20,000-50,000 QPS | With proper indexing |
| Redis (single node) | 100,000+ ops/sec | GET/SET operations |
| Cassandra (per node) | 10,000-50,000 writes/sec | Append-only, no locking |
| Kafka (single broker) | 10,000-100,000 msgs/sec | Depends on message size |
| Nginx (reverse proxy) | 50,000+ RPS | Static content |
| Lambda concurrent executions | 1,000 default (adjustable) | Per account per region |

### Storage Back-of-Envelope

| Calculation | Formula | Example |
|---|---|---|
| Daily storage | DAU * actions/user/day * bytes/action | 100M users * 5 posts/day * 1 KB = 500 GB/day |
| Annual storage | Daily * 365 | 500 GB/day * 365 = ~180 TB/year |
| QPS from DAU | DAU / 86,400 seconds (or /100,000 for approximation) | 100M DAU / 100K = 1,000 QPS average |
| Peak QPS | Average QPS * 2-5x | 1,000 * 3 = 3,000 QPS peak |
| Bandwidth | QPS * response size | 3,000 QPS * 10 KB = 30 MB/s |

See [Back-of-Envelope Estimation](./fundamentals/back-of-envelope-estimation.md) for detailed methodology.

### Availability Targets

| Level | Uptime | Downtime/Year | Typical Use |
|---|---|---|---|
| 99% (two nines) | | 3.65 days | Internal tools |
| 99.9% (three nines) | | 8.77 hours | Standard SaaS |
| 99.99% (four nines) | | 52.6 minutes | Production APIs |
| 99.999% (five nines) | | 5.26 minutes | Mission-critical infra |

See [Availability and Reliability](./fundamentals/availability-reliability.md).

---

## Component Selection Quick Reference

| Problem | Component | Implementation Example | Canonical File |
|---|---|---|---|
| Route HTTP traffic to services | **API Gateway** | AWS API Gateway, Kong, Nginx | [API Gateway](./architecture/api-gateway.md) |
| Distribute traffic across servers | **Load Balancer** | ALB (L7), NLB (L4), Nginx, HAProxy | [Load Balancing](./scalability/load-balancing.md) |
| Reduce read latency | **Cache** | Redis (external), local in-process cache | [Caching](./caching/caching.md) |
| Serve static assets globally | **CDN** | CloudFront, Cloudflare, Akamai | [CDN](./caching/cdn.md) |
| Rate limit API requests | **Token Bucket in Redis** | Redis INCR + TTL, API Gateway throttling | [Rate Limiting](./resilience/rate-limiting.md) |
| Decouple services | **Message Queue** | SQS (simple), Kafka (streaming), RabbitMQ | [Message Queues](./messaging/message-queues.md) |
| Full-text search | **Inverted Index** | Elasticsearch, Solr | [Search and Indexing](./patterns/search-and-indexing.md) |
| Unique ID generation | **Snowflake / ULID** | Twitter Snowflake, UUID v7 | [Distributed Transactions](./resilience/distributed-transactions.md) |
| Distributed locking | **Redis Lock with TTL** | Redlock algorithm, DynamoDB conditional writes | [Redis](./caching/redis.md) |
| Workflow orchestration | **State Machine** | AWS Step Functions, Temporal | [Serverless](./architecture/serverless.md) |
| Change Data Capture | **CDC / Streams** | DynamoDB Streams, Debezium + Kafka | [Event-Driven Architecture](./messaging/event-driven-architecture.md) |
| Real-time leaderboard | **Sorted Set** | Redis ZADD/ZRANK | [Redis](./caching/redis.md) |
| Geospatial queries | **Geohash / Quad-tree** | Redis GEO, PostGIS R-tree | [Geospatial Indexing](./patterns/geospatial-indexing.md) |
| Count unique visitors | **HyperLogLog** | Redis PFADD/PFCOUNT (1.5 KB for millions) | [Probabilistic Data Structures](./patterns/probabilistic-data-structures.md) |
| Check set membership | **Bloom Filter** | Redis BF.ADD (avoid recrawling URLs) | [Probabilistic Data Structures](./patterns/probabilistic-data-structures.md) |
| Prevent cascading failures | **Circuit Breaker** | Hystrix pattern, resilience4j | [Circuit Breaker](./resilience/circuit-breaker.md) |
| Multi-step distributed transactions | **Saga Pattern** | Step Functions, event-driven compensating actions | [Distributed Transactions](./resilience/distributed-transactions.md) |
| Feature rollout control | **Feature Flags** | LaunchDarkly, custom Redis-backed flags | [Feature Flags](./resilience/feature-flags.md) |
| Separate read/write optimization | **CQRS** | SQL for writes, denormalized NoSQL for reads | [CQRS](./messaging/cqrs.md) |

---

## Common Patterns by Problem Type

### High Read Volume
- **Cache hot data** in Redis (cache-aside pattern) --> [Caching](./caching/caching.md)
- **CDN for static assets** (images, CSS, JS) --> [CDN](./caching/cdn.md)
- **Read replicas** for database reads --> [Database Replication](./storage/database-replication.md)
- **Denormalize** into pre-computed views --> [Data Modeling](./fundamentals/data-modeling.md)
- **Fan-out on write** to pre-compute feeds --> [Fan-Out](./patterns/fan-out.md)

### High Write Volume
- **Append-only storage** (Cassandra, Kafka) --> [Cassandra](./storage/cassandra.md)
- **Batch/aggregate writes** before persisting --> [Message Queues](./messaging/message-queues.md)
- **Shard the database** by partition key --> [Sharding](./scalability/sharding.md)
- **Write-behind cache** for async persistence --> [Caching](./caching/caching.md)
- **Event sourcing** (immutable event log) --> [Event Sourcing](./messaging/event-sourcing.md)

### Low Latency Required
- **In-memory cache** (Redis: 0.1-0.5ms) --> [Redis](./caching/redis.md)
- **CDN edge caching** (reduce network hops) --> [CDN](./caching/cdn.md)
- **gRPC** instead of REST (binary, streaming) --> [gRPC](./api-design/grpc.md)
- **Database indexing** (B-tree, composite index) --> [Database Indexing](./storage/database-indexing.md)
- **Connection pooling** (avoid TCP handshake per request)
- **Pre-compute** results at write time (CQRS) --> [CQRS](./messaging/cqrs.md)

### Strong Consistency Required
- **SQL with ACID** (PostgreSQL, MySQL) --> [SQL Databases](./storage/sql-databases.md)
- **Distributed locks** (Redis Redlock, Zookeeper) --> [Redis](./caching/redis.md)
- **Two-phase commit** (for cross-service atomicity) --> [Distributed Transactions](./resilience/distributed-transactions.md)
- **Quorum reads/writes** (Cassandra with QUORUM consistency) --> [Cassandra](./storage/cassandra.md)
- **Conditional writes** (DynamoDB optimistic locking) --> [DynamoDB](./storage/dynamodb.md)

### High Availability Required
- **Multi-AZ deployment** with automatic failover
- **Load balancer** health checks --> [Load Balancing](./scalability/load-balancing.md)
- **Circuit breaker** to isolate failures --> [Circuit Breaker](./resilience/circuit-breaker.md)
- **Retry with exponential backoff + jitter** --> [Rate Limiting](./resilience/rate-limiting.md)
- **Eventual consistency** (favor AP in CAP) --> [CAP Theorem](./fundamentals/cap-theorem.md)
- **Async processing** with dead-letter queues --> [Message Queues](./messaging/message-queues.md)

### Real-Time Communication
- **WebSocket** for bidirectional (chat, gaming) --> [Real-Time Protocols](./api-design/real-time-protocols.md)
- **SSE** for server-to-client broadcast (live comments, notifications) --> [Real-Time Protocols](./api-design/real-time-protocols.md)
- **Redis Pub/Sub** for cross-server message routing --> [Redis](./caching/redis.md)
- **Kafka** for durable event streaming --> [Message Queues](./messaging/message-queues.md)

---

## Case Study Quick Reference

| System | Key Challenge | Core Pattern | Canonical File |
|---|---|---|---|
| **Twitter** | Massive read-to-write ratio, celebrity fan-out | Hybrid fan-out (write for normal users, read for celebrities), Redis timelines | [Twitter](./case-studies/twitter.md) |
| **News Feed (Facebook)** | Pre-compute vs. on-demand feed generation | Fan-out on write + hybrid merge for mega-accounts | [News Feed](./case-studies/news-feed.md) |
| **WhatsApp** | Ordered delivery, at-least-once, offline users | WebSocket + Redis Pub/Sub + inbox pattern (ACK-based deletion) | [WhatsApp](./case-studies/whatsapp.md) |
| **TicketMaster** | Strong consistency, surge traffic, no double-booking | Two-phase booking (reserve + confirm), Redis distributed lock with TTL, virtual waiting room | [TicketMaster](./case-studies/ticketmaster.md) |
| **Tinder** | High write volume (swipes), geospatial matching | Cassandra for swipes (100K+ writes/sec), geohashing for proximity | [Tinder](./case-studies/tinder.md) |
| **Facebook Live Comments** | Sub-200ms broadcast to millions of concurrent viewers | SSE + partitioned Redis Pub/Sub (hash of video ID mod N) | [Facebook Live Comments](./case-studies/facebook-live-comments.md) |
| **Dropbox** | Large file sync, resumability, deduplication | Chunking + fingerprinting, pre-signed URLs, delta sync | [Dropbox](./case-studies/dropbox.md) |
| **Web Crawler** | Billions of URLs, politeness, deduplication | BFS with SQS + Bloom filter + exponential backoff | [Web Crawler](./case-studies/web-crawler.md) |
| **Ad Click Aggregator** | High volume event aggregation, exactly-once counting | Kafka + MapReduce aggregation, idempotent writes | [Ad Click Aggregator](./case-studies/ad-click-aggregator.md) |
| **UPI Payments** | Strong consistency, idempotency, high throughput | Saga pattern, idempotency keys, event sourcing | [UPI Payments](./case-studies/upi-payments.md) |
| **Netflix** | Global video delivery, personalization at scale | CDN + microservices + Cassandra + recommendation engine | [Netflix](./case-studies/netflix.md) |

---

## Red Flags in Design

These patterns signal a weak design in interviews. Avoid them.

| Red Flag | Why It Is Wrong | What To Do Instead |
|---|---|---|
| **No requirements phase** | Jumping to architecture without understanding the problem | Spend 5 minutes on FRs, NFRs, scope, and CAP trade-off |
| **"Just use Kafka/Redis/DynamoDB"** without justification | Buzzword-dropping without articulating why | State the access pattern, then derive the storage choice. See [Data Modeling](./fundamentals/data-modeling.md) |
| **Single database for everything** | No polyglot persistence; using SQL for cache and NoSQL for transactions | Match each data shape to its optimal store |
| **No numbers** | No QPS, no storage estimate, no latency target | Do back-of-envelope math. "100M DAU / 100K seconds = 1K QPS." See [Back-of-Envelope Estimation](./fundamentals/back-of-envelope-estimation.md) |
| **Synchronous chain of microservices** | Latency compounds, any failure cascades | Use message queues or Step Functions for decoupling. See [Message Queues](./messaging/message-queues.md) |
| **No failure handling** | Happy-path-only design that ignores network partitions, timeouts, and crashes | Add retries, DLQs, circuit breakers, and idempotency |
| **Sharding from day one** | Over-engineering for a startup that has 1,000 users | Scale vertically first, then read replicas, then shard. See [Scaling Overview](./fundamentals/scaling-overview.md) |
| **Storing images/videos in the database** | Blobs destroy DB performance and replication | Use S3 for media, store URLs in the database. See [Object Storage](./storage/object-storage.md) |
| **No caching layer** | Every read hits the database | Add Redis cache-aside for hot data. See [Caching](./caching/caching.md) |
| **"It is eventually consistent" without explaining impact** | Hand-waving consistency without understanding consequences | State what happens when data is stale and how you mitigate it. See [CAP Theorem](./fundamentals/cap-theorem.md) |
| **Ignoring the "celebrity" / hot key problem** | One viral user overwhelms a shard or cache node | Use random suffix sharding, N-cache strategy, or fan-out on read. See [Fan-Out](./patterns/fan-out.md) |
| **No monitoring or observability** | Building a system you cannot debug in production | Add metrics (P99 latency, error rate), structured logs, distributed tracing. See [Monitoring](./observability/monitoring.md) |
