# System Design Knowledge Base

A comprehensive, concept-driven knowledge base covering **traditional system design**, **Generative AI system design**, and **Kubernetes system design** — built for architects, senior engineers, and interview preparation.

---

## What's Inside

### Traditional System Design (`docs/traditional-system-design/`)

**62 canonical topic files | 14 case studies | 246 glossary terms**

Covers the full stack of distributed systems: scalability, storage, caching, messaging, architecture, resilience, security, observability, API design, and advanced patterns.

**[→ Browse Traditional System Design](docs/traditional-system-design/index.md)**

| Category | Topics |
|----------|--------|
| **Fundamentals** | System design framework, scaling, CAP theorem, networking, estimation |
| **Storage** | SQL, NoSQL, object storage, indexing, replication, Cassandra, DynamoDB |
| **Caching** | Strategies, Redis, CDN |
| **Messaging** | Message queues, event-driven architecture, event sourcing, CQRS |
| **Architecture** | API gateway, microservices, serverless |
| **Resilience** | Rate limiting, circuit breaker, distributed transactions, feature flags |
| **Case Studies** | Twitter, Netflix, Uber, WhatsApp, Dropbox, Instagram, Google Maps, and more |

### Generative AI System Design (`docs/genai-system-design/`)

**58 canonical topic files | 6 case studies | 11 design patterns | 157 indexed concepts**

Covers the full GenAI system lifecycle: LLM foundations, inference infrastructure, RAG, agents, evaluation, safety, performance optimization, and production patterns.

**[→ Browse GenAI System Design](docs/genai-system-design/index.md)**

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

### Kubernetes System Design (`docs/kubernetes-system-design/`)

**64 canonical topic files | 9 case studies | 5 design patterns**

Covers the full Kubernetes lifecycle: cluster architecture, workload design, networking, storage, scaling, security, deployment strategies, observability, platform engineering, and production operations.

**[→ Browse Kubernetes System Design](docs/kubernetes-system-design/index.md)**

| Category | Topics |
|----------|--------|
| **Foundations** | Kubernetes architecture, control plane, API server & etcd, container runtimes, networking model |
| **Cluster Design** | Cluster topology, node pools, multi-cluster, cloud vs bare-metal |
| **Workload Design** | Pod patterns, deployments, StatefulSets, jobs, GPU workloads |
| **Networking** | Services, Gateway API, service mesh, DNS, network policies |
| **Storage** | PV/PVC, CSI drivers, stateful data patterns, model delivery |
| **Scaling** | HPA, VPA, Karpenter, KEDA, GPU autoscaling |
| **Security** | RBAC, pod security, supply chain, secrets, runtime security |
| **Deployment** | GitOps, Helm, CI/CD pipelines, progressive delivery |
| **Observability** | Monitoring, logging, cost management, SLOs |
| **Platform** | Internal developer platforms, multi-tenancy, self-service, DX |
| **Operations** | Upgrades, disaster recovery, troubleshooting, cost optimization |
| **Patterns** | Operator, sidecar, CRD, anti-patterns, migration strategies |
| **Case Studies** | Spotify, Airbnb, Pinterest, multi-tenant, migration, stateful, GPU, edge, enterprise |

---

## Learning Path

### For Traditional System Design
Start with [Foundations](docs/traditional-system-design/01-fundamentals/system-design-framework.md) → Building Blocks → Communication → Reliability → Case Studies

### For GenAI System Design
Start with [Foundations](docs/genai-system-design/01-foundations/transformers.md) → LLM Architecture → RAG → Agents → Production Readiness → Case Studies

### For Kubernetes System Design
Start with [Foundations](docs/kubernetes-system-design/01-foundations/01-kubernetes-architecture.md) → Cluster Design → Workload Design → Networking → Security → Operations → Case Studies

---

## Quick Reference

- [Traditional System Design Index](docs/traditional-system-design/index.md)
- [GenAI System Design Index](docs/genai-system-design/index.md)
- [Kubernetes System Design Index](docs/kubernetes-system-design/index.md)
- [Glossary (246 terms)](docs/glossary.md)
- [Cheat Sheet](docs/cheat-sheet.md)

---

## Repository Structure

```
docs/
├── traditional-system-design/
│   ├── 01-fundamentals/       # System design foundations
│   ├── 02-scalability/        # Load balancing, sharding, autoscaling
│   ├── 03-storage/            # SQL, NoSQL, object storage, indexing
│   ├── 04-caching/            # Redis, CDN, caching strategies
│   ├── 05-messaging/          # Kafka, event sourcing, CQRS
│   ├── 06-architecture/       # Microservices, serverless, API gateway
│   ├── 07-api-design/         # REST, gRPC, GraphQL, real-time
│   ├── 08-resilience/         # Circuit breaker, rate limiting, transactions
│   ├── 09-security/           # Auth, encryption, API security
│   ├── 10-observability/      # Monitoring, logging
│   ├── 11-patterns/           # Fan-out, search, video streaming
│   ├── 12-case-studies/       # 14 real-world system designs
│   └── meta/
├── genai-system-design/
│   ├── 01-foundations/        # Transformers, LLMs, embeddings
│   ├── 02-llm-architecture/   # Serving, GPU, quantization
│   ├── 03-model-strategies/   # Fine-tuning, model selection
│   ├── 04-rag/                # RAG pipelines, chunking, retrieval
│   ├── 05-vector-search/      # Vector databases, ANN algorithms
│   ├── 06-prompt-engineering/  # Prompt design, structured output
│   ├── 07-agents/             # Agent patterns, tool use, multi-agent
│   ├── 08-orchestration/      # LangChain, LlamaIndex, DSPy
│   ├── 09-evaluation/         # Eval frameworks, hallucination detection
│   ├── 10-safety/             # Guardrails, PII, governance
│   ├── 11-performance/        # Latency, caching, cost optimization
│   ├── 12-patterns/           # Design patterns
│   ├── 13-case-studies/       # Chatbot, copilot, enterprise search
│   └── meta/
├── kubernetes-system-design/
│   ├── 01-foundations/        # Architecture, control plane, etcd, runtimes
│   ├── 02-cluster-design/     # Topology, node pools, multi-cluster
│   ├── 03-workload-design/    # Pods, deployments, StatefulSets, jobs
│   ├── 04-networking-design/  # Services, Gateway API, service mesh
│   ├── 05-storage-design/     # PV/PVC, CSI, stateful data patterns
│   ├── 06-scaling-design/     # HPA, VPA, Karpenter, KEDA
│   ├── 07-security-design/    # RBAC, policies, supply chain, secrets
│   ├── 08-deployment-design/  # GitOps, Helm, CI/CD, progressive delivery
│   ├── 09-observability-design/ # Monitoring, logging, cost, SLOs
│   ├── 10-platform-design/    # IDP, multi-tenancy, self-service
│   ├── 11-operations/         # Upgrades, DR, troubleshooting
│   ├── 12-patterns/           # Operator, sidecar, CRD patterns
│   ├── 13-case-studies/       # Spotify, Airbnb, Pinterest, and more
│   └── meta/
├── glossary.md
└── cheat-sheet.md
```
