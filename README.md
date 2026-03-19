# System Design Knowledge Base

A comprehensive, concept-driven knowledge base covering both **traditional system design** and **Generative AI system design** — built for architects, senior engineers, and interview preparation.

---

## What's Inside

### Traditional System Design (`docs/`)

**62 canonical topic files | 14 case studies | 246 glossary terms**

Covers the full stack of distributed systems: scalability, storage, caching, messaging, architecture, resilience, security, observability, API design, and advanced patterns.

**[→ Browse Traditional System Design](docs/index.md)**

| Category | Topics |
|----------|--------|
| **Fundamentals** | System design framework, scaling, CAP theorem, networking, estimation |
| **Storage** | SQL, NoSQL, object storage, indexing, replication, Cassandra, DynamoDB |
| **Caching** | Strategies, Redis, CDN |
| **Messaging** | Message queues, event-driven architecture, event sourcing, CQRS |
| **Architecture** | API gateway, microservices, serverless |
| **Resilience** | Rate limiting, circuit breaker, distributed transactions, feature flags |
| **Case Studies** | Twitter, Netflix, Uber, WhatsApp, Dropbox, Instagram, Google Maps, and more |

### Generative AI System Design (`docs/genai/`)

**58 canonical topic files | 6 case studies | 11 design patterns | 157 indexed concepts**

Covers the full GenAI system lifecycle: LLM foundations, inference infrastructure, RAG, agents, evaluation, safety, performance optimization, and production patterns.

**[→ Browse GenAI System Design](docs/genai/index.md)**

| Category | Topics |
|----------|--------|
| **Foundations** | Transformers, LLM landscape, tokenization, embeddings, multimodal, alignment |
| **LLM Architecture** | Model serving (vLLM, TGI, Triton), GPU compute, quantization, KV cache, parallelism |
| **Model Strategies** | Fine-tuning (LoRA/QLoRA), model selection, training infrastructure, distillation |
| **RAG** | Pipeline architectures, document ingestion, chunking, retrieval/reranking, GraphRAG |
| **Vector Search** | Vector databases, embedding models, ANN algorithms, hybrid search |
| **Prompt Engineering** | Design patterns, structured output, prompt injection, context management |
| **Agents** | Architecture patterns (ReAct, LATS), tool use/MCP, multi-agent, memory, code agents |
| **Orchestration** | LangChain, LlamaIndex, DSPy, Haystack, build-vs-buy |
| **Evaluation** | Eval frameworks (RAGAS), hallucination detection, LLM observability, benchmarks |
| **Safety** | Guardrails, PII protection, red teaming, AI governance |
| **Performance** | Latency optimization, semantic caching, cost optimization, model routing |
| **Case Studies** | Chatbot, copilot, enterprise search, voice AI, GenAI gateway, K8s for GenAI |

---

## Learning Path

### For Traditional System Design
Start with [Foundations](docs/fundamentals/system-design-framework.md) → Building Blocks → Communication → Reliability → Case Studies

### For GenAI System Design
Start with [Foundations](docs/genai/foundations/transformers.md) → LLM Architecture → RAG → Agents → Production Readiness → Case Studies

---

## Quick Reference

- [Traditional System Design Index](docs/index.md)
- [GenAI System Design Index](docs/genai/index.md)
- [Glossary (246 terms)](docs/glossary.md)
- [Cheat Sheet](docs/cheat-sheet.md)

---

## Repository Structure

```
docs/
├── fundamentals/       # System design foundations
├── scalability/        # Load balancing, sharding, autoscaling
├── storage/            # SQL, NoSQL, object storage, indexing
├── caching/            # Redis, CDN, caching strategies
├── messaging/          # Kafka, event sourcing, CQRS
├── architecture/       # Microservices, serverless, API gateway
├── resilience/         # Circuit breaker, rate limiting, transactions
├── security/           # Auth, encryption, API security
├── observability/      # Monitoring, logging
├── api-design/         # REST, gRPC, GraphQL, real-time
├── patterns/           # Fan-out, search, video streaming
├── case-studies/       # 14 real-world system designs
├── genai/              # Generative AI system design (58 files)
│   ├── foundations/    # Transformers, LLMs, embeddings
│   ├── llm-architecture/  # Serving, GPU, quantization
│   ├── rag/            # RAG pipelines, chunking, retrieval
│   ├── agents/         # Agent patterns, tool use, multi-agent
│   ├── evaluation/     # Eval frameworks, hallucination detection
│   ├── safety/         # Guardrails, PII, governance
│   ├── performance/    # Latency, caching, cost optimization
│   ├── case-studies/   # Chatbot, copilot, enterprise search
│   └── ...             # + vector-search, prompt-engineering, orchestration, patterns
└── meta/               # Concept index, source maps
```
