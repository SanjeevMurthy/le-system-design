# Design Spec: Generative AI System Design Knowledge Base

**Date**: 2026-03-20
**Status**: Approved (post-review revision)
**Scope**: Build a production-grade, research-driven GenAI system design documentation layer under `docs/genai/`

---

## 1. Problem Statement

The existing repository contains a comprehensive traditional system design knowledge base (62 topic files, 14 case studies, 153 glossary terms) but has zero coverage of Generative AI system design. The single GenAI source file (`source/GenAI/Kubernetes for Generative AI Solutions.pdf`) is insufficient. A complete GenAI knowledge base must be built primarily from deep research, covering foundations through production patterns.

## 2. Goals

- Cover the full GenAI system design lifecycle: foundations, inference, RAG, agents, evaluation, safety, production
- Include real-world examples from OpenAI, Google, Anthropic, Meta, Microsoft, Perplexity, GitHub Copilot, LangChain/LlamaIndex ecosystems
- Maintain architect-level depth — decision-making references, not tutorials
- Follow the existing repo convention: one concept = one canonical file, no duplication
- Cross-link with existing traditional system design docs where concepts overlap

## 3. Non-Goals

- Runnable code samples or tutorials
- Covering traditional system design topics already in `docs/` (cross-link instead)
- Model training from scratch (focus is on system design, not ML research)
- Vendor-specific deployment guides

## 4. Architecture Decision: Namespace Isolation

All GenAI docs live under `docs/genai/` to cleanly separate from the existing traditional system design knowledge base. This enables:
- Independent navigation and learning paths
- Clear ownership boundaries
- No naming collisions (both KBs have "patterns", "performance", "safety" concepts)
- Cross-linking between the two KBs via relative paths

## 5. Directory Structure

```
docs/genai/
├── index.md                          # GenAI learning roadmap + navigation
│
├── foundations/
│   ├── transformers.md               # Attention, MHA/GQA/MQA, positional encoding, Pre-LN/RMSNorm, MoE
│   ├── llm-landscape.md              # GPT, Claude, Gemini, LLaMA, Mistral, DeepSeek, Qwen
│   ├── tokenization.md               # BPE, SentencePiece, WordPiece — cost/context impact
│   ├── embeddings.md                 # word2vec → text-embedding-3, Matryoshka, quantized embeddings
│   ├── multimodal-models.md          # Vision-language, audio, video, document understanding
│   └── alignment.md                  # RLHF, DPO, Constitutional AI, SFT, pre-training vs post-training
│
├── llm-architecture/
│   ├── model-serving.md              # vLLM, TensorRT-LLM, TGI, Triton, SGLang
│   ├── gpu-compute.md                # A100/H100/H200/B200, memory bandwidth, tensor cores
│   ├── quantization.md               # INT8/INT4, GPTQ, AWQ, GGUF, FP8
│   ├── kv-cache.md                   # PagedAttention, continuous batching, prefix caching
│   ├── context-scaling.md            # RoPE interpolation, NTK-aware, YaRN, ring attention
│   └── model-parallelism.md          # Tensor, pipeline, data, expert parallelism, NVLink
│
├── model-strategies/
│   ├── fine-tuning.md                # Full FT, LoRA, QLoRA, adapters, prefix tuning
│   ├── model-selection.md            # Cost/latency/quality framework, decision tree
│   ├── training-infrastructure.md    # DeepSpeed ZeRO, FSDP, Megatron-LM, compute cost
│   └── distillation.md              # Teacher-student, synthetic data, knowledge transfer
│
├── rag/
│   ├── rag-pipeline.md               # Naive → Advanced → Modular → Agentic RAG
│   ├── document-ingestion.md         # Parsing, OCR, table extraction, metadata enrichment
│   ├── chunking.md                   # Fixed, semantic, recursive, parent-child, proposition-based
│   ├── retrieval-reranking.md        # Dense/sparse/hybrid retrieval, cross-encoder, query transformation
│   ├── graphrag.md                   # Knowledge graphs + RAG, Microsoft GraphRAG
│   └── multimodal-rag.md            # Image/table/PDF RAG, vision models for retrieval
│
├── vector-search/
│   ├── vector-databases.md           # Pinecone, Weaviate, Milvus, Qdrant, Chroma, pgvector
│   ├── embedding-models.md           # OpenAI, Cohere, BGE, E5, Nomic — MTEB benchmarks
│   ├── ann-algorithms.md             # HNSW, IVF, PQ, ScaNN, DiskANN
│   └── hybrid-search.md             # Vector + keyword fusion, RRF, SPLADE
│
├── prompt-engineering/
│   ├── prompt-patterns.md            # Zero/few-shot, CoT, ToT, self-consistency
│   ├── structured-output.md          # JSON mode, function calling, constrained decoding
│   ├── prompt-injection.md           # Direct/indirect injection, defense-in-depth
│   └── context-management.md        # Token counting, truncation, summarization
│
├── agents/
│   ├── agent-architecture.md         # ReAct, Plan-and-Execute, LATS, Reflexion
│   ├── tool-use.md                   # Function calling, MCP, tool ecosystems
│   ├── multi-agent.md                # AutoGen, CrewAI, LangGraph, orchestration patterns
│   ├── memory-systems.md            # Short-term, long-term, episodic, conversation history
│   └── code-agents.md               # GitHub Copilot, Cursor, Devin, Claude Code
│
├── orchestration/
│   ├── orchestration-frameworks.md   # LangChain, LlamaIndex, Semantic Kernel, Haystack, DSPy
│   ├── prompt-chaining.md            # Sequential, parallel, conditional, map-reduce
│   └── build-vs-buy.md              # Framework selection, anti-patterns, when to go custom
│
├── evaluation/
│   ├── eval-frameworks.md            # RAGAS, DeepEval, LangSmith, Braintrust
│   ├── hallucination-detection.md    # Detection methods, grounding, factual consistency
│   ├── llm-observability.md          # LangSmith, Langfuse, Arize Phoenix — tracing
│   └── benchmarks.md               # MMLU, HumanEval, MT-Bench, Chatbot Arena
│
├── safety/
│   ├── guardrails.md                 # Guardrails AI, NeMo Guardrails, Llama Guard
│   ├── pii-protection.md             # Detection, redaction, GDPR/CCPA compliance
│   ├── red-teaming.md               # Adversarial testing, jailbreak catalogs
│   └── ai-governance.md             # EU AI Act, NIST AI RMF, model cards, audit trails
│
├── performance/
│   ├── latency-optimization.md       # Streaming, speculative decoding, disaggregated serving
│   ├── semantic-caching.md           # GPTCache, exact vs semantic match, TTL
│   ├── cost-optimization.md          # Token economics, model cascading, batch inference
│   └── model-routing.md            # Cheap-first routing, confidence escalation, fallback chains
│
├── case-studies/
│   ├── chatbot-architecture.md       # Session management, streaming, multi-turn
│   ├── copilot-architecture.md       # IDE integration, contextual suggestions, FIM
│   ├── enterprise-search.md          # Semantic search + generation, ACL, multi-tenant RAG
│   ├── voice-ai.md                  # STT → LLM → TTS pipeline, real-time constraints
│   ├── genai-gateway.md             # LiteLLM, Portkey, unified API, multi-provider
│   └── kubernetes-genai.md          # GPU scheduling, node pools, inference serving on K8s
│
├── patterns/
│   ├── genai-design-patterns.md      # Gateway, circuit breaker for LLMs, retry with fallback
│   └── deployment-patterns.md       # Blue-green, canary, A/B, shadow deployment for models
│
└── meta/
    ├── genai-source-inventory.md     # Catalog of research sources
    ├── genai-concept-index.md        # Master deduplicated concept list
    └── genai-source-map.md          # Which sources informed each topic
```

**Total: 58 canonical topic files + 1 index + 3 meta artifacts = 62 files**

### Disposition of Research Outlines

The following intermediate research files were created during the brainstorming phase and exist in the repo:
- `docs/genai/00-genai-foundations-inference-model-strategies-outline.md`
- `source/GenAI/genai-domains-outline.md`

These files are **consumed as source material** during Phase 4 (Knowledge Extraction). After their content is distributed into canonical files, they are moved to `source/GenAI/drafts/` as archived reference material and excluded from the final `docs/genai/` directory.

## 6. Mandatory Template

Every canonical file follows this 12-section structure:

```markdown
# <Topic Name>

## 1. Overview
Brief definition, why this matters, 2-3 sentence positioning.

## 2. Where It Fits in GenAI Systems
How this topic connects to the broader pipeline. Short paragraph + positioning diagram.

## 3. Core Concepts
Technical meat — subtopics, definitions, mechanisms. Deepest section.

## 4. Architecture
MUST include at least one Mermaid diagram. System-level view of components and data flow.

## 5. Design Patterns
Named patterns with when-to-use guidance.

## 6. Implementation Approaches
Concrete approaches, tool/framework options, configuration examples (pseudocode, not runnable code).

## 7. Tradeoffs
Decision tables: Option A vs B vs C with axes like cost, latency, quality, complexity.

## 8. Failure Modes
What goes wrong and how to detect/mitigate. Production war stories where available.

## 9. Optimization Techniques
How to improve performance, reduce cost, increase quality.

## 10. Real-World Examples
MUST name companies/products. At least 3 per topic.
Format: Company — what they do — why it matters.

## 11. Related Topics
Cross-links to other GenAI files and traditional system design docs.

## 12. Source Traceability
Where the information came from (research, papers, documentation).
```

### Template Flexibility

- **Case study files** (`case-studies/`): May adapt sections 5-9 to fit a system design walkthrough structure (Requirements, Core Components, Data Flow, Key Design Decisions) while keeping sections 1-4 and 10-12 intact.
- **Pattern catalog files** (`patterns/`): May merge Sections 3 (Core Concepts) and 5 (Design Patterns) since the patterns ARE the core concepts.

## 7. Required Architectural Diagrams

Three mandatory diagrams must appear across the knowledge base:

### RAG Pipeline (in `rag/rag-pipeline.md`)
```
User Query → Query Transform → Retriever → Reranker → Context Assembly → LLM → Response
```

### Agent Loop (in `agents/agent-architecture.md`)
```
User → Planner → Tool Selection → Tool Execution → Observation → Memory → Planner (loop)
```

### LLM Inference Pipeline (in `llm-architecture/model-serving.md`)
```
Input → Tokenizer → Prefill → KV Cache → Decode (autoregressive) → Detokenizer → Output
```

Additional Mermaid diagrams are required in every file's Section 4 (Architecture).

## 8. Content Standards

- **Depth**: Architect-level decision-making references, not tutorials or textbook explanations
- **Diagrams**: Every file MUST have a Mermaid diagram in Section 4 (Architecture). Section 2 (Where It Fits) should include a Mermaid diagram where it adds clarity; a concise positioning paragraph suffices for topics where a diagram would be forced (e.g., governance, benchmarks)
- **Real-world examples**: Every file must reference at least 3 companies/products with specifics. For standards/methodology topics (e.g., `ai-governance.md`, `benchmarks.md`), reference 3 relevant industry frameworks, research papers, or standards bodies instead
- **No duplication**: Each concept has exactly one canonical home; other files cross-link
- **Cross-linking**: Each file links to both GenAI siblings and traditional system design docs
- **Research-driven**: Content must go beyond the `/source` directory; incorporate industry best practices, modern architectures, and real-world implementations

## 9. Learning Path

```
Stage 1: Foundations
  transformers → llm-landscape → tokenization → embeddings → multimodal-models → alignment

Stage 2: How LLMs Run
  model-serving → gpu-compute → quantization → kv-cache → context-scaling → model-parallelism

Stage 3: Model Customization
  model-selection → fine-tuning → distillation → training-infrastructure

Stage 4: RAG (the #1 enterprise pattern)
  rag-pipeline → document-ingestion → chunking → retrieval-reranking → graphrag → multimodal-rag

Stage 5: Vector Infrastructure
  embedding-models → vector-databases → ann-algorithms → hybrid-search

Stage 6: Prompt Engineering
  prompt-patterns → structured-output → context-management → prompt-injection

Stage 7: Agents
  agent-architecture → tool-use → memory-systems → multi-agent → code-agents

Stage 8: Orchestration
  orchestration-frameworks → prompt-chaining → build-vs-buy

Stage 9: Production Readiness
  eval-frameworks → hallucination-detection → benchmarks → llm-observability
  guardrails → pii-protection → red-teaming → ai-governance
  latency-optimization → semantic-caching → cost-optimization → model-routing

Stage 10: Case Studies & Patterns
  chatbot-architecture → copilot-architecture → enterprise-search → voice-ai
  genai-gateway → kubernetes-genai → genai-design-patterns → deployment-patterns
```

## 10. Deduplication Rules with Existing Docs

| Concept | Canonical Home (existing `docs/`) | GenAI files may... |
|---------|----------------------------------|-------------------|
| Vector search / ANN basics | `patterns/recommendation-engines.md` | Expand fully in `genai/vector-search/` (justified: GenAI needs dedicated depth) |
| Kubernetes / autoscaling | `scalability/autoscaling.md` | Cross-link; `kubernetes-genai.md` covers GPU-specific K8s only |
| Rate limiting | `resilience/rate-limiting.md` | Cross-link; `cost-optimization.md` covers LLM API quota specifics |
| Circuit breaker | `resilience/circuit-breaker.md` | Cross-link; `genai-design-patterns.md` covers LLM-specific retry/fallback |
| Caching strategies | `caching/caching.md` | Cross-link; `semantic-caching.md` covers embedding-based cache only |
| Search & indexing | `patterns/search-and-indexing.md` | Cross-link; `hybrid-search.md` covers vector+keyword fusion |
| Encryption / TLS | `security/encryption.md` | Cross-link only; GenAI safety covers AI-specific concerns |
| Monitoring / Prometheus | `observability/monitoring.md` | Cross-link; `llm-observability.md` covers LLM-specific tracing only |
| Streaming / SSE / WebSockets | `api-design/real-time-protocols.md` | Cross-link; `latency-optimization.md` covers LLM streaming specifics only |
| API Gateway patterns | `architecture/api-gateway.md` | Cross-link; `genai-gateway.md` covers LLM-specific multi-provider routing |
| Load balancing | `scalability/load-balancing.md` | Cross-link; `model-routing.md` covers model-level routing/fallback only |
| Feature flags / canary | `resilience/feature-flags.md` | Cross-link; `deployment-patterns.md` covers model-specific A/B and canary |
| Database replication / CDC | `storage/database-replication.md` | Cross-link; `document-ingestion.md` covers CDC for doc indexing pipelines |
| Distributed transactions / Saga | `resilience/distributed-transactions.md` | Cross-link only; agent compensation patterns reference but don't re-explain |

## 11. Meta Artifacts

### `docs/genai/index.md`
- Learning roadmap (10 stages)
- Topic navigation table with all 58 files
- Quick reference links to glossary, concept index, cheat sheet (if created)
- Stats line (e.g., "58 canonical topic files | 6 case studies | X glossary terms")

### `docs/genai/meta/genai-concept-index.md`
- Every concept appears ONCE, mapped to its canonical file
- Content boundaries table (same format as existing `docs/meta/concept-index.md`)
- Aliases and related concepts for each entry

### `docs/genai/meta/genai-source-inventory.md`
- Catalog of all research sources used (papers, documentation, blog posts)
- Organized by domain

### `docs/genai/meta/genai-source-map.md`
- Which research sources informed each topic file
- Coverage matrix

### Glossary Expansion
- Add GenAI terms to the existing `docs/glossary.md` (do NOT create a separate glossary)
- Estimated ~100-150 new terms

### Existing Concept Index Update
- Update `docs/meta/concept-index.md` Content Boundaries table to acknowledge the `docs/genai/` namespace
- Add cross-references for concepts that now have expanded GenAI coverage (e.g., vector search, embeddings)
- Ensure the master deduplication authority reflects both knowledge bases

### Root Index Update
- Update `docs/index.md` to add a Stage 7 or dedicated section linking to `docs/genai/index.md`

## 12. Execution Model

Follow the 8-phase approach from the prompt:

1. **Phase 1 — Source + Research Analysis**: Scan `/source/GenAI/`, perform deep research, output `genai-source-inventory.md`
2. **Phase 2 — Concept Taxonomy**: Build `genai-concept-index.md` with all concepts, aliases, definitions
3. **Phase 3 — Document Structure**: Create all directories and `doc-structure` reference
4. **Phase 4 — Knowledge Extraction**: For each concept, combine repo sources + research into working drafts (ephemeral — not committed, used only as input for Phase 5)
5. **Phase 5 — Final Documentation**: Write all 58 canonical files using the mandatory template
6. **Phase 6 — Index**: Create `docs/genai/index.md` with learning roadmap
7. **Phase 7 — Source Map**: Create `genai-source-map.md`
8. **Phase 8 — Glossary**: Expand `docs/glossary.md` with ~100-150 GenAI terms
9. **Phase 9 — Cross-link Validation**: Final pass to verify all cross-links resolve, update `docs/meta/concept-index.md`, archive research outlines to `source/GenAI/drafts/`

### Parallelization Strategy
- Use up to 3 parallel agents per batch
- Group files by domain for parallel writing (e.g., all `foundations/` files in one batch)
- Each agent writes 3-5 files per invocation
- Estimated ~10-12 batches to complete all 58 files
- Cross-links to not-yet-written files should use the planned file path; validated in Phase 9

## 13. Acceptance Criteria

- [ ] Covers full GenAI system lifecycle (foundations → production)
- [ ] Includes real-world systems (OpenAI, Google, Anthropic, Meta, Microsoft, etc.)
- [ ] No duplication within GenAI docs or with existing traditional system design docs
- [ ] Every file has Mermaid diagram in Section 4; Section 2 diagrams where they add clarity
- [ ] Fully navigable via `docs/genai/index.md`
- [ ] Deep, production-level insights (architect-level, not tutorial-level)
- [ ] Cross-linked with existing `docs/` where concepts overlap
- [ ] All 58 canonical files follow the mandatory 12-section template (case studies and pattern catalogs may adapt sections 5-9)
- [ ] Glossary expanded with GenAI terms
- [ ] Meta artifacts complete (concept index, source inventory, source map)
- [ ] Existing `docs/meta/concept-index.md` updated with GenAI cross-references
- [ ] Research outline files archived to `source/GenAI/drafts/`
- [ ] All cross-links validated (Phase 9)
