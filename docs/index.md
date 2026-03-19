# System Design Knowledge Base

A comprehensive, concept-driven system design reference built from multiple authoritative sources. Every topic exists in exactly one canonical file — no duplication, full cross-linking.

**57 canonical topic files | 10 case studies | 153 glossary terms**

---

## Learning Path

### Stage 1: Foundations

Start here to build the mental framework for all system design work.

1. [System Design Framework](fundamentals/system-design-framework.md) — requirements, estimation, interview methodology
2. [Scaling Overview](fundamentals/scaling-overview.md) — vertical vs horizontal, when to scale what
3. [Availability & Reliability](fundamentals/availability-reliability.md) — nines, fault tolerance, redundancy
4. [CAP Theorem](fundamentals/cap-theorem.md) — CAP, PACELC, consistency models
5. [Networking Fundamentals](fundamentals/networking-fundamentals.md) — DNS, TCP/UDP, OSI, proxies
6. [Back-of-Envelope Estimation](fundamentals/back-of-envelope-estimation.md) — QPS, storage, bandwidth math

### Stage 2: Core Building Blocks

The infrastructure primitives that every system is built from.

**Traffic & Distribution:**
1. [Load Balancing](scalability/load-balancing.md) — L4/L7, algorithms, reverse proxy
2. [Autoscaling](scalability/autoscaling.md) — HPA, Kubernetes, traffic patterns
3. [Consistent Hashing](scalability/consistent-hashing.md) — hash rings, virtual nodes
4. [Sharding](scalability/sharding.md) — strategies, shard keys, celebrity problem

**Data Storage:**
5. [SQL Databases](storage/sql-databases.md) — relational model, ACID, Postgres
6. [NoSQL Databases](storage/nosql-databases.md) — document, KV, wide-column, graph
7. [Object Storage](storage/object-storage.md) — S3, pre-signed URLs, multipart
8. [Database Indexing](storage/database-indexing.md) — B-trees, LSM trees, hash indexes
9. [Database Replication](storage/database-replication.md) — leader/follower, quorum, WAL, CDC
10. [Time-Series Databases](storage/time-series-databases.md) — compression, downsampling
11. [Cassandra](storage/cassandra.md) — tunable consistency, write path
12. [DynamoDB](storage/dynamodb.md) — partition keys, GSI/LSI, DAX

**Caching:**
13. [Caching Strategies](caching/caching.md) — cache-aside, write-through, pitfalls
14. [Redis](caching/redis.md) — data structures, rate limiters, pub/sub
15. [CDN](caching/cdn.md) — edge caching, invalidation

### Stage 3: Communication & Architecture

How services talk to each other and how systems are organized.

**Messaging:**
1. [Message Queues](messaging/message-queues.md) — Kafka, SQS, consumer groups
2. [Event-Driven Architecture](messaging/event-driven-architecture.md) — pub/sub, choreography vs orchestration
3. [Event Sourcing](messaging/event-sourcing.md) — append-only logs, hydration
4. [CQRS](messaging/cqrs.md) — read/write separation, materialized views

**Architecture:**
5. [API Gateway](architecture/api-gateway.md) — routing, auth, complexity budget
6. [Microservices](architecture/microservices.md) — decomposition, service discovery
7. [Serverless](architecture/serverless.md) — Lambda, vendor lock-in, FaaS

**API Design:**
8. [REST API](api-design/rest-api.md) — resource naming, idempotency, status codes
9. [gRPC](api-design/grpc.md) — Protocol Buffers, binary serialization
10. [GraphQL](api-design/graphql.md) — queries, N+1 problem, data loaders
11. [Real-Time Protocols](api-design/real-time-protocols.md) — WebSockets, SSE, WebRTC

### Stage 4: Reliability & Operations

Making systems survive the real world.

**Resilience:**
1. [Rate Limiting](resilience/rate-limiting.md) — token bucket, sliding window, Redis implementation
2. [Circuit Breaker](resilience/circuit-breaker.md) — backoff, jitter, thundering herd
3. [Distributed Transactions](resilience/distributed-transactions.md) — 2PC, saga pattern
4. [Feature Flags](resilience/feature-flags.md) — progressive releases, kill switches

**Security:**
5. [Authentication & Authorization](security/authentication-authorization.md) — OAuth, JWT, RBAC
6. [Encryption](security/encryption.md) — at rest, in transit, TLS
7. [API Security](security/api-security.md) — input validation, DDoS protection

**Observability:**
8. [Monitoring](observability/monitoring.md) — Prometheus, Grafana, golden signals, P99
9. [Logging](observability/logging.md) — ELK stack, distributed tracing

### Stage 5: Advanced Patterns

Specialized techniques for specific problem domains.

1. [Fan-Out](patterns/fan-out.md) — read vs write, hybrid, celebrity problem
2. [Probabilistic Data Structures](patterns/probabilistic-data-structures.md) — Bloom filters, HyperLogLog
3. [Recommendation Engines](patterns/recommendation-engines.md) — candidate gen, ranking, vector search
4. [Video Streaming](patterns/video-streaming.md) — adaptive bitrate, HLS/DASH
5. [Search & Indexing](patterns/search-and-indexing.md) — inverted index, Elasticsearch
6. [Geospatial Indexing](patterns/geospatial-indexing.md) — geohashing, quadtrees, R-trees

### Stage 6: Case Studies

Real-world system designs that tie everything together. Study these after mastering the building blocks.

| Case Study | Key Patterns | Difficulty |
|-----------|-------------|-----------|
| [Twitter](case-studies/twitter.md) | Hybrid fan-out, timeline, search | Medium |
| [News Feed](case-studies/news-feed.md) | Fan-out, ranking, pre-computation | Medium |
| [WhatsApp](case-studies/whatsapp.md) | WebSockets, inbox pattern, delivery guarantees | Medium |
| [Facebook Live Comments](case-studies/facebook-live-comments.md) | SSE, partitioned pub/sub | Medium |
| [Dropbox](case-studies/dropbox.md) | Chunking, delta sync, pre-signed URLs | Medium |
| [Ticketmaster](case-studies/ticketmaster.md) | Distributed locks, virtual waiting room | Hard |
| [Tinder](case-studies/tinder.md) | Geospatial, atomic swiping, Bloom filters | Hard |
| [Web Crawler](case-studies/web-crawler.md) | URL frontier, SQS, politeness | Hard |
| [Ad Click Aggregator](case-studies/ad-click-aggregator.md) | Lambda/Kappa, Flink, logarithmic counting | Hard |
| [UPI Payments](case-studies/upi-payments.md) | NPCI closed-loop, transaction integrity | Hard |

---

## Quick Reference

- [Glossary](glossary.md) — 153 system design terms defined
- [Concept Index](meta/concept-index.md) — master deduplicated concept list
- [Source Inventory](meta/source-inventory.md) — catalog of all source materials
- [Source Traceability Map](meta/source-map.md) — which sources informed each topic
