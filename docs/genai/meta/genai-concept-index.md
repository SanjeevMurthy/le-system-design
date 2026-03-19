# GenAI Concept Index

Master deduplicated concept list across all 58 topic files. Each concept has exactly one canonical home. Other files may reference but must not re-explain in depth.

---

## Content Boundaries (Deduplication Rules)

| Concept | Canonical File | Other files may only... |
|---------|---------------|------------------------|
| Self-attention mechanism | foundations/transformers | Reference Q/K/V computation; not re-derive the math |
| KV cache | llm-architecture/kv-cache | Mention KV cache size impact; not explain PagedAttention internals |
| Tokenization algorithms (BPE, WordPiece, Unigram) | foundations/tokenization | Reference token counts; not explain merge rules |
| Embedding models and training | foundations/embeddings | Reference embedding dimensions; not explain contrastive training |
| RLHF / DPO pipeline | foundations/alignment | Mention alignment approach; not re-explain the loss function |
| RAG pipeline stages | rag/rag-pipeline | Reference "RAG approach"; not re-explain naive vs advanced RAG |
| LoRA / QLoRA mechanics | model-strategies/fine-tuning | Reference "LoRA fine-tuning"; not re-explain low-rank decomposition |
| GPTQ / AWQ / SmoothQuant | llm-architecture/quantization | Reference quantization level; not re-explain calibration process |
| Prompt injection attack types | prompt-engineering/prompt-injection | Reference injection risk; not catalog attack types |
| Guardrail frameworks | safety/guardrails | Reference guardrail layer; not re-explain NeMo Guardrails architecture |
| Vector database selection | vector-search/vector-databases | Reference vector store; not compare Pinecone vs Qdrant |
| Model routing strategies | performance/model-routing | Reference routing concept; not re-explain FrugalGPT cascading |
| Agent loop patterns (ReAct, LATS) | agents/agent-architecture | Reference agent pattern; not re-explain reasoning loops |
| GraphRAG pipeline | rag/graphrag | Reference graph-based retrieval; not re-explain community summarization |
| Hallucination detection methods | evaluation/hallucination-detection | Reference hallucination risk; not re-explain claim decomposition |
| PII detection and anonymization | safety/pii-protection | Reference PII handling; not re-explain Presidio architecture |
| EU AI Act / NIST AI RMF | safety/ai-governance | Reference regulatory requirements; not summarize act provisions |
| GPU architecture (A100/H100) | llm-architecture/gpu-compute | Reference GPU requirements; not re-explain tensor core architecture |
| Speculative decoding | performance/latency-optimization | Reference latency technique; not re-explain draft-verify mechanism |
| Semantic caching | performance/semantic-caching | Reference caching approach; not re-explain GPTCache internals |

---

## Foundations

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Transformer architecture | foundations/transformers | Transformer model, attention mechanism | Self-attention, MHA, FFN, layer norm |
| Self-attention | foundations/transformers | Scaled dot-product attention | Q/K/V projections, causal masking |
| Multi-Head Attention (MHA) | foundations/transformers | MHA | GQA, MQA, KV cache |
| Grouped-Query Attention (GQA) | foundations/transformers | GQA | MHA, MQA, KV heads |
| Multi-Query Attention (MQA) | foundations/transformers | MQA | MHA, GQA |
| Rotary Position Embedding (RoPE) | foundations/transformers | RoPE, rotary encoding | Position Interpolation, ALiBi, NTK scaling |
| ALiBi positional encoding | foundations/transformers | Attention with Linear Biases | RoPE, positional encoding |
| SwiGLU activation | foundations/transformers | GLU variants | FFN, GELU, ReLU |
| RMSNorm | foundations/transformers | Root Mean Square Normalization | LayerNorm, Pre-LN, Post-LN |
| Mixture of Experts (MoE) | foundations/transformers | Sparse MoE, expert routing | Mixtral, expert parallelism, load balancing |
| Feed-forward network (FFN) | foundations/transformers | MLP layer, position-wise FFN | SwiGLU, MoE, d_ff |
| Causal masking | foundations/transformers | Autoregressive mask | Decoder-only, next-token prediction |
| Encoder-decoder architecture | foundations/transformers | Seq2seq | T5, Whisper, cross-attention |
| Decoder-only architecture | foundations/transformers | Autoregressive LM | GPT, LLaMA, Claude |
| LLM model families | foundations/llm-landscape | GPT, Claude, Gemini, LLaMA, Mistral | Model selection, pricing, context windows |
| GPT family (OpenAI) | foundations/llm-landscape | GPT-4o, GPT-4, o1, o3, GPT-4o mini | Reasoning models, extended thinking |
| Claude family (Anthropic) | foundations/llm-landscape | Claude 4.6, Claude Sonnet, Haiku | Constitutional AI, prompt caching |
| Gemini family (Google) | foundations/llm-landscape | Gemini Pro, Flash, Ultra | Native multimodal, TPU, long context |
| LLaMA family (Meta) | foundations/llm-landscape | LLaMA 3.1, LLaMA 2 | Open-weight, community fine-tunes |
| Mistral/Mixtral family | foundations/llm-landscape | Mistral 7B, Mixtral 8x7B | SWA, MoE, Apache 2.0 |
| DeepSeek models | foundations/llm-landscape | DeepSeek-V3, DeepSeek-R1 | MLA, cost-efficient training |
| Closed vs open-weight tradeoff | foundations/llm-landscape | Proprietary vs open-source | Data privacy, fine-tuning, vendor lock-in |
| Byte-Pair Encoding (BPE) | foundations/tokenization | BPE, BBPE, byte-level BPE | Merge rules, vocabulary, tokenizer |
| SentencePiece | foundations/tokenization | SP tokenizer | BPE, Unigram, language-agnostic |
| WordPiece | foundations/tokenization | WP | BERT tokenizer, ## prefix |
| Vocabulary size tradeoffs | foundations/tokenization | Vocab design | Multilingual efficiency, embedding table |
| Special tokens | foundations/tokenization | BOS, EOS, PAD, chat templates | Instruction formatting, role markers |
| Multilingual tokenization efficiency | foundations/tokenization | Fertility rate | Token inflation, non-English cost |
| Text embeddings | foundations/embeddings | Sentence embeddings, vector representations | Bi-encoder, MTEB, similarity metrics |
| Matryoshka Representation Learning | foundations/embeddings | MRL, variable-dimension embeddings | Dimension truncation, storage optimization |
| Embedding quantization | foundations/embeddings | Binary quantization, INT8 quantization | Product quantization, compression |
| Cosine similarity | foundations/embeddings | Cosine distance | Dot product, L2 distance, similarity metrics |
| Bi-encoder vs cross-encoder | foundations/embeddings | Two-stage retrieval | Reranking, ColBERT, late interaction |
| MTEB benchmark | foundations/embeddings | Massive Text Embedding Benchmark | Embedding evaluation, BEIR |
| ColBERT | foundations/embeddings | Late interaction | Multi-vector retrieval, MaxSim |
| Instruction-tuned embeddings | foundations/embeddings | Task-prefix embeddings | E5, BGE, instruction prefix |
| Vision-language models (VLMs) | foundations/multimodal-models | VLM, multimodal LLM | CLIP, LLaVA, GPT-4V, visual encoder |
| CLIP / SigLIP | foundations/multimodal-models | Contrastive image-text models | Multimodal embeddings, zero-shot classification |
| Whisper ASR | foundations/multimodal-models | Automatic speech recognition | STT, encoder-decoder, audio processing |
| Native vs bolt-on multimodal | foundations/multimodal-models | End-to-end vs bridged multimodal | Gemini, GPT-4o vs LLaVA, InternVL |
| Document understanding (VLM-based) | foundations/multimodal-models | Visual document AI | OCR replacement, LayoutLM, Donut |
| RLHF | foundations/alignment | Reinforcement Learning from Human Feedback | PPO, reward model, preference data |
| DPO | foundations/alignment | Direct Preference Optimization | Preference pairs, reference model |
| Constitutional AI (CAI) | foundations/alignment | RLAIF, principle-based alignment | Anthropic, self-critique |
| SFT (Supervised Fine-Tuning) | foundations/alignment | Instruction tuning | Alpaca, Self-Instruct, Evol-Instruct |
| Extended thinking / reasoning models | foundations/alignment | Chain-of-thought at inference, o1, o3 | Thinking tokens, process reward models |
| Alignment tax | foundations/alignment | Safety-helpfulness tradeoff | False refusals, over-cautious behavior |
| Synthetic data for alignment | foundations/alignment | Self-Instruct, Evol-Instruct, RLAIF | UltraFeedback, UltraChat |

---

## LLM Architecture

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Model serving | llm-architecture/model-serving | LLM inference serving | vLLM, TGI, TensorRT-LLM, SGLang |
| Continuous batching | llm-architecture/model-serving | Iteration-level scheduling, Orca | Static batching, throughput |
| Speculative decoding | llm-architecture/model-serving | Draft-verify, Medusa, EAGLE | Latency optimization, decode speedup |
| GPU compute for AI | llm-architecture/gpu-compute | A100, H100, H200, B200, TPU | Tensor cores, HBM, NVLink, NVSwitch |
| Roofline model | llm-architecture/gpu-compute | Compute vs memory bound | Arithmetic intensity, bandwidth |
| Multi-Instance GPU (MIG) | llm-architecture/gpu-compute | GPU partitioning | A100 MIG, resource isolation |
| Quantization techniques | llm-architecture/quantization | GPTQ, AWQ, SmoothQuant, FP8, INT4/INT8 | Weight-only, W8A8, calibration |
| GGUF format | llm-architecture/quantization | GGML, K-quants | llama.cpp, edge deployment |
| KV cache management | llm-architecture/kv-cache | Key-value cache | PagedAttention, cache eviction, prefix caching |
| PagedAttention | llm-architecture/kv-cache | vLLM paging | Virtual memory for KV cache, fragmentation |
| Prefix caching | llm-architecture/kv-cache | RadixAttention, automatic prefix caching | SGLang, prompt caching, KV reuse |
| Attention sinks / StreamingLLM | llm-architecture/kv-cache | Streaming KV cache | Token eviction, infinite context |
| Context scaling | llm-architecture/context-scaling | Context window extension | Position Interpolation, YaRN, NTK scaling |
| Lost-in-the-middle | llm-architecture/context-scaling | Positional bias in long context | Context placement, retrieval |
| Ring Attention | llm-architecture/context-scaling | Distributed sequence attention | Sequence parallelism, infinite context |
| Tensor parallelism | llm-architecture/model-parallelism | TP, Megatron-LM | Intra-node, AllReduce, NVLink |
| Pipeline parallelism | llm-architecture/model-parallelism | PP, GPipe, PipeDream | Inter-node, micro-batches, pipeline bubbles |
| Expert parallelism | llm-architecture/model-parallelism | EP | MoE serving, all-to-all communication |
| Data parallelism / FSDP / ZeRO | llm-architecture/model-parallelism | DP, FSDP, DeepSpeed ZeRO | Gradient sharding, training distribution |
| Disaggregated serving | llm-architecture/model-parallelism | Splitwise, DistServe, prefill-decode separation | Prefill/decode optimization |

---

## Model Strategies

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| LoRA | model-strategies/fine-tuning | Low-Rank Adaptation | QLoRA, DoRA, adapter tuning |
| QLoRA | model-strategies/fine-tuning | Quantized LoRA | NF4, double quantization |
| Full fine-tuning vs PEFT | model-strategies/fine-tuning | Parameter-efficient fine-tuning | LoRA, prefix tuning, adapters |
| Fine-tuning data strategies | model-strategies/fine-tuning | SFT data, domain adaptation | LIMA, data quality vs quantity |
| Model selection framework | model-strategies/model-selection | Model evaluation, model comparison | Benchmarks, cost-quality tradeoffs |
| Training infrastructure | model-strategies/training-infrastructure | Pre-training infrastructure | DeepSpeed, Megatron-LM, FSDP, Datatrove |
| Knowledge distillation | model-strategies/distillation | Model distillation, teacher-student | Soft targets, feature-based, response-based |
| Synthetic data distillation | model-strategies/distillation | Alpaca, Vicuna, Orca | Self-Instruct, Evol-Instruct |

---

## RAG

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| RAG architecture | rag/rag-pipeline | Retrieval-Augmented Generation | Naive RAG, advanced RAG, modular RAG |
| Self-RAG | rag/rag-pipeline | Adaptive retrieval | Self-reflection, retrieval gating |
| CRAG (Corrective RAG) | rag/rag-pipeline | Corrective retrieval | Web search fallback, quality evaluation |
| HyDE | rag/rag-pipeline | Hypothetical Document Embedding | Query transformation, zero-shot retrieval |
| Document ingestion pipeline | rag/document-ingestion | Document parsing, ETL | Unstructured, Docling, LlamaParse, OCR |
| Chunking strategies | rag/chunking | Text splitting, recursive chunking | Token-aware, semantic, proposition-based |
| Late chunking | rag/chunking | Contextual chunk embeddings | Jina AI, long-context embedding |
| Hierarchical chunking | rag/chunking | Parent-child chunks | Auto-merging retriever, sentence window |
| Retrieval and reranking | rag/retrieval-reranking | Two-stage retrieval, cross-encoder reranking | DPR, BM25, SPLADE, Cohere Rerank |
| Reciprocal Rank Fusion (RRF) | rag/retrieval-reranking | RRF | Hybrid search fusion, rank aggregation |
| GraphRAG | rag/graphrag | Graph-based RAG, knowledge graph RAG | Community summarization, Leiden algorithm |
| Knowledge graph construction | rag/graphrag | Entity extraction, relation extraction | Neo4j, REBEL, Diffbot |
| Multimodal RAG | rag/multimodal-rag | Visual RAG, image retrieval RAG | ColPali, CLIP retrieval, document image search |

---

## Vector Search

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Vector databases | vector-search/vector-databases | Vector stores | Pinecone, Qdrant, Weaviate, Milvus, pgvector |
| Multi-tenancy in vector DBs | vector-search/vector-databases | Namespace isolation | Tenant partitioning, metadata filtering |
| Embedding model selection | vector-search/embedding-models | Embedding model comparison | MTEB, domain-specific models, Matryoshka |
| HNSW algorithm | vector-search/ann-algorithms | Hierarchical Navigable Small World | ef_construction, ef_search, M parameter |
| IVF / IVF-PQ | vector-search/ann-algorithms | Inverted File Index | Product Quantization, FAISS |
| DiskANN | vector-search/ann-algorithms | Disk-based ANN | Billion-scale, SSD-based search |
| Hybrid search | vector-search/hybrid-search | Dense + sparse retrieval | BM25, SPLADE, RRF, alpha tuning |
| SPLADE | vector-search/hybrid-search | Learned sparse retrieval | Term expansion, sparse neural IR |

---

## Prompt Engineering

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Prompt patterns | prompt-engineering/prompt-patterns | Prompt templates, prompting techniques | Few-shot, CoT, ToT, self-consistency |
| Chain-of-Thought (CoT) | prompt-engineering/prompt-patterns | CoT prompting, step-by-step reasoning | Zero-shot CoT, few-shot CoT |
| Few-shot in-context learning | prompt-engineering/prompt-patterns | Few-shot prompting, ICL | Example selection, example ordering |
| Tree-of-Thought (ToT) | prompt-engineering/prompt-patterns | ToT | Deliberate search, branch evaluation |
| Self-consistency | prompt-engineering/prompt-patterns | SC decoding | Majority voting, multi-path reasoning |
| Structured output generation | prompt-engineering/structured-output | JSON mode, function calling | Constrained decoding, Outlines, Instructor |
| Constrained decoding | prompt-engineering/structured-output | Grammar-guided generation | Outlines, XGrammar, finite-state machines |
| Prompt injection | prompt-engineering/prompt-injection | Jailbreaking, adversarial prompting | Direct injection, indirect injection |
| Indirect prompt injection | prompt-engineering/prompt-injection | Data poisoning via retrieval | RAG injection, tool output manipulation |
| Context management | prompt-engineering/context-management | Context window management | Token budgeting, prompt compression, LLMLingua |
| Prompt caching | prompt-engineering/context-management | KV prefix caching (provider-level) | Anthropic prompt caching, cost reduction |

---

## Agents

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Agent architecture patterns | agents/agent-architecture | Agent loops, cognitive architectures | ReAct, Plan-and-Execute, LATS, Reflexion |
| ReAct pattern | agents/agent-architecture | Reasoning + Acting | Thought-Action-Observation loop |
| Plan-and-Execute | agents/agent-architecture | Plan-and-Solve | Planning LLM + execution LLM |
| LATS (Language Agent Tree Search) | agents/agent-architecture | Tree-search agents | MCTS for language agents |
| Reflexion | agents/agent-architecture | Self-reflection agents | Verbal reinforcement learning |
| Tool use / function calling | agents/tool-use | Function calling, API calling | OpenAI functions, Anthropic tools, MCP |
| Model Context Protocol (MCP) | agents/tool-use | MCP | Anthropic, tool interoperability |
| Multi-agent systems | agents/multi-agent | Multi-agent orchestration | AutoGen, CrewAI, LangGraph, debate |
| Supervisor pattern | agents/multi-agent | Agent supervisor, orchestrator agent | Delegation, routing |
| Memory systems | agents/memory-systems | Agent memory, conversational memory | MemGPT, episodic, semantic, procedural |
| Generative agent memory | agents/memory-systems | Reflection, importance scoring | Park et al., retrieval-based memory |
| Code agents | agents/code-agents | AI coding assistants, copilots | GitHub Copilot, Cursor, Devin, Claude Code |
| SWE-bench | agents/code-agents | Software engineering benchmark | Code agent evaluation |

---

## Orchestration

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Orchestration frameworks | orchestration/orchestration-frameworks | LLM frameworks | LangChain, LlamaIndex, Semantic Kernel, Haystack |
| DSPy | orchestration/orchestration-frameworks | Declarative prompt programming | MIPRO, BootstrapFinetune, prompt optimization |
| Prompt chaining | orchestration/prompt-chaining | Pipeline composition, chain of prompts | LCEL, sequential chains, map-reduce |
| Build vs buy decision | orchestration/build-vs-buy | Framework selection | Thin wrapper vs full framework |

---

## Evaluation

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Evaluation frameworks | evaluation/eval-frameworks | LLM evaluation tools | RAGAS, DeepEval, LangSmith, Braintrust, TruLens |
| LLM-as-judge | evaluation/eval-frameworks | GPT-4 judge, automated evaluation | MT-Bench, position bias, verbosity bias |
| RAGAS metrics | evaluation/eval-frameworks | Faithfulness, answer relevancy, context precision | RAG evaluation, claim decomposition |
| Hallucination detection | evaluation/hallucination-detection | Factuality checking, faithfulness | NLI-based, SelfCheckGPT, FActScore |
| Claim decomposition | evaluation/hallucination-detection | Atomic fact verification | FActScore, NLI scoring |
| LLM observability | evaluation/llm-observability | LLM monitoring, tracing | LangSmith, Langfuse, Arize Phoenix, Datadog |
| LLM benchmarks | evaluation/benchmarks | Model evaluation benchmarks | MMLU, HumanEval, MT-Bench, GPQA, MATH |
| Benchmark contamination | evaluation/benchmarks | Data leakage, test set contamination | Evaluation integrity, temporal benchmarks |

---

## Safety

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Guardrails | safety/guardrails | Safety rails, content filtering | NeMo Guardrails, Guardrails AI, Llama Guard |
| Input/output guardrail architecture | safety/guardrails | Sandwich pattern, pre/post filtering | Toxicity, topic control, groundedness |
| PII protection | safety/pii-protection | PII detection, data anonymization | Presidio, AWS Comprehend, Cloud DLP |
| Differential privacy | safety/pii-protection | DP | Privacy-preserving ML |
| Red teaming | safety/red-teaming | Adversarial testing, jailbreak testing | PAIR, TAP, GCG, PyRIT |
| Automated red teaming | safety/red-teaming | LLM-based attack generation | Rainbow Teaming, PAIR, TAP |
| AI governance | safety/ai-governance | AI regulation, AI compliance | EU AI Act, NIST AI RMF, ISO 42001 |
| Model cards / system cards | safety/ai-governance | Model documentation | Transparency, audit trail |

---

## Performance

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Latency optimization | performance/latency-optimization | TTFT, TPS, decode latency | Speculative decoding, streaming, disaggregated serving |
| Prompt compression | performance/latency-optimization | LLMLingua, LongLLMLingua | Token reduction, latency reduction |
| Semantic caching | performance/semantic-caching | Similarity-based caching | GPTCache, embedding-based cache lookup |
| Exact vs semantic cache | performance/semantic-caching | Deterministic vs approximate caching | Cache hit rate, similarity threshold |
| Cost optimization | performance/cost-optimization | Token cost, GPU cost | Tiered routing, prompt caching, batch API |
| Self-hosting economics | performance/cost-optimization | Build vs buy cost analysis | Breakeven analysis, GPU amortization |
| Model routing | performance/model-routing | LLM routing, model cascading | FrugalGPT, RouteLLM, tiered models |
| Fallback chains | performance/model-routing | Model failover | Multi-provider resilience, circuit breaker |

---

## Case Studies

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| Chatbot architecture | case-studies/chatbot-architecture | Conversational AI system design | Session management, streaming, multi-turn |
| Copilot architecture | case-studies/copilot-architecture | AI coding assistant architecture | IDE integration, FIM, ghost text |
| Enterprise search | case-studies/enterprise-search | AI-powered knowledge search | Multi-source, ACL, hybrid retrieval |
| Voice AI pipeline | case-studies/voice-ai | Voice agents, conversational voice | STT-LLM-TTS, real-time audio, WebRTC |
| GenAI gateway | case-studies/genai-gateway | LLM gateway, AI proxy | Multi-provider, rate limiting, observability |
| Kubernetes for GenAI | case-studies/kubernetes-genai | K8s GPU scheduling | GPU operator, KNative, autoscaling |

---

## Patterns

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|------------------|
| GenAI design patterns | patterns/genai-design-patterns | Architectural patterns for LLM systems | Strangler fig, gateway, guardrail sandwich |
| Deployment patterns | patterns/deployment-patterns | GenAI deployment strategies | Blue-green, canary, shadow, A/B for LLMs |
