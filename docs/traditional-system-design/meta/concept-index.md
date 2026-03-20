# Concept Index

## How to Use This Index
Each concept appears ONCE, mapped to its canonical file in the knowledge base. The "Content Boundaries" section defines which file owns which concept to prevent duplication. Other files that touch the same concept should cross-link to the canonical file and state which variant or aspect they use, rather than re-explaining the concept from scratch.

## Content Boundaries (Deduplication Rules)

| Concept | Canonical File | Other files may only... |
|---------|---------------|------------------------|
| Fan-out (read vs write, hybrid) | 11-patterns/fan-out.md | Cross-link and state which variant is used |
| Saga pattern | 08-resilience/distributed-transactions.md | Cross-link only |
| Two-phase commit (2PC) | 08-resilience/distributed-transactions.md | Cross-link only |
| Event sourcing (append-only logs, hydration) | 05-messaging/event-sourcing.md | Cross-link only |
| CQRS (read/write separation) | 05-messaging/cqrs.md | Cross-link only |
| Caching strategies (TTL, cache-aside, write-through/back/around) | 04-caching/caching.md | Cross-link only |
| Redis internals (data structures, pub/sub, persistence) | 04-caching/redis.md | Cross-link only |
| Inverted index / full-text search / Elasticsearch | 11-patterns/search-and-indexing.md | Cross-link only |
| Geospatial (geohashing, quadtrees, R-trees) | 11-patterns/geospatial-indexing.md | Cross-link only |
| Batch/stream processing (Lambda/Kappa, Flink, Spark) | 05-messaging/event-driven-architecture.md (section within) | Cross-link only |
| WAL and CDC | 03-storage/database-replication.md (section within) | Cross-link only |
| Service discovery (ZooKeeper, etcd) | 06-architecture/microservices.md (section within) | Cross-link only |
| Networking (DNS, TCP/UDP, OSI, IP) | 01-fundamentals/networking-fundamentals.md | 07-api-design/ covers app-layer only |
| Scalability overview (vertical vs horizontal) | 01-fundamentals/scaling-overview.md | 02-scalability/ folder has mechanisms |
| ACID transactions | 03-storage/sql-databases.md (section within) | Cross-link only; 08-resilience/ covers distributed txns |
| Consistency models (strong, eventual, causal) | 01-fundamentals/cap-theorem.md (section within) | Cross-link and state which model is chosen |
| Encoding formats (JSON, Protobuf, Avro, Thrift) | 07-api-design/grpc.md (Protobuf section) | rest-api.md covers JSON; others cross-link |
| Bloom filters / Count-Min Sketch / HyperLogLog | 11-patterns/probabilistic-data-structures.md | Cross-link only |
| Adaptive bitrate streaming (HLS, MPEG-DASH) | 11-patterns/video-streaming.md | Cross-link only |
| Virtual waiting room / queue-based admission | 08-resilience/rate-limiting.md (section within) | Cross-link only |
| Pre-signed URLs / multipart uploads | 03-storage/object-storage.md (section within) | Cross-link only |
| Distributed locking (Redis TTL locks) | 04-caching/redis.md (section within) | Cross-link only |
| Gossip protocol | 01-fundamentals/cap-theorem.md (section within) | Cross-link only |
| Vector search / embeddings / ANN | 11-patterns/recommendation-engines.md (section within) | Cross-link only |
| Back-of-envelope estimation (QPS, storage, bandwidth) | 01-fundamentals/back-of-envelope-estimation.md | Cross-link only |
| Feature flags / canary releases | 08-resilience/feature-flags.md | Cross-link only |
| Exponential backoff and jitter | 08-resilience/circuit-breaker.md (section within) | Cross-link only |

---

## Fundamentals

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| System design framework (requirements, HLD, deep dives) | 01-fundamentals/system-design-framework.md | Interview framework, delivery model, design methodology | back-of-envelope-estimation, scaling-overview |
| Scaling overview (vertical vs horizontal) | 01-fundamentals/scaling-overview.md | Scale up / scale out, shared-nothing architecture, elastic scaling | load-balancing, autoscaling, sharding |
| Availability and reliability | 01-fundamentals/availability-reliability.md | Nines of availability (99.9%--99.999%), fault tolerance, SLA/SLO, MTTF, MTTR | cap-theorem, circuit-breaker, database-replication |
| CAP theorem and consistency models | 01-fundamentals/cap-theorem.md | Brewer's theorem, CP vs AP, strong/eventual/causal consistency, BASE, gossip protocol, read-your-own-writes | sql-databases, nosql-databases, distributed-transactions |
| Networking fundamentals | 01-fundamentals/networking-fundamentals.md | DNS, TCP/UDP, IP addressing (IPv4/IPv6), OSI model, NAT, subnets, IGW/NAT gateway, forward/reverse proxy, SSL/TLS termination | load-balancing, api-gateway, cdn |
| Back-of-envelope estimation | 01-fundamentals/back-of-envelope-estimation.md | Capacity planning, QPS calculation, storage estimation, bandwidth estimation, latency numbers | system-design-framework, scaling-overview |

## Scalability

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Load balancing | 02-scalability/load-balancing.md | L4/L7 load balancer, round robin, least connections, IP hashing, weighted distribution, sticky sessions, health checks | api-gateway, autoscaling, networking-fundamentals |
| Autoscaling | 02-scalability/autoscaling.md | Horizontal Pod Autoscaler (HPA), Kubernetes autoscaling, metrics server, resource requests/limits, elastic scaling, traffic patterns (predictable/unpredictable spikes) | load-balancing, monitoring |
| Consistent hashing | 02-scalability/consistent-hashing.md | Hash ring, virtual nodes (vnodes), CRC mod 16384, token-based partitioning | sharding, cassandra, dynamodb, redis |
| Sharding | 02-scalability/sharding.md | Horizontal partitioning, data partitioning, shard key design, range-based/hash-based/directory-based sharding, rebalancing, hot spots, celebrity problem, compound shard keys | consistent-hashing, sql-databases, nosql-databases, cassandra |

## Storage

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| SQL databases | 03-storage/sql-databases.md | Relational databases, Postgres, MySQL, ACID transactions (atomicity, consistency, isolation, durability), schemas, joins, normalization, foreign keys, isolation levels (read committed, snapshot isolation, serializability) | nosql-databases, database-indexing, sharding |
| NoSQL databases | 03-storage/nosql-databases.md | Document stores (MongoDB, Manhattan), key-value stores, wide-column stores, graph databases (Neo4j), schema-on-read, denormalization, polyglot persistence | sql-databases, cassandra, dynamodb, redis |
| Object storage | 03-storage/object-storage.md | S3, GCS, Azure Blob Storage, blob storage, flat namespaces, immutable writes, erasure coding, 11 nines durability, pre-signed URLs, multipart uploads, metadata/data split | cdn, video-streaming |
| Database indexing | 03-storage/database-indexing.md | B-tree, hash index, LSM tree, SSTable, primary/secondary/composite index, write penalty, full table scan | sql-databases, nosql-databases, search-and-indexing |
| Database replication | 03-storage/database-replication.md | Leader-follower replication, multi-leader, leaderless, synchronous/asynchronous replication, WAL (Write-Ahead Log), CDC (Change Data Capture), replication lag | sql-databases, cassandra, cap-theorem |
| Time-series databases | 03-storage/time-series-databases.md | TSDB, LSM trees, append-only storage, Gorilla paper, delta encoding, delta-of-deltas compression, downsampling, MemTable, WAL | monitoring, database-indexing |
| Cassandra | 03-storage/cassandra.md | Wide-column store, leaderless architecture, keyspace, partition key, clustering key, tunable consistency (ANY/ONE/QUORUM/ALL), commit log, MemTable, SSTable, compaction, Bloom filter, gossip protocol, hinted handoff | consistent-hashing, nosql-databases, sharding |
| DynamoDB | 03-storage/dynamodb.md | Partition key (PK), sort key (SK), GSI (Global Secondary Index), LSI (Local Secondary Index), DAX (DynamoDB Accelerator), DynamoDB Streams, CDC, conditional writes, ACID transactions (up to 100 items) | nosql-databases, consistent-hashing, database-indexing |

## Caching

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Caching strategies | 04-caching/caching.md | Cache-aside (lazy loading), read-through, write-through, write-behind/write-back, write-around, TTL (Time to Live), cache eviction (LRU, LFU), cache stampede (thundering herd), cache warming, request coalescing, hot key problem, in-process vs external cache, consistency/stale data | redis, cdn, database-indexing |
| Redis | 04-caching/redis.md | In-memory data store, single-threaded engine, sorted sets (Z-sets), Redis Streams, pub/sub, geospatial API (geohashing), rate limiter (atomic INCR + TTL), distributed locking (TTL locks), consumer groups, hot key mitigation (random suffixes), Redis Cluster (16384 slots), MemoryDB | caching, rate-limiting, message-queues, geospatial-indexing |
| CDN (Content Delivery Network) | 04-caching/cdn.md | Edge locations, edge caching, static asset delivery, geographic distribution, pull vs push CDN, cache invalidation, origin server | object-storage, video-streaming, networking-fundamentals |

## Messaging

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Message queues | 05-messaging/message-queues.md | Kafka, RabbitMQ, SQS, Pulsar, producer/consumer, consumer groups, topics, partitions, append-only log, sequential I/O, visibility timeout, dead letter queue (DLQ), at-least-once/at-most-once/exactly-once delivery, back pressure, hot partition, message ordering | event-driven-architecture, event-sourcing |
| Event-driven architecture | 05-messaging/event-driven-architecture.md | Pub/sub, choreography vs orchestration, async processing, event bus, SNS/SQS fan-out, batch processing (MapReduce, Spark), stream processing (Flink, Kafka Streams), Lambda/Kappa architecture, windowed aggregation, Step Functions (orchestrator pattern) | message-queues, event-sourcing, cqrs |
| Event sourcing | 05-messaging/event-sourcing.md | Append-only event log, event replay, hydration, immutable audit trail, state reconstruction, "time machine" for data, Kafka/Kinesis as event store | cqrs, event-driven-architecture, message-queues |
| CQRS | 05-messaging/cqrs.md | Command Query Responsibility Segregation, read/write separation, command side (write, normalized SQL), query side (read, denormalized NoSQL/materialized views), separate read and write models | event-sourcing, event-driven-architecture, sql-databases, nosql-databases |

## Architecture

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| API gateway | 06-architecture/api-gateway.md | Central entry point, request routing, authentication/authorization, rate limiting, protocol translation, API composition, infrastructure maturity model (startup/growth/enterprise) | load-balancing, rate-limiting, microservices |
| Microservices | 06-architecture/microservices.md | Service-oriented architecture (SOA), service decomposition, functional partitioning, independent deployment, service discovery (ZooKeeper, etcd, Consul), service mesh, sidecar pattern, bounded contexts | api-gateway, event-driven-architecture, distributed-transactions |
| Serverless | 06-architecture/serverless.md | AWS Lambda, Functions-as-a-Service (FaaS), event-triggered compute, pay-per-invocation, cold start, vendor lock-in (Lambda + SQS + API Gateway + S3 ecosystem bind), zero infrastructure management | autoscaling, event-driven-architecture, api-gateway |

## Resilience

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Rate limiting | 08-resilience/rate-limiting.md | Throttling, fixed window, sliding window, token bucket, leaky bucket, DDoS protection, SLA enforcement, cost control, virtual waiting room/queue, API rate limits (e.g., Twitter 300/900 per 15 min) | api-gateway, redis, circuit-breaker |
| Circuit breaker | 08-resilience/circuit-breaker.md | Fail-fast pattern, closed/open/half-open states, cascading failure prevention, exponential backoff, jitter (thundering herd mitigation), retry policy, bulkhead pattern | rate-limiting, microservices, availability-reliability |
| Distributed transactions | 08-resilience/distributed-transactions.md | Two-phase commit (2PC), saga pattern (choreography vs orchestration), compensating transactions, rollback, coordinator/participant model, eventual consistency, cross-shard transactions | sql-databases, event-sourcing, microservices |
| Feature flags | 08-resilience/feature-flags.md | Feature toggles, canary releases, progressive rollout, kill switch, allow lists, A/B testing, configuration-centric deployment, audit trail, TTL + caching for flag sync | api-gateway, autoscaling |

## Security

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Authentication and authorization | 09-security/authentication-authorization.md | AuthN/AuthZ, OAuth 2.0, JWT (JSON Web Token), session tokens, RBAC (Role-Based Access Control), SSO (Single Sign-On), service accounts, API keys | api-security, api-gateway |
| Encryption | 09-security/encryption.md | Encryption at rest, encryption in transit, TLS 1.3, SSL/TLS certificates, HTTPS, key management, data protection | networking-fundamentals, api-security |
| API security | 09-security/api-security.md | Input validation, SQL injection prevention, XSS protection, CORS, IP-based filtering, DDoS mitigation, rate limiting at gateway, principle of least privilege, DevSecOps, custom binary access control | rate-limiting, authentication-authorization, api-gateway |

## Observability

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Monitoring | 10-observability/monitoring.md | Prometheus, Grafana, metrics collection, alerting, four golden signals (latency, traffic, errors, saturation), P99/P95/P50 percentiles, tail latency, ServiceMonitor (Kubernetes), dashboards, Open Cost, SLOs/SLAs | logging, autoscaling, availability-reliability |
| Logging | 10-observability/logging.md | ELK stack (Elasticsearch, Logstash, Kibana), centralized logging, structured logging, log aggregation, distributed tracing, post-mortem analysis, audit trails | monitoring, search-and-indexing |

## API Design

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| REST API | 07-api-design/rest-api.md | RESTful, HTTP methods (GET/POST/PUT/PATCH/DELETE), resource-based design, stateless, JSON, HATEOAS, OpenAPI/Swagger, idempotency, path/query parameters, pagination, API versioning | grpc, graphql, api-gateway |
| gRPC | 07-api-design/grpc.md | Protocol Buffers (Protobuf), binary serialization, HTTP/2, bidirectional streaming, service definitions (.proto), code generation, 5--10x faster than REST JSON, Thrift, Avro | rest-api, microservices, message-queues |
| GraphQL | 07-api-design/graphql.md | Schema-first design, queries/mutations/subscriptions, resolver functions, N+1 problem, data loaders, over-fetching/under-fetching prevention, client-defined response shape | rest-api, api-gateway |
| Real-time protocols | 07-api-design/real-time-protocols.md | WebSockets (bidirectional, persistent), SSE (Server-Sent Events, unidirectional), long polling, short polling, WebRTC (P2P audio/video), SFU (Selective Forwarding Unit), MCU (Multipoint Control Unit), HTTP/2 server push | fan-out, message-queues, redis |

## Patterns

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Fan-out | 11-patterns/fan-out.md | Fan-out on write (push, pre-computed feeds), fan-out on read (pull, computed at request time), hybrid fan-out, celebrity problem, write amplification, timeline generation | caching, message-queues, twitter, news-feed, facebook-live-comments |
| Probabilistic data structures | 11-patterns/probabilistic-data-structures.md | Bloom filter (set membership), Count-Min Sketch (frequency estimation, heavy hitters), HyperLogLog (cardinality estimation, unique counts), space-efficient approximation | redis, web-crawler, ad-click-aggregator, search-and-indexing |
| Recommendation engines | 11-patterns/recommendation-engines.md | Three-stage pipeline (candidate generation, ranking, reranking), collaborative filtering, content-based filtering, vector search, embeddings, HNSW (Hierarchical Navigable Small Worlds), approximate nearest neighbor (ANN), FAISS, Pinecone, exploration vs exploitation | search-and-indexing, message-queues |
| Video streaming | 11-patterns/video-streaming.md | Adaptive bitrate streaming (ABS), HLS (HTTP Live Streaming), MPEG-DASH, video transcoding/encoding, chunked delivery, M3U8 manifest/index file, progressive download, RTMP/RTSP, resolution ladder (480p/720p/1080p/4K) | cdn, object-storage |
| Search and indexing | 11-patterns/search-and-indexing.md | Inverted index, full-text search, Elasticsearch, Solr, tokenization, TF-IDF, relevance scoring, CDC-based sync to search index, autocomplete/typeahead (trie, prefix search) | database-indexing, database-replication, probabilistic-data-structures |
| Geospatial indexing | 11-patterns/geospatial-indexing.md | Geohashing, quadtrees, R-trees (PostGIS), proximity search, radius-based queries, spatial partitioning, dynamic grid sizing, 2D indexing | redis, database-indexing, search-and-indexing |

## Case Studies

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Twitter | 12-case-studies/twitter.md | Microblogging at scale, hybrid fan-out (write for normal users, read for celebrities), home timeline, tweet delivery, massive read-to-write ratio | fan-out, caching, redis, message-queues |
| Ticketmaster | 12-case-studies/ticketmaster.md | Ticket booking, two-phase booking (reserve + confirm), distributed locking (Redis TTL), virtual waiting room, strong consistency, seat inventory, surge management | distributed-transactions, redis, rate-limiting, sql-databases |
| Tinder | 12-case-studies/tinder.md | Geospatial matching, swipe storage (Cassandra), reciprocal swipe atomic logic, Bloom filter for repeat profiles, 30-90 day cache reset, profile ranking | geospatial-indexing, cassandra, redis, probabilistic-data-structures |
| UPI payments | 12-case-studies/upi-payments.md | Unified Payments Interface, NPCI, closed-loop ecosystem, PSP (Payment Service Provider), VPA (Virtual Payment Address), push/pull transactions, acknowledgment/rollback flow | distributed-transactions, encryption, authentication-authorization |
| Facebook live comments | 12-case-studies/facebook-live-comments.md | Live broadcasting, SSE connections at scale, pub/sub partitioning (Redis), video ID hash partitioning, firehose mitigation, sub-200ms delivery | fan-out, redis, real-time-protocols |
| WhatsApp | 12-case-studies/whatsapp.md | Messaging at scale, WebSocket connections, inbox pattern, at-least-once delivery with ACK, message ordering, group chat, presence/status management | real-time-protocols, redis, message-queues, encryption |
| Dropbox | 12-case-studies/dropbox.md | File storage and sync, chunking (5MB parts), fingerprinting (content hashing), delta sync, pre-signed URL upload, adaptive polling, sync service, reconciliation | object-storage, caching, message-queues |
| Web crawler | 12-case-studies/web-crawler.md | URL frontier, BFS crawling, politeness (robots.txt, domain rate limiting), Bloom filter for deduplication, DNS resolution, SQS with visibility timeouts and DLQ, bandwidth estimation | probabilistic-data-structures, message-queues, back-of-envelope-estimation |
| Ad click aggregator | 12-case-studies/ad-click-aggregator.md | Click event aggregation, hybrid stream/batch (Lambda/Kappa), Flink windowed aggregation, Spark reconciliation, logarithmic counting (2^n write reduction), real-time analytics | event-driven-architecture, message-queues, probabilistic-data-structures |
| News feed | 12-case-studies/news-feed.md | Feed generation, hybrid fan-out (pre-computed flag), feed ranking, merge at read time, timeline caching, social graph traversal | fan-out, caching, redis, message-queues |
| Uber | 12-case-studies/uber.md | Ride-sharing at scale, real-time location tracking (H3/S2 hexagonal cells), matching/dispatch system, surge pricing (supply/demand feedback loop), ETA calculation (ML + graph), trip state machine, payment processing (saga pattern) | geospatial-indexing, redis, message-queues, event-driven-architecture, cassandra, sql-databases, distributed-transactions, real-time-protocols |
| Google Maps | 12-case-studies/google-maps.md | Mapping at scale, map tile rendering (pre-rendered PNG/vector tiles via CDN), route planning (A* on hierarchical routing tiles), real-time traffic (probe data aggregation), ETA prediction (graph + ML), geocoding, adaptive rerouting | geospatial-indexing, cdn, object-storage, message-queues, event-driven-architecture, cassandra, redis, time-series-databases |

---

## Generative AI (GenAI Namespace)

GenAI concepts live under `docs/genai-system-design/` with their own concept index at `genai-system-design/meta/genai-concept-index.md`. The following GenAI concepts extend topics that also exist in the traditional system design knowledge base:

| GenAI Concept | GenAI Canonical File | Related Traditional File | Relationship |
|---|---|---|---|
| Vector databases | genai-system-design/vector-search/vector-databases.md | 11-patterns/recommendation-engines.md | Expands vector search section |
| Semantic caching | genai-system-design/performance/semantic-caching.md | 04-caching/caching.md | GenAI-specific caching pattern |
| LLM observability | genai-system-design/evaluation/llm-observability.md | 10-observability/monitoring.md | LLM-specific tracing |
| GenAI gateway | genai-system-design/case-studies/genai-gateway.md | 06-architecture/api-gateway.md | LLM multi-provider routing |
| Streaming (LLM) | genai-system-design/performance/latency-optimization.md | 07-api-design/real-time-protocols.md | LLM streaming specifics |
| GPU scheduling (K8s) | genai-system-design/case-studies/kubernetes-genai.md | 02-scalability/autoscaling.md | GPU-specific autoscaling |
| Model deployment | genai-system-design/patterns/deployment-patterns.md | 08-resilience/feature-flags.md | Model-specific canary/A-B |
| LLM rate limiting | genai-system-design/performance/cost-optimization.md | 08-resilience/rate-limiting.md | LLM API quota management |
| LLM circuit breaker | genai-system-design/patterns/genai-design-patterns.md | 08-resilience/circuit-breaker.md | LLM-specific retry/fallback |

---

## Source Coverage Matrix

The following table maps each source to the primary concepts it contributes to the knowledge base.

| Source | Key Concepts Covered |
|--------|---------------------|
| YouTube Report 1 | Client-server/P2P, API contracts, load balancing, proxies, rate limiting (fixed window, token bucket), feature flags, ACID transactions, container runtimes (CRI, runc, containerd), Kubernetes cost management (HPA, spot instances, affinity rules) |
| YouTube Report 2 | Scaling paradigms, API gateway, infrastructure maturity model, SQL vs NoSQL, Cassandra write path, S3/CDN, full-text search + CDC, SSE vs WebSockets, fan-out (read/write/hybrid), Twitter/Facebook Live/Ticketmaster/Tinder/UPI case studies, ELK + Prometheus/Grafana |
| YouTube Report 3 | Requirements framework (FR vs NFR), CAP theorem, load balancing (L4/L7), consistency models, API gateway vs reverse proxy, fan-out, SSE vs WebSockets, pub/sub, long polling, Twitter/Ticketmaster/Tinder/UPI case studies |
| YouTube Report 4 | SQL vs NoSQL vs object storage, Redis internals (sorted sets, streams, pub/sub, geospatial, hot key), sharding strategies, consistent hashing, 2PC, saga pattern, recommendation engine pipeline, vector search, WebRTC (SFU/MCU), serverless, event sourcing |
| YouTube Report 5 | System design framework (Hello Interview), fan-out problem, hot shard/celebrity problem, SQS vs Kafka, DynamoDB (PK/SK, GSI/LSI, DAX, Streams), consistency models, Facebook News Feed, Facebook Post Search, WhatsApp, web crawler, ad click aggregator, Bloom filter, Count-Min Sketch |
| YouTube Report 6 | Scaling paradigms, nines of availability, reliability vs availability, consistency models, gossip protocol, ACID, partitioning/sharding, time-series DBs (LSM trees, Gorilla compression, downsampling), choreography vs orchestration, saga pattern, Kubernetes (5 pillars), observability, video streaming (ABS, HLS, MPEG-DASH) |
| YouTube Report 7 | Data modeling (5 DB types), normalization vs denormalization, B-tree vs hash index, geospatial indexing (geohash, quadtree, R-tree), inverted index, consistent hashing + virtual nodes, Cassandra deep dive, caching architectures (4 layers, cache stampede, hot keys), probabilistic data structures (Bloom filter, Count-Min Sketch, HyperLogLog), Dropbox/Google Drive case study |
| YouTube Report 8 | Networking (IP, DNS, TCP/UDP, OSI), cloud computing, WebSockets, proxies, REST/GraphQL/gRPC, SQL vs NoSQL, caching + CAP, consistent hashing, circuit breaker, message queues, CQRS, event sourcing, back-of-envelope estimation |
| YouTube Report 9 | (No separate report 9 -- content integrated across reports above) |
| DDIA (Kleppmann) | Reliability/scalability/maintainability, data models, storage engines (B-tree, LSM), encoding (JSON, Protobuf, Thrift, Avro), replication (leader-follower, leaderless), partitioning (range, hash, consistent hashing), transactions (ACID, isolation levels), distributed system challenges, consistency/consensus, batch processing (MapReduce), stream processing (Kafka, Flink), CDC |
| Alex Xu Vol 2 | Proximity service (geohashing), nearby friends, Google Maps, distributed message queue, metrics/monitoring, ad click aggregation, hotel reservation, distributed email, S3-like object storage, real-time leaderboard (Redis sorted sets), payment system, digital wallet, stock exchange |
| Acing System Design (Tan) | System design walkthrough, non-functional requirements, scaling databases, distributed transactions (event sourcing, CDC, choreography/orchestration), common services, rate limiting, notification service, database auditing, autocomplete/typeahead, Flickr, CDN design, messaging app, Airbnb, news feed, top-10 products |
| System Design Guide | Foundations, distributed system attributes, theorems (CAP), core components, DNS/load balancers/API gateways, databases/indexing, distributed cache, pub/sub/queues, API security, URL shortener, proximity service, Twitter, Instagram, Google Docs, Netflix |
| Grokking System Design | URL shortener, Pastebin, Instagram, Twitter, Dropbox, Facebook Messenger, YouTube/Netflix, typeahead, API rate limiting, web crawler, Yelp/proximity, Uber, Ticketmaster, system design glossary (caching, sharding, proxies, SQL/NoSQL, CAP, consistent hashing, long polling/WebSockets/SSE) |
