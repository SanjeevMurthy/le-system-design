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

## Architecture

### Phase 0: PDF Extraction (Python Script)

**Script:** `/scripts/extract_pdfs.py`

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
(Extracted real-world examples, case studies, math)

## Tables & Comparisons
(Reconstructed comparison tables)

## Key Takeaways
(Final summaries, pro tips, tradeoff callouts found in text)
```

**Heuristics:**
- TOC bookmarks -> chapter boundaries (available for 4 of 5 PDFs)
- ALL CAPS or larger font lines -> section headers (fallback for Grokking)
- Lines containing "example", "case study", "scenario", "consider" -> tagged as examples
- Comparison patterns (vs., pros/cons, tradeoff) -> tagged as comparisons
- Bullet/numbered lists -> preserved structure
- Table detection via column-aligned text patterns

### Phase 1: Source Analysis (3 parallel agents)

Run after extraction completes. Three agents work simultaneously:

**Agent 1:** `/docs/meta/source-inventory.md`
- Catalogs all 14 original sources + extracted PDF chapters
- For each: type, scope, concepts covered

**Agent 2:** `/docs/meta/concept-index.md`
- Master deduplicated concept list from all sources
- Grouped into domains with aliases and cross-references
- Each concept is UNIQUE

**Agent 3:** `/docs/meta/source-map.md` + `/docs/glossary.md`
- Topic -> source file traceability mapping
- Glossary of all key terms with concise definitions

### Phase 2: Documentation Generation (3 parallel agents, 2 batches)

**Batch 1:**

| Agent | Folders | Files (~) |
|-------|---------|-----------|
| Agent 1 | fundamentals/ + scalability/ | 10 |
| Agent 2 | storage/ + caching/ | 11 |
| Agent 3 | messaging/ + architecture/ + reliability/ | 10 |

**Batch 2:**

| Agent | Folders | Files (~) |
|-------|---------|-----------|
| Agent 1 | security/ + observability/ + api-design/ (partial) | 7 |
| Agent 2 | api-design/ (partial) + patterns/ | 6 |
| Agent 3 | case-studies/ | 10 |

**Agent rules:**
- Each agent receives: the 12-section template, its assigned topic list, paths to ALL source files
- Each agent produces: complete canonical `.md` files with Mermaid diagrams, cross-links, source traceability
- No agent writes to another agent's files
- Cross-links use relative paths (e.g., `../caching/redis.md`)

### Phase 3: Finalization (main thread)

- Build `/docs/index.md` with learning path, topic categories, study order
- Cross-link verification pass
- Quality check against all acceptance criteria

## Concept Taxonomy (45 canonical topic files)

```
/docs/
  index.md
  glossary.md

  fundamentals/
    system-design-framework.md
    scalability.md
    reliability-availability.md
    cap-theorem.md
    networking-fundamentals.md
    back-of-envelope-estimation.md

  scalability/
    load-balancing.md
    horizontal-scaling.md
    consistent-hashing.md
    sharding.md

  storage/
    sql-databases.md
    nosql-databases.md
    object-storage.md
    database-indexing.md
    database-replication.md
    time-series-databases.md
    cassandra.md
    dynamodb.md

  caching/
    caching.md
    redis.md
    cdn.md

  messaging/
    message-queues.md
    event-driven-architecture.md
    event-sourcing-cqrs.md

  architecture/
    api-gateway.md
    microservices.md
    serverless.md

  reliability/
    rate-limiting.md
    circuit-breaker.md
    distributed-transactions.md
    feature-flags.md

  security/
    authentication-authorization.md
    encryption.md
    api-security.md

  observability/
    monitoring.md
    logging.md

  api-design/
    rest-api.md
    grpc.md
    graphql.md
    real-time-protocols.md

  patterns/
    fan-out.md
    probabilistic-data-structures.md
    recommendation-engines.md
    video-streaming.md

  case-studies/
    twitter.md
    ticketmaster.md
    tinder.md
    upi-payments.md
    facebook-live-comments.md
    whatsapp.md
    dropbox.md
    web-crawler.md
    ad-click-aggregator.md
    news-feed.md

  meta/
    source-inventory.md
    concept-index.md
    source-map.md
```

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

- [ ] No duplicate concepts across files
- [ ] All major system design topics covered (~45 canonical files)
- [ ] Every topic follows the 12-section template
- [ ] Mermaid diagrams present where applicable
- [ ] `/docs/index.md` exists with learning path and navigation
- [ ] `/docs/meta/source-inventory.md` exists
- [ ] `/docs/meta/concept-index.md` exists
- [ ] `/docs/meta/source-map.md` exists
- [ ] `/docs/glossary.md` exists
- [ ] Cross-links between related topics
- [ ] No raw summaries of individual source files
- [ ] Content is technically deep, not superficial
- [ ] Each topic combines multiple source explanations into one superior explanation
- [ ] Documentation navigable on GitHub
