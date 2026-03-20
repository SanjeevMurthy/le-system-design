# System Design Knowledge Base

A comprehensive, concept-driven system design reference built from multiple authoritative sources. Every topic exists in exactly one canonical file — no duplication, full cross-linking.

**62 canonical topic files | 58 GenAI topic files | 14 case studies | 153 glossary terms | [Cheat Sheet](../cheat-sheet.md)**

---

## Learning Path

### Stage 1: Foundations

Start here to build the mental framework for all system design work.

1. [System Design Framework](01-fundamentals/system-design-framework.md) — requirements, estimation, interview methodology
2. [Data Modeling](01-fundamentals/data-modeling.md) — schema design, normalization vs denormalization, polyglot persistence
3. [Scaling Overview](01-fundamentals/scaling-overview.md) — vertical vs horizontal, when to scale what
3. [Availability & Reliability](01-fundamentals/availability-reliability.md) — nines, fault tolerance, redundancy
4. [CAP Theorem](01-fundamentals/cap-theorem.md) — CAP, PACELC, consistency models
5. [Networking Fundamentals](01-fundamentals/networking-fundamentals.md) — DNS, TCP/UDP, OSI, proxies
6. [Back-of-Envelope Estimation](01-fundamentals/back-of-envelope-estimation.md) — QPS, storage, bandwidth math

### Stage 2: Core Building Blocks

The infrastructure primitives that every system is built from.

**Traffic & Distribution:**
1. [Load Balancing](02-scalability/load-balancing.md) — L4/L7, algorithms, reverse proxy
2. [Autoscaling](02-scalability/autoscaling.md) — HPA, Kubernetes, traffic patterns
3. [Consistent Hashing](02-scalability/consistent-hashing.md) — hash rings, virtual nodes
4. [Sharding](02-scalability/sharding.md) — strategies, shard keys, celebrity problem

**Data Storage:**
5. [SQL Databases](03-storage/sql-databases.md) — relational model, ACID, Postgres
6. [NoSQL Databases](03-storage/nosql-databases.md) — document, KV, wide-column, graph
7. [Object Storage](03-storage/object-storage.md) — S3, pre-signed URLs, multipart
8. [Database Indexing](03-storage/database-indexing.md) — B-trees, LSM trees, hash indexes
9. [Database Replication](03-storage/database-replication.md) — leader/follower, quorum, WAL, CDC
10. [Time-Series Databases](03-storage/time-series-databases.md) — compression, downsampling
11. [Cassandra](03-storage/cassandra.md) — tunable consistency, write path
12. [DynamoDB](03-storage/dynamodb.md) — partition keys, GSI/LSI, DAX

**Caching:**
13. [Caching Strategies](04-caching/caching.md) — cache-aside, write-through, pitfalls
14. [Redis](04-caching/redis.md) — data structures, rate limiters, pub/sub
15. [CDN](04-caching/cdn.md) — edge caching, invalidation

### Stage 3: Communication & Architecture

How services talk to each other and how systems are organized.

**Messaging:**
1. [Message Queues](05-messaging/message-queues.md) — Kafka, SQS, consumer groups
2. [Event-Driven Architecture](05-messaging/event-driven-architecture.md) — pub/sub, choreography vs orchestration
3. [Event Sourcing](05-messaging/event-sourcing.md) — append-only logs, hydration
4. [CQRS](05-messaging/cqrs.md) — read/write separation, materialized views

**Architecture:**
5. [API Gateway](06-architecture/api-gateway.md) — routing, auth, complexity budget
6. [Microservices](06-architecture/microservices.md) — decomposition, service discovery
7. [Serverless](06-architecture/serverless.md) — Lambda, vendor lock-in, FaaS

**API Design:**
8. [REST API](07-api-design/rest-api.md) — resource naming, idempotency, status codes
9. [gRPC](07-api-design/grpc.md) — Protocol Buffers, binary serialization
10. [GraphQL](07-api-design/graphql.md) — queries, N+1 problem, data loaders
11. [Real-Time Protocols](07-api-design/real-time-protocols.md) — WebSockets, SSE, WebRTC

### Stage 4: Reliability & Operations

Making systems survive the real world.

**Resilience:**
1. [Rate Limiting](08-resilience/rate-limiting.md) — token bucket, sliding window, Redis implementation
2. [Circuit Breaker](08-resilience/circuit-breaker.md) — backoff, jitter, thundering herd
3. [Distributed Transactions](08-resilience/distributed-transactions.md) — 2PC, saga pattern
4. [Feature Flags](08-resilience/feature-flags.md) — progressive releases, kill switches

**Security:**
5. [Authentication & Authorization](09-security/authentication-authorization.md) — OAuth, JWT, RBAC
6. [Encryption](09-security/encryption.md) — at rest, in transit, TLS
7. [API Security](09-security/api-security.md) — input validation, DDoS protection

**Observability:**
8. [Monitoring](10-observability/monitoring.md) — Prometheus, Grafana, golden signals, P99
9. [Logging](10-observability/logging.md) — ELK stack, distributed tracing

### Stage 5: Advanced Patterns

Specialized techniques for specific problem domains.

1. [Fan-Out](11-patterns/fan-out.md) — read vs write, hybrid, celebrity problem
2. [Probabilistic Data Structures](11-patterns/probabilistic-data-structures.md) — Bloom filters, HyperLogLog
3. [Recommendation Engines](11-patterns/recommendation-engines.md) — candidate gen, ranking, vector search
4. [Video Streaming](11-patterns/video-streaming.md) — adaptive bitrate, HLS/DASH
5. [Search & Indexing](11-patterns/search-and-indexing.md) — inverted index, Elasticsearch
6. [Geospatial Indexing](11-patterns/geospatial-indexing.md) — geohashing, quadtrees, R-trees

### Stage 6: Case Studies

Real-world system designs that tie everything together. Study these after mastering the building blocks.

| Case Study | Key Patterns | Difficulty |
|-----------|-------------|-----------|
| [Twitter](12-case-studies/twitter.md) | Hybrid fan-out, timeline, search | Medium |
| [News Feed](12-case-studies/news-feed.md) | Fan-out, ranking, pre-computation | Medium |
| [WhatsApp](12-case-studies/whatsapp.md) | WebSockets, inbox pattern, delivery guarantees | Medium |
| [Facebook Live Comments](12-case-studies/facebook-live-comments.md) | SSE, partitioned pub/sub | Medium |
| [Dropbox](12-case-studies/dropbox.md) | Chunking, delta sync, pre-signed URLs | Medium |
| [Ticketmaster](12-case-studies/ticketmaster.md) | Distributed locks, virtual waiting room | Hard |
| [Tinder](12-case-studies/tinder.md) | Geospatial, atomic swiping, Bloom filters | Hard |
| [Web Crawler](12-case-studies/web-crawler.md) | URL frontier, SQS, politeness | Hard |
| [Ad Click Aggregator](12-case-studies/ad-click-aggregator.md) | Lambda/Kappa, Flink, logarithmic counting | Hard |
| [UPI Payments](12-case-studies/upi-payments.md) | NPCI closed-loop, transaction integrity | Hard |
| [Instagram](12-case-studies/instagram.md) | Image pipeline, feed ranking, Stories | Medium |
| [Netflix](12-case-studies/netflix.md) | Transcoding, ABR streaming, Open Connect CDN | Hard |
| [Uber](12-case-studies/uber.md) | Geospatial matching, surge pricing, ETA | Hard |
| [Google Maps](12-case-studies/google-maps.md) | Tile serving, route planning, real-time traffic | Hard |

### Stage 7: Generative AI System Design

A complete knowledge base for GenAI system design — from transformer foundations through production patterns.

**[→ GenAI System Design Knowledge Base](../genai-system-design/index.md)** — 58 topic files covering LLM architecture, RAG, agents, evaluation, safety, and production patterns.

---

## Quick Reference

- [Cheat Sheet](../cheat-sheet.md) — interview framework, decision matrices, key numbers
- [Glossary](../glossary.md) — 153 system design terms defined
- [Concept Index](meta/concept-index.md) — master deduplicated concept list
- [Source Inventory](meta/source-inventory.md) — catalog of all source materials
- [Source Traceability Map](meta/source-map.md) — which sources informed each topic
