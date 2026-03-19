# System Design Knowledge Base — Design Spec

## Goal

Transform raw learning materials in `/source` (4 PDF books, 1 PDF notes, 9 YouTube video report markdowns) into a production-quality, deduplicated, concept-driven system design knowledge base suitable for both deep learning and interview preparation.

## Constraints

- No duplicate concepts across files
- Every concept exists in ONE canonical file
- All output in Markdown with Mermaid diagrams where applicable
- Every topic follows the 12-section template (Overview, Why It Matters, Core Concepts, How It Works, Architecture/Flow, Types/Variants, Use Cases, Tradeoffs, Common Pitfalls, Real-World Examples, Related Concepts, Source Traceability)
- File sizes balanced (avoid >1500 lines or overly fragmented files)
- Cross-linking between related topics
- Source traceability for every topic

## Source Materials

| Source | Type | Pages | Key Coverage |
|--------|------|-------|-------------|
| Designing Data-Intensive Applications (Kleppmann) | Book PDF | 613 | Storage engines, replication, partitioning, transactions, consistency, batch/stream processing |
| System Design Interview Vol. 2 (Alex Xu) | Book PDF | 544 | 13 case studies: proximity, message queue, ad clicks, hotel, payment, stock exchange |
| Acing the System Design Interview (Zhiyong Tan) | Book PDF | 473 | Concepts + 11 case studies: rate limiting, CDN, news feed, messaging, Airbnb |
| System Design Guide for Software Professionals | Book PDF | 421 | Foundations + building blocks + 6 full designs: URL shortener, Twitter, Instagram, Netflix, Google Docs, proximity |
| System Design - Grokking | Notes PDF | 80 | Classic interview designs: URL shortener, Instagram, Dropbox, Twitter, YouTube, Uber |
| YouTube Video Reports 1-9 | Markdown | ~1300 lines | Distributed systems fundamentals, case studies (Twitter, Ticketmaster, Tinder, UPI), Redis, Kafka, caching, sharding, Cassandra, recommendation engines, video streaming |

**Non-source files (must be excluded from content extraction):**
- `/initialize.md` — project brief/instructions, not source material
- `/x-prompts.txt` — prompt notes, not source material

## Architecture

### Phase 0: PDF Extraction (Python Script)

**Script:** `/scripts/extract_pdfs.py`

**Dependencies:** PyMuPDF >= 1.23.0 (required for `page.find_tables()` API)

Build a Python script using PyMuPDF (fitz) that:
- Reads each PDF, detects chapter/section boundaries from TOC metadata + heading heuristics
- Extracts text per chapter, cleans formatting artifacts
- Identifies and tags: examples, tables, key definitions, case studies
- Outputs structured markdown per chapter

**Output:**
```
/source/extracted/
  ddia/
    ch01-reliable-scalable-maintainable.md
    ...ch12-future-of-data-systems.md
  alex-xu-vol2/
    ch01-proximity-service.md
    ...ch13-stock-exchange.md
  acing-system-design/
    ch01-system-design-concepts.md
    ...ch17-top10-products-dashboard.md
  system-design-guide/
    ch01-basics.md
    ...ch16-cheat-sheet.md
  grokking/
    01-url-shortener.md
    ...XX-system-design-basics.md
```

**Each extracted file format:**
```markdown
# Chapter Title
> Source: <book name>, Chapter N, Pages X-Y

## Key Concepts
- Bullet list of main concepts covered

## Content
(Cleaned extracted text, preserving section structure)

## Examples & Scenarios
(Extracted real-world examples, case studies, math — only if detected)

## Tables & Comparisons
(Reconstructed comparison tables — only if tables detected, omit section otherwise)

## Key Takeaways
(Final summaries, pro tips, tradeoff callouts found in text — only if detected)
```

**Heuristics:**
- TOC bookmarks -> chapter boundaries (available for 4 of 5 PDFs)
- Font size analysis for Grokking PDF: compute median body font size, then flag lines with font size >= 1.3x median as section headers. Additionally detect ALL CAPS lines of length > 10 characters as headers.
- Example tagging: lines starting with "Example:", "Case Study:", "Scenario:", or containing "for example," / "for instance," / "e.g.," -> tagged as examples. Avoid false positives from generic words like "consider" used in normal prose.
- Comparison patterns: lines containing " vs ", "pros and cons", "tradeoff", "trade-off", "comparison" near section headers -> tagged as comparisons
- Bullet/numbered lists -> preserved structure
- Table detection: use `page.find_tables()` (PyMuPDF >= 1.23) as primary strategy. Fallback to column-alignment heuristics only if the API finds no tables on a page that visually contains tabular data.

**Validation gate (Phase 0 -> Phase 1):**
After extraction completes, the script runs a self-validation step:
1. Verify each expected chapter file exists and is non-empty (> 100 characters)
2. Print a summary: book name, chapters extracted, total files, any failures
3. If any book fails completely, log the error and continue with remaining books
4. Output a manifest file `/source/extracted/manifest.json` listing all generated files, their status, and any failures

Phase 1 may launch if the manifest confirms at least 4 of 5 books extracted successfully (since YouTube markdown reports provide fallback coverage). If 2+ books fail, halt and require manual intervention. The manifest must clearly flag which books are missing so Phase 1 agents can note coverage gaps.

### Phase 1: Source Analysis (3 parallel agents)

Run after Phase 0 extraction completes and manifest is validated.

**Input scope for ALL Phase 1 agents:**
- YouTube markdown reports: `/source/youtube-video-reports/1.md` through `9.md` (read directly, no extraction needed)
- Extracted PDF chapters: `/source/extracted/**/*.md`
- Agents must NOT read `/initialize.md` or `/x-prompts.txt` as source material

**Agent 1:** `/docs/meta/source-inventory.md`
- Catalogs all sources: 9 YouTube reports + all extracted PDF chapters
- For each: type, scope, concepts covered

**Agent 2:** `/docs/meta/concept-index.md`
- Master deduplicated concept list from all sources
- Grouped into domains with aliases and cross-references
- Each concept is UNIQUE
- Must define explicit content boundaries for overlapping topics (see Content Boundaries section below)

**Agent 3:** `/docs/meta/source-map.md` + `/docs/glossary.md`
- Topic -> source file traceability mapping
- Glossary of all key terms with concise definitions

**Phase 1 -> Phase 2 gate:** ALL three agents must complete before Phase 2 starts. Specifically, `concept-index.md` must be finalized and reviewed because it defines the canonical concept boundaries that Phase 2 agents must respect.

### Phase 2: Documentation Generation (3 parallel agents, 2 batches)

**Batch 1:**

| Agent | Folders | Specific Files |
|-------|---------|----------------|
| Agent 1 | fundamentals/ + scalability/ | system-design-framework, scaling-overview, availability-reliability, cap-theorem, networking-fundamentals, back-of-envelope-estimation, load-balancing, autoscaling, consistent-hashing, sharding (10 files) |
| Agent 2 | storage/ + caching/ | sql-databases, nosql-databases, object-storage, database-indexing, database-replication, time-series-databases, cassandra, dynamodb, caching, redis, cdn (11 files) |
| Agent 3 | messaging/ + architecture/ + resilience/ | message-queues, event-driven-architecture, event-sourcing, cqrs, api-gateway, microservices, serverless, rate-limiting, circuit-breaker, distributed-transactions, feature-flags (11 files) |

**Batch 2:**

| Agent | Folders | Specific Files |
|-------|---------|----------------|
| Agent 1 | security/ + observability/ + api-design/ (partial) | authentication-authorization, encryption, api-security, monitoring, logging, rest-api, grpc (7 files) |
| Agent 2 | api-design/ (partial) + patterns/ | graphql, real-time-protocols, fan-out, probabilistic-data-structures, recommendation-engines, video-streaming, search-and-indexing, geospatial-indexing (8 files) |
| Agent 3 | case-studies/ | twitter, ticketmaster, tinder, upi-payments, facebook-live-comments, whatsapp, dropbox, web-crawler, ad-click-aggregator, news-feed (10 files) |

**Agent rules:**
- Each agent receives: the 12-section template, its assigned topic list with explicit file names, paths to ALL source files, and the finalized `concept-index.md` with content boundaries
- Each agent produces: complete canonical `.md` files with Mermaid diagrams, cross-links, source traceability
- No agent writes to another agent's files
- Cross-links use relative paths (e.g., `../caching/redis.md`) and may reference files being generated by other agents in the same batch — these are written speculatively as relative paths and verified in Phase 3
- Case study files in `case-studies/` must NOT re-explain concepts that have canonical files. Instead, they cross-link to the canonical file and focus on the specific application of the concept within the case study context.

**Agent failure handling:** If an agent fails mid-execution, its already-written files remain. The failed agent can be re-run with only the remaining unwritten files as its assignment. Other agents' work is unaffected since there is no shared file ownership.

### Phase 3: Finalization (main thread)

- Build `/docs/index.md` with learning path, topic categories, study order
- **Cross-link verification:** Run a script that scans all `.md` files in `/docs/`, extracts relative links, and verifies each target file exists. Report broken links for manual fix.
- **Deduplication audit:** Grep for key concept terms (e.g., "fan-out on write", "two-phase commit", "saga pattern") across all files. Flag any file that contains >3 sentences explaining a concept owned by a different canonical file.
- **Mermaid syntax check:** Validate all mermaid code blocks parse correctly (basic regex + structure check)
- Quality check against all acceptance criteria

## Content Boundaries (Deduplication Rules)

These rules define which file owns which concept to prevent duplication:

| Concept | Canonical File | Other files may only... |
|---------|---------------|------------------------|
| Fan-out (read vs write, hybrid) | `patterns/fan-out.md` | Cross-link and state which variant is used |
| Saga pattern | `resilience/distributed-transactions.md` | Cross-link only |
| Two-phase commit (2PC) | `resilience/distributed-transactions.md` | Cross-link only |
| Event sourcing (append-only logs, hydration) | `messaging/event-sourcing.md` | Cross-link only |
| CQRS (read/write separation) | `messaging/cqrs.md` | Cross-link only |
| Caching strategies (TTL, cache-aside, write-through/back/around, stampede, invalidation) | `caching/caching.md` | Cross-link only |
| Redis internals (data structures, pub/sub, persistence, streams, geo) | `caching/redis.md` | Cross-link only |
| Inverted index / full-text search / Elasticsearch | `patterns/search-and-indexing.md` | Cross-link only |
| Geospatial (geohashing, quadtrees, R-trees) | `patterns/geospatial-indexing.md` | Cross-link only |
| Batch/stream processing (Lambda/Kappa, Flink, Spark) | `messaging/event-driven-architecture.md` (section within) | Cross-link only |
| WAL and CDC | `storage/database-replication.md` (section within) | Cross-link only |
| Service discovery (ZooKeeper, etcd) | `architecture/microservices.md` (section within) | Cross-link only |
| Networking (DNS, TCP/UDP, OSI, IP) | `fundamentals/networking-fundamentals.md` | `api-design/` files cover application-layer protocol design only |
| Scalability overview (vertical vs horizontal, scaling philosophy) | `fundamentals/scaling-overview.md` | `scalability/` folder files cover specific mechanisms |

## Concept Taxonomy (57 canonical topic files)

```
/docs/
  index.md
  glossary.md

  fundamentals/
    system-design-framework.md        # requirements, estimation, interview methodology
    scaling-overview.md               # vertical vs horizontal, scaling philosophy
    availability-reliability.md       # nines, fault tolerance, redundancy, blast radius
    cap-theorem.md                    # CAP, PACELC, consistency models
    networking-fundamentals.md        # DNS, TCP/UDP, OSI model, subnets, NAT
    back-of-envelope-estimation.md    # QPS, storage, bandwidth math

  scalability/
    load-balancing.md                 # L4/L7, algorithms, reverse proxy
    autoscaling.md                    # HPA, Kubernetes scaling, traffic patterns
    consistent-hashing.md             # hash rings, virtual nodes
    sharding.md                       # strategies, shard keys, cross-shard txns

  storage/
    sql-databases.md                  # relational model, ACID, Postgres internals
    nosql-databases.md                # document, KV, wide-column, graph
    object-storage.md                 # S3, blob, pre-signed URLs, multipart
    database-indexing.md              # B-trees, LSM trees, hash indexes
    database-replication.md           # leader/follower, multi-leader, quorum, WAL, CDC
    time-series-databases.md          # LSM, compression, downsampling
    cassandra.md                      # architecture, tunable consistency, write path
    dynamodb.md                       # partition/sort keys, GSI/LSI, DAX, streams

  caching/
    caching.md                        # strategies, patterns, pitfalls (NOT Redis-specific)
    redis.md                          # Redis-specific: data structures, pub/sub, persistence
    cdn.md                            # edge caching, invalidation, static delivery

  messaging/
    message-queues.md                 # Kafka, SQS, consumer groups, DLQ, backpressure
    event-driven-architecture.md      # pub/sub, choreography vs orchestration, batch/stream
    event-sourcing.md                 # append-only logs, hydration, audit trail
    cqrs.md                           # read/write separation, materialized views

  architecture/
    api-gateway.md                    # routing, auth, rate limiting, complexity budget
    microservices.md                  # decomposition, monolith-first, service discovery
    serverless.md                     # Lambda, vendor lock-in, FaaS patterns

  resilience/
    rate-limiting.md                  # fixed window, token bucket, sliding window
    circuit-breaker.md                # states, exponential backoff, jitter, thundering herd
    distributed-transactions.md       # 2PC, saga, compensating actions
    feature-flags.md                  # progressive releases, canary, kill switches

  security/
    authentication-authorization.md   # OAuth, JWT, RBAC, session management
    encryption.md                     # at rest, in transit, TLS
    api-security.md                   # input validation, DDoS protection, least privilege

  observability/
    monitoring.md                     # Prometheus, Grafana, golden signals, P99
    logging.md                        # ELK stack, structured logging, tracing

  api-design/
    rest-api.md                       # resource naming, methods, idempotency, status codes
    grpc.md                           # protobufs, binary serialization, streaming
    graphql.md                        # queries, mutations, N+1, data loaders
    real-time-protocols.md            # WebSockets, SSE, long polling, WebRTC, SFU

  patterns/
    fan-out.md                        # read vs write, hybrid, celebrity problem
    probabilistic-data-structures.md  # bloom filters, count-min sketch, HyperLogLog
    recommendation-engines.md         # candidate gen, ranking, vector search, HNSW
    video-streaming.md                # adaptive bitrate, HLS/DASH, chunking, transcoding
    search-and-indexing.md            # inverted index, Elasticsearch, full-text search
    geospatial-indexing.md            # geohashing, quadtrees, R-trees, proximity

  case-studies/
    twitter.md                        # hybrid fan-out, timeline, search
    ticketmaster.md                   # two-phase booking, distributed locks, waiting room
    tinder.md                         # geospatial, atomic swiping, bloom filters
    upi-payments.md                   # NPCI, PSP model, transaction integrity
    facebook-live-comments.md         # SSE, partitioned pub/sub, connection mapping
    whatsapp.md                       # WebSockets, inbox pattern, at-least-once delivery
    dropbox.md                        # chunking, delta sync, pre-signed URLs
    web-crawler.md                    # frontier, politeness, SQS, bandwidth math
    ad-click-aggregator.md            # Kappa/Lambda, Flink, logarithmic counting
    news-feed.md                      # hybrid fan-out, ranking, pre-computation

  meta/
    source-inventory.md
    concept-index.md
    source-map.md
```

**Changes from original taxonomy:**
- Renamed `fundamentals/scalability.md` -> `fundamentals/scaling-overview.md` to avoid collision with `scalability/` folder
- Renamed `fundamentals/reliability-availability.md` -> `fundamentals/availability-reliability.md` to avoid shadowing `resilience/` folder
- Renamed `reliability/` folder -> `resilience/` to eliminate name collision with the fundamentals file
- Split `event-sourcing-cqrs.md` into `event-sourcing.md` and `cqrs.md` (separable patterns)
- Added `patterns/search-and-indexing.md` (heavily covered across sources, critical for interviews)
- Added `patterns/geospatial-indexing.md` (covered by Alex Xu Vol 2 Ch 1, Acing, and YouTube reports)
- Renamed `horizontal-scaling.md` -> `autoscaling.md` (broader scope: HPA, traffic patterns, K8s scaling)
- Batch/stream processing covered as section within `event-driven-architecture.md`
- Service discovery covered as section within `microservices.md`
- WAL/CDC covered as section within `database-replication.md`

## Topic File Template

Every canonical topic file follows this exact structure:

```markdown
# <Topic Name>

## 1. Overview
Clear explanation of the concept.

## 2. Why It Matters
Why this exists in system design.

## 3. Core Concepts
Key components and terminology.

## 4. How It Works
Detailed explanation.

## 5. Architecture / Flow
(MUST include Mermaid diagram if applicable)

## 6. Types / Variants
Different approaches if applicable.

## 7. Use Cases
Real-world scenarios.

## 8. Tradeoffs
Pros vs cons.

## 9. Common Pitfalls
Mistakes engineers make.

## 10. Real-World Examples
Companies, systems, patterns.

## 11. Related Concepts
Cross-links to other docs.

## 12. Source Traceability
List source files used.
```

## Acceptance Criteria

- [ ] No duplicate concepts across files (verified by deduplication audit grep in Phase 3)
- [ ] All major system design topics covered (~57 canonical files)
- [ ] Every topic follows the 12-section template
- [ ] Mermaid diagrams present where applicable and syntax-valid
- [ ] `/docs/index.md` exists with learning path and navigation
- [ ] `/docs/meta/source-inventory.md` exists
- [ ] `/docs/meta/concept-index.md` exists
- [ ] `/docs/meta/source-map.md` exists
- [ ] `/docs/glossary.md` exists
- [ ] Cross-links between related topics (all relative links resolve to existing files)
- [ ] No raw summaries of individual source files
- [ ] Content is technically deep, not superficial
- [ ] Each topic combines multiple source explanations into one superior explanation
- [ ] Documentation navigable on GitHub (relative links, each folder has content, index at `/docs/`)
