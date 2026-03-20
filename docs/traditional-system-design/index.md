# System Design Knowledge Base

A comprehensive, concept-driven system design reference built from multiple authoritative sources. Every topic exists in exactly one canonical file — no duplication, full cross-linking.

**62 canonical topic files | 58 GenAI topic files | 64 K8s topic files | 14 case studies | 153 glossary terms | [Cheat Sheet](../cheat-sheet.md)**

---

## Learning Path

### Stage 1: Foundations

Start here to build the mental framework for all system design work.

1. [System Design Framework](01-fundamentals/01-system-design-framework.md) — requirements, estimation, interview methodology
2. [Data Modeling](01-fundamentals/02-data-modeling.md) — schema design, normalization vs denormalization, polyglot persistence
3. [Scaling Overview](01-fundamentals/03-scaling-overview.md) — vertical vs horizontal, when to scale what
4. [Availability & Reliability](01-fundamentals/04-availability-reliability.md) — nines, fault tolerance, redundancy
5. [CAP Theorem](01-fundamentals/05-cap-theorem.md) — CAP, PACELC, consistency models
6. [Networking Fundamentals](01-fundamentals/06-networking-fundamentals.md) — DNS, TCP/UDP, OSI, proxies
7. [Back-of-Envelope Estimation](01-fundamentals/07-back-of-envelope-estimation.md) — QPS, storage, bandwidth math

### Stage 2: Core Building Blocks

The infrastructure primitives that every system is built from.

**Traffic & Distribution:**
1. [Load Balancing](02-scalability/01-load-balancing.md) — L4/L7, algorithms, reverse proxy
2. [Autoscaling](02-scalability/02-autoscaling.md) — HPA, Kubernetes, traffic patterns
3. [Consistent Hashing](02-scalability/03-consistent-hashing.md) — hash rings, virtual nodes
4. [Sharding](02-scalability/04-sharding.md) — strategies, shard keys, celebrity problem

**Data Storage:**
1. [SQL Databases](03-storage/01-sql-databases.md) — relational model, ACID, Postgres
2. [NoSQL Databases](03-storage/02-nosql-databases.md) — document, KV, wide-column, graph
3. [Object Storage](03-storage/03-object-storage.md) — S3, pre-signed URLs, multipart
4. [Database Indexing](03-storage/04-database-indexing.md) — B-trees, LSM trees, hash indexes
5. [Database Replication](03-storage/05-database-replication.md) — leader/follower, quorum, WAL, CDC
6. [Time-Series Databases](03-storage/06-time-series-databases.md) — compression, downsampling
7. [Cassandra](03-storage/07-cassandra.md) — tunable consistency, write path
8. [DynamoDB](03-storage/08-dynamodb.md) — partition keys, GSI/LSI, DAX

**Caching:**
1. [Caching Strategies](04-caching/01-caching.md) — cache-aside, write-through, pitfalls
2. [Redis](04-caching/02-redis.md) — data structures, rate limiters, pub/sub
3. [CDN](04-caching/03-cdn.md) — edge caching, invalidation

### Stage 3: Communication & Architecture

How services talk to each other and how systems are organized.

**Messaging:**
1. [Message Queues](05-messaging/01-message-queues.md) — Kafka, SQS, consumer groups
2. [Event-Driven Architecture](05-messaging/02-event-driven-architecture.md) — pub/sub, choreography vs orchestration
3. [Event Sourcing](05-messaging/03-event-sourcing.md) — append-only logs, hydration
4. [CQRS](05-messaging/04-cqrs.md) — read/write separation, materialized views

**Architecture:**
1. [API Gateway](06-architecture/01-api-gateway.md) — routing, auth, complexity budget
2. [Microservices](06-architecture/02-microservices.md) — decomposition, service discovery
3. [Serverless](06-architecture/03-serverless.md) — Lambda, vendor lock-in, FaaS

**API Design:**
1. [REST API](07-api-design/01-rest-api.md) — resource naming, idempotency, status codes
2. [gRPC](07-api-design/02-grpc.md) — Protocol Buffers, binary serialization
3. [GraphQL](07-api-design/03-graphql.md) — queries, N+1 problem, data loaders
4. [Real-Time Protocols](07-api-design/04-real-time-protocols.md) — WebSockets, SSE, WebRTC

### Stage 4: Reliability & Operations

Making systems survive the real world.

**Resilience:**
1. [Rate Limiting](08-resilience/01-rate-limiting.md) — token bucket, sliding window, Redis implementation
2. [Circuit Breaker](08-resilience/02-circuit-breaker.md) — backoff, jitter, thundering herd
3. [Distributed Transactions](08-resilience/03-distributed-transactions.md) — 2PC, saga pattern
4. [Feature Flags](08-resilience/04-feature-flags.md) — progressive releases, kill switches

**Security:**
1. [Authentication & Authorization](09-security/01-authentication-authorization.md) — OAuth, JWT, RBAC
2. [Encryption](09-security/02-encryption.md) — at rest, in transit, TLS
3. [API Security](09-security/03-api-security.md) — input validation, DDoS protection

**Observability:**
1. [Monitoring](10-observability/01-monitoring.md) — Prometheus, Grafana, golden signals, P99
2. [Logging](10-observability/02-logging.md) — ELK stack, distributed tracing

### Stage 5: Advanced Patterns

Specialized techniques for specific problem domains.

1. [Fan-Out](11-patterns/01-fan-out.md) — read vs write, hybrid, celebrity problem
2. [Probabilistic Data Structures](11-patterns/02-probabilistic-data-structures.md) — Bloom filters, HyperLogLog
3. [Recommendation Engines](11-patterns/03-recommendation-engines.md) — candidate gen, ranking, vector search
4. [Video Streaming](11-patterns/04-video-streaming.md) — adaptive bitrate, HLS/DASH
5. [Search & Indexing](11-patterns/05-search-and-indexing.md) — inverted index, Elasticsearch
6. [Geospatial Indexing](11-patterns/06-geospatial-indexing.md) — geohashing, quadtrees, R-trees

### Stage 6: Case Studies

Real-world system designs that tie everything together. Study these after mastering the building blocks.

| Case Study | Key Patterns | Difficulty |
|-----------|-------------|-----------|
| [Twitter](12-case-studies/01-twitter.md) | Hybrid fan-out, timeline, search | Medium |
| [News Feed](12-case-studies/02-news-feed.md) | Fan-out, ranking, pre-computation | Medium |
| [WhatsApp](12-case-studies/03-whatsapp.md) | WebSockets, inbox pattern, delivery guarantees | Medium |
| [Facebook Live Comments](12-case-studies/04-facebook-live-comments.md) | SSE, partitioned pub/sub | Medium |
| [Dropbox](12-case-studies/05-dropbox.md) | Chunking, delta sync, pre-signed URLs | Medium |
| [Ticketmaster](12-case-studies/06-ticketmaster.md) | Distributed locks, virtual waiting room | Hard |
| [Tinder](12-case-studies/07-tinder.md) | Geospatial, atomic swiping, Bloom filters | Hard |
| [Web Crawler](12-case-studies/08-web-crawler.md) | URL frontier, SQS, politeness | Hard |
| [Ad Click Aggregator](12-case-studies/09-ad-click-aggregator.md) | Lambda/Kappa, Flink, logarithmic counting | Hard |
| [UPI Payments](12-case-studies/10-upi-payments.md) | NPCI closed-loop, transaction integrity | Hard |
| [Instagram](12-case-studies/11-instagram.md) | Image pipeline, feed ranking, Stories | Medium |
| [Netflix](12-case-studies/12-netflix.md) | Transcoding, ABR streaming, Open Connect CDN | Hard |
| [Uber](12-case-studies/13-uber.md) | Geospatial matching, surge pricing, ETA | Hard |
| [Google Maps](12-case-studies/14-google-maps.md) | Tile serving, route planning, real-time traffic | Hard |

### Stage 7: Generative AI System Design

A complete knowledge base for GenAI system design — from transformer foundations through production patterns.

**[→ GenAI System Design Knowledge Base](../genai-system-design/index.md)** — 58 topic files covering LLM architecture, RAG, agents, evaluation, safety, and production patterns.

### Stage 8: Kubernetes System Design

A complete knowledge base for Kubernetes system design — from cluster architecture through production operations.

**[→ Kubernetes System Design Knowledge Base](../kubernetes-system-design/index.md)** — 64 topic files covering cluster design, workload patterns, networking, scaling, security, deployment, observability, platform engineering, and operations.

---

## Quick Reference

- [Cheat Sheet](../cheat-sheet.md) — interview framework, decision matrices, key numbers
- [Glossary](../glossary.md) — 153 system design terms defined
- [Concept Index](meta/concept-index.md) — master deduplicated concept list
- [Source Inventory](meta/source-inventory.md) — catalog of all source materials
- [Source Traceability Map](meta/source-map.md) — which sources informed each topic
