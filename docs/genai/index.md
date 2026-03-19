# Generative AI System Design Knowledge Base

A comprehensive, research-driven knowledge base for Generative AI system design -- from transformer fundamentals through production deployment. Every topic exists in exactly one canonical file -- no duplication, full cross-linking.

**58 canonical topic files | 6 case studies | 11 design patterns | [Traditional System Design →](../index.md)**

---

## Learning Path

### Stage 1: Foundations

Start here to build the conceptual foundation for all GenAI system design work.

1. [Transformer Architecture](foundations/transformers.md) — self-attention, multi-head attention, encoder/decoder, positional encoding
2. [Large Language Model Landscape](foundations/llm-landscape.md) — frontier model families, pricing, capabilities, selection criteria
3. [Tokenization](foundations/tokenization.md) — BPE, SentencePiece, vocabulary design, cost and context implications
4. [Embeddings](foundations/embeddings.md) — dense vector representations, distance metrics, dimensionality tradeoffs
5. [Multimodal Models](foundations/multimodal-models.md) — vision-language architectures, native vs bolt-on multimodality, cross-modal reasoning
6. [Alignment](foundations/alignment.md) — pre-training vs post-training, RLHF, DPO, safety tuning, behavioral steering

### Stage 2: How LLMs Run

The infrastructure and mechanics of serving models at scale.

1. [Model Serving Infrastructure](llm-architecture/model-serving.md) — inference runtimes, continuous batching, streaming, deployment topologies
2. [GPU Compute](llm-architecture/gpu-compute.md) — GPU selection, memory hierarchy, utilization, cost drivers
3. [Quantization](llm-architecture/quantization.md) — INT4/INT8/FP8, GPTQ, AWQ, accuracy-memory tradeoffs
4. [KV Cache Management](llm-architecture/kv-cache.md) — PagedAttention, memory allocation, cache eviction strategies
5. [Context Window Scaling](llm-architecture/context-scaling.md) — RoPE, ALiBi, ring attention, long-context architectures
6. [Model Parallelism](llm-architecture/model-parallelism.md) — tensor, pipeline, and data parallelism, multi-GPU serving

### Stage 3: Model Customization

Adapting foundation models to specific domains and tasks.

1. [Model Selection Criteria](model-strategies/model-selection.md) — cost-quality-latency Pareto frontier, evaluation methodology, vendor risk
2. [Fine-Tuning Approaches](model-strategies/fine-tuning.md) — full fine-tuning, LoRA, QLoRA, SFT, data requirements
3. [Model Distillation](model-strategies/distillation.md) — teacher-student training, knowledge transfer, 5-100x size reduction
4. [Training Infrastructure](model-strategies/training-infrastructure.md) — distributed training, fault tolerance, GPU clusters, checkpointing

### Stage 4: Retrieval-Augmented Generation (RAG)

Grounding LLM outputs in external knowledge.

1. [RAG Pipeline Architecture](rag/rag-pipeline.md) — end-to-end RAG design, indexing, retrieval, generation, evaluation
2. [Document Ingestion Pipelines](rag/document-ingestion.md) — parsing, extraction, cleaning, metadata handling across document types
3. [Chunking Strategies](rag/chunking.md) — fixed-size, semantic, recursive, parent-child, overlap tuning
4. [Retrieval and Reranking](rag/retrieval-reranking.md) — two-stage retrieval, cross-encoders, ColBERT, score fusion
5. [GraphRAG](rag/graphrag.md) — knowledge graphs + RAG, multi-hop reasoning, entity extraction, community detection
6. [Multimodal RAG](rag/multimodal-rag.md) — image/table/PDF retrieval, multimodal embeddings, vision-language generation

### Stage 5: Vector Infrastructure

The storage and search layer for semantic retrieval.

1. [Embedding Models](vector-search/embedding-models.md) — model selection, contrastive training, Matryoshka embeddings, benchmarking
2. [Vector Databases](vector-search/vector-databases.md) — Pinecone, Weaviate, Qdrant, Milvus, architecture and tradeoffs
3. [ANN Algorithms](vector-search/ann-algorithms.md) — HNSW, IVF, PQ, ScaNN, recall-latency-memory tradeoffs
4. [Hybrid Search](vector-search/hybrid-search.md) — dense + sparse fusion, RRF, SPLADE, keyword-semantic combination

### Stage 6: Prompt Engineering

Controlling LLM behavior through input design.

1. [Prompt Design Patterns](prompt-engineering/prompt-patterns.md) — few-shot, chain-of-thought, ReAct, system prompts, structured templates
2. [Structured Output](prompt-engineering/structured-output.md) — JSON mode, function calling schemas, constrained decoding, validation
3. [Context Window Management](prompt-engineering/context-management.md) — token budgeting, priority-based allocation, compression strategies
4. [Prompt Injection](prompt-engineering/prompt-injection.md) — attack taxonomy, direct/indirect injection, defense-in-depth strategies

### Stage 7: Agents

Autonomous multi-step reasoning systems.

1. [Agent Architecture Patterns](agents/agent-architecture.md) — ReAct loops, plan-and-execute, state machines, control flow design
2. [Tool Use and Function Calling](agents/tool-use.md) — function schemas, execution sandboxing, error recovery, MCP
3. [Agent Memory Systems](agents/memory-systems.md) — working, episodic, and semantic memory, cross-session persistence
4. [Multi-Agent Systems](agents/multi-agent.md) — role specialization, coordination protocols, adversarial self-critique
5. [Code Generation Agents](agents/code-agents.md) — IDE integration, codebase context, test-driven iteration, copilot architectures

### Stage 8: Orchestration

Composing LLM calls into production workflows.

1. [Orchestration Frameworks](orchestration/orchestration-frameworks.md) — LangChain, LlamaIndex, Semantic Kernel, Haystack, DSPy comparison
2. [Prompt Chaining and Composition](orchestration/prompt-chaining.md) — sequential decomposition, branching, parallel chains, error handling
3. [Build vs Buy](orchestration/build-vs-buy.md) — framework adoption tradeoffs, when to use raw API calls vs orchestration layers

### Stage 9: Production Readiness

Making GenAI systems reliable, safe, observable, and cost-effective.

**Evaluation & Observability:**
1. [Evaluation Frameworks](evaluation/eval-frameworks.md) — offline/online eval, LLM-as-judge, human-in-the-loop, regression testing
2. [Hallucination Detection](evaluation/hallucination-detection.md) — faithfulness scoring, citation verification, groundedness checks
3. [LLM Benchmarks](evaluation/benchmarks.md) — MMLU, HumanEval, MTBENCH, benchmark limitations, custom eval suites
4. [LLM Observability](evaluation/llm-observability.md) — token-level tracing, cost attribution, quality monitoring, prompt versioning

**Safety & Governance:**
5. [Guardrails](safety/guardrails.md) — input/output validation, content filtering, NeMo Guardrails, deterministic enforcement
6. [PII Protection](safety/pii-protection.md) — detection, masking, anonymization across the GenAI pipeline
7. [Red Teaming](safety/red-teaming.md) — adversarial testing, attack taxonomies, automated red teaming, jailbreak defense
8. [AI Governance](safety/ai-governance.md) — model cards, audit trails, bias testing, regulatory compliance (EU AI Act, NIST)

**Performance & Cost:**
9. [Latency Optimization](performance/latency-optimization.md) — prefill/decode pipeline, speculative decoding, streaming, batching strategies
10. [Semantic Caching](performance/semantic-caching.md) — vector-based cache lookup, similarity thresholds, cache invalidation
11. [Cost Optimization](performance/cost-optimization.md) — token economics, prompt compression, tiered models, TCO analysis
12. [Model Routing](performance/model-routing.md) — dynamic model selection, cascading, cost-quality routing, fallback chains

### Stage 10: Case Studies & Patterns

Real-world GenAI system designs and reusable architectural patterns.

| Case Study | Key Patterns | Difficulty |
|-----------|-------------|-----------|
| [Chatbot Architecture](case-studies/chatbot-architecture.md) | Session management, streaming, guardrails, conversation history | Medium |
| [Copilot Architecture](case-studies/copilot-architecture.md) | IDE integration, codebase context, inline completion, agentic editing | Hard |
| [Enterprise Search](case-studies/enterprise-search.md) | Multi-source ingestion, hybrid retrieval, access control, citations | Hard |
| [Voice AI Agents](case-studies/voice-ai.md) | STT/TTS pipeline, real-time streaming, conversational latency budget | Hard |
| [GenAI Gateway](case-studies/genai-gateway.md) | Multi-provider routing, failover, cost tracking, unified API | Medium |
| [Kubernetes for GenAI](case-studies/kubernetes-genai.md) | GPU scheduling, model lifecycle, autoscaling, multi-tenancy | Hard |

| Pattern Reference | Scope |
|------------------|-------|
| [GenAI Design Patterns](patterns/genai-design-patterns.md) | 11 reusable patterns: fallback, guardrail, cache-aside, fan-out, gateway, and more |
| [Deployment Patterns](patterns/deployment-patterns.md) | Shadow deployment, canary with eval, blue-green for models, A/B testing |

---

## Quick Reference

- [Glossary](../glossary.md) — system design and GenAI terms defined
- [Concept Index](../meta/concept-index.md) — master deduplicated concept list
- [Source Inventory](../meta/source-inventory.md) — catalog of all source materials
- [Source Traceability Map](../meta/source-map.md) — which sources informed each topic
- [Traditional System Design →](../index.md) — the companion knowledge base for classical distributed systems
