# GenAI Source Map

Source traceability map showing which research sources informed each of the 58 topic files.

---

## Foundations

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| foundations/transformers | Vaswani et al. "Attention Is All You Need" (2017); Shazeer "MQA" (2019); Ainslie et al. "GQA" (2023); Su et al. "RoPE" (2021); Shazeer "SwiGLU" (2020) | Dao et al. "FlashAttention" (2022); Jiang et al. "Mixtral" (2024); Meta "LLaMA 3" (2024); Fedus et al. "Switch Transformers" (2022); Zhang & Sennrich "RMSNorm" (2019); Press et al. "ALiBi" (2022); Kwon et al. "PagedAttention/vLLM" (2023); Hoffmann et al. "Chinchilla" (2022); DeepSeek-V2 (2024) |
| foundations/llm-landscape | Brown et al. "GPT-3" (2020); OpenAI "GPT-4 Technical Report" (2023); Touvron et al. "LLaMA 1/2" (2023); Meta "LLaMA 3" (2024); Jiang et al. "Mistral 7B" / "Mixtral" (2023-2024); Bai et al. "Constitutional AI" (2022) | DeepSeek-V2/V3/R1 (2024-2025); Alibaba "Qwen 2" (2024); Google "Gemini" (2023); Google "Gemini 1.5" (2024); Google "Gemma" (2024); Microsoft "Phi-3" (2024); Cohere "Command R+" (2024); Hoffmann et al. "Chinchilla" (2022); Anthropic model cards (2024-2026) |
| foundations/tokenization | Sennrich et al. "BPE for NMT" (ACL 2016); Kudo & Richardson "SentencePiece" (2018); Kudo "Unigram LM" (2018); Schuster & Nakajima "WordPiece" (2012); Radford et al. "GPT-2" (2019, byte-level BPE) | Meta "LLaMA 3" (2024, tokenizer change); OpenAI tiktoken; Google "Gemini" (256K vocab); Petrov et al. "Tokenizer Unfairness" (NeurIPS 2023); Provilkov et al. "BPE-Dropout" (2020); Jiang et al. "LLMLingua" (2023); Mistral AI tokenizer docs |
| foundations/embeddings | Mikolov et al. "Word2Vec" (2013); Reimers & Gurevych "Sentence-BERT" (2019); Kusupati et al. "Matryoshka" (NeurIPS 2022); Khattab & Zaharia "ColBERT" (2020); Wang et al. "E5" (2022); Xiao et al. "BGE" (2023) | Chen et al. "BGE-M3" (2024); Muennighoff et al. "MTEB" (2023); OpenAI "text-embedding-3" (2024); Cohere "Embed v3" (2023); Nussbaum et al. "Nomic Embed" (2024); Gao et al. "HyDE" (2023); Jegou et al. "Product Quantization" (2011); Jina AI "Late Chunking" (2024); Voyage AI docs; Pennington et al. "GloVe" (2014) |
| foundations/multimodal-models | Radford et al. "CLIP" (2021); Zhai et al. "SigLIP" (2023); Liu et al. "LLaVA" (2023); Li et al. "BLIP-2" (2023); Radford et al. "Whisper" (2022); Google "Gemini" (2023); OpenAI GPT-4V/GPT-4o system cards | Alayrac et al. "Flamingo" (2022); Girdhar et al. "ImageBind" (Meta, 2023); Chen et al. "InternVL" (2024); Huang et al. "LayoutLMv3" (2022); Kim et al. "Donut" (2022); Chen et al. "FastV token pruning" (2024); Video understanding survey (Tang et al., 2024) |
| foundations/alignment | Ouyang et al. "InstructGPT/RLHF" (OpenAI, 2022); Rafailov et al. "DPO" (Stanford, 2023); Bai et al. "Constitutional AI" (Anthropic, 2022); Schulman et al. "PPO" (2017); Zhou et al. "LIMA" (Meta, 2023) | Wang et al. "Self-Instruct" (2022); Xu et al. "Evol-Instruct/WizardLM" (2023); Tunstall et al. "Zephyr" (2023); Lightman et al. "Step-by-Step Verification" (2023); Hoffmann et al. "Chinchilla" (2022); Li et al. "Phi-1.5" (2023); Gao et al. "Reward Hacking Scaling Laws" (2023); Zou et al. "GCG" (2023); Ethayarajh et al. "KTO" (2024); Hong et al. "ORPO" (2024); Meng et al. "SimPO" (2024); Cui et al. "UltraFeedback" (2023); Meta "LLaMA 3 alignment" (2024) |

---

## LLM Architecture

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| llm-architecture/model-serving | Kwon et al. "PagedAttention/vLLM" (2023); Yu et al. "Orca" (continuous batching, 2022); Zheng et al. "SGLang/RadixAttention" (2024); Leviathan et al. "Speculative Decoding" (2023); NVIDIA "TensorRT-LLM" (2023) | HuggingFace "TGI" (2023); Gerganov "llama.cpp/GGUF" (2023); Cai et al. "Medusa" (2024); Li et al. "EAGLE" (2024); Patel et al. "Splitwise" (2024); Zhong et al. "DistServe" (2024); Agrawal et al. "Sarathi" (2024); Dao et al. "FlashAttention" (2022); Frantar et al. "GPTQ" (2023); Lin et al. "AWQ" (2024); Xiao et al. "SmoothQuant" (2023); NVIDIA Triton (2019) |
| llm-architecture/gpu-compute | NVIDIA A100/H100/H200/B200 whitepapers (2020-2024); Williams et al. "Roofline Model" (2009); Meta "LLaMA 3.1 training infrastructure" (2024) | Kwon et al. "vLLM" (2023); Dao et al. "FlashAttention" (2022); NVIDIA TensorRT-LLM benchmarks; Epoch AI "Training Cost Trends" (2024); Google "TPUv4/v5" (Jouppi et al., 2023); Patel et al. "Splitwise" (2024); NVIDIA DCGM, MIG, NVLink/NVSwitch documentation; CoreWeave docs; InfiniBand for AI (NVIDIA/Mellanox) |
| llm-architecture/quantization | Frantar et al. "GPTQ" (2022); Lin et al. "AWQ" (2023); Xiao et al. "SmoothQuant" (2022); Dettmers et al. "LLM.int8()" (2022); Dettmers et al. "QLoRA/NF4" (2023) | Micikevicius et al. "FP8 Formats" (NVIDIA, 2022); Kim et al. "SqueezeLLM" (2023); Liu et al. "SpinQuant" (Meta, 2024); Gerganov "K-quant/GGUF" (2023); turboderp "ExLlamaV2/EXL2" (2023); IST Austria "Marlin Kernels" (2024); Liu et al. "KIVI" (KV cache quantization, 2024); Xiao et al. "Attention Sinks" (2023) |
| llm-architecture/kv-cache | Kwon et al. "PagedAttention/vLLM" (2023); Shazeer "MQA" (2019); Ainslie et al. "GQA" (2023); Zhang et al. "H2O" (KV eviction, 2023); Xiao et al. "Attention Sinks/StreamingLLM" (2023) | Zheng et al. "SGLang/RadixAttention" (2023); Yu et al. "Orca" (2022); Dao et al. "FlashAttention" (2022); Patel et al. "Splitwise" (2024); Zhong et al. "DistServe" (2024); Liu et al. "Mooncake" (2024); Liu et al. "KIVI" (2024); Agrawal et al. "Sarathi" (chunked prefill, 2024); Liu et al. "Scissorhands" (2023); Beltagy et al. "Longformer" (SWA, 2020) |
| llm-architecture/context-scaling | Su et al. "RoPE" (2021); Chen et al. "Position Interpolation" (2023); Peng et al. "YaRN" (2023); Press et al. "ALiBi" (2022); Xiao et al. "StreamingLLM" (2023); Liu et al. "Lost in the Middle" (2024) | Liu et al. "Ring Attention" (2023); Dao et al. "FlashAttention" (2022); Kamradt "Needle in a Haystack" (2023); Hsieh et al. "RULER" (2024); Zhang et al. "H2O" (2023); Jiang et al. "LLMLingua" (2023); Mu et al. "Gisting" (2023); Google "Gemini 1.5" (2024); Meta "LLaMA 3.1" (2024); bloc97 "NTK-Aware RoPE" (2023); Beltagy et al. "Longformer" (2020) |
| llm-architecture/model-parallelism | Shoeybi et al. "Megatron-LM" (NVIDIA, 2019); Narayanan et al. "3D Parallelism" (2021); Rajbhandari et al. "ZeRO" (2020); Huang et al. "GPipe" (2019); Lepikhin et al. "GShard" (2020) | Zhao et al. "PyTorch FSDP" (2023); Rajbhandari et al. "ZeRO-Infinity" (2021); Narayanan et al. "PipeDream" (2019); Korthikanti et al. "Sequence Parallelism" (2022); Jacobs et al. "DeepSpeed Ulysses" (2023); Liu et al. "Ring Attention" (2023); Fedus et al. "Switch Transformers" (2022); Patel et al. "Splitwise" (2024); Zhong et al. "DistServe" (2024); Meta "LLaMA 3.1 training" (2024); DeepSeek-V3 (2024); Chowdhery et al. "PaLM" (2022); Smith et al. "Megatron-Turing NLG" (2022) |

---

## Model Strategies

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| model-strategies/fine-tuning | Hu et al. "LoRA" (2021); Dettmers et al. "QLoRA" (2023); Zhou et al. "LIMA" (Meta, 2023) | Houlsby et al. "Adapters" (2019); Li & Liang "Prefix Tuning" (2021); Lester et al. "Prompt Tuning" (2021); Liu et al. "P-Tuning v2" (2022); Liu et al. "DoRA" (2024); Jain et al. "NEFTune" (2023); Sheng et al. "S-LoRA" (2023); Wang et al. "Self-Instruct" (2022); Wu et al. "BloombergGPT" (2023); Taori et al. "Alpaca" (2023); Tunstall et al. "Zephyr" (2023) |
| model-strategies/model-selection | Hendrycks et al. "MMLU" (2020); Chen et al. "HumanEval" (2021); Zheng et al. "MT-Bench/Chatbot Arena" (2023); Hoffmann et al. "Chinchilla" (2022) | Li et al. "AlpacaEval" (2023); Zhou et al. "IFEval" (2023); Rein et al. "GPQA" (2023); OpenAI "GPT-4 Technical Report" (2023); Anthropic model documentation; Google "Gemini" (2023); Mistral AI model cards; Alibaba "Qwen 2.5" (2024); BerriAI "LiteLLM"; Sheng et al. "S-LoRA" (2023); Leviathan et al. "Speculative Decoding" (2023) |
| model-strategies/training-infrastructure | Rajbhandari et al. "ZeRO" (2020); Shoeybi et al. "Megatron-LM" (NVIDIA, 2019); Zhao et al. "PyTorch FSDP" (2023); Hoffmann et al. "Chinchilla" (2022); Meta "LLaMA 3 training" (2024) | Narayanan et al. "Megatron-LM v2" (2021); Rajbhandari et al. "ZeRO-Infinity" (2021); Dao et al. "FlashAttention" (2022); Meta "TorchTitan" (2024); HuggingFace "Datatrove" (2024); Soldaini et al. "Dolma" (AI2, 2024); Groeneveld et al. "OLMo" (AI2, 2024); Databricks "MosaicML Composer"; NVIDIA "NeMo Framework"; Weights & Biases; Zaharia et al. "MLflow" |
| model-strategies/distillation | Hinton et al. "Knowledge Distillation" (2015); Sanh et al. "DistilBERT" (2019); Wang et al. "Self-Instruct" (2022); Mukherjee et al. "Orca" (Microsoft, 2023) | Taori et al. "Alpaca" (2023); Chiang et al. "Vicuna" (LMSYS, 2023); Mitra et al. "Orca 2" (2023); Tunstall et al. "Zephyr" (2023); Gunasekar et al. "Phi-1" (2023); Abdin et al. "Phi-3" (2024); Xu et al. "Evol-Instruct" (2023); Ding et al. "UltraChat" (2023); Cui et al. "UltraFeedback" (2023); Google "Gemma 2" (2024); Romero et al. "FitNets" (2015); Zagoruyko & Komodakis "Attention Transfer" (2017) |

---

## RAG

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| rag/rag-pipeline | Lewis et al. "RAG" (NeurIPS 2020); Asai et al. "Self-RAG" (ICLR 2024); Gao et al. "HyDE" (2022); Liu et al. "Lost in the Middle" (2024); Es et al. "RAGAS" (2023) | Yan et al. "CRAG" (2024); Zheng et al. "Step-back Prompting" (2024); Santhanam et al. "ColBERTv2" (2022); Formal et al. "SPLADE" (2021); Jiang et al. "LLMLingua" (2023); Edge et al. "GraphRAG" (2024); Gao et al. "Modular RAG" (2024); Cormack et al. "RRF" (2009) |
| rag/document-ingestion | Unstructured.io documentation; IBM "Docling" (2024); LlamaIndex "LlamaParse" (2024) | Nassar et al. "TableFormer" (2022); Microsoft "Table Transformer" (2022); Broder "MinHash/LSH" (1997); Barbaresi "Trafilatura" (2021); Pfitzmann et al. "DocLayNet" (2022); AWS Textract; Google Document AI; Azure Document Intelligence; Smith "Tesseract OCR" (2007); Firecrawl docs; Apache Airflow; Prefect |
| rag/chunking | LangChain "Text Splitters" docs; LlamaIndex "SemanticSplitterNodeParser" docs; Kamradt "5 Levels of Text Splitting" (2023) | Chen et al. "Dense X Retrieval" (proposition-based, 2023); Jina AI "Late Chunking" (2024); LlamaIndex "Auto-Merging Retriever"; Pinecone "Chunking Strategies" (2024); Weaviate chunk size blog (2024); Liu et al. "Lost in the Middle" (2024); tree-sitter docs; Unstructured.io docs; LangChain "MarkdownHeaderTextSplitter" |
| rag/retrieval-reranking | Karpukhin et al. "DPR" (2020); Nogueira & Cho "BERT Reranking" (2019); Khattab & Zaharia "ColBERT" (2020); Cormack et al. "RRF" (2009) | Formal et al. "SPLADE v2" (2022); Santhanam et al. "ColBERTv2" (2022); Gao et al. "HyDE" (2023); Zheng et al. "Step-back Prompting" (2024); Xiao et al. "BGE Reranker" (2023); Cohere Rerank docs; Thakur et al. "BEIR" (2021); Robertson & Zaragoza "BM25" (2009); Manning et al. "Introduction to IR" (2008); LangChain "MultiQueryRetriever" |
| rag/graphrag | Edge et al. "Microsoft GraphRAG" (2024); Microsoft graphrag open-source (GitHub, 2024) | Microsoft "LazyGraphRAG" (2024); Traag et al. "Leiden Algorithm" (2019); Ji et al. "Knowledge Graph Survey" (2022); Huguet Cabot & Navigli "REBEL" (2021); Neo4j vector index docs; AWS Neptune GraphRAG blog; Diffbot docs; LangChain GraphCypherQAChain; LlamaIndex KnowledgeGraphIndex; Fortunato & Hric "Community Detection" (2016); Christophides et al. "Entity Resolution" (2021) |
| rag/multimodal-rag | Faysse et al. "ColPali" (2024); Radford et al. "CLIP" (2021); Zhai et al. "SigLIP" (2023) | Unstructured.io docs; IBM "Docling" (2024); Radford et al. "Whisper" (2022); Li et al. "BLIP-2" (2023); Liu et al. "LLaVA" (2023); VikParuchuri "Marker" (2024); Google Document AI; Azure Document Intelligence; AWS Textract; Weaviate Multi2Vec-CLIP docs; Chen et al. "Multimodal RAG Survey" (AAAI 2024); Faysse et al. "ViDoRe" (2024) |

---

## Vector Search

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| vector-search/vector-databases | Pinecone, Qdrant, Weaviate, Milvus documentation (2024) | pgvector GitHub changelog; Subramanya et al. "DiskANN" (2019); Pinecone case studies (Notion); Zilliz case studies (Uber); Qdrant blog/case studies (Shopify); Supabase pgvector docs |
| vector-search/embedding-models | OpenAI "text-embedding-3" (2024); Kusupati et al. "Matryoshka" (2022); Chen et al. "BGE-M3" (2024); Muennighoff et al. "MTEB" (2023) | Cohere "Embed v3" (2023); Wang et al. "E5-Mistral" (2024); Nussbaum et al. "Nomic Embed" (2024); Voyage AI docs; Jina AI docs; Reimers & Gurevych "Sentence-BERT" (2019); Oord et al. "InfoNCE/CPC" (2018); MTEB leaderboard |
| vector-search/ann-algorithms | Malkov & Yashunin "HNSW" (IEEE TPAMI, 2018); Subramanya et al. "DiskANN" (NeurIPS 2019); Jegou et al. "Product Quantization / IVF" (2011) | Guo et al. "ScaNN" (ICML 2020); Johnson et al. "FAISS" (2019); ann-benchmarks.com (Aumuller et al., 2020); Qdrant/Milvus/pgvector documentation; Spotify HNSW usage; Airbnb filtered search blog |
| vector-search/hybrid-search | Cormack et al. "RRF" (SIGIR 2009); Thakur et al. "BEIR" (NeurIPS 2021); Formal et al. "SPLADE" (SIGIR 2021) | Formal et al. "SPLADE++ distillation" (2022); Chen et al. "BGE-M3" (2024); Weaviate/Qdrant/Pinecone hybrid search docs; Azure AI Search hybrid benchmarks; Vespa at Spotify; Cohere RAG hybrid default |

---

## Prompt Engineering

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| prompt-engineering/prompt-patterns | Wei et al. "Chain-of-Thought" (2022); Brown et al. "GPT-3 Few-shot" (2020); Yao et al. "ReAct" (2023); Wang et al. "Self-Consistency" (2023); Yao et al. "Tree-of-Thought" (2023) | Kojima et al. "Zero-shot CoT" (2022); Zhou et al. "Least-to-Most" (2023); Khattab et al. "DSPy" (2023); Yang et al. "OPRO" (2023); Jiang et al. "LLMLingua" (2023); Gao et al. "HyDE" (2022); Zheng et al. "Step-back Prompting" (2023); Holtzman et al. "Nucleus Sampling" (2020); Lu et al. "Example Ordering" (2022) |
| prompt-engineering/structured-output | OpenAI JSON mode / Structured Outputs docs (2023-2024); Willard & Louf "Outlines" (2023); Anthropic tool use docs (2024) | Microsoft "Guidance" (2023); Jason Liu "Instructor" (2023); Chen et al. "XGrammar" (2024); Zheng et al. "SGLang" (2024); Beurer-Kellner et al. "LMQL" (2023); Pydantic docs; Zod docs; Vercel AI SDK; Google Gemini function calling docs; Holtzman et al. "Nucleus Sampling" (2020) |
| prompt-engineering/prompt-injection | Perez & Ribeiro "HackAPrompt" (EMNLP 2023); Greshake et al. "Indirect Prompt Injection" (2023); Anthropic "Many-shot Jailbreaking" (2024) | Microsoft "Crescendo" (2024); Microsoft "Skeleton Key" (2024); Wallace et al. "Instruction Hierarchy" (OpenAI, 2024); Willison "Dual-LLM Pattern" (2023); Protect AI "LLM Guard" (2023); Lakera Guard docs; OWASP LLM Top 10 (2024); Bing Chat/Sydney incident reports (2023); Rehberger "ChatGPT Plugin Exploits" (2023) |
| prompt-engineering/context-management | Liu et al. "Lost in the Middle" (2024); Jiang et al. "LLMLingua" (2023); Anthropic/OpenAI/Google prompt/context caching docs (2024) | Pan et al. "LLMLingua-2" (2024); OpenAI tiktoken; Kudo & Richardson "SentencePiece" (2018); Zilliz "GPTCache" (2023); Google "Gemini 1.5" (2024); Agarwal et al. "Many-shot ICL" (2024); LangChain "Conversation Summary Memory"; Cursor engineering blog (2024); Google "NotebookLM" docs |

---

## Agents

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| agents/agent-architecture | Yao et al. "ReAct" (ICLR 2023); Shinn et al. "Reflexion" (NeurIPS 2023); Zhou et al. "LATS" (ICML 2024); Sumers et al. "CoALA" (TMLR 2024) | Wang et al. "Plan-and-Solve" (2023); Schick et al. "Toolformer" (2023); Asai et al. "Self-RAG" (2024); Wang et al. "Voyager" (2023); Jimenez et al. "SWE-bench" (2024); Zhou et al. "WebArena" (2024); Kocsis & Szepesvari "MCTS" (2006); Snell et al. "Test-Time Compute Scaling" (2024); Richards "AutoGPT" (2023); Nakajima "BabyAGI" (2023) |
| agents/tool-use | OpenAI function calling / Structured Outputs docs (2023-2024); Anthropic tool use docs (2024); Anthropic "Model Context Protocol (MCP)" (2024); Schick et al. "Toolformer" (NeurIPS 2023) | Google Gemini function calling docs; Patil et al. "Gorilla" (2023); Li et al. "API-Bank" (2023); Qin et al. "ToolBench/ToolLLM" (ICLR 2024); Greshake et al. "Indirect Prompt Injection" (2023); Yao et al. "ReAct" (2023); OpenAI "ChatGPT Plugins" (2023); LangChain tools docs; MCP specification |
| agents/multi-agent | Du et al. "Multi-agent Debate" (2023); Wu et al. "AutoGen" (Microsoft, 2023); Park et al. "Generative Agents" (Stanford, 2023) | Moura "CrewAI" (2024); LangGraph multi-agent docs (2024-2025); Asai et al. "Self-RAG" (2023); Chase "Supervisor Pattern" (LangChain, 2024); Hayes-Roth "Blackboard Architecture" (1985); Wooldridge "MultiAgent Systems" (2009); Liu et al. "Lost in the Middle" (2024) |
| agents/memory-systems | Packer et al. "MemGPT" (2023); Park et al. "Generative Agents" (Stanford, 2023) | Liu et al. "Lost in the Middle" (2024); LangChain "ConversationSummaryMemory" / "EntityMemory" docs; Tulving "Episodic Memory" (1983); Asai et al. "Self-RAG" (2023); Mem0 docs (2024-2025); Letta platform docs (2024-2025); OpenAI "ChatGPT Memory" (2024) |
| agents/code-agents | Chen et al. "Codex/HumanEval" (OpenAI, 2021); Jimenez et al. "SWE-bench" (2024); GitHub Copilot docs (2024-2025) | Bavarian et al. "Fill-in-the-Middle" (OpenAI, 2022); Cursor/Anysphere engineering blog; Cognition Labs "Devin" (2024); Anthropic "Claude Code" (2025); Gauthier "Aider" (2023-2025); Pearce et al. "Copilot Security" (2022); Leviathan et al. "Speculative Decoding" (2023); tree-sitter docs; AWS "Amazon Q Developer" (2024-2025); Liu et al. "Lost in the Middle" (2024) |

---

## Orchestration

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| orchestration/orchestration-frameworks | LangChain/LCEL docs (2022-present); LlamaIndex docs (2022-present); Khattab et al. "DSPy" (ICLR 2024); Microsoft "Semantic Kernel" (2023-present) | deepset "Haystack" (2019-present); LangSmith docs; LlamaParse docs; Opsahl-Ong et al. "MIPRO" (2024); Yao et al. "ReAct" (2023); Framework community benchmarks |
| orchestration/prompt-chaining | Wu et al. "AI Chains" (CHI 2022); Wei et al. "Chain-of-Thought" (2022); Yao et al. "ReAct" (2023) | Wang et al. "Self-Consistency" (2023); LangChain "Map-Reduce" docs; LangChain "LCEL" docs; LangGraph docs (2024); Asai et al. "Self-RAG" (2024); Yan et al. "CRAG" (2024); Ning et al. "Skeleton-of-Thought" (2023); Khattab et al. "DSPy" (2024); LangChain "Router Chains"; Semantic Kernel planner |
| orchestration/build-vs-buy | LangChain/LangGraph/LangSmith docs; LlamaIndex/LlamaParse docs; Microsoft "Semantic Kernel" docs; deepset "Haystack 2.0" docs | Khattab et al. "DSPy" (2024); Opsahl-Ong et al. "MIPRO" (2024); Gamma et al. "Design Patterns" (1994, adapter pattern); Industry migration blogs (Shopify, Stripe, Notion, 2024-2025) |

---

## Evaluation

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| evaluation/eval-frameworks | Es et al. "RAGAS" (2023); Zheng et al. "LLM-as-Judge / MT-Bench" (LMSYS, 2023); DeepEval docs (Confident AI) | LangSmith docs; Braintrust docs; Patronus AI docs (Lynx model); TruLens docs; Artstein & Poesio "Inter-Coder Agreement" (2008); Dror et al. "Statistical Significance in NLP" (2018); Vectara "HHEM" (2023) |
| evaluation/hallucination-detection | Ji et al. "Hallucination Survey" (2023); Min et al. "FActScore" (2023); Manakul et al. "SelfCheckGPT" (2023); Es et al. "RAGAS" (faithfulness, 2023) | Honovich et al. "TRUE" (NLI-based, 2022); Asai et al. "Self-RAG" (2023); Yan et al. "CRAG" (2024); Vectara "HHEM" (2023); Lin et al. "TruthfulQA" (2022); Li et al. "HaluEval" (2023); Wei et al. "Google SAFE" (2024); Kadavath et al. "Models Know What They Know" (2022); Gao et al. "LLM Citations" (2023); Bai et al. "Constitutional AI" (2022) |
| evaluation/llm-observability | LangSmith docs; Langfuse docs; Arize Phoenix docs; Weights & Biases Weave docs | OpenTelemetry specification / OpenInference; Anyscale "LLM Performance Benchmarks" (2024); Kohavi et al. "Trustworthy Experiments" (2020); Andreessen Horowitz "AI Infrastructure" (2024); Datadog LLM Monitoring docs; Helicone docs; Portkey docs; Google SRE principles (adapted) |
| evaluation/benchmarks | Hendrycks et al. "MMLU" (2021); Chen et al. "HumanEval" (2021); Zheng et al. "MT-Bench/Chatbot Arena" (2023); Jimenez et al. "SWE-bench" (2024) | Wang et al. "MMLU-Pro" (2024); Liu et al. "HumanEval+" (2024); Jain et al. "LiveCodeBench" (2024); Rein et al. "GPQA" (2023); Hendrycks et al. "MATH" (2021); Srivastava et al. "BigBench" (2022); Wei et al. "Emergent Abilities" (2022); Schaeffer et al. "Emergent Abilities Mirage" (2023); Min et al. "FActScore" (2023); Lin et al. "TruthfulQA" (2022); HuggingFace Open LLM Leaderboard; Meta "LLaMA 3 evaluation" (2024); Jacovi et al. / Oren et al. (contamination) |

---

## Safety

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| safety/guardrails | Rebedea et al. "NeMo Guardrails" (NVIDIA, 2023); Inan et al. "Llama Guard" (Meta, 2023); Guardrails AI docs (2023-present) | Meta "Llama Guard 2/3" (2024); MLCommons "AI Safety Benchmark" (2024); OpenAI Moderation API; Jigsaw "Perspective API"; Azure AI Content Safety / Prompt Shields; Lakera Guard; OWASP LLM Top 10 (2024); Protect AI "LLM Guard"; Hanu "Detoxify"; Es et al. "RAGAS groundedness" (2023); Markov et al. "Content Filtering" (OpenAI, 2023); Wallace et al. "Instruction Hierarchy" (2024) |
| safety/pii-protection | Microsoft "Presidio" (2019-present); GDPR (EU 2016/679); HIPAA de-identification guidelines (45 CFR 164.514) | AWS Comprehend PII/Medical; Google Cloud DLP; CCPA (2018); Sweeney "k-anonymity" (2002); Carlini et al. "Training Data Extraction" (2021); Lukas et al. "PII in Language Models" (2023); Bellare et al. "Format-Preserving Encryption" (2016); Dwork & Roth "Differential Privacy" (2014); Inan et al. "Llama Guard" (2023); Apple "Private Cloud Compute" (2024); NIST AI RMF; MLCommons AI Safety; OWASP LLM Top 10 |
| safety/red-teaming | Chao et al. "PAIR" (2023); Mehrotra et al. "TAP" (2024); Zou et al. "GCG" (2023); Anthropic "Many-shot Jailbreaking" (2024) | Russinovich et al. "Crescendo" (Microsoft, 2024); Samvelyan et al. "Rainbow Teaming" (2024); MITRE ATLAS; Microsoft "PyRIT" (2024); DAN jailbreak community; DEF CON AI Red Teaming (2023); Anthropic RSP (2023-2024); Google "Frontier Safety Framework" (2024); NIST AI 100-2e2023 |
| safety/ai-governance | EU AI Act (Regulation 2024/1689); NIST AI RMF (AI 100-1, 2023); ISO/IEC 42001:2023 | NIST AI RMF Playbook; NIST "Adversarial ML Taxonomy" (2024); OECD AI Principles (2019/2024); G7 "Hiroshima Process AI Code of Conduct" (2023); US Executive Order 14110 (2023); Mitchell et al. "Model Cards" (2019); OpenAI System Cards (2023-2024); Anthropic RSP; Frontier Model Forum; Caliskan et al. "WEAT" (2017); NIST AI Safety Institute (2024) |

---

## Performance

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| performance/latency-optimization | Leviathan et al. "Speculative Decoding" (2023); Patel et al. "Splitwise" (2024); Dao et al. "FlashAttention" (2022); Jiang et al. "LLMLingua" (2023) | Cai et al. "Medusa" (2024); Li et al. "EAGLE" (2024); Zhong et al. "DistServe" (2024); Liu et al. "Mooncake" (2024); Agrawal et al. "Sarathi" (2024); Jiang et al. "LongLLMLingua" (2024); Zheng et al. "SGLang/RadixAttention" (2024); Kwon et al. "vLLM/PagedAttention" (2023); Shah et al. "FlashAttention-3" (2024); Zhang et al. "H2O" (2023); Groq LPU docs; WHATWG "Server-Sent Events"; Anthropic/OpenAI prompt caching docs |
| performance/semantic-caching | Zilliz/Bang Liu "GPTCache" (2023); Kusupati et al. "Matryoshka" (2022) | Zhu et al. "Scalable Semantic Cache" (2024); Johnson et al. "FAISS" (2019); Malkov & Yashunin "HNSW" (2018); Anthropic/OpenAI prompt caching docs; Redis vector search; Milvus docs; LangChain caching; Portkey AI gateway; Wang et al. "E5" (2022); Xiao et al. "BGE" (2023); Megiddo & Modha "ARC" (cache replacement, 2003) |
| performance/cost-optimization | Chen et al. "FrugalGPT" (Stanford, 2023); Jiang et al. "LLMLingua" (2023); OpenAI/Anthropic/Google pricing docs and APIs | Jiang et al. "LongLLMLingua" (2024); Anthropic prompt caching; OpenAI Batch API; OpenAI "GPT-4o mini" blog; Anyscale "Serving LLMs Cost Analysis"; Ding et al. "Hybrid LLM Routing" (2024); Martian "Cost Controls" blog; AWS/GCP/Azure spot instance pricing; LangChain "Conversation Summary Memory"; AutoGPT/BabyAGI token budget management |
| performance/model-routing | Chen et al. "FrugalGPT" (2023); Ong et al. "RouteLLM" (LMSYS, 2024); Ding et al. "Hybrid LLM Routing" (2024) | BerriAI "LiteLLM"; Portkey AI Gateway; OpenRouter; Martian "Model Router"; Unify AI; Anthropic model tiering; Kadavath et al. "Models Know What They Know" (2022); Wang et al. "Self-Consistency" (2023); Zheng et al. "LLM-as-Judge" (2023); Nygard "Circuit Breaker Pattern" (2007); Kohavi et al. "A/B Testing" (2020) |

---

## Case Studies

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| case-studies/chatbot-architecture | Production architecture patterns from Notion, Intercom, Zendesk engineering blogs; LangChain/LlamaIndex chat agent documentation | Anthropic/OpenAI streaming API docs; Redis/DynamoDB session management patterns; NeMo Guardrails; WebSocket/SSE specifications |
| case-studies/copilot-architecture | Chen et al. "Codex/HumanEval" (2021); GitHub Copilot documentation; Cursor/Anysphere engineering blog | Bavarian et al. "Fill-in-the-Middle" (2022); tree-sitter docs; LSP specification; Gauthier "Aider" docs; Anthropic "Claude Code" (2025); Leviathan et al. "Speculative Decoding" (2023) |
| case-studies/enterprise-search | Hybrid search patterns from Weaviate/Pinecone/Qdrant documentation; ACL enforcement patterns from enterprise deployments | Lewis et al. "RAG" (2020); Cormack et al. "RRF" (2009); Formal et al. "SPLADE" (2021); Google Workspace / SharePoint / Confluence connector documentation |
| case-studies/voice-ai | Radford et al. "Whisper" (2022); OpenAI GPT-4o Realtime API docs; ElevenLabs documentation | Deepgram Nova-2; WebRTC specification; XTTS/Coqui docs; Fish Speech; Silero VAD; Daily.co/LiveKit/Twilio real-time communication platforms |
| case-studies/genai-gateway | Portkey AI Gateway docs; BerriAI "LiteLLM" docs; Kong/Envoy proxy documentation | OpenAI/Anthropic/Google API specifications; Nginx/HAProxy patterns; OpenTelemetry for LLM; Helicone docs; Rate limiting and circuit breaker patterns |
| case-studies/kubernetes-genai | NVIDIA GPU Operator docs; Kubernetes scheduler documentation; KNative Serving docs | NVIDIA MIG / time-slicing docs; KEDA autoscaler; vLLM Kubernetes deployment guides; Ray Serve on K8s; Triton Inference Server K8s integration |

---

## Patterns

| Topic File | Primary Sources | Secondary Sources |
|------------|----------------|-------------------|
| patterns/genai-design-patterns | Cross-cutting patterns synthesized from multiple domain files; industry engineering blogs (Stripe, Notion, Replit, Perplexity) | Gamma et al. "Design Patterns" (1994, adapted); Nygard "Release It!" (circuit breaker); Fowler "Strangler Fig Pattern"; GenAI-specific patterns from LangChain, LlamaIndex documentation |
| patterns/deployment-patterns | Blue-green, canary, shadow deployment patterns adapted for GenAI; LLM evaluation-driven deployment | Kohavi et al. "A/B Testing" (2020); Google SRE principles; Feature flag systems (LaunchDarkly); LangSmith/Braintrust experiment management; Model versioning patterns from MLflow/W&B |
