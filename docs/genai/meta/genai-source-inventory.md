# GenAI Source Inventory

A catalog of research papers, industry documentation, frameworks, and technical articles used to build this knowledge base. Organized by domain.

---

## Research Papers

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| Vaswani et al., "Attention Is All You Need" (2017) | Paper | Foundations | Transformer architecture, self-attention, multi-head attention, positional encoding |
| Brown et al., "Language Models are Few-Shot Learners" (GPT-3, 2020) | Paper | Foundations | In-context learning, few-shot prompting, scaling laws, GPT-3 architecture |
| Touvron et al., "LLaMA: Open and Efficient Foundation Language Models" (Meta, 2023) | Paper | Foundations | LLaMA 1 architecture, training data composition, open-weight LLMs |
| Touvron et al., "LLaMA 2: Open Foundation and Fine-Tuned Chat Models" (Meta, 2023) | Paper | Foundations | LLaMA 2, GQA, RLHF alignment, safety tuning, reward model training |
| Meta AI, "The Llama 3 Herd of Models" (2024) | Paper | Foundations | LLaMA 3/3.1 architecture, 4D parallelism, 128K context, training infrastructure |
| OpenAI, "GPT-4 Technical Report" (2023) | Paper | Foundations | GPT-4 capabilities, multimodal vision, safety evaluation |
| Google DeepMind, "Gemini: A Family of Highly Capable Multimodal Models" (2023) | Paper | Foundations | Native multimodal architecture, Gemini 1.0 Ultra/Pro/Nano |
| Reid et al., "Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context" (2024) | Paper | Foundations | 1M-token context window, MoE architecture, long-context retrieval |
| Jiang et al., "Mistral 7B" (Mistral AI, 2023) | Paper | Foundations | Sliding window attention, GQA, byte-fallback BPE tokenizer |
| Jiang et al., "Mixtral of Experts" (Mistral AI, 2024) | Paper | Foundations | Sparse MoE, top-2 routing, expert load balancing |
| DeepSeek AI, "DeepSeek-V2: A Strong, Economical, and Efficient MoE Language Model" (2024) | Paper | Foundations | Multi-head Latent Attention (MLA), MoE, KV cache compression |
| DeepSeek AI, "DeepSeek-V3 Technical Report" (2024) | Paper | Foundations | 671B MoE, FP8 training, cost-efficient frontier training |
| DeepSeek AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL" (2025) | Paper | Foundations | Reasoning models, reinforcement learning for reasoning |
| Hoffmann et al., "Training Compute-Optimal Large Language Models" (Chinchilla, 2022) | Paper | Foundations | Scaling laws, compute-optimal training, data/parameter tradeoffs |
| Shazeer, "Fast Transformer Decoding: One Write-Head is All You Need" (2019) | Paper | Architecture | Multi-Query Attention (MQA) |
| Ainslie et al., "GQA: Training Generalized Multi-Query Transformer Models" (2023) | Paper | Architecture | Grouped-Query Attention (GQA) |
| Su et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding" (2021) | Paper | Architecture | Rotary Position Embedding (RoPE) |
| Press et al., "Train Short, Test Long: Attention with Linear Biases" (ALiBi, 2022) | Paper | Architecture | ALiBi positional encoding, length generalization |
| Shazeer, "GLU Variants Improve Transformer" (2020) | Paper | Architecture | SwiGLU activation function |
| Zhang & Sennrich, "Root Mean Square Layer Normalization" (2019) | Paper | Architecture | RMSNorm |
| Fedus et al., "Switch Transformers: Scaling to Trillion Parameter Models" (2022) | Paper | Architecture | Mixture of Experts, sparse routing |
| Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention" (2022) | Paper | Architecture | IO-aware attention, tiling, HBM optimization |
| Dao, "FlashAttention-2: Faster Attention with Better Parallelism" (2023) | Paper | Architecture | Improved parallelism, work partitioning |
| Shah et al., "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision" (2024) | Paper | Architecture | H100 TMA, FP8 tensor cores, warp specialization |
| Kwon et al., "Efficient Memory Management for LLM Serving with PagedAttention" (vLLM, 2023) | Paper | Serving | PagedAttention, virtual memory for KV cache, continuous batching |
| Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models" (2022) | Paper | Serving | Continuous batching, iteration-level scheduling |
| Zheng et al., "SGLang: Efficient Execution of Structured Language Model Programs" (2024) | Paper | Serving | RadixAttention, prefix caching, compressed FSM for structured generation |
| Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (Google, 2023) | Paper | Serving | Speculative decoding, draft-verify paradigm |
| Cai et al., "Medusa: Simple LLM Inference Acceleration Framework" (2024) | Paper | Serving | Multi-head speculative decoding |
| Li et al., "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty" (2024) | Paper | Serving | Feature-level speculation |
| Patel et al., "Splitwise: Efficient Generative LLM Inference Using Phase Splitting" (Microsoft, 2024) | Paper | Serving | Disaggregated prefill/decode serving |
| Zhong et al., "DistServe: Disaggregating Prefill and Decoding for Goodput-optimized LLM Serving" (2024) | Paper | Serving | Disaggregated serving, goodput optimization |
| Agrawal et al., "Sarathi: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2024) | Paper | Serving | Chunked prefill, latency-throughput tradeoff |
| Shoeybi et al., "Megatron-LM: Training Multi-Billion Parameter Language Models" (NVIDIA, 2019) | Paper | Parallelism | Tensor parallelism |
| Huang et al., "GPipe: Efficient Training of Giant Neural Networks" (Google, 2019) | Paper | Parallelism | Pipeline parallelism |
| Narayanan et al., "Efficient Large-Scale Language Model Training on GPU Clusters" (2021) | Paper | Parallelism | 3D parallelism, interleaved 1F1B schedule |
| Rajbhandari et al., "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models" (2020) | Paper | Parallelism | ZeRO stages 1-3, memory optimization |
| Zhao et al., "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel" (Meta, 2023) | Paper | Parallelism | FSDP implementation, scaling |
| Lepikhin et al., "GShard: Scaling Giant Models with Conditional Computation" (Google, 2020) | Paper | Parallelism | Expert parallelism, MoE sharding |
| Liu et al., "Ring Attention with Blockwise Transformers for Near-Infinite Context" (2023) | Paper | Parallelism | Ring attention, sequence-level distribution |
| Frantar et al., "GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers" (2022) | Paper | Quantization | Weight-only INT4 quantization, OBQ-based approach |
| Lin et al., "AWQ: Activation-aware Weight Quantization for LLM Compression" (MIT, 2024) | Paper | Quantization | Activation-aware weight quantization |
| Xiao et al., "SmoothQuant: Accurate and Efficient Post-Training Quantization" (MIT/NVIDIA, 2023) | Paper | Quantization | W8A8 quantization, activation smoothing |
| Dettmers et al., "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale" (2022) | Paper | Quantization | Mixed-precision INT8, outlier handling |
| Dettmers et al., "QLoRA: Efficient Finetuning of Quantized Language Models" (2023) | Paper | Quantization/Fine-tuning | QLoRA, NF4 data type, double quantization |
| Micikevicius et al., "FP8 Formats for Deep Learning" (NVIDIA, 2022) | Paper | Quantization | FP8 training and inference |
| Liu et al., "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache" (2024) | Paper | Quantization | KV cache quantization |
| Chen et al., "Extending Context Window of LLMs via Positional Interpolation" (2023) | Paper | Context Scaling | Position Interpolation (PI), RoPE extension |
| Peng et al., "YaRN: Efficient Context Window Extension of Large Language Models" (2023) | Paper | Context Scaling | YaRN, NTK-aware scaling |
| Xiao et al., "Efficient Streaming Language Models with Attention Sinks" (StreamingLLM, 2023) | Paper | Context Scaling | Attention sinks, streaming inference |
| Zhang et al., "H2O: Heavy-Hitter Oracle for Efficient Generative Inference" (2023) | Paper | Context Scaling | KV cache eviction policies |
| Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (2024) | Paper | Context Scaling | Positional bias in long contexts |
| Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models" (2021) | Paper | Fine-tuning | Low-rank adaptation, parameter-efficient fine-tuning |
| Houlsby et al., "Parameter-Efficient Transfer Learning for NLP" (2019) | Paper | Fine-tuning | Bottleneck adapters |
| Li and Liang, "Prefix-Tuning: Optimizing Continuous Prompts for Generation" (2021) | Paper | Fine-tuning | Prefix tuning |
| Liu et al., "DoRA: Weight-Decomposed Low-Rank Adaptation" (2024) | Paper | Fine-tuning | DoRA, improved LoRA variant |
| Sheng et al., "S-LoRA: Serving Thousands of Concurrent LoRA Adapters" (2023) | Paper | Fine-tuning | Multi-adapter serving |
| Zhou et al., "LIMA: Less Is More for Alignment" (Meta, 2023) | Paper | Fine-tuning/Alignment | Data quality vs quantity for SFT |
| Hinton et al., "Distilling the Knowledge in a Neural Network" (Google, 2015) | Paper | Distillation | Knowledge distillation, soft targets, temperature scaling |
| Sanh et al., "DistilBERT, a distilled version of BERT" (HuggingFace, 2019) | Paper | Distillation | Task-agnostic distillation |
| Mukherjee et al., "Orca: Progressive Learning from Complex Explanation Traces of GPT-4" (Microsoft, 2023) | Paper | Distillation | Explanation-based distillation |
| Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS 2020) | Paper | RAG | Original RAG architecture, retriever-generator paradigm |
| Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (ICLR 2024) | Paper | RAG | Self-reflective RAG, adaptive retrieval |
| Yan et al., "Corrective Retrieval Augmented Generation" (CRAG, 2024) | Paper | RAG | Corrective retrieval, web search fallback |
| Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE, 2023) | Paper | RAG | Hypothetical Document Embedding |
| Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Microsoft, 2024) | Paper | RAG | GraphRAG, community summarization, knowledge graphs |
| Gao et al., "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (2024) | Paper | RAG | Modular RAG architecture patterns |
| Formal et al., "SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking" (SIGIR 2021) | Paper | Retrieval | Learned sparse retrieval, term expansion |
| Karpukhin et al., "Dense Passage Retrieval for Open-Domain QA" (DPR, EMNLP 2020) | Paper | Retrieval | Dense bi-encoder retrieval |
| Nogueira & Cho, "Passage Re-ranking with BERT" (2019) | Paper | Retrieval | Cross-encoder reranking |
| Khattab & Zaharia, "ColBERT: Efficient and Effective Passage Search" (SIGIR 2020) | Paper | Retrieval | Late interaction, multi-vector retrieval |
| Santhanam et al., "ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction" (2022) | Paper | Retrieval | ColBERTv2, PLAID compression |
| Cormack et al., "Reciprocal Rank Fusion" (SIGIR 2009) | Paper | Retrieval | RRF for hybrid search fusion |
| Thakur et al., "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of IR Models" (NeurIPS 2021) | Paper | Retrieval | Zero-shot retrieval evaluation |
| Malkov & Yashunin, "Efficient and Robust ANN Using Hierarchical Navigable Small World Graphs" (2018) | Paper | Vector Search | HNSW algorithm |
| Subramanya et al., "DiskANN: Fast Accurate Billion-point Nearest Neighbor Search" (NeurIPS 2019) | Paper | Vector Search | Disk-based ANN, billion-scale search |
| Jegou et al., "Product Quantization for Nearest Neighbor Search" (IEEE TPAMI, 2011) | Paper | Vector Search | Product Quantization (PQ), IVF |
| Johnson et al., "Billion-scale Similarity Search with GPUs" (FAISS, 2019) | Paper | Vector Search | FAISS library, GPU-accelerated search |
| Mikolov et al., "Efficient Estimation of Word Representations in Vector Space" (Word2Vec, 2013) | Paper | Embeddings | Word embeddings, Skip-gram, CBOW |
| Pennington et al., "GloVe: Global Vectors for Word Representation" (EMNLP 2014) | Paper | Embeddings | Co-occurrence-based word vectors |
| Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" (2019) | Paper | Embeddings | Sentence embeddings, bi-encoder training |
| Kusupati et al., "Matryoshka Representation Learning" (NeurIPS 2022) | Paper | Embeddings | Variable-dimension embeddings, nested representations |
| Wang et al., "Text Embeddings by Weakly-Supervised Contrastive Pre-training" (E5, 2022) | Paper | Embeddings | E5 embedding model, contrastive learning |
| Xiao et al., "C-Pack: Packaged Resources To Advance General Chinese Embedding" (BGE, 2023) | Paper | Embeddings | BGE embedding models, reranker |
| Chen et al., "BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity" (2024) | Paper | Embeddings | BGE-M3, dense+sparse+multi-vector |
| Muennighoff et al., "MTEB: Massive Text Embedding Benchmark" (EACL 2023) | Paper | Embeddings | Embedding evaluation benchmark |
| Radford et al., "Learning Transferable Visual Models From Natural Language Supervision" (CLIP, 2021) | Paper | Multimodal | CLIP, contrastive image-text pre-training |
| Zhai et al., "Sigmoid Loss for Language Image Pre-Training" (SigLIP, 2023) | Paper | Multimodal | SigLIP, sigmoid contrastive loss |
| Liu et al., "Visual Instruction Tuning" (LLaVA, 2023) | Paper | Multimodal | Vision-language models, visual instruction tuning |
| Li et al., "BLIP-2: Bootstrapping Language-Image Pre-training" (Salesforce, 2023) | Paper | Multimodal | Q-Former, frozen encoder bridging |
| Alayrac et al., "Flamingo: a Visual Language Model for Few-Shot Learning" (DeepMind, 2022) | Paper | Multimodal | Perceiver Resampler, few-shot visual learning |
| Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper, 2022) | Paper | Multimodal | Whisper ASR, encoder-decoder for speech |
| Girdhar et al., "ImageBind: One Embedding Space To Bind Them All" (Meta, 2023) | Paper | Multimodal | Six-modality embedding alignment |
| Faysse et al., "ColPali: Efficient Document Retrieval with Vision Language Models" (2024) | Paper | Multimodal RAG | Visual document retrieval, ColBERT-style VLM |
| Sennrich et al., "Neural Machine Translation of Rare Words with Subword Units" (BPE, ACL 2016) | Paper | Tokenization | Byte-Pair Encoding for NLP |
| Kudo & Richardson, "SentencePiece: A Simple and Language Independent Subword Tokenizer" (2018) | Paper | Tokenization | SentencePiece library, language-agnostic tokenization |
| Kudo, "Subword Regularization" (ACL 2018) | Paper | Tokenization | Unigram language model tokenizer |
| Petrov et al., "Language Model Tokenizers Introduce Unfairness Between Languages" (NeurIPS 2023) | Paper | Tokenization | Multilingual tokenization efficiency analysis |
| Ouyang et al., "Training Language Models to Follow Instructions with Human Feedback" (InstructGPT, 2022) | Paper | Alignment | RLHF, reward model training, PPO for LLMs |
| Schulman et al., "Proximal Policy Optimization Algorithms" (OpenAI, 2017) | Paper | Alignment | PPO algorithm |
| Rafailov et al., "Direct Preference Optimization" (DPO, Stanford, 2023) | Paper | Alignment | DPO, reference-model-based preference optimization |
| Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (Anthropic, 2022) | Paper | Alignment | Constitutional AI, RLAIF, principle-based alignment |
| Wang et al., "Self-Instruct: Aligning Language Models with Self-Generated Instructions" (2022) | Paper | Alignment | Synthetic instruction data generation |
| Xu et al., "WizardLM: Empowering Large Language Models to Follow Complex Instructions" (2023) | Paper | Alignment | Evol-Instruct, instruction complexity evolution |
| Tunstall et al., "Zephyr: Direct Distillation of LM Alignment" (HuggingFace, 2023) | Paper | Alignment | DPO on synthetic preferences, distilled alignment |
| Lightman et al., "Let's Verify Step by Step" (OpenAI, 2023) | Paper | Alignment | Process reward models, step-level verification |
| Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022) | Paper | Prompt Engineering | Chain-of-thought prompting |
| Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023) | Paper | Agents | ReAct pattern, interleaved reasoning and action |
| Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" (2023) | Paper | Prompt Engineering | Tree-of-Thought, deliberate search |
| Wang et al., "Self-Consistency Improves Chain of Thought Reasoning" (2023) | Paper | Prompt Engineering | Self-consistency sampling |
| Khattab et al., "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines" (ICLR 2024) | Paper | Orchestration | DSPy, programmatic prompt optimization |
| Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (NeurIPS 2023) | Paper | Agents | Reflexion, verbal self-reflection |
| Zhou et al., "Language Agent Tree Search Unifies Reasoning Acting and Planning" (LATS, ICML 2024) | Paper | Agents | LATS, MCTS for language agents |
| Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (Microsoft, 2023) | Paper | Agents | AutoGen, multi-agent conversation |
| Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (Stanford, 2023) | Paper | Agents | Generative agent memory, reflection, planning |
| Packer et al., "MemGPT: Towards LLMs as Operating Systems" (2023) | Paper | Agents | Virtual context management, tiered memory |
| Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools" (NeurIPS 2023) | Paper | Agents | Self-supervised tool learning |
| Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" (ICLR 2024) | Paper | Evaluation | SWE-bench, real-world code evaluation |
| Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (LMSYS, 2023) | Paper | Evaluation | MT-Bench, Chatbot Arena, LLM-as-judge |
| Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation" (2023) | Paper | Evaluation | RAGAS metrics: faithfulness, relevance, precision, recall |
| Hendrycks et al., "Measuring Massive Multitask Language Understanding" (MMLU, 2021) | Paper | Evaluation | MMLU benchmark |
| Chen et al., "Evaluating Large Language Models Trained on Code" (HumanEval, 2021) | Paper | Evaluation | HumanEval benchmark, Codex |
| Min et al., "FActScore: Fine-grained Atomic Evaluation of Factual Precision" (2023) | Paper | Evaluation | Claim decomposition, factual verification |
| Lin et al., "TruthfulQA: Measuring How Models Mimic Human Falsehoods" (2022) | Paper | Evaluation | Truthfulness benchmark |
| Ji et al., "Survey of Hallucination in Natural Language Generation" (2023) | Paper | Evaluation | Hallucination taxonomy (intrinsic, extrinsic) |
| Manakul et al., "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection" (2023) | Paper | Evaluation | Self-consistency-based hallucination detection |
| Zou et al., "Universal and Transferable Adversarial Attacks on Aligned Language Models" (GCG, 2023) | Paper | Safety | Gradient-based adversarial suffixes |
| Chao et al., "Jailbreaking Black Box LLMs in Twenty Queries" (PAIR, 2023) | Paper | Safety | Automated jailbreak generation |
| Mehrotra et al., "Tree of Attacks with Pruning" (TAP, 2024) | Paper | Safety | Tree-search jailbreak strategies |
| Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023) | Paper | Safety | Indirect prompt injection attacks |
| Perez & Ribeiro, "HackAPrompt: Exposing Systemic Weaknesses of LLMs" (EMNLP 2023) | Paper | Safety | Prompt injection taxonomy |
| Carlini et al., "Extracting Training Data from Large Language Models" (USENIX 2021) | Paper | Safety | Training data extraction, memorization |
| Mitchell et al., "Model Cards for Model Reporting" (FAT* 2019) | Paper | Governance | Model documentation, transparency |
| Chen et al., "FrugalGPT: How to Use LLMs While Reducing Cost and Improving Performance" (Stanford, 2023) | Paper | Performance | Model cascading, cost-aware routing |
| Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (LMSYS, 2024) | Paper | Performance | Learned model routing |
| Jiang et al., "LLMLingua: Compressing Prompts for Accelerated Inference" (Microsoft, 2023) | Paper | Performance | Prompt compression, token reduction |
| Willard & Louf, "Efficient Guided Generation for Large Language Models" (Outlines, 2023) | Paper | Structured Output | Constrained decoding with formal grammars |
| Wu et al., "AI Chains: Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts" (CHI 2022) | Paper | Orchestration | Prompt chaining |
| Williams et al., "Roofline: An Insightful Visual Performance Model for Multicore Architectures" (2009) | Paper | GPU Compute | Compute vs memory bound analysis |

---

## Industry Documentation

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| OpenAI API Documentation | Docs | Platform | GPT-4o, o1/o3, function calling, structured outputs, JSON mode, batch API, fine-tuning API |
| OpenAI tiktoken library | Tool | Tokenization | BPE tokenizer implementation, cl100k_base, o200k_base |
| Anthropic API Documentation | Docs | Platform | Claude model family, tool use, prompt caching, extended thinking, message batches |
| Anthropic "Constitutional AI" model cards | Docs | Alignment | Constitutional principles, safety evaluation, model behavior |
| Google Gemini API Documentation | Docs | Platform | Gemini models, context caching, function calling, multimodal input |
| Google Vertex AI Documentation | Docs | Platform | Enterprise deployment, grounding, model garden, tuning |
| Google Cloud Document AI | Docs | Document Processing | Layout-aware OCR, entity extraction, document parsing |
| AWS Bedrock Documentation | Docs | Platform | Multi-model access, knowledge bases, guardrails, agents |
| AWS Amazon Textract | Docs | Document Processing | OCR, table extraction, form parsing |
| AWS Amazon Comprehend | Docs | PII/NLP | PII detection, sentiment analysis, entity recognition |
| Azure OpenAI Service Documentation | Docs | Platform | Enterprise GPT deployment, PTUs, content filtering |
| Azure AI Document Intelligence | Docs | Document Processing | Document parsing, layout analysis |
| Azure AI Content Safety | Docs | Safety | Content moderation, Prompt Shields |
| NVIDIA A100/H100/H200/B200 Whitepapers | Docs | GPU Compute | GPU architecture, tensor cores, HBM, NVLink, NVSwitch |
| NVIDIA TensorRT-LLM Documentation | Docs | Serving | Fused kernels, FP8, in-flight batching, MoE parallelism |
| NVIDIA NeMo Framework Documentation | Docs | Training | LLM training, Guardrails (Colang), alignment |
| NVIDIA Triton Inference Server | Docs | Serving | Model serving, ensemble pipelines, dynamic batching |
| NVIDIA DCGM (Data Center GPU Manager) | Docs | Monitoring | GPU utilization, temperature, memory monitoring |
| Cohere API Documentation | Docs | Platform | Command R+, Embed v3, Rerank, RAG with citations |
| Voyage AI Documentation | Docs | Embeddings | Domain-specific embedding models (code, law) |
| Jina AI Documentation | Docs | Embeddings | Jina Embeddings v3, LoRA adapters, late chunking |
| Pinecone Documentation | Docs | Vector Search | Serverless vector DB, namespaces, hybrid search, metadata filtering |
| Qdrant Documentation | Docs | Vector Search | Binary quantization, scalar quantization, HNSW tuning |
| Weaviate Documentation | Docs | Vector Search | Hybrid search, multi-tenancy, embedded vectorizers |
| Milvus Documentation | Docs | Vector Search | Disaggregated architecture, GPU indexing, IVF-PQ |
| pgvector Documentation | Docs | Vector Search | PostgreSQL vector extension, HNSW, halfvec |
| Deepgram Documentation | Docs | Voice AI | Streaming ASR, Nova-2 model |
| ElevenLabs Documentation | Docs | Voice AI | TTS API, voice cloning, streaming synthesis |
| Twelve Labs Documentation | Docs | Video AI | Video understanding API, multimodal video embeddings |

---

## Frameworks and Tools

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| LangChain Documentation | Tool | Orchestration | LCEL, chains, agents, retrieval, text splitters |
| LangGraph Documentation | Tool | Orchestration | State machines, multi-agent, checkpointing |
| LangSmith Documentation | Tool | Observability | Tracing, evaluation, datasets, annotation |
| LlamaIndex Documentation | Tool | RAG | Data connectors, node parsers, query engines, LlamaParse |
| Semantic Kernel (Microsoft) | Tool | Orchestration | Enterprise AI orchestration, .NET/Python/Java SDK |
| Haystack 2.0 (deepset) | Tool | RAG | Pipeline-based RAG, component architecture |
| DSPy (Stanford NLP) | Tool | Orchestration | Programmatic prompt optimization, MIPRO, BootstrapFinetune |
| vLLM | Tool | Serving | PagedAttention, continuous batching, tensor parallelism, prefix caching |
| TGI (HuggingFace Text Generation Inference) | Tool | Serving | Production serving, FlashAttention, quantization |
| SGLang | Tool | Serving | RadixAttention, structured generation, prefix caching |
| llama.cpp / GGML | Tool | Serving | CPU/edge inference, GGUF quantization formats (Q4_K_M, Q5_K_M) |
| HuggingFace Transformers | Tool | Model Library | Model hub, tokenizers, training, inference |
| HuggingFace TRL (Transformer Reinforcement Learning) | Tool | Alignment | SFTTrainer, DPOTrainer, PPOTrainer |
| HuggingFace Text Embeddings Inference (TEI) | Tool | Serving | Embedding model serving, dynamic batching |
| Axolotl | Tool | Fine-tuning | YAML-based fine-tuning, LoRA/QLoRA support |
| LLaMA-Factory | Tool | Fine-tuning | Unified fine-tuning interface, web UI |
| torchtune (Meta) | Tool | Fine-tuning | Native PyTorch fine-tuning |
| DeepSpeed (Microsoft) | Tool | Training | ZeRO optimization, DeepSpeed-Chat RLHF pipeline |
| Megatron-LM (NVIDIA) | Tool | Training | 3D parallelism, large-scale model training |
| FSDP (PyTorch) | Tool | Training | Fully Sharded Data Parallel |
| PyRIT (Microsoft) | Tool | Red Teaming | Python Risk Identification Toolkit for generative AI |
| Guardrails AI | Tool | Safety | Programmable output validation, RAIL spec |
| NeMo Guardrails (NVIDIA) | Tool | Safety | Colang language, programmable rails, topical control |
| Llama Guard (Meta) | Tool | Safety | LLM-based input/output safety classifier |
| LLM Guard (Protect AI) | Tool | Safety | Open-source LLM security toolkit |
| Lakera Guard | Tool | Safety | Real-time prompt injection detection |
| Microsoft Presidio | Tool | PII | PII detection and de-identification SDK |
| Outlines (dottxt) | Tool | Structured Output | Grammar-constrained decoding |
| Instructor (Jason Liu) | Tool | Structured Output | Pydantic-based structured extraction |
| Guidance (Microsoft) | Tool | Structured Output | Template-based constrained generation |
| RAGAS | Tool | Evaluation | RAG evaluation metrics |
| DeepEval | Tool | Evaluation | CI/CD LLM evaluation framework |
| Braintrust | Tool | Evaluation | Experiment management, LLM evaluation |
| TruLens | Tool | Evaluation | Feedback function-based evaluation |
| Patronus AI | Tool | Evaluation | Enterprise guardrail evaluation, Lynx model |
| Langfuse | Tool | Observability | Open-source LLM observability |
| Arize Phoenix | Tool | Observability | Embedding analysis, trace visualization |
| Helicone | Tool | Observability | Proxy-based LLM monitoring |
| Portkey AI Gateway | Tool | Gateway | Multi-provider routing, caching, observability |
| LiteLLM (BerriAI) | Tool | Gateway | Unified LLM API interface, 100+ providers |
| OpenRouter | Tool | Gateway | Unified LLM routing API |
| GPTCache (Zilliz) | Tool | Caching | Semantic caching for LLM applications |
| Unstructured.io | Tool | Document Processing | Document parsing, chunking, multi-format ingestion |
| Docling (IBM) | Tool | Document Processing | Layout-aware document parsing |
| Firecrawl | Tool | Document Processing | Web scraping for LLM applications |
| Trafilatura | Tool | Document Processing | Web text extraction |
| tree-sitter | Tool | Code Analysis | AST parsing for code chunking |
| AutoGen (Microsoft) | Tool | Multi-Agent | Multi-agent conversation framework |
| CrewAI | Tool | Multi-Agent | Role-playing AI agent orchestration |
| Mem0 | Tool | Memory | LLM memory infrastructure |
| Letta (MemGPT) | Tool | Memory | Virtual context management platform |

---

## Blog Posts and Technical Articles

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| Anthropic, "Many-shot Jailbreaking" (2024) | Blog | Safety | Many-shot in-context jailbreaking |
| Microsoft, "Crescendo: Multi-Turn LLM Jailbreak Attack" (2024) | Blog | Safety | Multi-turn escalation attacks |
| Microsoft, "Skeleton Key: AI Jailbreak Technique" (2024) | Blog | Safety | Skeleton key bypass technique |
| OpenAI, "Learning to Reason with LLMs" (o1 announcement, 2024) | Blog | Alignment | Reasoning models, inference-time compute |
| Greg Kamradt, "5 Levels of Text Splitting" (2023) | Blog | RAG | Chunking strategies from naive to agentic |
| Greg Kamradt, "Needle in a Haystack" pressure test (2023) | Blog | Evaluation | Long-context retrieval evaluation methodology |
| Microsoft Research, "LazyGraphRAG" (2024) | Blog | RAG | Cost-efficient graph-based RAG |
| Simon Willison, "Dual LLM Pattern for Building AI Assistants" (2023) | Blog | Safety | Dual-LLM architecture for prompt injection defense |
| Anyscale, "LLM Performance Benchmarks" (2024) | Blog | Performance | Serving throughput and latency benchmarks |
| Andreessen Horowitz, "The State of AI Infrastructure" (2024) | Blog | Infrastructure | AI infrastructure survey, cost analysis |
| Pinecone, "Chunking Strategies for LLM Applications" (2024) | Blog | RAG | Chunk size impact on retrieval quality |
| Weaviate, "Impact of Chunk Size on RAG" (2024) | Blog | RAG | Empirical chunk size evaluation |
| Cursor Engineering Blog (2024) | Blog | Code Agents | IDE context engine, codebase indexing |
| Spotify Engineering Blog | Blog | Vector Search | HNSW usage for recommendation |
| Airbnb Engineering Blog | Blog | Vector Search | Filtered vector search for listings |

---

## Benchmark Datasets and Evaluation Resources

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| MMLU / MMLU-Pro | Benchmark | General | Multitask language understanding (57 subjects) |
| HumanEval / HumanEval+ | Benchmark | Code | Function-level code generation evaluation |
| SWE-bench / SWE-bench Lite | Benchmark | Code | Real-world GitHub issue resolution |
| LiveCodeBench | Benchmark | Code | Contamination-free code evaluation |
| MT-Bench | Benchmark | Chat | Multi-turn instruction following (LLM-as-judge) |
| Chatbot Arena (LMSYS) | Benchmark | Chat | Human preference Elo ranking, crowdsourced A/B |
| AlpacaEval 2 | Benchmark | Chat | Instruction following win rate |
| Arena-Hard | Benchmark | Chat | Hard subset of Arena prompts |
| IFEval | Benchmark | Instruction | Precise instruction-following evaluation |
| GPQA | Benchmark | Reasoning | Graduate-level Q&A benchmark |
| MATH | Benchmark | Reasoning | Mathematical problem solving |
| GSM8K | Benchmark | Reasoning | Grade school math |
| ARC-AGI | Benchmark | Reasoning | Abstract reasoning corpus |
| BigBench | Benchmark | General | Broad capability evaluation (200+ tasks) |
| TruthfulQA | Benchmark | Safety | Truthfulness evaluation on adversarial questions |
| HarmBench / AdvBench | Benchmark | Safety | Adversarial robustness evaluation |
| HaluEval | Benchmark | Hallucination | Hallucination evaluation benchmark |
| FActScore | Benchmark | Hallucination | Fine-grained factual precision |
| MTEB (Massive Text Embedding Benchmark) | Benchmark | Embeddings | 56+ datasets across 8 embedding tasks |
| BEIR | Benchmark | Retrieval | Zero-shot IR evaluation across 18 datasets |
| MS MARCO | Benchmark | Retrieval | Passage and document ranking |
| RULER | Benchmark | Long Context | Real context size evaluation for long-context models |
| ViDoRe | Benchmark | Multimodal RAG | Visual document retrieval benchmark |
| WebArena | Benchmark | Agents | Realistic web environment for autonomous agents |
| Open LLM Leaderboard (HuggingFace) | Benchmark | General | Community-maintained model evaluation |
| ann-benchmarks.com | Benchmark | Vector Search | ANN algorithm performance comparison |

---

## Regulatory and Standards Sources

| Source | Type | Domain | Key Topics Covered |
|--------|------|--------|--------------------|
| EU AI Act (Regulation 2024/1689) | Regulation | Governance | Risk classification, GPAI rules, compliance timelines |
| NIST AI Risk Management Framework (AI 100-1) | Standard | Governance | AI risk management, MAP-MEASURE-MANAGE-GOVERN |
| NIST Adversarial ML Taxonomy (AI 100-2e2023) | Standard | Safety | Adversarial machine learning taxonomy |
| ISO/IEC 42001:2023 | Standard | Governance | AI management system standard |
| OECD AI Principles (2019, updated 2024) | Standard | Governance | International AI principles |
| US Executive Order 14110 on AI (2023) | Regulation | Governance | Safe, secure, and trustworthy AI requirements |
| GDPR (Regulation EU 2016/679) | Regulation | Privacy | Data protection, PII definitions, anonymization |
| CCPA (California AB-375) | Regulation | Privacy | Consumer data privacy rights |
| HIPAA (45 CFR 164.514) | Regulation | Privacy | Health data de-identification |
| OWASP Top 10 for LLM Applications v1.1 (2024) | Standard | Safety | LLM-specific vulnerability taxonomy |
| MLCommons AI Safety Benchmark v0.5 (2024) | Standard | Safety | AI safety evaluation taxonomy |
| MITRE ATLAS | Standard | Safety | Adversarial threat landscape for AI systems |
| Anthropic Responsible Scaling Policy (2023-2024) | Policy | Governance | Frontier model safety commitments |
| Frontier Model Forum (OpenAI, Anthropic, Google, Microsoft) | Policy | Governance | Industry safety collaboration |
