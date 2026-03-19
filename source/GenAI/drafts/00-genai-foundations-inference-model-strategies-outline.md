# Generative AI System Design Knowledge Base
# Domains 1-3: Foundations, LLM Architecture & Inference, Model Strategies

## Comprehensive Research Outline

---

# DOMAIN 1: FOUNDATIONS

---

## 1.1 Transformer Architecture

### What It Covers
The foundational neural network architecture ("Attention Is All You Need," Vaswani et al., 2017) that underpins all modern LLMs. Replaces recurrence and convolutions entirely with attention mechanisms, enabling parallelized training and superior performance on sequence tasks.

### Why It Matters for System Design
Every GenAI system is built on transformers. Understanding the architecture is essential for:
- Predicting inference latency and memory requirements
- Choosing between encoder, decoder, and encoder-decoder variants
- Understanding why KV cache exists and how it scales
- Making informed decisions about model parallelism strategies
- Estimating compute costs for training and inference

### Core Concepts

#### 1.1.1 Self-Attention Mechanism
- **Scaled dot-product attention**: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`
- Queries, Keys, Values are linear projections of the input
- The `sqrt(d_k)` scaling prevents vanishing gradients in softmax for large dimensions
- Permutation-invariant: operates on sets, not sequences (hence the need for positional encoding)
- Computational complexity: O(n^2 * d) where n = sequence length, d = dimension
- Memory complexity: O(n^2) for the attention matrix -- this is the fundamental bottleneck that drives most inference optimizations

**Key system design decision**: The quadratic scaling of attention with sequence length is why context window management, chunking strategies, and efficient attention methods (FlashAttention, sparse attention) exist as entire subfields.

#### 1.1.2 Multi-Head Attention (MHA)
- Splits the d_model dimension into h parallel attention heads
- Each head independently computes attention on d_k = d_model/h dimensions
- Outputs are concatenated and linearly projected
- Standard configuration: GPT-3 uses 96 heads with d_model=12288, so d_k=128
- Enables the model to attend to different representation subspaces simultaneously

**Variants critical for inference optimization**:
- **Multi-Query Attention (MQA)**: Shares K and V across all heads, keeping separate Q projections. Drastically reduces KV cache size and memory bandwidth requirements. Used by PaLM, Falcon.
- **Grouped-Query Attention (GQA)**: Compromise between MHA and MQA -- projects K,V to fewer head groups. Used by LLaMA 2 70B, LLaMA 3, Mistral 7B. Achieves quality close to MHA with efficiency close to MQA.

**Key architectural decision**: MHA vs GQA vs MQA directly determines KV cache memory requirements, which in turn determines maximum batch size and throughput during inference.

#### 1.1.3 Positional Encoding
- **Sinusoidal (original Transformer)**: Uses sin/cos functions with varying wavelengths across dimensions. No learned parameters. Can theoretically extrapolate to unseen sequence lengths.
- **Learned absolute embeddings**: Trainable vectors per position. Used by GPT-2, BERT. Cannot extrapolate beyond training length.
- **Rotary Position Embedding (RoPE)**: Encodes absolute positions via rotation matrices on Q and K vectors. Divides d-dimensional space into d/2 subspaces. Used by LLaMA, Mistral, Qwen, most modern open-source LLMs. Enables position interpolation for context extension.
- **ALiBi (Attention with Linear Biases)**: Adds distance-dependent penalties directly to attention scores instead of modifying embeddings. Used by BLOOM, MPT. Simpler but effective for extrapolation.

**Key system design decision**: RoPE has become the de facto standard because it enables context window extension via Position Interpolation (PI) and NTK-aware scaling without full retraining -- critical for deploying models at longer context lengths than they were trained on.

#### 1.1.4 Encoder vs Decoder vs Encoder-Decoder
- **Encoder-only (BERT, RoBERTa)**: Bidirectional attention, excels at understanding/classification. Not used for generation.
- **Decoder-only (GPT, LLaMA, Claude, Mistral)**: Causal/autoregressive attention mask. Dominant architecture for modern LLMs. All generative models use this.
- **Encoder-Decoder (T5, BART, Whisper)**: Full bidirectional encoding + autoregressive decoding. Used for translation, summarization, speech-to-text.

**Key system design decision**: Decoder-only has won for general-purpose LLMs. Encoder-decoder is preferred for specific tasks with clear input-output structure (e.g., Whisper for ASR).

#### 1.1.5 Feed-Forward Network (FFN)
- Two-layer MLP applied independently to each position
- Typically d_ff = 4 * d_model (e.g., 12288 -> 49152 -> 12288 for GPT-3)
- This is where MoE replaces the FFN with multiple expert FFNs
- Modern variants use SwiGLU activation (LLaMA, Mistral) instead of ReLU/GELU

#### 1.1.6 Layer Normalization
- **Post-LN (original Transformer)**: LayerNorm after residual addition. Training instability at scale.
- **Pre-LN (GPT-2 onwards)**: LayerNorm before attention/FFN blocks. More stable training. Used by virtually all modern LLMs.
- **RMSNorm**: Simplified variant used by LLaMA, Mistral. Removes mean-centering, only normalizes by RMS. Slightly faster with comparable quality.

### Real-World Examples
| Model | Attention Type | Positional Encoding | Norm | FFN Activation |
|-------|---------------|---------------------|------|----------------|
| GPT-3 (175B) | MHA (96 heads) | Learned absolute | Pre-LN | GELU |
| GPT-4 | Rumored MoE | Unknown | Unknown | Unknown |
| LLaMA 2 (7B-70B) | GQA (70B), MHA (7B/13B) | RoPE | RMSNorm | SwiGLU |
| LLaMA 3 (8B, 70B) | GQA (all sizes) | RoPE | RMSNorm | SwiGLU |
| Mistral 7B | GQA | RoPE | RMSNorm | SwiGLU |
| Claude (Opus/Sonnet/Haiku) | Undisclosed | Undisclosed | Undisclosed | Undisclosed |
| Gemini | Undisclosed (rumored MoE) | Undisclosed | Undisclosed | Undisclosed |
| BLOOM (176B) | MHA | ALiBi | Pre-LN | GELU |
| Falcon (40B) | MQA | RoPE | Pre-LN | GELU |

### Trade-offs and Failure Modes
- **Quadratic attention**: O(n^2) memory and compute limits practical context windows without optimizations
- **Position encoding extrapolation**: Models fail catastrophically outside trained context length unless using RoPE + interpolation or ALiBi
- **Pre-LN vs Post-LN**: Pre-LN enables training stability but may cap representational capacity at extreme scale
- **GQA trade-off**: ~1-2% quality reduction vs MHA in exchange for 2-4x inference throughput improvement

### Connections to Other Topics
- KV cache management (1.1.2 attention variant determines cache size)
- FlashAttention (optimizes 1.1.1 attention computation)
- Context window scaling (builds on 1.1.3 positional encoding)
- Model parallelism (tensor parallelism splits across 1.1.2 attention heads)
- MoE (replaces 1.1.5 FFN blocks)

---

## 1.2 Large Language Models (LLM Landscape)

### What It Covers
The current landscape of production LLMs, their architecture choices, parameter counts, context windows, and capabilities. This is the "model menu" that architects must navigate.

### Why It Matters for System Design
Model selection is the highest-leverage decision in GenAI system design. It determines cost, latency, quality ceiling, deployment constraints, and vendor lock-in.

### Core Concepts

#### 1.2.1 The GPT Family (OpenAI)
- **GPT-3 (175B, 2020)**: Demonstrated in-context learning. 2048 token context. Dense decoder-only transformer. 96 layers, 96 heads, d_model=12288.
- **GPT-3.5 Turbo (2022)**: Optimized for chat. RLHF-aligned. 4K/16K context. Powers early ChatGPT.
- **GPT-4 (2023)**: Rumored Mixture of Experts (~1.8T total, ~220B active per forward pass -- unconfirmed). 8K/32K/128K context. Multimodal (text + vision). State-of-the-art on most benchmarks at launch.
- **GPT-4o (2024)**: Natively multimodal (text + vision + audio). Lower latency. Cheaper. 128K context.
- **GPT-4o mini**: Smallest/cheapest. Optimized for high-volume, lower-complexity tasks.
- **o1, o3 (2024-2025)**: "Reasoning" models with chain-of-thought at inference time. Higher latency, much higher quality on math/code/reasoning.
- **Deployment**: Azure OpenAI Service, OpenAI API. Enterprise-grade with SLAs via Azure.
- **Pricing model**: Per-token (input/output priced separately).

#### 1.2.2 Claude (Anthropic)
- **Claude 3 family (2024)**: Haiku (fast/cheap), Sonnet (balanced), Opus (highest quality). 200K context window.
- **Claude 3.5 Sonnet (2024)**: Major quality leap. Competitive with GPT-4 on coding/reasoning.
- **Claude 4 family (2025)**: Opus 4, Sonnet 4, with extended thinking capabilities.
- **Claude 4.5 (2025)**: Opus 4.5 (200K context), Sonnet 4.5 (1M context with beta header).
- **Claude 4.6 (2026, current)**: Opus 4.6 (1M context, 128K output, $5/$25 per MTok), Sonnet 4.6 (1M context, 64K output, $3/$15 per MTok), Haiku 4.5 (200K context, 64K output, $1/$5 per MTok).
- **Key differentiators**: Constitutional AI alignment, extended thinking (chain-of-thought), large context windows (up to 1M tokens), strong instruction following.
- **Deployment**: Anthropic API, AWS Bedrock, Google Vertex AI.
- **Architecture**: Undisclosed. Focus on safety and alignment research.

#### 1.2.3 Gemini (Google DeepMind)
- **Gemini 1.0 (2023)**: Ultra, Pro, Nano variants. Natively multimodal (text, image, audio, video, code).
- **Gemini 1.5 Pro (2024)**: 1M token context window (extended to 2M). MoE architecture (rumored). Breakthrough on long-context tasks.
- **Gemini 2.0 Flash (2025)**: Optimized for speed. Multimodal input/output including audio.
- **Training infrastructure**: TPUv4/v5 (Viperfish). Google's custom silicon is a key competitive advantage, with training FLOPS reportedly 5x GPT-4's pre-training compute.
- **Deployment**: Google AI Studio, Vertex AI, Android on-device (Nano).

#### 1.2.4 LLaMA (Meta)
- **LLaMA 1 (2023)**: 7B, 13B, 33B, 65B parameters. Trained on trillions of tokens from publicly available data exclusively. LLaMA-13B outperforms GPT-3 175B on most benchmarks. LLaMA-65B competitive with Chinchilla-70B and PaLM-540B.
- **LLaMA 2 (2023)**: 7B, 13B, 70B. 4K context. GQA on 70B. RLHF for chat variants. Open-weight with commercial license.
- **LLaMA 3 (2024)**: 8B, 70B (405B training). 8K context. 128K token vocabulary (up from 32K). GQA on all sizes. 15T+ training tokens (7x LLaMA 2). 4x more code in training data.
- **LLaMA 3.1 (2024)**: 8B, 70B, 405B. 128K context window.
- **Impact**: Democratized open-source LLM ecosystem. Foundation for hundreds of fine-tuned variants (Vicuna, Alpaca, CodeLlama, etc.).

#### 1.2.5 Mistral
- **Mistral 7B (2023)**: Sliding window attention (4096 window), GQA, byte-fallback BPE tokenizer, rolling buffer KV cache. Outperforms LLaMA 2 13B on all benchmarks. Apache 2.0 license.
- **Mixtral 8x7B (2024)**: Sparse MoE. 8 experts, top-2 routing. 47B total parameters, 13B active per token. Outperforms/matches LLaMA 2 70B and GPT-3.5. 32K context. Apache 2.0.
- **Mixtral 8x22B (2024)**: Larger MoE variant.
- **Mistral Large, Medium, Small**: Commercial API models.
- **Key innovation**: Demonstrated that smaller, well-architected models can match much larger ones, especially with MoE.

#### 1.2.6 Other Notable Models
- **Qwen (Alibaba)**: Strong multilingual performance, especially Chinese.
- **DeepSeek**: DeepSeek-V2 with MoE, DeepSeek-R1 with reasoning capabilities. Very competitive open-source.
- **Gemma (Google)**: Open-source. 2B and 7B. Based on Gemini research. 2B trained on 2T tokens, 7B on 6T tokens. 8K context.
- **Phi (Microsoft)**: Small language models (1.3B-14B) with surprisingly strong performance. Demonstrates data quality > data quantity.
- **Yi (01.AI)**: Strong Chinese/English bilingual models.
- **Command R+ (Cohere)**: Optimized for RAG and enterprise search.

### Key Architectural Decisions for System Design
1. **Closed vs open-weight**: Closed (GPT-4, Claude, Gemini) = higher ceiling, API dependency, data privacy concerns. Open (LLaMA, Mistral) = self-hosting, fine-tuning flexibility, but operational burden.
2. **Model size vs quality**: 7B models are 10-50x cheaper to serve than 70B but with meaningful quality gaps on complex tasks.
3. **Context window**: 4K -> 128K -> 1M represents fundamentally different application possibilities (single query vs document analysis vs codebase understanding).
4. **Multimodal needs**: GPT-4o and Gemini are natively multimodal; most open-source models are text-only or require separate vision encoders.

### Trade-offs and Failure Modes
- **API rate limits**: Closed-model APIs throttle under load. Must design for fallback/retry.
- **Model deprecation**: OpenAI regularly deprecates model versions. Pin to specific versions; plan for migration.
- **Benchmark gaming**: Leaderboard scores don't always correlate with production task performance. Always evaluate on your specific use case.
- **Context window utilization**: Longer context != better use of context. Models degrade on "needle in a haystack" tasks in the middle of long contexts (the "lost in the middle" phenomenon).

---

## 1.3 Tokenization

### What It Covers
The process of converting raw text into discrete tokens (integers) that models process. The tokenizer is the interface between human language and model computation.

### Why It Matters for System Design
Tokenization directly impacts: cost (you pay per token), context utilization (more efficient tokenizer = more text per context window), multilingual performance, and code handling.

### Core Concepts

#### 1.3.1 Byte-Pair Encoding (BPE)
- **Algorithm**: Start with character-level vocabulary. Iteratively merge the most frequent adjacent pairs until target vocabulary size is reached.
- **Properties**: Deterministic, greedy. Produces subword units. Common words become single tokens; rare words decompose into subwords.
- **Used by**: GPT-2, GPT-3, GPT-4, LLaMA, Mistral, most modern LLMs.
- **Vocabulary sizes**: GPT-2 (50,257), GPT-4/LLaMA 3 (128,000), LLaMA 1/2 (32,000).
- **Byte-fallback BPE (Mistral, LLaMA)**: Falls back to raw bytes for unknown characters, ensuring any text can be encoded.

#### 1.3.2 SentencePiece
- **Google's library**: Language-agnostic tokenization. Treats input as raw byte stream (no pre-tokenization assumptions about word boundaries).
- **Supports multiple algorithms**: BPE and Unigram within the same framework.
- **Used by**: T5, LLaMA (uses SentencePiece BPE), NLLB, mBART.
- **Advantage**: Handles whitespace and multilingual text uniformly.

#### 1.3.3 WordPiece
- **Algorithm**: Similar to BPE but merges based on likelihood (mutual information) rather than frequency.
- **Uses "##" prefix** for subword continuation tokens.
- **Used by**: BERT, DistilBERT, ELECTRA.
- **Largely historical**: Most new models use BPE.

#### 1.3.4 Unigram
- **Algorithm**: Starts with large vocabulary, probabilistically removes tokens that least impact encoding quality.
- **Properties**: Probabilistic (multiple valid segmentations possible). Can sample different tokenizations.
- **Used by**: T5 (via SentencePiece), XLNet.

#### 1.3.5 The Tokenization Pipeline
| Stage | Purpose | Example |
|-------|---------|---------|
| Normalizer | Standardize text (lowercasing, unicode) | "HELLO World" -> "hello world" |
| Pre-tokenizer | Split into preliminary chunks | "hello world" -> ["hello", " world"] |
| Model | Apply BPE/WordPiece/Unigram | ["hello", " world"] -> [9906, 1917] |
| Post-processor | Add special tokens (BOS, EOS) | [9906, 1917] -> [1, 9906, 1917, 2] |
| Decoder | Convert IDs back to text | [9906, 1917] -> "hello world" |

### Key System Design Decisions
1. **Vocabulary size impact**: Larger vocabulary (128K vs 32K) = fewer tokens per text = cheaper and more context-efficient, but larger embedding table and softmax layer.
2. **Multilingual encoding efficiency**: BPE trained primarily on English text is 2-5x less efficient on Chinese, Japanese, Korean, Arabic. LLaMA 3's 128K vocabulary dramatically improved multilingual token efficiency.
3. **Code tokenization**: Models with code-heavy training data develop better code-specific tokens. A single Python keyword might be 1 token in CodeLlama but 2-3 tokens in a general model.
4. **Cost calculation**: `cost = (input_tokens + output_tokens) * price_per_token`. A 2x more efficient tokenizer halves your API cost for the same text.

### Trade-offs and Failure Modes
- **Tokenization artifacts**: "SolidGoldMagikarp"-style tokens that exist in vocabulary but were never/rarely seen in training can cause erratic behavior.
- **Counting failures**: LLMs cannot reliably count characters/letters because tokenization obscures character boundaries.
- **Arithmetic edge cases**: Numbers are tokenized inconsistently (e.g., "123456" might be split as ["123", "456"] or ["12", "34", "56"]).
- **Vocabulary mismatch in fine-tuning**: Fine-tuning with a different tokenizer than the base model was trained with causes catastrophic failure.

### Real-World Examples
- OpenAI's `tiktoken` library: Fast, production BPE implementation. `cl100k_base` encoding for GPT-4.
- LLaMA 3's vocabulary expansion (32K -> 128K) improved token efficiency by ~15% on English and dramatically more on non-English languages.
- Anthropic's Claude uses a custom tokenizer optimized for code and instruction-following tasks.

---

## 1.4 Embeddings

### What It Covers
Dense vector representations of text (words, sentences, documents) in continuous vector spaces where semantic similarity corresponds to geometric proximity.

### Why It Matters for System Design
Embeddings are the foundation of RAG systems, semantic search, clustering, classification, and recommendation engines in GenAI applications. The embedding model choice determines retrieval quality, storage costs, and latency.

### Core Concepts

#### 1.4.1 Word-Level Embeddings (Historical)
- **Word2Vec (2013)**: Skip-gram and CBOW. Fixed vectors per word. 100-300 dimensions. Cannot handle polysemy.
- **GloVe**: Global matrix factorization approach. Similar use case and limitations.
- **FastText**: Subword-level, handles OOV words. Still fixed per word.
- **Limitation**: No contextual understanding. "Bank" has the same vector regardless of financial vs river context.

#### 1.4.2 Contextual / Sentence Embeddings
- **BERT-based**: CLS token or mean pooling over BERT outputs. 768 dimensions.
- **Sentence-BERT (SBERT)**: Siamese network fine-tuned for semantic similarity. Foundation of modern sentence embedding.
- **E5, BGE, GTE**: Modern embedding models optimized for retrieval. Trained with contrastive learning.
- **all-MiniLM-L6-v2**: 384 dimensions. Lightweight, CPU-friendly. Good for prototyping.
- **all-mpnet-base-v2**: 768 dimensions. Stronger quality.

#### 1.4.3 Production Embedding Models
| Model | Provider | Dimensions | Max Tokens | Notes |
|-------|----------|------------|------------|-------|
| text-embedding-ada-002 | OpenAI | 1536 | 8191 | Legacy. Good quality. |
| text-embedding-3-small | OpenAI | 512-1536 | 8191 | Matryoshka representation. Cheaper. |
| text-embedding-3-large | OpenAI | 256-3072 | 8191 | Matryoshka. Highest quality. |
| bge-large-en-v1.5 | BAAI | 1024 | 512 | Open-source. MTEB leader. |
| mxbai-embed-large-v1 | Mixedbread | 1024 | 512 | State-of-art open-source. |
| Cohere embed-v3 | Cohere | 1024 | 512 | Multilingual. Optimized for RAG. |
| Voyage-3 | Voyage AI | 1024 | 32000 | Long-context embedding. |
| Gemini Embedding | Google | 768 | 2048 | Integrated with Vertex AI. |

#### 1.4.4 Embedding Dimensions and Matryoshka Representation Learning (MRL)
- **Concept**: Train embeddings such that the first d dimensions form a valid lower-dimensional embedding. A 3072-dim embedding can be truncated to 256-dim with graceful quality degradation.
- **Impact**: Enables dynamic dimension selection based on latency/storage constraints.
- **OpenAI's text-embedding-3 models** support this natively via the `dimensions` parameter.

#### 1.4.5 Embedding Quantization
- **Binary quantization**: 32x compression (float32 -> 1-bit). 96% retrieval quality retained with rescoring. 24.76x speedup.
- **Scalar (INT8) quantization**: 4x compression. 99.3% quality retained with rescoring. 3.66x speedup.
- **Combined approach**: Binary for fast initial retrieval (top-40), INT8 for rescoring (top-10). Reduces 200GB memory to 5.2GB.
- **Calibration requirement**: INT8 quantization needs a calibration dataset for accurate range mapping.
- **Vector DB support**: Faiss, Qdrant, Milvus, Weaviate all support quantized embeddings.

#### 1.4.6 Similarity Metrics
- **Cosine similarity**: Angle between vectors. Most common. Normalized, so magnitude doesn't matter.
- **Dot product**: Faster. Requires normalized vectors to match cosine.
- **Euclidean distance**: L2 norm. Used in some HNSW implementations.
- **Choice matters**: Some models are trained with cosine similarity; using dot product on un-normalized vectors will give incorrect results.

### Key System Design Decisions
1. **Dimension selection**: 384-dim (fast, cheap) vs 1024-dim (quality) vs 3072-dim (max quality). Each dimension adds ~4 bytes per vector in float32.
2. **Open-source vs API**: Open-source (BGE, E5) = no API costs, full control, but need GPU for large-scale encoding. API (OpenAI, Cohere) = simpler but ongoing cost per encoding.
3. **Embedding model must match query and document**: You cannot embed documents with OpenAI and query with BGE. The model must be the same for both.
4. **Re-embedding cost**: Changing embedding models requires re-encoding your entire corpus. At scale (millions of documents), this is days of compute.

### Trade-offs and Failure Modes
- **Semantic gap**: Embeddings capture semantic similarity, not factual correctness. "The capital of France is Paris" and "The capital of France is London" will have high similarity.
- **Domain mismatch**: General-purpose embedding models underperform on specialized domains (medical, legal, financial). Domain-specific fine-tuning can improve retrieval by 10-30%.
- **Dimensionality vs cost**: At 1M documents with 1536-dim float32 vectors, storage = 6GB. At 3072-dim, it doubles. Binary quantization reduces this to ~190MB.
- **Stale embeddings**: When your source data changes, embeddings must be re-computed. No incremental "update" is possible.

### Connections to Other Topics
- Vector search / RAG systems (embeddings are the retrieval mechanism)
- Semantic caching (cache based on query embedding similarity)
- Fine-tuning embedding models (improves domain-specific retrieval)
- Chunking strategies (what text gets embedded determines retrieval quality)

---

## 1.5 Pre-training vs Post-training

### What It Covers
The multi-stage training pipeline that transforms a randomly initialized model into a useful, aligned AI assistant: pre-training (learning language), supervised fine-tuning (learning to follow instructions), and alignment (learning human preferences).

### Why It Matters for System Design
Understanding the training pipeline determines: which training stages you can realistically perform yourself, how to evaluate model quality, why certain failure modes occur (hallucination, refusal, jailbreaks), and how to improve model behavior through fine-tuning or alignment.

### Core Concepts

#### 1.5.1 Pre-training
- **Objective**: Next-token prediction (causal language modeling) on massive text corpora.
- **Data scale**: LLaMA trained on trillions of tokens from public data. LLaMA 3 used 15T+ tokens. Modern frontier models likely use 10-15T tokens.
- **Compute requirements**: LLaMA-65B required ~1M GPU-hours on A100s. GPT-4 estimated at 25,000+ A100s for months.
- **Chinchilla scaling laws**: Optimal training requires ~20 tokens per parameter. A 7B model should see 140B tokens. Modern practice over-trains relative to this (LLaMA 7B trained on 1T tokens = ~143x Chinchilla optimal).
- **Data composition matters**: LLaMA 3 used 4x more code than LLaMA 2, resulting in significantly better code performance.
- **Data quality > quantity**: Phi models (Microsoft) demonstrate that carefully curated data can match models trained on 10x more data.

**Pre-training is NOT something most companies should do.** Cost: $1M-$100M+. Expertise: requires ML infrastructure team. Time: weeks to months. Use pre-trained open-weight models instead.

#### 1.5.2 Supervised Fine-tuning (SFT) / Instruction Tuning
- **Objective**: Train on (instruction, response) pairs to teach the model to follow instructions.
- **Data**: 10K-100K high-quality instruction-response pairs. Quality matters far more than quantity.
- **Methods**: Full fine-tuning, LoRA, QLoRA (see Domain 3).
- **Key insight (ULMFiT)**: Three stages -- pretrain on large corpus, adapt to domain, fine-tune on task. Gradual unfreezing of layers prevents catastrophic forgetting.
- **Self-Instruct / Alpaca**: Use a strong model (GPT-4) to generate synthetic training data for a weaker model. Scalable but quality ceiling = teacher model.

#### 1.5.3 Reinforcement Learning from Human Feedback (RLHF)
- **InstructGPT pipeline (3 steps)**:
  1. Collect human-annotated prompt-response pairs for SFT
  2. Train a reward model from human preference rankings (which response is better?)
  3. Optimize the SFT model against the reward model using PPO (Proximal Policy Optimization)
- **Reward model**: Trained on pairwise comparisons. Given (prompt, response_A, response_B), predicts which humans prefer.
- **PPO challenges**: Unstable training, reward hacking, mode collapse, high computational cost (requires 4 models: policy, reference, reward, value).
- **Used by**: ChatGPT, GPT-4, Claude (early versions), LLaMA 2-Chat.

#### 1.5.4 Direct Preference Optimization (DPO)
- **Innovation**: Eliminates the separate reward model entirely. Derives the optimal policy in closed form from the reward modeling objective.
- **Training**: Simple classification loss on preference pairs (chosen vs rejected responses). No RL loop.
- **Advantages over RLHF/PPO**: Simpler to implement, more stable training, no sampling during fine-tuning, computationally cheaper.
- **Performance**: Matches or exceeds PPO-based RLHF on sentiment control, summarization, and dialogue tasks.
- **Used by**: Zephyr (distilled DPO -- dDPO), many open-source alignment efforts, increasingly adopted in industry.
- **Variants**: IPO, KTO, ORPO, SimPO -- active research area.

#### 1.5.5 Constitutional AI (CAI)
- **Anthropic's approach**: Replaces human preference labeling with a "constitution" -- a set of rules/principles.
- **Process**: Model critiques its own responses against the constitution, then revises. This generates preference data automatically.
- **RLAIF (RL from AI Feedback)**: Uses the model's own judgments (guided by constitution) instead of human labelers.
- **Advantage**: Scales better than human annotation. More consistent. Principles are explicitly stated and auditable.
- **Used by**: Claude models.

#### 1.5.6 Extended Thinking / Reasoning at Inference Time
- **Chain-of-thought at inference**: Models like OpenAI's o1/o3 and Claude's "extended thinking" allocate more compute at inference time for reasoning tasks.
- **Not a training stage per se**, but trained to use "thinking tokens" that are not shown to the user.
- **Trade-off**: Higher latency and cost for significantly better performance on math, code, logic, and planning tasks.

### Key System Design Decisions
1. **Which stages can you do?** Pre-training: almost never. SFT: yes, if you have good data. RLHF: rarely (complex). DPO: feasible with preference data.
2. **Buy vs build alignment**: Use API models (already aligned) vs fine-tune open-weight models (control alignment yourself).
3. **Data flywheel**: Collect user feedback to generate preference pairs for ongoing DPO/RLHF. This is how production systems improve over time.

### Trade-offs and Failure Modes
- **RLHF reward hacking**: Model learns to game the reward model rather than genuinely improve.
- **Mode collapse**: RLHF can make models overly verbose or sycophantic.
- **DPO distribution drift**: If preference data distribution is far from the SFT model's output distribution, DPO can underperform.
- **Alignment tax**: Alignment can reduce performance on certain capabilities (e.g., over-refusal on benign requests).
- **Catastrophic forgetting**: Full fine-tuning on a narrow domain can destroy general capabilities.

### Real-World Pipeline Example
```
Raw text corpus (15T tokens)
  -> Pre-training (next-token prediction) -> Base model (LLaMA 3)
    -> SFT on instruction data (100K examples) -> Instruct model
      -> DPO on preference pairs (50K pairs) -> Aligned model
        -> Safety fine-tuning (Constitutional AI / red-teaming) -> Production model
```

---

## 1.6 Mixture of Experts (MoE) Architecture

### What It Covers
A sparse architecture that replaces dense FFN layers with multiple "expert" subnetworks, routing each token to only a subset of experts. This enables models with massive parameter counts but manageable inference compute.

### Why It Matters for System Design
MoE enables a fundamentally different cost-quality tradeoff: you get the knowledge capacity of a very large model with the inference cost of a much smaller one. This directly impacts GPU memory planning, serving costs, and model selection.

### Core Concepts

#### 1.6.1 Architecture
- **Standard MoE layer**: Replace FFN with N expert FFN networks + a router/gating network.
- **Output**: `y = sum(G(x)_i * E_i(x))` where G is the gate function and E are experts.
- **Sparse activation**: Only k experts are activated per token (typically k=1 or k=2).
- **Expert structure**: Each expert is typically an identical FFN architecture. Only weights differ.
- **Placement**: Usually replaces every other FFN layer (GShard pattern) or every FFN layer.

#### 1.6.2 Routing Mechanisms
- **Noisy Top-k Gating (Shazeer, 2017)**: Add tunable Gaussian noise to router logits, then keep top-k, apply softmax. The noise encourages exploration across experts.
- **Top-1 routing (Switch Transformer)**: Simplified to single expert per token. Reduced compute and communication. Halved expert batch sizes.
- **Top-2 routing (Mixtral, GShard)**: Each token routed to 2 experts. Second expert picked probabilistically in some implementations.
- **Expert Choice routing**: Flips the paradigm -- experts choose their tokens rather than tokens choosing experts. Better load balancing.

#### 1.6.3 Load Balancing
- **Problem**: Without intervention, a few "popular" experts receive most tokens while others are underutilized.
- **Auxiliary loss**: Encourages uniform routing by penalizing uneven distribution. Computed as coefficient of variation of expert importance scores.
- **Router Z-loss (ST-MoE)**: Penalizes large logits entering the gating network. Reduces roundoff errors and improves stability.
- **Expert capacity**: Each expert has a maximum token capacity per batch. `Expert Capacity = (tokens_per_batch / num_experts) * capacity_factor`. Tokens exceeding capacity overflow and skip that expert.
- **Capacity factor**: 1.0-1.25 recommended. Higher = more memory, less token dropping.

#### 1.6.4 Key Models
| Model | Experts | Active | Total Params | Active Params | Routing |
|-------|---------|--------|-------------|---------------|---------|
| Switch Transformer | 2048 | 1 | 1.6T | ~1B | Top-1 |
| GShard | 2048 | 2 | 600B | ~1B | Top-2 |
| Mixtral 8x7B | 8 | 2 | 46.7B | 12.8B | Top-2 |
| Mixtral 8x22B | 8 | 2 | ~141B | ~39B | Top-2 |
| DeepSeek-V2 | 160 | 6 | 236B | 21B | Top-6 |
| GPT-4 (rumored) | 16 | 2 | ~1.8T | ~220B | Top-2 |
| Gemini (rumored) | Unknown | Unknown | Unknown | Unknown | Unknown |

#### 1.6.5 Expert Specialization
- **Encoder experts**: Tend to specialize in token categories (punctuation, proper nouns, verbs).
- **Decoder experts**: Less clear specialization, likely due to load balancing pressure.
- **Multilingual**: Experts do NOT specialize by language. Tokens route across languages.

### Key System Design Decisions
1. **Memory vs compute**: Mixtral 8x7B needs 47B parameters in VRAM (all experts loaded) but only computes with 13B per token. You need the memory of a 47B model for the compute of a 13B model.
2. **MoE vs dense for deployment**: If VRAM-constrained (single GPU), dense models may be better. If multi-GPU/multi-node, MoE wins on throughput.
3. **Expert parallelism**: Each GPU holds a subset of experts. Requires all-to-all communication for routing. High-bandwidth interconnect (NVLink) critical.
4. **Fine-tuning MoE**: Sparse models overfit more easily. Freeze non-expert weights for stability. Use higher regularization. MoE benefits disproportionately from instruction tuning.

### Trade-offs and Failure Modes
- **Token dropping**: When experts overflow, tokens are dropped. This can cause information loss.
- **Communication overhead**: All-to-all routing across GPUs is bandwidth-intensive.
- **Uneven expert utilization**: Poor routing means some experts are wasted parameters.
- **Fine-tuning challenges**: Worse generalization than dense on small datasets. Better on knowledge-heavy tasks, worse on reasoning.
- **Quantization complexity**: Must quantize experts individually; extreme compression possible (QMoE: <1 bit/param, 1.6T Switch Transformer 3.2TB -> 160GB).

### Efficiency Optimizations
- **MegaBlocks**: Block-sparse GPU kernels for dynamic expert assignment. No token dropping. 17x+ speedups.
- **QMoE**: Extreme quantization for deployment.
- **Hierarchical all-to-all**: Tree-based communication reduces routing hops.
- **Task-level routing**: Static expert assignment per task. Preload only k experts. 2.6x throughput gain.

### Connections to Other Topics
- GPU compute requirements (1.6 affects VRAM planning)
- Model parallelism (expert parallelism is a distinct strategy)
- Fine-tuning (MoE has unique challenges)
- Quantization (expert-aware quantization required)
- KV cache management (attention layers are shared across experts -- only FFN differs)

---

## 1.7 Multimodal Models

### What It Covers
Models that process and generate across multiple modalities: text, images, audio, video, and structured data.

### Why It Matters for System Design
Multimodal capabilities enable new application categories (visual QA, document understanding, audio agents) and require different infrastructure (image preprocessing, audio streaming, larger context windows for visual tokens).

### Core Concepts

#### 1.7.1 Vision-Language Models (VLMs)
- **Architecture pattern**: Vision encoder (e.g., ViT/CLIP) + projection layer + LLM decoder.
- **Image tokenization**: Images are encoded into a sequence of visual tokens (e.g., 576 tokens for a 336x336 image in LLaVA). These tokens consume context window space.
- **GPT-4V / GPT-4o**: Natively multimodal. Can understand charts, diagrams, screenshots, handwriting.
- **Claude Vision**: Supports image input across all Claude 3+ models. Up to 20 images per request.
- **Gemini**: Natively multimodal from pre-training (not bolted-on vision encoder). Processes text, image, audio, video interleaved.
- **Open-source**: LLaVA, InternVL, Qwen-VL, CogVLM.

#### 1.7.2 Audio Models
- **Whisper (OpenAI)**: Encoder-decoder transformer for ASR. 1.5B parameters. Trained on 680K hours. Multilingual.
- **GPT-4o audio**: Native audio input/output. Real-time voice conversation with <500ms latency.
- **Gemini audio**: Native audio processing including music understanding.

#### 1.7.3 Video Understanding
- **Gemini 1.5**: Can process up to 1 hour of video within its context window.
- **Approach**: Sample frames at regular intervals, encode each as visual tokens.
- **Challenge**: Video generates enormous token counts (1 hour = potentially millions of visual tokens).

#### 1.7.4 Document Understanding
- **Layout-aware models**: Process document structure (tables, headers, columns).
- **Use cases**: Invoice processing, contract analysis, form extraction.
- **Models**: DocTR, LayoutLM, GPT-4V (with prompting for document analysis).

### Key System Design Decisions
1. **Visual token budget**: Images consume significant context window space. A 4K context model can only process a few images. Need 128K+ for document-heavy workloads.
2. **Preprocessing pipeline**: Image resizing, compression, format conversion must happen before the model. Latency adds up.
3. **Cost**: Visual tokens are typically charged at image-level rates. GPT-4V charges per image based on resolution.
4. **Modality-specific preprocessing**: Audio needs resampling, VAD (voice activity detection), streaming chunking. Video needs frame extraction, scene detection.

### Trade-offs
- **Native vs bolted-on multimodal**: GPT-4o and Gemini (natively multimodal from pre-training) generally outperform architectures that add vision post-hoc.
- **Context consumption**: A single high-res image might use 1000+ tokens worth of context, reducing available text context.
- **Hallucination on images**: VLMs can confidently describe content not present in images. Evaluation is harder than text-only.

---

# DOMAIN 2: LLM ARCHITECTURE & INFERENCE

---

## 2.1 Model Serving Infrastructure

### What It Covers
The software frameworks and systems that serve LLM inference in production: handling requests, managing GPU resources, optimizing throughput and latency.

### Why It Matters for System Design
The inference serving layer is where cost, latency, and reliability are determined. A well-optimized serving stack can reduce costs by 4-10x compared to naive deployment.

### Core Concepts

#### 2.1.1 vLLM
- **Core innovation**: PagedAttention -- manages KV cache like virtual memory pages, eliminating fragmentation.
- **Continuous batching**: Immediately removes completed sequences and starts new ones, maximizing GPU utilization.
- **Performance**: 2-4x throughput improvement over naive HuggingFace serving.
- **Supported features**: Speculative decoding, automatic prefix caching, FP8/INT8/AWQ/GPTQ quantization.
- **Deployment**: Docker, Kubernetes, Ray Serve, Modal, SkyPilot, AWS SageMaker.
- **OpenAI-compatible API**: Drop-in replacement for OpenAI API endpoints.
- **Model support**: Generative, pooling (embeddings), multimodal, MoE, encoder-decoder.
- **Parallelism**: Data parallel, expert parallel, context parallel configurations.
- **Community**: Most popular open-source LLM serving framework. Strong ecosystem.

#### 2.1.2 TensorRT-LLM (NVIDIA)
- **Architecture**: Built on PyTorch. High-level Python API for model definition and optimization.
- **Quantization**: FP8, FP4, INT4 AWQ, INT8 SmoothQuant, mixed precision.
- **Key features**: Custom attention kernels, inflight batching, paged KV caching, speculative decoding (including N-gram), multi-block attention for long sequences, disaggregated serving.
- **Performance benchmarks**: 40,000 tokens/sec on B200 GPUs (LLaMA 4), 24,000 tokens/sec (LLaMA 3), 3.6x throughput boost with speculative decoding, 3x faster AllReduce with NVSwitch.
- **Supported models**: LLaMA 3/4, GPT-OSS, DeepSeek R1/V3, Mixtral, EXAONE.
- **Deployment**: NVIDIA Dynamo, Triton Inference Server, Kubernetes auto-scaling.
- **Best for**: Maximum performance on NVIDIA hardware. Production deployments requiring lowest latency.

#### 2.1.3 Text Generation Inference (TGI) -- Hugging Face
- **Focus**: Production-ready serving for HuggingFace models.
- **Features**: Continuous batching, tensor parallelism, quantization (GPTQ, AWQ, bitsandbytes).
- **Deployment**: HuggingFace Inference Endpoints, self-hosted Docker.
- **Integration**: Native HuggingFace hub integration. Easy model loading.

#### 2.1.4 Triton Inference Server (NVIDIA)
- **Purpose**: General-purpose model serving (not LLM-specific).
- **Features**: Multi-framework support (TensorRT, PyTorch, ONNX), dynamic batching, model ensemble, A/B testing.
- **Use case**: When serving LLMs alongside traditional ML models in a unified platform.
- **Integration**: Pairs with TensorRT-LLM as the LLM backend.

#### 2.1.5 SGLang
- **Innovation**: Structured generation language. Optimizes for structured output (JSON, regex-constrained generation).
- **RadixAttention**: Efficient prefix caching with radix tree data structure.
- **Competitive with vLLM** on throughput, sometimes faster for structured generation workloads.

#### 2.1.6 Ollama / llama.cpp
- **llama.cpp**: C/C++ implementation of LLaMA inference. CPU and GPU (Metal, CUDA, ROCm). Uses GGUF quantized formats.
- **Ollama**: User-friendly wrapper around llama.cpp. Run LLMs locally on laptop.
- **Use case**: Development, prototyping, edge/on-device deployment. Not for high-throughput production serving.

### Key System Design Decisions
1. **vLLM vs TensorRT-LLM**: vLLM = broader model support, easier setup, community-driven. TensorRT-LLM = maximum NVIDIA GPU utilization, tighter optimization, more complex setup.
2. **Self-hosted vs managed**: Self-hosted (vLLM/TGI on your GPUs) vs managed (HuggingFace Endpoints, AWS SageMaker, Replicate). Self-hosted is cheaper at scale but requires ML ops expertise.
3. **Single model vs model router**: Production systems often route between models (fast/cheap for simple queries, powerful/expensive for complex ones).
4. **Autoscaling**: GPU autoscaling is slow (minutes to start new instances). Must plan for traffic spikes with pre-warmed instances.

### Trade-offs and Failure Modes
- **Cold start**: Loading a 70B model takes 30-60 seconds. First request latency is unacceptable without pre-warming.
- **OOM crashes**: KV cache growth is unbounded during inference. Without PagedAttention, a single long-context request can OOM the entire server.
- **Batching efficiency**: High batch sizes improve throughput but increase latency for individual requests. Must tune based on SLA requirements.
- **Quantization compatibility**: Not all serving frameworks support all quantization formats. Verify before committing.

---

## 2.2 GPU Compute

### What It Covers
The GPU hardware landscape for LLM training and inference: architectures, memory, bandwidth, and cost considerations.

### Why It Matters for System Design
GPU selection determines cost, throughput, maximum model size, and deployment density. The memory bandwidth bottleneck, not compute, is the primary constraint for LLM inference.

### Core Concepts

#### 2.2.1 NVIDIA GPU Lineup
| GPU | Memory | Bandwidth | FP16 TFLOPS | FP8 TFLOPS* | Interconnect | Use Case |
|-----|--------|-----------|-------------|-------------|--------------|----------|
| A100 (80GB) | 80GB HBM2e | 2.0 TB/s | 312 | N/A | NVLink 600GB/s | Training + inference. Current workhorse. |
| H100 SXM | 80GB HBM3 | 3.35 TB/s | 1,979* | 3,958* | NVLink 900GB/s | Next-gen training + inference. 4x A100 on training. |
| H100 NVL | 94GB HBM3 | 3.9 TB/s | 1,671* | 3,341* | NVLink 600GB/s | Inference-optimized. More memory. |
| H200 | 141GB HBM3e | 4.8 TB/s | ~1,979* | ~3,958* | NVLink 900GB/s | Maximum memory. Larger models without parallelism. |
| B200 | 192GB HBM3e | 8 TB/s | ~4,500* | ~9,000* | NVLink 1.8TB/s | Next-gen. 2x H100 on inference. |

*With sparsity

#### 2.2.2 Why Memory Bandwidth Matters More Than Compute
- **LLM inference is memory-bandwidth bound**, not compute-bound.
- **Prefill phase**: Processing input tokens. Compute-bound (matrix-matrix multiplication). GPU utilization is high.
- **Decode phase**: Generating tokens one at a time. Memory-bound (matrix-vector multiplication). Speed is limited by how fast weights can be loaded from HBM.
- **Implication**: H100's 3.35 TB/s bandwidth vs A100's 2.0 TB/s = ~67% faster decode, not the 4x that raw TFLOPS would suggest.
- **KV cache bandwidth**: Reading the KV cache during attention also consumes bandwidth. Longer sequences = more bandwidth consumed per token.

#### 2.2.3 Memory Planning
- **Model weights**: `parameters * bytes_per_param`. LLaMA-70B in FP16 = 140GB (2 GPUs minimum).
- **KV cache**: `2 * num_layers * num_heads * head_dim * precision_bytes * seq_len * batch_size`. LLaMA-7B, batch=1, seq=4096, FP16 = ~2GB.
- **Activations**: Temporary memory during forward pass. Significant for training; smaller for inference.
- **Rule of thumb**: Reserve 60-70% of VRAM for weights, 20-30% for KV cache, 10% for overhead.

#### 2.2.4 Multi-GPU Configurations
- **DGX H100**: 8x H100 GPUs, NVLink interconnect. ~$300K-$400K. Typical production unit.
- **NVLink vs PCIe**: NVLink provides 900 GB/s vs PCIe Gen5's 128 GB/s. Essential for tensor parallelism.
- **Multi-node**: InfiniBand or RoCE for inter-node communication. Needed for 405B+ models.

#### 2.2.5 Alternative Hardware
- **Google TPU v5e/v5p**: Custom ASIC. Optimized for large-batch inference and training. Used exclusively in GCP.
- **AMD MI300X**: 192GB HBM3. Competitive with H100 on some workloads. Growing ROCm ecosystem.
- **Intel Gaudi 2/3**: Alternative accelerator. Supported by some frameworks.
- **Apple Silicon (M1/M2/M3)**: Unified memory. Surprisingly capable for small model inference via llama.cpp/MLX. 128GB M2 Ultra can run 70B quantized models.
- **AWS Inferentia/Trainium**: Custom chips for AWS. Cost-effective for specific workloads.

### Key System Design Decisions
1. **GPU generation**: A100 is ~50% cheaper per GPU-hour than H100 but 2-4x slower. Evaluate cost-per-token, not cost-per-GPU.
2. **GPU memory vs GPU count**: A single H200 (141GB) can run LLaMA-70B in FP16 without parallelism. 2x A100 (80GB) requires tensor parallelism overhead.
3. **Cloud vs on-prem**: Cloud GPU prices ($2-4/hr H100) vs on-prem ($30K-40K per GPU amortized over 3 years). Break-even is typically at 50-70% utilization.
4. **Spot instances**: 60-80% discount but can be preempted. Good for batch inference, not real-time serving.

### Trade-offs and Failure Modes
- **GPU memory fragmentation**: Without PagedAttention, memory fragments as requests complete, reducing effective capacity.
- **Thermal throttling**: Sustained load reduces clock speeds. Monitor GPU temperatures in production.
- **Driver/CUDA compatibility**: Specific framework versions require specific CUDA versions. Dependency management is non-trivial.
- **NVLink failure**: If one GPU in an NVLink domain fails, the entire domain may be affected.

---

## 2.3 Quantization

### What It Covers
Reducing the numerical precision of model weights (and sometimes activations) from FP32/FP16 to INT8, INT4, or lower, trading small accuracy reductions for large memory and speed gains.

### Why It Matters for System Design
Quantization is the most impactful single optimization for inference cost. A 4-bit quantized model uses 4x less memory than FP16, enabling larger batch sizes or deployment on smaller GPUs.

### Core Concepts

#### 2.3.1 Quantization Fundamentals
- **Symmetric quantization**: Maps floating-point range [-max, max] to integer range [-127, 127]. Simple but wastes range if distribution is asymmetric.
- **Asymmetric (zero-point) quantization**: Maps [min, max] to [0, 255]. Better utilization of integer range but slightly more complex.
- **Per-tensor vs per-channel vs per-group**: Granularity of quantization. Per-group (e.g., 128 weights share a scale factor) balances accuracy and overhead.
- **Weight-only quantization**: Only quantize weights (static). Activations remain in FP16. Simpler, less accuracy loss.
- **Weight + activation quantization**: Both quantized. Higher speedup but harder to maintain quality due to activation outliers.

#### 2.3.2 Post-Training Quantization (PTQ) Methods

**GPTQ (Frantar et al., 2023)**
- Processes layers sequentially using inverse Hessian matrices to identify weight importance.
- Redistributes quantization error across related weights.
- Requires calibration dataset (small, ~128 samples).
- INT4 with group_size=128 is the standard configuration.
- Serializable -- quantized models can be shared directly.
- **Performance**: LLaMA-2-13B: 58.03 avg benchmark (vs 58.66 FP16). Only ~1% degradation.
- **Inference speed**: 2x faster than bitsandbytes for text generation. exllama kernels critical.
- **Quantization time**: ~4 GPU hours for 175B model.
- **Used by**: TheBloke's quantized model collection (thousands of models on HuggingFace).

**AWQ (Activation-Aware Weight Quantization, MIT/MLSys 2024 Best Paper)**
- Key insight: Protecting only 1% of salient weights (determined by activation magnitude) greatly reduces quantization error.
- Per-channel scaling based on offline activation statistics.
- TinyChat framework: 3x+ speedup over HuggingFace FP16 on both desktop and mobile GPUs.
- Can run LLaMA-2 70B on mobile hardware.
- Outperforms GPTQ on coding and math benchmarks.

**bitsandbytes (LLM.int8() and NF4)**
- **INT8 (LLM.int8())**: Mixed-precision decomposition. Outlier features (>6 magnitude) computed in FP16, rest in INT8. Zero degradation on benchmarks. 2x memory reduction. 15-23% speed penalty on large models.
- **NF4 (4-bit NormalFloat)**: Information-theoretically optimal for normally distributed weights. Used by QLoRA.
- **Zero-shot**: No calibration dataset required. Works on any model with nn.Linear layers.
- **4-bit not serializable**: Must quantize at load time (unlike GPTQ).
- **Best for**: Fine-tuning with LoRA adapters (faster than GPTQ for training).

**GGUF (llama.cpp format)**
- Hierarchical block quantization with super-blocks containing sub-blocks.
- Each level has its own scale factor, enabling mixed-precision.
- Supports Q4_0, Q4_1, Q5_0, Q5_1, Q8_0 and many more formats.
- Designed for CPU+GPU hybrid inference.
- Ubiquitous for local/edge deployment.

#### 2.3.3 Quantization-Aware Training (QAT)
- Inserts "fake quantization" during training: quantize -> dequantize -> train normally.
- Optimizer finds weights that are robust to quantization error ("wider minima").
- Higher quality than PTQ at same bit-width but requires training compute.
- Used for extreme quantization (INT4, INT2).

#### 2.3.4 Extreme Quantization
- **BitNet 1.58b**: Ternary weights (+1, 0, -1). Multiplication replaced with addition/subtraction. "13B BitNet 1.58b is more efficient than 3B FP16."
- **QMoE**: <1 bit per parameter. Switch Transformer 1.6T from 3.2TB to 160GB.
- **FP8**: H100 native support. 2x throughput vs FP16 with minimal accuracy loss. Becoming standard for training and inference on Hopper+ GPUs.

### Key System Design Decisions
1. **INT8 vs INT4**: INT8 = near-zero quality loss, 2x compression. INT4 = ~1-3% quality loss, 4x compression. For most applications, INT4 GPTQ/AWQ is the sweet spot.
2. **GPTQ vs AWQ vs bitsandbytes**:
   - Production inference: GPTQ or AWQ (serializable, fast).
   - Fine-tuning: bitsandbytes (no calibration, fast training).
   - Deployment pipeline: bitsandbytes for training -> GPTQ/AWQ for serving.
3. **Quantization + serving framework**: Verify compatibility. vLLM supports AWQ, GPTQ, FP8. TensorRT-LLM supports FP8, AWQ, SmoothQuant.
4. **Model size determines tolerance**: Larger models (70B+) tolerate quantization better. 7B models show more degradation at INT4.

### Benchmarks Summary
| Model | Method | Avg Benchmark | vs FP16 | Memory | Generation Speed |
|-------|--------|--------------|---------|--------|-----------------|
| LLaMA-2-7B | FP16 | 54.32 | baseline | 14GB | baseline |
| LLaMA-2-7B | bitsandbytes 4-bit | 53.40 | -1.7% | 3.5GB | ~0.5x |
| LLaMA-2-7B | GPTQ 4-bit | 53.23 | -2.0% | 3.5GB | ~2x faster than bnb |
| LLaMA-2-13B | FP16 | 58.66 | baseline | 26GB | baseline |
| LLaMA-2-13B | GPTQ 4-bit (act_order) | 58.03 | -1.1% | 6.5GB | ~2x faster than bnb |
| BLOOM-176B | FP16 | -- | baseline | 352GB (8x A100) | 239ms/tok |
| BLOOM-176B | INT8 | -- | ~0% loss | 176GB (4x A100) | 282ms/tok |

### Trade-offs and Failure Modes
- **Outlier features**: Activation outliers at large model scale (>6B params) cause classic INT8 to fail catastrophically. Mixed-precision (LLM.int8()) or SmoothQuant required.
- **Calibration data dependency**: GPTQ quality depends on calibration data. Poor calibration = poor quantized model.
- **Perplexity vs task performance**: Perplexity may increase slightly but downstream task performance can be preserved. Always evaluate on your specific task.
- **Quantization does NOT speed up prefill**: Prefill is compute-bound, not memory-bound. Quantization primarily speeds up the decode phase.

---

## 2.4 KV Cache Management

### What It Covers
Managing the key-value tensors cached during autoregressive generation to avoid redundant computation. The KV cache is the single largest memory consumer during inference after model weights.

### Why It Matters for System Design
KV cache management directly determines: maximum sequence length, maximum batch size, memory utilization efficiency, and therefore cost per token. Poor KV cache management is the #1 cause of OOM failures in production LLM serving.

### Core Concepts

#### 2.4.1 Why KV Cache Exists
- During autoregressive generation, each new token needs to attend to all previous tokens.
- Without caching, generating token N requires recomputing attention for all N-1 previous tokens.
- KV cache stores the K and V projections from all previous tokens in all layers.
- **Size formula**: `2 * num_layers * num_kv_heads * head_dim * precision_bytes * seq_len * batch_size`
- **Example**: LLaMA-7B, batch=1, seq=4096, FP16: ~2GB. At batch=32: ~64GB (more than the model weights!).

#### 2.4.2 PagedAttention (vLLM)
- **Inspiration**: Virtual memory paging in operating systems.
- **Problem solved**: Traditional KV cache pre-allocates contiguous memory for max sequence length. This causes massive internal fragmentation (60-80% waste for variable-length sequences).
- **Solution**: Store KV cache in non-contiguous fixed-size blocks. Use block tables (like page tables) to map logical positions to physical blocks.
- **Benefits**: Near-zero memory waste, enables larger batch sizes, 2-4x throughput improvement.
- **Copy-on-write**: Enables efficient beam search and parallel sampling by sharing KV cache blocks across sequences.

#### 2.4.3 Continuous Batching (In-Flight Batching)
- **Problem**: Static batching waits for the longest sequence in a batch to complete before processing new requests. If one request generates 10 tokens and another generates 500, the short request's GPU is idle for 490 tokens.
- **Solution**: Remove completed sequences immediately and insert new requests mid-batch.
- **Impact**: Dramatically improves GPU utilization in real-world workloads where generation lengths vary significantly.
- **Supported by**: vLLM, TensorRT-LLM, TGI, SGLang.

#### 2.4.4 KV Cache Compression
- **FP8 KV cache**: Quantize cached keys/values to FP8 instead of FP16. 2x reduction. Supported by TensorRT-LLM, vLLM.
- **Grouped-query attention reduces cache**: GQA with fewer KV heads directly reduces cache size proportionally. LLaMA-2 70B with 8 KV heads (vs 64 in MHA) = 8x cache reduction.
- **Sliding window attention (Mistral)**: Only cache the last W tokens. Rolling buffer discards older entries. Constant memory regardless of sequence length.
- **Token merging/eviction**: Intelligently drop or merge KV entries for less-important tokens. Research-active area.

#### 2.4.5 Prefix Caching
- **Concept**: If multiple requests share the same system prompt (e.g., all use the same 2000-token system message), cache the KV for that prefix and reuse it.
- **Impact**: Eliminates redundant computation for shared prefixes. Critical for production systems with consistent system prompts.
- **vLLM**: Automatic prefix caching.
- **SGLang**: RadixAttention uses radix tree for efficient prefix sharing.
- **Anthropic/OpenAI**: Offer prompt caching features in their APIs with reduced pricing for cached tokens.

### Key System Design Decisions
1. **KV cache budget**: Decide what fraction of GPU memory to allocate to KV cache vs weights. This determines max concurrent requests.
2. **Sequence length limits**: Enforce maximum sequence length per request to prevent a single long request from consuming all KV cache.
3. **Prefix caching strategy**: Standardize system prompts across requests to maximize cache reuse.
4. **GQA model preference**: Prefer GQA models (LLaMA 3, Mistral) over MHA models for inference -- smaller KV cache = more concurrent requests.

### Trade-offs and Failure Modes
- **OOM from KV cache growth**: A single 128K context request on LLaMA-70B FP16 consumes ~40GB of KV cache alone.
- **Fragmentation without paging**: Traditional allocation wastes 60-80% of KV cache memory on padding.
- **Sliding window information loss**: With Mistral's 4096 sliding window, information beyond 4096 tokens ago is lost (though the model can still propagate information through hidden states).

---

## 2.5 Speculative Decoding

### What It Covers
Using a smaller, faster "draft" model to predict multiple tokens, then verifying them in parallel with the larger "target" model. Accelerates inference without changing the output distribution.

### Why It Matters for System Design
Speculative decoding can provide 2-3x inference speedup with zero quality loss. It's one of the few "free lunch" optimizations in LLM inference.

### Core Concepts

#### 2.5.1 How It Works
1. **Draft phase**: A small model (e.g., 1B parameters) generates K candidate tokens autoregressively.
2. **Verify phase**: The large target model processes all K draft tokens in a single forward pass (like prefill -- compute-bound, efficient).
3. **Accept/reject**: Compare draft and target distributions. Accept matching tokens; reject and resample at the first mismatch.
4. **Mathematical guarantee**: The output distribution is identical to the target model alone. No quality loss.

#### 2.5.2 Performance
- **2-3x speedup** on T5-XXL (Leviathan et al., 2023).
- **TensorRT-LLM**: 3.6x throughput boost with speculative decoding.
- **Acceptance rate**: Depends on how well the draft model approximates the target. Higher agreement = more tokens accepted per speculation round.
- **Optimal K**: Typically 3-8 draft tokens. Too many = wasted compute on rejected tokens.

#### 2.5.3 Draft Model Selection
- **Separate small model**: LLaMA-7B drafting for LLaMA-70B. Requires draft model loading.
- **Same model, fewer layers**: Use the first N layers of the target model as the draft.
- **N-gram speculation**: Use the input prompt's n-gram statistics to predict likely next tokens. No draft model needed. Supported by TensorRT-LLM.
- **Medusa heads**: Add multiple lightweight prediction heads to the target model. Each head predicts a different future position. No separate model.

### Key System Design Decisions
1. **Draft model overhead**: The draft model consumes GPU memory. Ensure total memory (target + draft + KV caches) fits in VRAM.
2. **When to use**: Best for single-request latency optimization. Less impactful when already throughput-optimized with large batches (batch processing saturates GPU compute).
3. **Draft-target alignment**: The draft model should be from the same family or fine-tuned on similar data. Poor alignment = low acceptance rate = no speedup.

### Trade-offs
- **Memory overhead**: Draft model weights + additional KV cache.
- **Diminishing returns at high batch sizes**: When GPUs are already compute-saturated, speculative decoding adds overhead without benefit.
- **Implementation complexity**: Correct implementation of the acceptance-rejection sampling is non-trivial.

---

## 2.6 Model Parallelism

### What It Covers
Strategies for distributing model computation across multiple GPUs when a model doesn't fit in a single GPU's memory.

### Why It Matters for System Design
Any model larger than ~30B parameters in FP16 requires multi-GPU deployment. The parallelism strategy determines latency, throughput, and hardware utilization.

### Core Concepts

#### 2.6.1 Tensor Parallelism (TP)
- **How**: Split individual layers (attention heads, MLP weight matrices) across GPUs. Each GPU holds a slice of every layer.
- **Communication**: All-reduce after each layer. Requires high-bandwidth interconnect (NVLink, not PCIe).
- **Latency**: Same as single GPU for each token (parallel computation). No pipeline bubbles.
- **Best for**: Reducing per-token latency. Within a single node (NVLink).
- **Example**: LLaMA-70B with TP=4 on 4x H100. Each GPU holds 1/4 of every layer's weights. All-reduce 4x per layer.

#### 2.6.2 Pipeline Parallelism (PP)
- **How**: Split the model vertically -- GPU 0 runs layers 0-15, GPU 1 runs layers 16-31, etc.
- **Communication**: Send activations between stages. Lower bandwidth requirement than TP.
- **Pipeline bubbles**: Some GPUs idle while others process. Microbatching reduces bubbles.
- **Best for**: Multi-node deployment where inter-node bandwidth is limited.
- **Example**: LLaMA-70B with PP=2 across 2 nodes. Each node runs half the layers.

#### 2.6.3 Data Parallelism (DP)
- **How**: Replicate the full model on each GPU. Each GPU processes different requests.
- **Communication**: None during inference (each GPU is independent).
- **Best for**: Scaling throughput when the model fits on a single GPU.
- **Example**: LLaMA-7B INT4 on 4x A100s. Each GPU independently serves requests. 4x throughput.

#### 2.6.4 Expert Parallelism (EP) -- for MoE
- **How**: Distribute experts across GPUs. Each GPU holds a subset of experts.
- **Communication**: All-to-all for routing tokens to correct experts.
- **Used by**: Mixtral, DeepSeek, Switch Transformer deployments.

#### 2.6.5 Sequence Parallelism
- **How**: Split the sequence dimension across GPUs for operations not amenable to TP (LayerNorm, Dropout).
- **Reduces activation memory**: Each GPU only stores activations for its sequence chunk.
- **Used alongside TP** in modern training setups.

#### 2.6.6 Context Parallelism / Ring Attention
- **How**: Split long sequences across GPUs. Each GPU computes attention for its chunk, passing KV states in a ring topology.
- **Enables**: Very long context processing (1M+ tokens) that wouldn't fit in single-GPU KV cache.
- **Used by**: Systems processing extremely long documents or codebases.

### Key System Design Decisions
1. **TP vs PP**: TP for latency-sensitive serving within a node. PP for multi-node or when NVLink isn't available.
2. **TP degree**: Must divide the number of attention heads evenly. TP=2, 4, 8 are standard.
3. **Combined strategies**: Production often uses TP within a node + PP across nodes + DP for multiple replicas.
4. **Hardware topology**: TP requires NVLink-speed interconnect (900 GB/s). PP can work with PCIe or InfiniBand (200-400 GB/s).

### Trade-offs
- **TP overhead**: All-reduce per layer adds latency proportional to tensor size / NVLink bandwidth. At TP=8, this can be 15-20% overhead.
- **PP bubble overhead**: 10-25% efficiency loss from pipeline bubbles unless microbatching is well-tuned.
- **Failure domains**: TP failure on one GPU kills the entire request. PP failure on one stage kills the pipeline.

---

## 2.7 Inference Optimization

### What It Covers
The full stack of optimizations that reduce latency, increase throughput, and lower cost for LLM inference.

### Why It Matters for System Design
The difference between naive and optimized inference is 5-20x in cost and throughput. This is the primary lever for production cost management.

### Core Concepts

#### 2.7.1 FlashAttention
- **Innovation**: IO-aware exact attention algorithm. Fuses operations and uses tiling to minimize GPU HBM reads/writes.
- **Key insight**: Standard attention materializes the N*N attention matrix in HBM. FlashAttention never materializes it -- computes attention in SRAM tiles.
- **Performance**: BERT-large 15% faster, GPT-2 3x faster, long-context (1K-4K) 2.4x faster.
- **Enables longer context**: By reducing memory from O(n^2) to O(n), enables training on 16K-64K sequences that were previously impossible.
- **FlashAttention-2**: Further optimized parallelism and work partitioning. 2x faster than FlashAttention-1.
- **FlashAttention-3**: Optimized for H100 Hopper architecture.
- **Adoption**: Universal. Used by virtually all modern LLM training and inference.

#### 2.7.2 Kernel Fusion
- **Concept**: Combine multiple sequential GPU operations into a single kernel to eliminate intermediate memory reads/writes.
- **Examples**: Fused attention (FlashAttention), fused LayerNorm + residual + activation, fused QKV projection.
- **Tools**: TensorRT compiler, Triton (OpenAI's GPU compiler language), torch.compile.
- **Impact**: 10-50% speedup depending on the operations fused.

#### 2.7.3 Batching Strategies
- **Static batching**: Group requests, process together. Simple but wasteful (wait for longest request).
- **Continuous batching**: Insert/remove requests dynamically. 2-5x throughput improvement.
- **Chunked prefill**: Split long prefill into chunks, interleave with decode tokens from other requests. Prevents long prefill from blocking other requests.

#### 2.7.4 Disaggregated Serving
- **Concept**: Separate prefill (compute-heavy) and decode (memory-heavy) onto different GPU pools.
- **Benefit**: Each pool is hardware-optimized. Prefill pool uses compute-dense GPUs; decode pool uses bandwidth-dense GPUs.
- **Supported by**: TensorRT-LLM, DistServe.
- **Trade-off**: Requires KV cache transfer between pools. Network bandwidth becomes a bottleneck.

#### 2.7.5 Prefix/Prompt Caching
- **vLLM**: Automatic prefix caching.
- **OpenAI API**: Cached prompts at 50% discount.
- **Anthropic API**: Prompt caching available.
- **Impact**: For systems with long, shared system prompts, can reduce latency by 50-80% and cost by 50%.

### Inference Process Breakdown
| Phase | Nature | Bottleneck | Key Optimization |
|-------|--------|-----------|-----------------|
| Prefill | Matrix-matrix multiply | Compute-bound | FlashAttention, chunked prefill |
| Decode | Matrix-vector multiply | Memory-bandwidth-bound | Quantization, KV cache compression, batching |

---

## 2.8 Context Window Scaling

### What It Covers
Techniques to extend the effective context window of pre-trained LLMs beyond their training length.

### Why It Matters for System Design
Long context is critical for document analysis, codebase understanding, multi-turn conversation, and RAG with large retrieved context. But longer context = more memory, higher latency, higher cost.

### Core Concepts

#### 2.8.1 Position Interpolation (PI)
- **Method**: Linearly down-scale input position indices to fit within the original training context window.
- **Key insight**: Interpolation error is ~600x smaller than extrapolation error.
- **Requirements**: Minimal fine-tuning (<1000 steps).
- **Result**: Extend LLaMA models from 2K to 32K context with strong quality retention.
- **Used by**: Many open-source model extensions.

#### 2.8.2 RoPE Scaling / NTK-Aware Interpolation
- **YaRN (Yet another RoPE extensioN)**: More sophisticated RoPE scaling that adjusts different frequency components differently.
- **NTK-aware**: Adjusts the base frequency of RoPE to better distribute position information.
- **Dynamic NTK**: Adjusts scaling factor based on actual sequence length at inference time.
- **Used by**: Most open-source models that extend context beyond training length.

#### 2.8.3 Sliding Window Attention (SWA)
- **Mistral 7B**: Attention window of 4096 tokens. Each layer only attends to the last W tokens.
- **Rolling buffer KV cache**: Constant memory regardless of sequence length.
- **Effective receptive field**: With L layers and window W, information can propagate L*W tokens through the hidden state chain.
- **Trade-off**: Cannot directly attend to distant tokens, but information propagates through layers.

#### 2.8.4 ALiBi (Attention with Linear Biases)
- **Method**: Add constant linear penalties to attention scores based on distance.
- **No position embeddings needed**: Simpler architecture.
- **Extrapolation**: Better than learned positions, competitive with RoPE for moderate extensions.
- **Used by**: BLOOM, MPT.

#### 2.8.5 Ring Attention
- **Distributes long-context attention across multiple GPUs in a ring topology.
- Enables million+ token context processing.
- Each GPU processes a sequence chunk; KV blocks are passed around the ring.

### Key System Design Decisions
1. **Native long context vs extended**: Models trained natively on 128K (LLaMA 3.1, Gemini) are better than 4K models extended to 128K.
2. **Context length vs quality**: "Lost in the middle" phenomenon -- models struggle with information in the middle of long contexts. Don't assume more context = better performance.
3. **Cost scaling**: Most APIs charge linearly per token. 128K input context = 32x the cost of 4K input.
4. **Chunking + RAG vs full context**: Often better to retrieve relevant chunks than stuff the entire document into context.

---

## 2.9 Distillation

### What It Covers
Training smaller "student" models to mimic the behavior of larger "teacher" models, transferring knowledge into a more deployable form factor.

### Why It Matters for System Design
Distillation enables deploying models that are 3-10x smaller/faster while retaining 90-97% of the teacher's capability. Critical for edge deployment, cost reduction, and latency optimization.

### Core Concepts

#### 2.9.1 Knowledge Distillation Framework
- **Teacher**: Large, expensive model (e.g., GPT-4, LLaMA-70B).
- **Student**: Smaller model (e.g., LLaMA-7B, Phi-2).
- **Training signal**: Soft labels (probability distributions) from teacher, not hard labels. Temperature-scaled softmax creates softer distributions that carry more information.
- **Loss**: Weighted combination of distillation loss (KL divergence from teacher) and hard-label cross-entropy.

#### 2.9.2 Notable Distilled Models
| Student | Teacher | Compression | Quality Retention |
|---------|---------|-------------|-------------------|
| DistilBERT | BERT | 40% smaller | 97% quality, 71% faster |
| Zephyr-7B | Larger LLMs (dDPO) | ~10x smaller | Surpasses LLaMA-2-Chat-70B on MT-Bench |
| Alpaca (7B) | GPT-3.5 | ~25x smaller | Comparable on simple tasks |
| Vicuna (13B) | ShareGPT conversations | ~13x smaller | 90% of ChatGPT quality (self-reported) |
| Phi-2 (2.7B) | Synthetic data from GPT-4 | ~65x smaller | Matches 13B models on some benchmarks |
| Gemma (2B) | Gemini research | N/A | Strong for size |

#### 2.9.3 Synthetic Data Distillation
- **Process**: Use teacher model to generate high-quality training data for the student.
- **Self-Instruct**: Teacher generates instruction-response pairs. Filter for quality. Train student.
- **Alpaca approach**: 52K instruction-response pairs generated by GPT-3.5 for $500. Trained LLaMA-7B.
- **Scale**: Can generate millions of training examples cheaply.
- **Quality ceiling**: Student cannot exceed teacher's capability on the generated examples.
- **Legal considerations**: Some model licenses (OpenAI ToS) restrict using outputs for training competing models.

#### 2.9.4 Distillation for Alignment (dDPO)
- **Zephyr approach**: Distill alignment from a large aligned model to a smaller one using DPO.
- **Process**: Generate preference pairs using the teacher, then DPO-train the student.
- **Result**: Zephyr-7B surpasses much larger models on alignment benchmarks.

### Key System Design Decisions
1. **When to distill**: When you need a custom model at a specific size/latency point that doesn't exist off-the-shelf.
2. **Teacher selection**: Strongest available model as teacher. API cost for generating training data is a one-time expense.
3. **Data volume**: Typically 50K-500K examples for effective distillation. Quality > quantity.
4. **Evaluation**: Must evaluate student on YOUR task, not general benchmarks. Distillation quality varies by domain.

### Trade-offs
- **Data licensing**: OpenAI, Anthropic, Google restrict using model outputs for competitive training. Open-weight model outputs (LLaMA, Mistral) have fewer restrictions.
- **Quality ceiling**: Student cannot exceed teacher on distilled capabilities (but may exceed teacher on specific tasks after task-specific fine-tuning).
- **Cascading errors**: Synthetic data amplifies teacher biases and errors.

---

# DOMAIN 3: MODEL STRATEGIES

---

## 3.1 Fine-tuning Approaches

### What It Covers
Methods for adapting pre-trained models to specific tasks, domains, or behaviors. Ranges from full weight updates to parameter-efficient techniques that modify <1% of parameters.

### Why It Matters for System Design
Fine-tuning is the primary way to customize LLMs for production use cases. The method chosen determines: compute cost, data requirements, risk of quality degradation, and deployment complexity.

### Core Concepts

#### 3.1.1 Full Fine-tuning
- **What**: Update ALL model parameters on task-specific data.
- **Compute**: Requires 3-4x the inference memory (model + gradients + optimizer states + activations).
- **Example**: Fine-tuning LLaMA-7B FP16 requires ~56GB VRAM (model=14GB, gradients=14GB, optimizer=28GB).
- **Risk**: Catastrophic forgetting -- model loses general capabilities when fine-tuned on narrow domain.
- **When to use**: Abundant task-specific data (>100K examples), need maximum quality on specific task, can afford the compute.
- **Typical setup**: 8x A100 for 7B models, 32x A100 for 70B models.

#### 3.1.2 LoRA (Low-Rank Adaptation)
- **Core idea**: Freeze pre-trained weights. Inject trainable low-rank decomposition matrices (A and B) into each layer. Delta = B * A where B is d*r and A is r*d, with rank r << d.
- **Rank (r)**: Typically 4-64. Lower rank = fewer parameters but less expressiveness.
- **Alpha (lora_alpha)**: Scaling factor for the LoRA update. Common setting: alpha = 2 * rank.
- **Target modules**: Usually Q, K, V, O projections. Can also target MLP layers.
- **Parameter reduction**: 10,000x fewer trainable parameters than full fine-tuning (GPT-3 175B: 4.7M vs 175B trainable params).
- **Memory reduction**: 3x reduction in GPU memory.
- **Quality**: On par or better than full fine-tuning on RoBERTa, DeBERTa, GPT-2, GPT-3.
- **Inference**: Merge LoRA weights into base model. ZERO additional inference latency.
- **Multi-task**: Same base model + different LoRA adapters for different tasks. Hot-swap adapters.
- **Training time**: Much faster per step due to fewer gradient computations.

**LoRA configuration example**:
```python
LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                    # rank
    lora_alpha=32,           # scaling factor
    lora_dropout=0.1,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
)
# Trainable: 2,359,296 (0.19%) of 1,231,940,608 total
```

#### 3.1.3 QLoRA
- **Innovation**: Combines 4-bit NormalFloat quantization (NF4) with LoRA fine-tuning.
- **Three techniques**: NF4 quantization, double quantization (quantize the quantization constants), paged optimizers (manage memory spikes).
- **Breakthrough**: Fine-tune a 65B model on a single 48GB GPU while preserving full 16-bit quality.
- **Guanaco**: QLoRA-trained model achieving 99.3% of ChatGPT performance on Vicuna benchmark. 24 hours training on a single GPU.
- **Memory math**: 65B model in NF4 = ~16.5GB. LoRA adapters + optimizer states + activations fit in remaining 31.5GB of a 48GB GPU.
- **Best for**: Fine-tuning large models (13B-70B) on consumer/limited hardware.

#### 3.1.4 Adapters
- **Architecture**: Insert small trainable bottleneck layers (down-project, activation, up-project) between existing transformer layers.
- **Comparison to LoRA**: More inference overhead (additional layers vs merged weights). Less popular now.
- **Historical**: Houlsby et al. (2019). Paved the way for PEFT research.

#### 3.1.5 Prefix Tuning / P-Tuning
- **Prefix Tuning**: Prepend trainable continuous vectors to key and value in each attention layer.
- **P-Tuning v2**: Extended prefix tuning. "Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales."
- **Prompt Tuning**: Only prepend trainable soft tokens to the input. Simplest PEFT method.
- **Comparison**: Generally less effective than LoRA on most tasks. Useful when you want to keep the model completely frozen.

#### 3.1.6 Recommended PEFT Workflow
```
1. Quantize base model with bitsandbytes (NF4, zero-shot)
2. Fine-tune with QLoRA adapters
3. Merge adapters into dequantized base model (FP16)
4. Quantize merged model with GPTQ/AWQ (for deployment)
5. Serve with vLLM/TensorRT-LLM
```
This combines easy training (bitsandbytes), zero adapter merge degradation, and fast inference (GPTQ/AWQ).

### Real-World Examples
| Company/Product | Method | Details |
|----------------|--------|---------|
| OpenAI Fine-tuning API | Full FT (hosted) | GPT-3.5/GPT-4 fine-tuning. User provides JSONL. OpenAI handles infra. |
| Hugging Face AutoTrain | LoRA/QLoRA | No-code fine-tuning platform. |
| Databricks | Full FT, LoRA | Integrated with MLflow. |
| Anyscale | LoRA | Ray-based distributed fine-tuning. |
| Together AI | LoRA, full FT | API-based fine-tuning service. |
| Predibase | LoRA | LoRAX for serving multiple adapters simultaneously. |
| AWS SageMaker | QLoRA | Jumpstart fine-tuning templates. |

---

## 3.2 When to Fine-tune vs Prompt Engineer vs RAG

### What It Covers
The strategic decision framework for choosing between prompt engineering, retrieval-augmented generation, and fine-tuning (or combinations thereof).

### Why It Matters for System Design
This is the highest-ROI architectural decision after model selection. The wrong choice wastes months of effort or produces inferior results.

### Decision Framework

#### 3.2.1 Prompt Engineering (Try First)
**Best when**:
- Task is well-defined and expressible through instructions
- Base model already has the required knowledge
- Low data availability (<100 examples)
- Need to iterate quickly (minutes, not days)
- Multi-task flexibility needed

**Limitations**:
- Context window limits instruction complexity
- Inconsistent output format despite detailed instructions
- Cost per inference includes prompt tokens every time
- Cannot teach genuinely new knowledge or skills

**Examples**: Customer service routing, classification, summarization with specific formatting, translation.

#### 3.2.2 RAG (When Knowledge is the Gap)
**Best when**:
- Model lacks domain-specific or recent knowledge
- Need grounded, attributable answers
- Information changes frequently (can't freeze in weights)
- Need to cite sources
- Legal/compliance requirements for traceability

**Limitations**:
- Retrieval quality is a bottleneck (garbage in, garbage out)
- Adds latency (retrieval + embedding + generation)
- Chunking and indexing pipeline adds complexity
- Cannot change model behavior or style, only knowledge

**Examples**: Enterprise knowledge base QA, customer support with product docs, legal research, medical QA.

#### 3.2.3 Fine-tuning (When Behavior is the Gap)
**Best when**:
- Need consistent output format/style (e.g., always return JSON)
- Domain-specific reasoning (medical, legal, financial)
- Behavior modification (tone, safety, refusal patterns)
- Significant quality gap between prompted base model and requirements
- High volume justifies one-time training cost (amortized over millions of inferences)
- Want to eliminate long system prompts (reduce per-inference cost)

**Limitations**:
- Requires high-quality training data (100-10K+ examples)
- Risk of catastrophic forgetting
- Ongoing maintenance (model drift, data drift)
- Cannot easily update factual knowledge (re-train required)

**Examples**: Code generation in specific framework, structured data extraction, domain-specific chat assistant.

#### 3.2.4 Combined Approaches (Production Systems)
Most production systems combine approaches:

```
Fine-tuned model (behavior/format) + RAG (knowledge) + Prompt engineering (task routing)
```

| Approach | What It Fixes | Data Needed | Iteration Speed | Maintenance |
|----------|--------------|-------------|-----------------|-------------|
| Prompt engineering | Task definition | 0-10 examples | Minutes | Low |
| RAG | Knowledge gaps | Documents | Hours-Days | Medium (re-index) |
| Fine-tuning | Behavior/quality | 100-10K+ examples | Days-Weeks | High (re-train) |
| Combined | All of the above | All of the above | Varies | Highest |

#### 3.2.5 Decision Tree
```
Q: Does the base model have the required knowledge?
  No -> RAG (or fine-tune if knowledge is specialized reasoning, not facts)
  Yes -> Q: Does the model follow instructions well enough?
    No -> Q: Can you express the requirement as a prompt?
      Yes -> Prompt engineer
      No -> Fine-tune (LoRA first, full FT if LoRA insufficient)
    Yes -> Q: Is output quality/consistency sufficient?
      Yes -> Ship with prompt engineering
      No -> Fine-tune for quality, RAG for knowledge, or both
```

---

## 3.3 Model Selection Criteria

### What It Covers
Systematic framework for evaluating and selecting LLMs for production deployment across multiple dimensions.

### Why It Matters for System Design
Wrong model selection leads to over-spending (model too large), under-performing (model too small), vendor lock-in, or compliance violations.

### Core Evaluation Dimensions

#### 3.3.1 Quality / Capability
- **Task-specific evaluation**: Always evaluate on YOUR use case, not benchmarks. Prepare 200+ evaluation examples with ground truth.
- **Benchmark literacy**: MMLU (knowledge), HumanEval (code), GSM8K (math), MT-Bench (chat), IFEval (instruction following). Understand what each measures.
- **Failure analysis**: Evaluate not just accuracy but failure modes (hallucination rate, refusal rate, format compliance).

#### 3.3.2 Cost
- **Per-token pricing** (API models):
  | Model | Input ($/1M tokens) | Output ($/1M tokens) |
  |-------|---------------------|----------------------|
  | GPT-4o | $2.50 | $10.00 |
  | GPT-4o mini | $0.15 | $0.60 |
  | Claude Opus 4.6 | $5.00 | $25.00 |
  | Claude Sonnet 4.6 | $3.00 | $15.00 |
  | Claude Haiku 4.5 | $1.00 | $5.00 |

- **Self-hosted cost**: GPU cost / tokens served. A well-optimized vLLM deployment of LLaMA-70B on 2x H100 can serve at ~$0.50-1.00/1M input tokens.
- **Volume matters**: At 1B tokens/month, self-hosted is usually 2-5x cheaper than API. Below 100M tokens/month, API is often cheaper after factoring in ops costs.

#### 3.3.3 Latency
- **Time to first token (TTFT)**: Prefill latency. Depends on input length and model size.
- **Time per output token (TPOT)**: Decode latency. Determines perceived generation speed.
- **End-to-end**: TTFT + (num_output_tokens * TPOT). For chatbots, TTFT < 500ms and TPOT < 50ms are good targets.
- **Model size impact**: 7B models are ~10x faster than 70B models on the same hardware.

#### 3.3.4 Context Length
- **4K**: Barely sufficient for complex prompts. Limits RAG to small chunks.
- **8K-32K**: Adequate for most applications. Standard tier.
- **128K**: Full document analysis, long code files, multi-document QA.
- **1M (Claude, Gemini)**: Entire codebases, book-length analysis, extended conversations.

#### 3.3.5 Licensing
- **Proprietary API**: No weights, no self-hosting. Vendor lock-in. Data sent to third party.
- **Open-weight permissive** (Apache 2.0): Mistral, Falcon. Full freedom. Commercial use.
- **Open-weight restricted**: LLaMA (Meta license). Commercial use with conditions (>700M MAU requires special license).
- **Research only**: Some models restrict commercial use entirely.

#### 3.3.6 Data Privacy / Compliance
- **API models**: Data leaves your infrastructure. Must evaluate provider's data retention, training policies, and certifications (SOC 2, HIPAA BAA, GDPR).
- **Self-hosted**: Data stays on-prem. Required for highly regulated industries (healthcare, finance, defense).
- **Enterprise APIs**: Azure OpenAI, AWS Bedrock offer enhanced data protections and compliance certifications.

### Model Tiering Strategy (Production Pattern)
```
Tier 1 (Simple): GPT-4o mini / Haiku 4.5 / Mistral 7B
  -> Classification, routing, simple extraction. Cheapest. Fastest.

Tier 2 (Standard): GPT-4o / Sonnet 4.6 / LLaMA-70B
  -> Most production tasks. Good quality-cost balance.

Tier 3 (Premium): o3 / Opus 4.6 / LLaMA-405B
  -> Complex reasoning, critical tasks. Highest quality. Highest cost.
```
Route dynamically based on query complexity. This is the "model router" pattern.

---

## 3.4 Training Infrastructure

### What It Covers
The distributed training systems, frameworks, and infrastructure required to train and fine-tune LLMs at scale.

### Why It Matters for System Design
Even if you're not pre-training, understanding training infrastructure is essential for fine-tuning, evaluating training claims from model providers, and planning compute budgets.

### Core Concepts

#### 3.4.1 DeepSpeed (Microsoft)
- **ZeRO (Zero Redundancy Optimizer)**: Partitions optimizer states, gradients, and model parameters across GPUs.
  - **ZeRO Stage 1**: Partition optimizer states only. 4x memory reduction.
  - **ZeRO Stage 2**: Partition optimizer states + gradients. 8x memory reduction.
  - **ZeRO Stage 3**: Partition everything including parameters. Memory scales linearly with GPU count.
- **ZeRO-Offload**: Offload to CPU memory. Train 13B models on a single GPU (vs 1.4B with standard PyTorch DDP).
- **Performance**: BERT-Large in 44 minutes on 1024 V100s. GPT-2 1.5B 3.75x faster than NVIDIA Megatron.
- **1-bit Adam/LAMB**: 26x less communication while maintaining convergence.
- **3D Parallelism**: Combined data + model + pipeline parallelism. Scales to trillions of parameters.
- **Integration**: Minimal code changes from standard PyTorch.

#### 3.4.2 FSDP (PyTorch Fully Sharded Data Parallel)
- **Native PyTorch**: Part of core PyTorch. No external dependency.
- **Similar to ZeRO Stage 3**: Shards parameters, gradients, and optimizer states.
- **Advantages**: Simpler setup, PyTorch-native, growing community support.
- **vs DeepSpeed**: DeepSpeed has more features (ZeRO-Offload, advanced optimizers). FSDP is simpler and better integrated.

#### 3.4.3 Megatron-LM (NVIDIA)
- **Tensor parallelism**: Splits individual layers across GPUs. NVIDIA's implementation is the most optimized.
- **Pipeline parallelism**: Interleaved 1F1B schedule for reduced bubbles.
- **Sequence parallelism**: For LayerNorm and Dropout operations.
- **Used by**: Most large-scale training runs on NVIDIA hardware.

#### 3.4.4 Data Pipelines for Training
- **Data preparation**: Deduplication (MinHash, exact string matching), quality filtering (perplexity scoring, classifier-based), PII removal, license filtering.
- **Tokenization**: Pre-tokenize and store in binary format (e.g., Arrow/Parquet). Avoid tokenizing on-the-fly during training.
- **Data mixing**: Ratio of different data sources (web, code, books, scientific papers) significantly impacts model capabilities. LLaMA 3 used 4x more code data than LLaMA 2.
- **Curriculum learning**: Some teams train on easier data first, then harder data. Evidence is mixed on benefit.

#### 3.4.5 Compute Requirements (Approximate)
| Model Size | Training Data | GPU-Hours (A100) | Estimated Cost |
|-----------|--------------|------------------|---------------|
| 7B | 1T tokens | ~180K | $400K-700K |
| 13B | 1T tokens | ~350K | $800K-1.4M |
| 70B | 2T tokens | ~1.7M | $3.5M-7M |
| 175B | 300B tokens | ~3.5M | $7M-12M |
| 1T+ (frontier) | 10T+ tokens | ~25M+ | $50M-100M+ |

### Key System Design Decisions
1. **DeepSpeed vs FSDP**: DeepSpeed for maximum feature set and scale. FSDP for PyTorch-native simplicity.
2. **GPU cluster sizing**: For LoRA fine-tuning 7B: 1-2 A100s. Full fine-tuning 7B: 4-8 A100s. Fine-tuning 70B: 8-32 A100s.
3. **Training data quality vs quantity**: Phi models prove that 10x less but higher-quality data can match models trained on more data. Invest in data curation.
4. **Checkpoint frequency**: Save checkpoints every 100-1000 steps. A crashed training run without checkpoints wastes all compute since the last save.

---

## 3.5 Synthetic Data Generation for Training

### What It Covers
Using LLMs to generate training data for fine-tuning other (usually smaller) models.

### Why It Matters for System Design
Synthetic data democratizes model customization by replacing expensive human annotation with scalable LLM-generated data.

### Core Concepts

#### 3.5.1 Self-Instruct
- **Process**: Start with seed instructions -> LLM generates new instructions + responses -> Filter for quality and diversity -> Train student model.
- **Stanford Alpaca**: 52K instructions generated by GPT-3.5 for ~$500. Used to train LLaMA-7B into an instruction-following model.
- **Quality filtering**: Remove duplicates, too-short responses, responses that refuse to answer, and responses that reference being an AI.

#### 3.5.2 Evol-Instruct (WizardLM)
- **Concept**: Evolve simple instructions into complex ones using LLMs. Add constraints, reasoning steps, multiple requirements.
- **Impact**: Creates harder training examples that improve model capability on complex tasks.

#### 3.5.3 Synthetic Data for Evaluation
- **Generate test cases**: Use strong models to create evaluation datasets.
- **Preference data**: Generate (chosen, rejected) pairs for DPO training using model-as-judge.
- **Scalable**: Generate 100K+ evaluation examples across domains cheaply.

#### 3.5.4 Risks and Mitigations
- **Model collapse**: Training on synthetic data from the same model family risks feedback loops that degrade quality over generations.
- **Bias amplification**: Synthetic data inherits and can amplify biases from the generating model.
- **Factual errors**: LLMs hallucinate. Synthetic data contains hallucinations. Must verify factual claims.
- **Mitigation**: Mix synthetic with human-curated data (typically 80-90% synthetic, 10-20% human for critical examples).

### Real-World Examples
- **Microsoft Phi models**: Trained primarily on synthetic "textbook quality" data. 2.7B model matches 13B models.
- **Nvidia Nemotron**: Uses synthetic data pipeline for fine-tuning.
- **Hugging Face UltraChat**: 1.5M synthetic multi-turn conversations.
- **Scale AI + OpenAI**: Combine human annotation with synthetic augmentation.

---

## 3.6 Model Registries and Versioning

### What It Covers
Systems for tracking model versions, experiments, artifacts, and deployment metadata throughout the ML lifecycle.

### Why It Matters for System Design
Production LLM systems require: reproducibility (which model version served this response?), rollback capability, A/B testing, and audit trails.

### Core Concepts

#### 3.6.1 MLflow
- **Experiment tracking**: Log hyperparameters, metrics, artifacts for every training run.
- **Model registry**: Version models with stage transitions (staging -> production). Approval workflows.
- **LLM-specific features**: Prompt engineering UI, LLM evaluation (mlflow.evaluate), integration with LangChain/OpenAI.
- **Deployment**: Model serving with REST API. Integration with Databricks, SageMaker, Azure ML.
- **Open-source**: Apache 2.0. Self-hosted or Databricks-managed.

#### 3.6.2 Weights & Biases (W&B)
- **Experiment tracking**: Real-time training dashboards. Hyperparameter sweeps. Team collaboration.
- **Artifacts**: Version datasets and models with lineage tracking.
- **Tables**: Interactive data exploration for evaluation results.
- **LLM focus**: Trace logging for LLM chains, prompt management, evaluation tooling.
- **Commercial**: Free tier for individuals. Enterprise licensing.

#### 3.6.3 HuggingFace Hub
- **Model repository**: 500K+ models. Git-based versioning. Model cards for documentation.
- **Datasets**: 100K+ datasets with streaming support.
- **Spaces**: Deploy demo apps directly.
- **De facto standard**: Most open-source models are published here first.
- **SafeTensors**: Secure model serialization format. Prevents arbitrary code execution during model loading.

#### 3.6.4 Model Versioning Best Practices
1. **Immutable model IDs**: Hash-based or timestamp-based versioning (e.g., `claude-sonnet-4-6-20250929`).
2. **Metadata**: Store training config, data version, base model, evaluation results alongside every model version.
3. **A/B testing**: Serve multiple model versions simultaneously. Compare on real traffic.
4. **Rollback**: Maintain at least 2 production-ready versions for instant rollback.
5. **Lineage**: Track full provenance: base model -> fine-tuning data -> training config -> resulting model -> evaluation results.

### Key System Design Decisions
1. **MLflow vs W&B**: MLflow = open-source, self-hosted, Databricks integration. W&B = better UI, hosted, more LLM-specific features.
2. **HuggingFace Hub as registry**: For open-source models, HF Hub is often sufficient. For proprietary models, use MLflow/W&B.
3. **Adapter registries**: When using LoRA, version base model and adapter separately. Adapt-and-merge vs serve-adapter patterns.

---

# CROSS-CUTTING CONCERNS

---

## Architectural Decision Records (ADRs) for GenAI Systems

### ADR 1: Model Hosting Strategy
**Decision**: Self-hosted vs API vs hybrid.
**Factors**: Volume, latency SLA, data privacy, operational maturity, cost.
**Recommendation**: Start API, migrate high-volume workloads to self-hosted as volume grows.

### ADR 2: Quantization Strategy
**Decision**: FP16, INT8, or INT4 for serving.
**Factors**: Quality requirements, GPU budget, model size.
**Recommendation**: INT4 AWQ/GPTQ for most workloads. FP8 on H100+ for quality-critical tasks.

### ADR 3: Parallelism Strategy
**Decision**: TP degree, PP stages, DP replicas.
**Factors**: Model size, GPU count, interconnect bandwidth, latency SLA.
**Recommendation**: TP within NVLink domain, PP across nodes only if necessary, DP for throughput scaling.

### ADR 4: Fine-tuning vs RAG vs Prompting
**Decision**: How to customize model behavior.
**Factors**: Data availability, task type (knowledge vs behavior), iteration speed needs, budget.
**Recommendation**: Always start with prompting. Add RAG for knowledge. Fine-tune only when demonstrable quality gap remains.

---

# APPENDIX: COMPANY-MODEL-INFRASTRUCTURE MAP

| Company | Models | Serving Infra | Training Infra | Key Innovation |
|---------|--------|--------------|----------------|---------------|
| OpenAI | GPT-4/4o/o1/o3 | Custom, Azure | A100/H100 clusters | RLHF at scale, reasoning models |
| Anthropic | Claude 3/4/4.5/4.6 | Custom, AWS/GCP | A100/H100 clusters | Constitutional AI, long context |
| Google | Gemini, Gemma | TPUv4/v5, GCP | TPUv4/v5 | Native multimodal, custom silicon |
| Meta | LLaMA 1/2/3/3.1 | (not served) | Grand Teton (H100) | Open-weight democratization |
| Mistral | Mistral 7B, Mixtral | La Plateforme | H100 clusters | MoE efficiency, open-weight |
| Microsoft | Phi 1/2/3 | Azure | Azure ML | Small model + high-quality data |
| NVIDIA | Nemotron | NIM/TRT-LLM | DGX | Inference optimization, HW-SW co-design |
| Cohere | Command R/R+ | Custom | H100 clusters | Enterprise RAG optimization |
| Together AI | Serving/fine-tuning platform | FlashAttention | H100 clusters | Open-source training/serving |
| Databricks | DBRX (MoE) | Mosaic ML | Mosaic ML | Enterprise ML platform integration |
| DeepSeek | DeepSeek V2/V3/R1 | Custom | H100/H800 | Multi-head latent attention, cost efficiency |

---

# TOPIC DEPENDENCY MAP

```
Transformer Architecture
  |-> Attention variants (MHA, GQA, MQA)
  |     |-> KV Cache Management
  |     |-> FlashAttention
  |     |-> Model Parallelism (tensor parallelism splits heads)
  |-> Positional Encoding (RoPE, ALiBi)
  |     |-> Context Window Scaling (PI, YaRN, NTK)
  |-> FFN layers
  |     |-> MoE Architecture (replaces FFN)
  |           |-> Expert Parallelism
  |           |-> Routing & Load Balancing
  |
LLM Landscape
  |-> Model Selection
  |     |-> Cost/Latency/Quality tradeoffs
  |     |-> Licensing & Privacy
  |-> Tokenization
  |     |-> Cost calculation
  |     |-> Multilingual efficiency
  |-> Embeddings
  |     |-> Vector Search / RAG
  |     |-> Semantic Caching
  |
Training Pipeline
  |-> Pre-training (scaling laws, data composition)
  |-> SFT / Instruction Tuning
  |-> RLHF / DPO / CAI (alignment)
  |-> Fine-tuning (LoRA, QLoRA, full FT)
  |     |-> PEFT methods
  |     |-> Training infrastructure (DeepSpeed, FSDP)
  |-> Distillation / Synthetic Data
  |
Inference Pipeline
  |-> Model Serving (vLLM, TRT-LLM, TGI)
  |     |-> Continuous Batching
  |     |-> PagedAttention
  |     |-> Speculative Decoding
  |-> GPU Compute (H100, A100, memory planning)
  |-> Quantization (GPTQ, AWQ, FP8)
  |     |-> INT4 vs INT8 vs FP8
  |-> Model Parallelism (TP, PP, DP)
  |-> Optimization (FlashAttention, kernel fusion)
```

---

# RECOMMENDED READING ORDER FOR LEARNING

## Phase 1: Foundations (Week 1-2)
1. Transformer Architecture (1.1)
2. LLM Landscape (1.2)
3. Tokenization (1.3)
4. Embeddings (1.4)

## Phase 2: Training Understanding (Week 3)
5. Pre-training vs Post-training (1.5)
6. Fine-tuning Approaches (3.1)
7. When to Fine-tune vs Prompt vs RAG (3.2)

## Phase 3: Inference Deep Dive (Week 4-5)
8. GPU Compute (2.2)
9. Model Serving Infrastructure (2.1)
10. Quantization (2.3)
11. KV Cache Management (2.4)
12. Model Parallelism (2.6)
13. Inference Optimization (2.7)

## Phase 4: Advanced Topics (Week 6)
14. MoE Architecture (1.6)
15. Speculative Decoding (2.5)
16. Context Window Scaling (2.8)
17. Distillation (2.9)
18. Multimodal Models (1.7)

## Phase 5: Production Strategy (Week 7)
19. Model Selection Criteria (3.3)
20. Training Infrastructure (3.4)
21. Synthetic Data Generation (3.5)
22. Model Registries and Versioning (3.6)

---

*Research compiled from: Vaswani et al. (2017), Shazeer et al. (2017), Radford et al. (2018/2019), Devlin et al. (2018), Brown et al. (2020), Ouyang et al. (2022), Hu et al. (2021), Dettmers et al. (2022/2023), Frantar et al. (2023), Lin et al. (2024), Dao et al. (2022), Touvron et al. (2023), Jiang et al. (2023/2024), Rafailov et al. (2023), Leviathan et al. (2023), Fedus et al. (2022), NVIDIA documentation, Hugging Face documentation, Anthropic model documentation, Lilian Weng's research notes, Maarten Grootendorst's visual guides, and primary research papers.*
