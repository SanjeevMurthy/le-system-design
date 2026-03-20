# System Design Glossary

An alphabetical reference of key terms and concepts found across the system design knowledge base, covering traditional distributed systems, Generative AI, and Kubernetes system design.

---

## A

- **ACID**: Atomicity, Consistency, Isolation, Durability -- the four properties that guarantee database transactions are processed reliably, ensuring all-or-nothing completion, valid state transitions, independent concurrent execution, and data permanence.
- **Activation Function**: A mathematical function (e.g., ReLU, GELU, SiLU) applied after linear transformations in neural networks to introduce non-linearity, enabling the model to learn complex patterns.
- **Adapter Layer**: A small trainable module inserted into a frozen pre-trained model during parameter-efficient fine-tuning, allowing task-specific adaptation without modifying the original weights.
- **Adaptive Bitrate Streaming (ABS)**: A video delivery technique (via HLS or MPEG-DASH) where the source video is encoded into multiple resolutions and segmented into small chunks, allowing the client to dynamically switch quality based on network bandwidth.
- **Agentic RAG**: A RAG architecture where an LLM agent autonomously decides when to retrieve, what queries to issue, and how many retrieval iterations to perform, rather than following a fixed retrieve-then-generate pipeline.
- **AI Governance**: The organizational, regulatory, and technical framework for ensuring AI systems are developed and deployed in ways that are safe, fair, transparent, and accountable, encompassing model cards, audit trails, bias testing, and regulatory compliance.
- **Alignment**: The process of steering a language model's behavior from raw next-token prediction toward being helpful, harmless, and honest, typically through supervised fine-tuning (SFT) followed by preference optimization (RLHF or DPO).
- **ANN (Approximate Nearest Neighbor)**: A class of algorithms (HNSW, IVF, PQ, ScaNN) that find the k most similar vectors to a query in sub-linear time by trading a small amount of recall accuracy for orders-of-magnitude speedup over brute-force search.
- **Admission Controller (Kubernetes)**: A plugin that intercepts requests to the Kubernetes API server after authentication/authorization but before persistence, used for validation (rejecting non-compliant resources) and mutation (injecting sidecars, setting defaults); key for policy enforcement via OPA/Gatekeeper and Kyverno.
- **Ambient Mesh**: A sidecar-less service mesh architecture (pioneered by Istio) that uses per-node ztunnel proxies for L4 mTLS and optional per-namespace waypoint proxies for L7 policy, eliminating the resource overhead and operational complexity of sidecar injection.
- **API (Application Programming Interface)**: A formal contract between software intermediaries that defines endpoints, methods, parameters, and response formats, enabling systems to interact predictably regardless of underlying implementation.
- **ArgoCD**: A declarative, GitOps-based continuous delivery tool for Kubernetes that automatically synchronizes cluster state with Git repository definitions, supporting Application CRDs, sync waves, health checks, and automated rollback.
- **API Gateway**: A centralized entry point for microservices that handles cross-cutting concerns such as request routing, authentication, authorization, rate limiting, SSL termination, and logging.
- **Append-Only Log**: An immutable, sequential data structure where new entries are only added to the end, used in event sourcing, Kafka topics, LSM trees, and write-ahead logs for durability and auditability.
- **Attention Mechanism**: The core computation in Transformer models where each token computes a weighted sum over all other tokens' representations, with weights determined by learned query-key dot products, enabling the model to focus on relevant context regardless of position.
- **Argo Rollouts**: A Kubernetes controller that provides advanced deployment strategies (canary, blue-green, progressive delivery) with metrics-driven analysis and automated rollback, extending beyond native Kubernetes Deployment capabilities.
- **Autoscaling**: The automatic adjustment of compute resources (e.g., adding or removing server instances) in response to changing traffic loads, commonly implemented via Horizontal Pod Autoscaler (HPA) in Kubernetes.
- **Availability**: The percentage of time a system can accept requests and return desired responses, measured in "nines" (e.g., 99.99% or "four nines" allows 52.6 minutes of downtime per year).
- **AWQ (Activation-Aware Weight Quantization)**: A quantization method that identifies and preserves the most important weights (those corresponding to large activation magnitudes) at higher precision while aggressively quantizing the rest, achieving better quality than naive round-to-nearest quantization.

## B

- **Backstage**: An open-source developer portal (originally created by Spotify, now a CNCF project) that provides a unified service catalog, software templates, and plugin ecosystem for building internal developer platforms.
- **Back-of-the-Envelope Estimation**: Quick, order-of-magnitude calculations used during system design to validate feasibility -- for example, computing storage needs (3.6 trillion posts x 1 KB = 3.6 PB) or QPS (10^8 DAU / 10^5 seconds = 1,000 QPS).
- **Back Pressure**: A flow control mechanism where a downstream system signals an upstream producer to slow down when it cannot keep up with the incoming message rate.
- **BASE (Basically Available, Soft state, Eventual consistency)**: An alternative to ACID for distributed systems that prioritizes availability over immediate consistency, accepting that replicas will eventually converge.
- **Bastion Host / Jump Host**: A hardened server in a public subnet that serves as the single audited entry point for SSH access to instances in private subnets.
- **Batch Processing**: Periodically processing accumulated data in bulk, as opposed to real-time stream processing; tools include Airflow, Spark, and Hive with MapReduce.
- **Beam Search**: A decoding strategy that maintains the top-k most probable partial sequences at each generation step, trading compute for higher-quality output compared to greedy decoding.
- **Bloom Filter**: A space-efficient probabilistic data structure that tests set membership, returning "definitely not in the set" or "possibly in the set," used for URL deduplication in web crawlers and avoiding redundant database lookups.
- **BPE (Byte Pair Encoding)**: The dominant tokenization algorithm for modern LLMs that iteratively merges the most frequent adjacent byte/character pairs in a training corpus to build a subword vocabulary, used by GPT, LLaMA, and most open models.
- **B-Tree**: The industry-standard disk-based index structure that maintains sorted data across root nodes, child pointers, and leaf pages, supporting both exact-match and range queries efficiently.
- **Bulkhead Pattern**: A fault-tolerance mechanism that isolates a system into independent pools (e.g., separate thread pools per endpoint) so that failure in one pool does not cascade to the entire system.

## C

- **Calico**: A CNI plugin for Kubernetes that provides networking and network policy enforcement using BGP routing (no overlay) or VXLAN, supporting both Kubernetes NetworkPolicy and its own extended GlobalNetworkPolicy for cluster-wide rules.
- **Capsule**: A Kubernetes multi-tenancy framework that groups namespaces into "Tenants" with shared policies, resource quotas, and network restrictions, providing soft multi-tenancy without the overhead of separate clusters or virtual clusters.
- **Cache-Aside (Lazy Loading)**: A caching strategy where the application checks the cache first; on a miss, it fetches from the database and populates the cache for subsequent requests.
- **Cache Stampede (Thundering Herd)**: A failure scenario where a hot cache key expires and millions of simultaneous requests hit the database; mitigated by request coalescing or cache warming.
- **Cache Warming**: Pre-populating a cache with anticipated data before the first user request to eliminate cold-start misses.
- **Canary Release**: A deployment strategy that routes a small percentage of traffic (e.g., 5%) to a new software version to detect issues before full rollout.
- **CAP Theorem**: States that during a network partition in a distributed system, you must choose between Consistency (all nodes see the same data) and Availability (every request receives a response); Partition tolerance is assumed.
- **Cassandra**: A distributed NoSQL wide-column database designed for massive write throughput with no single point of failure, using a leaderless architecture, gossip protocol, tunable consistency (ANY/ONE/QUORUM/ALL), and an append-only storage model (commit log, MemTable, SSTable, compaction).
- **CDC (Change Data Capture)**: A pattern for logging data change events from a source database to an event stream, enabling downstream services to stay synchronized without polluting application logic.
- **CDN (Content Delivery Network)**: A geographically distributed network of edge servers that caches and serves static assets (images, CSS, JS, video) from locations proximate to end users, reducing latency.
- **Chain-of-Thought (CoT)**: A prompting technique that instructs the LLM to show its reasoning step-by-step before producing a final answer, dramatically improving accuracy on math, logic, and multi-step reasoning tasks.
- **Checkpointing**: Writing progress markers during data processing so that if a worker fails, the replacement can resume from the last checkpoint rather than reprocessing everything.
- **Chunking**: The process of splitting parsed documents into smaller, semantically coherent units that serve as atomic retrieval units in a RAG system, with strategies including fixed-size, recursive, semantic, and parent-child chunking.
- **Cilium**: An eBPF-based CNI plugin for Kubernetes that provides high-performance networking, network policy enforcement, load balancing, and observability directly in the Linux kernel, also offering sidecar-less service mesh capabilities.
- **Cluster Autoscaler**: A Kubernetes controller that automatically adjusts the number of nodes in a cluster by adding nodes when pods are unschedulable due to insufficient resources and removing underutilized nodes to reduce cost.
- **ClusterIP**: The default Kubernetes Service type that exposes a service on an internal IP address reachable only within the cluster, providing stable endpoints for pod-to-pod communication via kube-proxy and iptables/IPVS rules.
- **CNI (Container Network Interface)**: A CNCF specification that defines how networking plugins configure container network interfaces in Kubernetes, with implementations including Calico, Cilium, Flannel, Weave Net, and cloud-provider CNIs (AWS VPC CNI, Azure CNI).
- **Circuit Breaker**: A resilience pattern that monitors downstream service failures and "trips" to fail fast when an error threshold is exceeded, preventing cascading failures and allowing the failing service to recover.
- **Claude**: Anthropic's family of large language models, known for long context windows (up to 1M tokens), strong instruction-following, and Constitutional AI alignment; model tiers include Haiku (fast/cheap), Sonnet (balanced), and Opus (highest quality).
- **Client-Server Model**: The primary communication paradigm where a client initiates requests and a centralized server processes them and returns responses, following the HTTP request/response cycle.
- **ColBERT (Contextualized Late Interaction over BERT)**: A retrieval model that independently encodes query and document tokens into vectors and scores them via late interaction (MaxSim), achieving cross-encoder-like quality with bi-encoder-like efficiency through pre-computed document token embeddings.
- **Compaction**: A background process in append-only storage systems (e.g., Cassandra, LSM trees) that merges immutable SSTables, resolving duplicates and cleaning up deleted data (tombstones).
- **Compensating Transaction**: A reverse operation executed to undo the effects of a previously completed transaction step in a saga, restoring eventual consistency after a failure.
- **Consistent Hashing**: A distribution technique that maps both data keys and server nodes onto a virtual ring (0 to 2^32), so adding or removing a node only affects a small fraction of keys rather than triggering massive redistribution.
- **containerd**: The industry-standard container runtime that manages the complete container lifecycle (image pull, container creation, execution, storage) on a host, serving as the default CRI implementation in Kubernetes after the Docker shim deprecation.
- **CoreDNS**: The default DNS server in Kubernetes clusters that provides service discovery by resolving service names to ClusterIP addresses, supporting plugins for caching, forwarding, health checks, and custom DNS record generation.
- **CRD (Custom Resource Definition)**: A Kubernetes API extension mechanism that allows users to define new resource types (e.g., PostgresCluster, Certificate) with custom schemas, enabling declarative management of domain-specific objects through the standard Kubernetes API.
- **Crossplane**: A CNCF project that extends Kubernetes with the ability to provision and manage cloud infrastructure (databases, queues, buckets) using Custom Resource Definitions, enabling platform teams to offer self-service infrastructure through the Kubernetes API.
- **CSI (Container Storage Interface)**: A standard interface that enables Kubernetes to expose arbitrary block and file storage systems to containerized workloads, with driver implementations for AWS EBS, GCE PD, Azure Disk, Ceph, Longhorn, and many others.
- **Constitutional AI (CAI)**: Anthropic's alignment approach where the model critiques and revises its own outputs according to a set of explicit principles (a "constitution"), reducing reliance on human feedback for safety training.
- **Consumer Group**: A Kafka concept where multiple consumers share a topic's partitions, ensuring each message is processed by exactly one consumer within the group, enabling horizontal scaling.
- **Context Window**: The maximum number of tokens an LLM can process in a single forward pass, encompassing both input (system prompt, user message, retrieved context) and output tokens; ranges from 4K to 1M+ tokens across modern models.
- **Continuous Batching**: A serving optimization where the inference engine dynamically adds new requests to a running batch as previous requests finish generating, rather than waiting for an entire batch to complete before starting the next one, dramatically improving GPU utilization.
- **Contrastive Learning**: A training approach for embedding models that pulls semantically similar items closer together in vector space and pushes dissimilar items apart, using loss functions like InfoNCE or triplet loss.
- **Count-Min Sketch**: A probabilistic data structure that estimates the frequency of items in a data stream using sub-linear memory, useful for identifying heavy hitters in real-time monitoring.
- **CQRS (Command Query Responsibility Segregation)**: An architectural pattern that separates write operations (commands) from read operations (queries) into different services or data stores, allowing independent optimization and scaling.
- **Cross-Encoder**: A reranking model that takes a query-document pair as joint input to a single Transformer, producing a relevance score via full cross-attention; more accurate than bi-encoders but too slow for initial retrieval over large corpora.

## D

- **DaemonSet**: A Kubernetes workload controller that ensures a copy of a specific pod runs on every node (or a subset of nodes) in the cluster, typically used for node-level agents such as log collectors (Fluent Bit), monitoring exporters (node-exporter), and CNI plugins.
- **DAX (DynamoDB Accelerator)**: An in-memory, write-through cache for DynamoDB that provides microsecond read latency.
- **Dead Letter Queue (DLQ)**: A queue that stores messages that could not be processed successfully after multiple retry attempts, enabling later inspection and reprocessing.
- **Delta Encoding**: A compression technique used in time-series databases that stores only the difference between consecutive values rather than absolute values, dramatically reducing storage.
- **Denormalization**: The deliberate duplication of data across tables to eliminate expensive JOIN operations and optimize read latency, at the cost of increased storage and write complexity.
- **Dense Retrieval**: A retrieval approach that encodes queries and documents as dense vector embeddings and finds matches via approximate nearest neighbor search in vector space, excelling at semantic similarity but potentially missing exact keyword matches.
- **Distillation (Knowledge Distillation)**: The process of transferring knowledge from a large, expensive teacher model to a smaller, cheaper student model by training the student to match the teacher's output distributions, intermediate representations, or behavioral patterns.
- **DNS (Domain Name System)**: The internet's hierarchical naming system that translates human-readable domain names into machine-identifiable IP addresses.
- **DPO (Direct Preference Optimization)**: An alignment technique that directly optimizes a language model on preference pairs (chosen vs rejected responses) without training a separate reward model, simplifying the RLHF pipeline while achieving comparable alignment quality.
- **DSPy**: A framework for programming with LLMs that treats prompts as learnable parameters, automatically optimizing prompt templates and few-shot examples through compilation rather than manual prompt engineering.
- **DynamoDB**: AWS's fully managed NoSQL key-value and document database supporting horizontal scaling with consistent hashing, partition keys, sort keys, GSI/LSI, DynamoDB Streams for CDC, and ACID transactions across up to 100 items.

## E

- **ELK Stack**: A combination of Elasticsearch (search and indexing), Logstash (log collection and transformation), and Kibana (visualization and dashboarding) used for centralized logging and log analysis; Beats was later added as a lightweight data shipper.
- **Elasticsearch**: A distributed search and analytics engine that builds inverted indices for full-text search, supporting fuzzy matching, relevance scoring, and near-real-time indexing.
- **Embedding**: A dense, fixed-dimensional vector representation of text (or other data) in a continuous space where geometric proximity encodes semantic similarity, serving as the foundation for vector search, RAG, and recommendation systems.
- **Embedding Model**: A specialized neural network trained explicitly to produce vector representations optimized for similarity comparison via contrastive learning, distinct from the internal representations of generative LLMs.
- **Encryption at Rest**: Securing stored data by encrypting it on disk, protecting against unauthorized access to physical storage media.
- **EndpointSlice**: A Kubernetes API object that efficiently represents the network endpoints (pod IPs and ports) backing a Service, replacing the older Endpoints resource with better scalability for services with thousands of pods.
- **etcd**: A distributed, strongly consistent key-value store that uses the Raft consensus algorithm, serving as the single source of truth for all Kubernetes cluster state (pods, services, secrets, config maps, RBAC rules).
- **Encryption in Transit**: Protecting data as it moves between systems using protocols like TLS/SSL to prevent interception and tampering.
- **Eventual Consistency**: A consistency model where replicas will converge to the same state given sufficient time, but stale reads are temporarily possible; favored for high-availability systems like social media.
- **Event Driven Architecture (EDA)**: An architectural style where components communicate by announcing events that have already happened rather than requesting work, promoting loose coupling, scalability, and responsiveness.
- **Event Sourcing**: A pattern where all state changes are stored as an immutable, append-only sequence of events (the source of truth), and the current state is reconstructed by replaying ("hydrating") the event log.
- **Exponential Backoff with Jitter**: A retry strategy where wait time between retries increases exponentially, with a random component (jitter) added to prevent synchronized retry storms from multiple clients.
- **Extended Thinking**: A capability where an LLM generates internal reasoning tokens (a "scratchpad") before producing the visible response, enabling deeper multi-step reasoning on complex tasks at the cost of additional latency and token usage.

## F

- **Failover**: The process of automatically switching to a standby system component (e.g., promoting a secondary database leader to primary) when the active component fails.
- **Falco**: A CNCF runtime security tool for Kubernetes that detects anomalous activity in containers and hosts by monitoring system calls using eBPF or kernel modules, triggering alerts for suspicious behavior like shell-in-container, unexpected network connections, or file access violations.
- **Fan-Out on Read (Pull)**: A news feed strategy where feeds are assembled at request time by querying all followed accounts; avoids write amplification but increases read latency.
- **Fan-Out on Write (Push)**: A news feed strategy where a new post is immediately pushed to all followers' pre-computed inboxes; provides ultra-low read latency but causes high write amplification.
- **Feature Flag**: A configuration-driven mechanism (an "if-statement" backed by external config) that allows enabling or disabling features at runtime without a full code deployment, decoupling deployment from release.
- **Few-Shot Prompting**: A prompt technique that provides several input-output examples before the actual query, teaching the LLM the desired format, style, and reasoning pattern through in-context learning rather than fine-tuning.
- **FIM (Fill-in-the-Middle)**: A model training and inference technique where the model predicts missing content between a prefix and suffix, essential for code completion in IDEs where the cursor is in the middle of existing code.
- **Fine-Tuning**: The process of continuing training on a pre-trained language model using task-specific or domain-specific data to specialize its behavior, ranging from full-weight updates to parameter-efficient methods like LoRA.
- **Flagger**: A Kubernetes progressive delivery operator that automates canary, A/B, and blue-green deployments by gradually shifting traffic and evaluating metrics from Prometheus, Datadog, or other providers, automatically promoting or rolling back based on analysis.
- **FlashAttention**: An IO-aware attention algorithm that computes exact self-attention while minimizing GPU memory reads/writes by tiling the computation to exploit the SRAM-HBM memory hierarchy, reducing memory usage from O(n^2) to O(n) and providing 2-4x wall-clock speedup.
- **Flux**: A CNCF GitOps toolkit for Kubernetes that continuously reconciles cluster state with definitions stored in Git repositories, using Kustomization and HelmRelease CRDs to manage deployments, supporting multi-cluster and multi-tenancy patterns.
- **Forward Proxy**: An intermediary that acts on behalf of the client, concealing the client's identity from the destination server (e.g., for accessing geo-restricted content).
- **Function Calling**: The mechanism by which an LLM emits structured JSON invocations (function name + typed arguments) that the host application executes deterministically, enabling the model to interact with APIs, databases, and external tools.

## G

- **GeoDNS**: A DNS service that returns different IP addresses based on the geographic location of the requesting client, routing users to the nearest data center.
- **Geohashing**: A technique that recursively splits the world into a grid and encodes locations as strings where nearby points share common prefixes, enabling efficient proximity queries using standard B-Tree range lookups.
- **Gatekeeper**: A Kubernetes admission controller built on OPA (Open Policy Agent) that enforces custom policies defined as ConstraintTemplates, enabling organizations to codify and enforce cluster-wide governance rules like required labels, image registry restrictions, and resource limit mandates.
- **Gateway API**: The next-generation Kubernetes API for managing ingress traffic, replacing the Ingress resource with role-oriented, expressive, and extensible resources (GatewayClass, Gateway, HTTPRoute, GRPCRoute, TLSRoute) that support traffic splitting, header-based routing, and cross-namespace references.
- **GitOps**: An operational model where the desired state of infrastructure and applications is declaratively defined in Git, and automated controllers (ArgoCD, Flux) continuously reconcile the live system to match the Git source of truth, providing auditability, rollback, and drift detection.
- **Gossip Protocol**: A peer-to-peer communication protocol (also called epidemic protocol) where nodes periodically share state information with randomly selected peers, used by Cassandra and Redis for node discovery and liveness monitoring.
- **GPU (Graphics Processing Unit)**: In the inference context, a massively parallel processor with high-bandwidth memory (HBM) that accelerates LLM inference through matrix multiplication throughput; key models include NVIDIA A100, H100, and H200, with GPU memory capacity being the primary constraint for model serving.
- **GQA (Grouped Query Attention)**: An attention variant where multiple query heads share a single key-value head, reducing KV cache memory by 4-8x compared to multi-head attention while preserving most of the quality; used by LLaMA 2/3, Mistral, and Gemma.
- **GPT (Generative Pre-trained Transformer)**: OpenAI's family of decoder-only Transformer language models, spanning GPT-2 through GPT-4o, that popularized the pre-train-then-fine-tune paradigm and established the commercial LLM market.
- **GPTQ (GPT-Quantized)**: A post-training quantization method that uses approximate second-order information (Hessian inverse) to find optimal rounding decisions for weight quantization, enabling INT4 quantization with minimal quality degradation.
- **Grafana**: An open-source visualization and dashboarding tool commonly paired with Prometheus for real-time system health monitoring.
- **GraphQL**: A query language for APIs that allows clients to specify exactly what data they need in a single request, solving the over-fetching and under-fetching problems of REST.
- **GraphRAG**: A RAG architecture that augments vector retrieval with knowledge graph traversal, enabling multi-hop reasoning, relationship-aware retrieval, and entity-centric question answering that standard vector-only RAG cannot support.
- **gRPC**: A high-performance RPC framework using Protocol Buffers for binary serialization, achieving 5-10x faster communication than JSON-based REST, widely used for internal microservice communication.
- **GSI (Global Secondary Index)**: A DynamoDB index with a completely different partition key and sort key from the base table, enabling alternative query patterns.
- **Guardrails**: Programmable safety and quality enforcement layers that wrap LLM inference, intercepting inputs before they reach the model and validating outputs before they reach the user, providing deterministic behavioral constraints beyond what alignment training can guarantee.

## H

- **Hallucination**: The failure mode where an LLM generates text that is plausible-sounding but factually incorrect, unsupported by provided context, or entirely fabricated, representing the most consequential reliability challenge in production GenAI systems.
- **Hash Index**: An in-memory index structure providing O(1) key lookups but unable to support range queries or sorting; used in key-value stores like Redis.
- **HDFS (Hadoop Distributed File System)**: A distributed, append-only file system that stores data across DataNodes with configurable replication factors, managed by a NameNode for metadata.
- **Headless Service**: A Kubernetes Service with clusterIP set to "None" that does not allocate a virtual IP, instead returning individual pod IPs via DNS, enabling direct pod-to-pod communication; essential for StatefulSets where each pod needs a stable, addressable identity.
- **Helm**: The package manager for Kubernetes that bundles related manifests into reusable charts with Go templating and values.yaml for configuration, supporting versioned releases, upgrades, and rollbacks via `helm install/upgrade/rollback`.
- **HLS (HTTP Live Streaming)**: An adaptive bitrate streaming protocol developed by Apple that segments video into small chunks referenced by an M3U8 manifest file.
- **HNSW (Hierarchical Navigable Small Worlds)**: An algorithm for approximate nearest neighbor search that builds a multi-layer graph of proximity connections, enabling O(log N) search time with high recall; the dominant index type in production vector databases.
- **Horizontal Pod Autoscaler (HPA)**: A Kubernetes controller that automatically scales the number of pods based on observed CPU, memory, or custom metrics.
- **Horizontal Scaling (Scaling Out)**: Adding more machines to a system to distribute load, providing theoretically unlimited capacity and fault isolation; the standard approach for internet-scale systems.
- **Hot Key / Hot Shard**: A data key or partition that receives disproportionately high traffic (e.g., a viral celebrity's profile), overwhelming a single node; mitigated by key salting, dedicated shards, or N-cache strategies.
- **HyDE (Hypothetical Document Embeddings)**: A retrieval technique where the LLM generates a hypothetical answer to the query, which is then embedded and used as the search vector, bridging the semantic gap between short queries and long documents.
- **HyperLogLog**: A probabilistic algorithm for cardinality estimation (counting distinct elements) that uses constant/bounded memory (approximately 1.5 KB) regardless of the number of unique items.

## I

- **Idempotency**: The property that an operation produces the same result whether executed once or multiple times, critical for safe retries in distributed systems to prevent issues like double-charging.
- **Inference**: In the LLM context, the process of running a trained model to generate output tokens from input tokens, encompassing prefill (processing the prompt) and decode (generating tokens autoregressively) phases.
- **Ingress (Kubernetes)**: A Kubernetes API object that manages external HTTP/HTTPS access to services within a cluster, defining rules for host-based and path-based routing, TLS termination, and load balancing through an Ingress controller (NGINX, Traefik, etc.).
- **Inverted Index**: A data structure that maps tokens (words, terms) to the documents or records containing them, enabling fast full-text search; the foundation of Elasticsearch.
- **Istio**: The most widely deployed service mesh for Kubernetes, using Envoy sidecar proxies (or ambient ztunnel mode) to provide mTLS encryption, traffic management (canary, fault injection, retries), and fine-grained observability across microservices without application code changes.
- **IP Address**: A unique numerical identifier assigned to every device on a network, serving as its digital coordinate for routing (IPv4: 32-bit, IPv6: 128-bit).
- **IVF (Inverted File Index)**: An ANN algorithm that partitions the vector space into Voronoi cells using k-means clustering, searching only the nearest clusters at query time to reduce the search space.

## J

- **Jitter**: Random variation added to retry intervals in exponential backoff to prevent multiple clients from retrying simultaneously and causing a secondary overload ("retry storm").
- **JSON Mode**: A model inference setting that constrains the LLM to produce valid JSON output, typically enforced through guided decoding or grammar-based token masking at the logit level.
- **JWT (JSON Web Token)**: A compact, URL-safe token format used for securely transmitting authentication and authorization claims between parties, commonly passed in HTTP headers.

## K

- **Kafka**: A distributed event streaming platform that treats partitions as append-only log files with sequential I/O, providing high-throughput messaging with configurable retention periods, consumer groups, and replication via ZooKeeper.
- **Kappa Architecture**: A simplified alternative to Lambda architecture that uses a single streaming pipeline (e.g., Kafka + Flink) for both real-time and batch processing, avoiding the complexity of maintaining two separate pipelines.
- **Karpenter**: An open-source Kubernetes node provisioner (originally by AWS, now CNCF) that directly provisions right-sized compute instances in response to pending pods, replacing the Cluster Autoscaler with faster scaling, better bin-packing, and support for diverse instance types including GPU nodes.
- **KEDA (Kubernetes Event-Driven Autoscaling)**: A CNCF project that extends Kubernetes HPA with event-driven scaling based on external metrics sources (Kafka lag, Prometheus queries, cloud queue depth), enabling scale-to-zero and fine-grained autoscaling via ScaledObject and ScaledJob CRDs.
- **Knowledge Graph**: A structured representation of entities and their relationships (typically stored as subject-predicate-object triples), used in GraphRAG to enable multi-hop reasoning and relationship-aware retrieval beyond what flat vector search provides.
- **KServe**: A Kubernetes-native model inference platform (formerly KFServing) that provides serverless inference, autoscaling, canary rollouts, and multi-framework support (TensorFlow, PyTorch, Triton, vLLM) for deploying ML/AI models on Kubernetes.
- **Kubebuilder**: A Go framework for building Kubernetes operators and controllers, providing scaffolding, code generation, and testing utilities for implementing custom reconciliation logic against CRDs.
- **Kubecost**: A Kubernetes cost monitoring and management tool that provides real-time cost allocation, showback/chargeback reporting, and optimization recommendations based on resource utilization data.
- **kube-proxy**: A Kubernetes network component running on every node that maintains network rules (via iptables, IPVS, or nftables) to enable Service-to-Pod traffic routing, implementing the ClusterIP, NodePort, and LoadBalancer Service abstractions.
- **Kubernetes (K8s)**: An open-source container orchestration platform that automates deployment, scaling, and management of containerized applications using a declarative model where controllers continuously reconcile actual state with desired state across a cluster of machines.
- **Kustomize**: A Kubernetes-native configuration management tool that customizes YAML manifests without templating, using overlays, patches (strategic merge and JSON patch), and bases to compose environment-specific configurations while keeping the original manifests untouched.
- **KV Cache (Key-Value Cache)**: The mechanism that stores previously computed attention key and value tensors during autoregressive generation, eliminating redundant recomputation and reducing per-token generation from O(n^2) to O(n); its memory footprint is often the primary constraint on batch size and context length.
- **Kyverno**: A Kubernetes-native policy engine that uses YAML-based ClusterPolicy resources (rather than Rego) to validate, mutate, and generate Kubernetes resources, providing a lower learning curve alternative to OPA/Gatekeeper for policy-as-code.

## L

- **Lambda Architecture**: A data processing architecture that runs parallel batch (slow, accurate) and streaming (fast, approximate) pipelines against the same data, combining their outputs for both speed and correctness.
- **LangChain**: An open-source orchestration framework for building LLM applications that provides abstractions for chains, agents, memory, and tool integrations, enabling rapid prototyping of retrieval, generation, and agentic workflows.
- **Latency**: The time between a client sending a request and receiving a response; P99 latency measures the worst-case experience for the bottom 1% of requests, considered the most important metric for user retention.
- **Layer 4 Load Balancing**: Transport-layer load balancing that routes based on IP addresses and TCP/UDP ports without inspecting packet contents; exceptionally fast but unable to make content-aware decisions.
- **Layer 7 Load Balancing**: Application-layer load balancing that inspects HTTP headers, URLs, and cookies for intelligent routing decisions; supports SSL termination and feature-based routing but adds processing overhead.
- **Leaderless Replication**: A database replication strategy where all nodes are equal and accept both reads and writes, using quorum-based consensus (e.g., Cassandra, DynamoDB).
- **Least Connections**: A load balancing algorithm that routes traffic to the server with the fewest active connections, providing load-aware distribution for requests with variable processing times.
- **LimitRange**: A Kubernetes policy object that constrains resource requests and limits at the pod/container level within a namespace, setting defaults and enforcing min/max boundaries to prevent individual workloads from consuming excessive resources.
- **Linearizability**: The strongest consistency guarantee where all operations appear to execute atomically and in real-time order, as if there were only one copy of the data.
- **Linkerd**: A lightweight, security-focused service mesh for Kubernetes that provides mTLS, observability, and reliability features with minimal configuration, using a Rust-based micro-proxy instead of Envoy for lower resource overhead.
- **LlamaIndex**: An open-source data framework for building RAG and agentic LLM applications, specializing in data ingestion, indexing, and retrieval with deep integrations to vector databases and document loaders.
- **LLaMA (Large Language Model Meta AI)**: Meta's family of open-weight language models (LLaMA 1/2/3), ranging from 7B to 405B parameters, that catalyzed the open-source LLM ecosystem by providing high-quality models available for research and commercial use.
- **LLM (Large Language Model)**: A neural network with billions of parameters trained on massive text corpora to predict the next token, capable of generating coherent text, following instructions, reasoning, and performing diverse language tasks through in-context learning.
- **Long Polling**: A communication technique where the client sends a request that the server holds open until new data is available, then responds and the cycle repeats; simpler than WebSockets but ties up connections.
- **LoRA (Low-Rank Adaptation)**: A parameter-efficient fine-tuning method that freezes pre-trained weights and injects trainable low-rank decomposition matrices (A and B) into attention layers, reducing trainable parameters by 90-99% while achieving quality close to full fine-tuning.
- **LSI (Local Secondary Index)**: A DynamoDB index sharing the same partition key as the base table but with a different sort key, providing alternative sorting views on the same partition.
- **LSM Tree (Log-Structured Merge Tree)**: A write-optimized storage structure that performs sequential writes to a Write-Ahead Log and MemTable, then flushes to immutable on-disk segments (SSTables), avoiding random disk seeks.

## M

- **Matryoshka Embeddings**: An embedding training technique that produces vectors where truncating to a shorter prefix still yields a useful embedding, enabling adaptive dimensionality reduction -- store full 1024-dim vectors but search with 256-dim prefixes for faster retrieval with graceful quality degradation.
- **MCP (Model Context Protocol)**: An open standard for connecting LLMs to external data sources and tools, providing a unified protocol for tool discovery, invocation, and context sharing across different AI applications and providers.
- **MCU (Multipoint Control Unit)**: A video conferencing architecture where the server mixes all participant streams into one; CPU-intensive and inflexible, as users cannot individually select or pin speakers.
- **MemTable**: An in-memory, sorted data structure (typically a red-black tree or skip list) that buffers writes before they are flushed to disk as immutable SSTables in LSM-tree-based storage engines.
- **Message Broker**: A program that translates messages between the formal messaging protocols of senders and receivers, decoupling producers from consumers; examples include Kafka and RabbitMQ.
- **Metadata Service**: A shared service that stores information (e.g., IDs, configurations) used by multiple components, reducing message sizes by allowing systems to pass IDs instead of full data payloads.
- **Microservices**: An architectural style where an application is composed of small, independently deployable services with well-defined interfaces, enabling isolated fault domains and independent scaling at the cost of operational complexity.
- **MoE (Mixture of Experts)**: A model architecture that routes each token to a subset of specialized "expert" sub-networks via a learned gating function, enabling models with very large total parameter counts (e.g., Mixtral 8x7B) while only activating a fraction of parameters per token for efficient inference.
- **Model Parallelism**: The set of techniques (tensor, pipeline, data, and expert parallelism) for distributing a model's computation across multiple GPUs when a single device cannot hold the entire model or when throughput requirements demand multi-device execution.
- **Model Routing**: The architectural practice of dynamically selecting which LLM serves each request based on query complexity, cost constraints, and quality thresholds, enabling 60-80% of queries to be served by cheaper models without sacrificing quality on hard queries.
- **MQA (Multi-Query Attention)**: An attention variant where all query heads share a single key-value head, maximally reducing KV cache memory at the cost of some quality; used in Falcon and PaLM.
- **MTBF (Mean Time Between Failures)**: The average time elapsed between system failures, used as a reliability metric.
- **MTTR (Mean Time to Recovery)**: The average time required to restore a system after a failure, used as an availability metric.
- **Multi-Agent System**: An architecture that decomposes complex tasks across multiple specialized LLM-powered agents that coordinate through structured communication protocols, enabling parallel reasoning, adversarial self-critique, and dynamic task decomposition.
- **Multipart Upload**: A technique for uploading large files by splitting them into smaller chunks (typically 5 MB) that are uploaded in parallel and reassembled by the storage provider, improving throughput and resilience.

## N

- **Namespace (Kubernetes)**: A virtual cluster within a Kubernetes cluster that provides scope for resource names, RBAC policies, resource quotas, and network policies, serving as the primary isolation boundary for multi-tenancy.
- **NAT Gateway**: A managed network component that allows instances in private subnets to initiate outbound internet connections while preventing inbound connections from the external internet.
- **NetworkPolicy**: A Kubernetes API object that specifies how groups of pods are allowed to communicate with each other and with external endpoints, defining ingress and egress rules based on pod labels, namespace selectors, and CIDR blocks; requires a CNI plugin (Calico, Cilium) that implements the spec.
- **Node Affinity**: A Kubernetes scheduling constraint that attracts pods to nodes with specific labels (e.g., gpu-type=a100, zone=us-east-1a), supporting both required (hard) and preferred (soft) rules to influence pod placement without mandating it.
- **NeMo Guardrails**: NVIDIA's open-source toolkit for adding programmable guardrails to LLM applications, providing a Colang DSL for defining conversational boundaries, topic control, and fact-checking flows.
- **Normalization**: A database design philosophy where each piece of information exists in exactly one location, enforced through primary and foreign keys, ensuring referential integrity at the cost of requiring JOIN operations for reads.
- **NoSQL**: A broad category of non-relational databases that sacrifice some ACID properties for horizontal scalability and flexible schemas; includes key-value (Redis), document (MongoDB), wide-column (Cassandra), and graph (Neo4j) types.

## O

- **Object Storage**: A flat-namespace storage system (e.g., AWS S3, GCS) designed for large binary objects with immutable writes, achieving 11 nines of durability through erasure coding across multiple facilities.
- **Observability**: The degree to which a system's internal state can be understood from its external outputs (metrics, logs, traces), enabling engineers to diagnose issues and measure performance.
- **OPA (Open Policy Agent)**: A CNCF graduated policy engine that evaluates policies written in Rego against structured data, used in Kubernetes via Gatekeeper as an admission controller to enforce governance rules on resource creation and modification.
- **OpenCost**: A CNCF project that provides real-time Kubernetes cost monitoring by combining cluster resource usage with cloud billing data, offering an open-source alternative to commercial tools like Kubecost.
- **OpenTelemetry (OTel)**: A CNCF observability framework providing vendor-neutral APIs, SDKs, and a Collector for generating and exporting traces, metrics, and logs, serving as the emerging standard for instrumentation across Kubernetes workloads.
- **Operator (Kubernetes)**: A pattern for extending Kubernetes that combines a CRD with a custom controller implementing domain-specific operational logic (e.g., database provisioning, backup, failover), encoding human operational knowledge into software that watches and reconciles custom resources.
- **Orchestration**: A saga coordination pattern where a central orchestrator manages the sequence of steps in a distributed transaction, issuing commands and handling compensating transactions on failure.
- **Orchestration Framework (GenAI)**: Middleware libraries (LangChain, LlamaIndex, Haystack, DSPy, Semantic Kernel) that connect application logic to LLM inference, retrieval, tool execution, and memory management through composable abstractions.
- **OSI Model**: The 7-layer Open Systems Interconnection conceptual framework (Physical, Data Link, Network, Transport, Session, Presentation, Application) that characterizes networking functions.

## P

- **P99 Latency**: The response time at the 99th percentile, meaning 99% of requests complete faster; reveals worst-case "tail latency" that averages conveniently hide and is critical for user experience.
- **PACELC Theorem**: An extension of CAP stating that even when no partition exists (Else), a system must choose between Latency and Consistency.
- **PagedAttention**: A memory management technique (pioneered in vLLM) that allocates KV cache in non-contiguous pages rather than pre-allocating contiguous blocks, reducing GPU memory waste by 60-80% and enabling higher batch sizes.
- **Partition Key**: In distributed databases (e.g., Cassandra, DynamoDB), the key component that determines which physical node stores the data via consistent hashing.
- **Peer-to-Peer (P2P)**: A decentralized communication model where every node acts as both client and server, offering superior resilience but lacking centralized authority; exemplified by BitTorrent and WebRTC.
- **PersistentVolume (PV)**: A Kubernetes storage resource provisioned by an administrator or dynamically via a StorageClass, representing a piece of networked or local storage with a lifecycle independent of any pod that uses it.
- **PersistentVolumeClaim (PVC)**: A Kubernetes request for storage by a user, specifying size, access mode (RWO/ROX/RWX), and StorageClass; the control plane binds it to a matching PersistentVolume, enabling pods to consume durable storage.
- **PII (Personally Identifiable Information)**: Data that can uniquely identify a person (e.g., name, government ID, email), subject to regulations like GDPR and CCPA.
- **Pinecone**: A fully managed, cloud-native vector database purpose-built for similarity search, offering serverless and pod-based deployment tiers with built-in metadata filtering, namespaces, and hybrid search capabilities.
- **Pod**: The smallest deployable unit in Kubernetes, consisting of one or more tightly coupled containers that share a network namespace (same IP), storage volumes, and lifecycle; every container in Kubernetes runs inside a pod.
- **PodDisruptionBudget (PDB)**: A Kubernetes policy that limits the number of pods of a replicated application that can be simultaneously unavailable during voluntary disruptions (node drains, upgrades), ensuring minimum availability during maintenance.
- **Pod Security Standards**: A Kubernetes framework defining three security profiles -- Privileged (unrestricted), Baseline (prevents known privilege escalations), and Restricted (hardened best practices) -- enforced by the Pod Security Admission controller.
- **Polyglot Persistence**: The practice of using different storage technologies for different data needs within the same system, choosing each engine based on specific access patterns and consistency requirements.
- **Pre-Signed URL**: A temporary, time-limited URL generated by the application server that allows a client to upload or download directly to/from object storage (e.g., S3), bypassing the application server as a bandwidth bottleneck.
- **Prefix Caching**: A serving optimization that caches the KV cache entries for shared prompt prefixes (system prompts, few-shot examples) across requests, avoiding redundant prefill computation for the common portion of prompts.
- **Prometheus**: An open-source monitoring system built around a time-series database that pulls metrics from HTTP endpoints, supports PromQL for querying, and integrates with Alertmanager for notifications.
- **Prompt Caching**: A provider-level feature (offered by Anthropic, Google, and others) that caches the processed representation of long, static prompt sections (system prompts, large context documents) server-side, reducing cost and latency for subsequent requests that reuse the same prefix.
- **Prompt Chaining**: The architectural pattern of decomposing a complex LLM task into a sequence of simpler, focused prompts where each step's output feeds the next step's input, improving reliability and debuggability.
- **Prompt Engineering**: The systematic discipline of designing and optimizing the text input to an LLM to control its behavior, format, reasoning approach, and output quality, encompassing techniques from zero-shot through chain-of-thought to structured templates.
- **Prompt Injection**: A security vulnerability where crafted input text is interpreted by the LLM as instructions rather than data, overriding or subverting the developer's system prompt; the most critical vulnerability class in LLM-integrated applications.
- **Protocol Buffers (Protobuf)**: Google's language-neutral binary serialization format used by gRPC that is significantly more compact and faster to parse than JSON.
- **Pub/Sub (Publish/Subscribe)**: An asynchronous messaging pattern where publishers emit events to topics without knowing the subscribers, and subscribers receive all messages on topics they have registered interest in.

## Q

- **QLoRA (Quantized Low-Rank Adaptation)**: A fine-tuning technique that combines LoRA with 4-bit NormalFloat quantization of the base model, enabling fine-tuning of 65B+ parameter models on a single 48GB GPU with minimal quality loss.
- **QPS (Queries Per Second)**: A throughput metric representing the number of requests a system processes per second; a fundamental capacity planning number.
- **Quad-Tree**: A spatial index structure where each node has four children, recursively splitting space into quadrants with finer grids in areas of high data density, used for geospatial queries.
- **Quantization**: In the LLM context, the process of reducing model weight precision from higher-bit formats (FP32, FP16) to lower-bit formats (INT8, INT4, FP8) to reduce memory footprint and increase inference throughput, often the only way to fit large models on available hardware.
- **Quorum**: The minimum number of nodes that must agree for a read or write operation to be considered successful in a distributed system; typically set to N/2 + 1 for consistency guarantees.

## R

- **R-Tree**: The production standard spatial index (used in PostGIS) that groups nearby objects using overlapping bounding rectangles, handling multi-dimensional spatial queries more efficiently than quad-trees.
- **RAG (Retrieval-Augmented Generation)**: An architecture that grounds LLM outputs in external knowledge by retrieving relevant documents at inference time and injecting them into the context window, enabling factual, up-to-date, and attributable responses without model retraining.
- **RAGAS (Retrieval-Augmented Generation Assessment)**: An evaluation framework for RAG systems that measures component-level quality through metrics like faithfulness, answer relevance, context precision, and context recall, enabling targeted debugging of retrieval vs generation failures.
- **Rate Limiting**: A defense mechanism that caps the number of requests a client can make within a time window, protecting against DDoS attacks, maintaining SLAs, and controlling infrastructure costs.
- **RBAC (Role-Based Access Control)**: A security model where permissions are assigned to roles rather than individual users, and users are assigned roles, simplifying access management.
- **ReAct (Reasoning + Acting)**: An agent prompting framework where the LLM alternates between Thought (reasoning about what to do), Action (invoking a tool), and Observation (interpreting the tool's result) in a loop until the task is complete.
- **Read-Through Cache**: A caching pattern where the cache itself fetches data from the database on a miss, simplifying application logic by making the cache act as a proxy.
- **Red Teaming**: The systematic practice of adversarially attacking an AI system to discover safety failures, policy violations, and exploitable behaviors before real users do, encompassing manual probing, automated fuzzing, and structured attack taxonomies.
- **Redis**: A single-threaded, in-memory data structure server providing sub-millisecond latency for caching, rate limiting, leaderboards (sorted sets), pub/sub messaging, geospatial queries, and distributed locking with TTL.
- **Redundancy**: The duplication of critical system components (servers, databases, network paths) so that if one fails, another can take over, eliminating single points of failure.
- **Replication**: Creating and maintaining copies of data on multiple machines to increase availability, reduce latency (geo-proximity), and scale read throughput.
- **ResourceQuota**: A Kubernetes object that limits the total amount of compute resources (CPU, memory), storage, and object counts (pods, services, PVCs) that can be consumed within a namespace, preventing any single tenant from monopolizing cluster capacity.
- **Reranking**: The second stage of a two-stage retrieval pipeline where a more expensive model (cross-encoder or ColBERT) rescores and reorders candidates produced by the initial fast retrieval stage, significantly improving ranking quality.
- **Reverse Proxy**: An intermediary that sits in front of backend servers, receiving client requests and forwarding them to appropriate servers while concealing the backend's identity; handles SSL termination, caching, and IP masking.
- **Ring Attention**: A distributed attention technique that partitions the KV cache across multiple GPUs in a ring topology, with each GPU computing attention over its local partition and passing results to the next, enabling context lengths that exceed single-GPU memory.
- **RLHF (Reinforcement Learning from Human Feedback)**: An alignment technique that trains a reward model from human preference comparisons, then uses reinforcement learning (PPO) to optimize the language model's outputs against the reward model.
- **RoPE (Rotary Position Embedding)**: A positional encoding method that encodes absolute position through rotation matrices applied to query-key pairs, naturally encoding relative distances and supporting position extrapolation beyond training length; used by LLaMA, Mistral, and most modern open models.
- **Round Robin**: A simple load balancing algorithm that distributes requests sequentially across servers in rotation; easy to implement but load-agnostic.
- **RRF (Reciprocal Rank Fusion)**: A score fusion algorithm for hybrid search that combines ranked lists from different retrieval systems (dense + sparse) using reciprocal rank: score = sum(1 / (k + rank_i)), with no need for score normalization.

## S

- **Saga Pattern**: A distributed transaction pattern consisting of a sequence of local transactions, each with a compensating transaction that can undo its effects if a subsequent step fails, coordinated via choreography (parallel) or orchestration (linear).
- **Semantic Caching**: A caching technique for LLM responses that uses vector similarity (not exact key match) to determine cache hits, returning cached responses for semantically similar queries to reduce latency and inference cost.
- **Semantic Search**: A search approach that matches queries to documents based on meaning rather than keyword overlap, typically implemented by embedding both queries and documents into a shared vector space and performing nearest neighbor search.
- **SFU (Selective Forwarding Unit)**: The modern standard for video conferencing (used by Zoom, Google Meet) where the server forwards individual streams to clients without mixing, allowing client-side layout control with minimal server CPU.
- **Sharding**: Horizontal partitioning of data across multiple distributed nodes, where each shard holds a subset of the data, enabling storage and throughput beyond single-machine limits.
- **Single Point of Failure (SPOF)**: Any component whose failure would cause the entire system to become unavailable; eliminated through redundancy, replication, and failover mechanisms.
- **SLA (Service Level Agreement)**: A formal contract specifying performance guarantees (e.g., response time under 100ms, 99.99% uptime) between a service provider and its consumers.
- **SLO (Service Level Objective)**: An internal reliability target (e.g., 99.9% of requests complete in under 200ms) that defines acceptable performance thresholds, providing a tighter goal than the external SLA and enabling error budget-based operations.
- **Sort Key (Clustering Key)**: In DynamoDB or Cassandra, the secondary key component that determines the sorted order of items within a partition, enabling efficient range queries.
- **Sparse Retrieval**: A retrieval approach based on lexical term matching (BM25, TF-IDF, or learned sparse representations like SPLADE), excelling at exact keyword matching and rare terms but unable to handle synonyms or paraphrases.
- **Speculative Decoding**: An inference acceleration technique where a small, fast "draft" model generates candidate tokens that the larger "target" model verifies in parallel, accepting correct predictions and rejecting others; achieves 2-3x speedup with no quality degradation.
- **SPLADE (Sparse Lexical and Expansion Model)**: A learned sparse retrieval model that uses a Transformer to predict term importance weights and expand the query/document vocabulary with semantically related terms, bridging the gap between dense and sparse retrieval.
- **Spot Instance**: Discounted cloud compute capacity (up to 80-90% savings) that can be reclaimed by the provider with short notice, suitable for fault-tolerant workloads when combined with soft affinity rules.
- **SQS (Simple Queue Service)**: AWS's managed message queue service with built-in features like visibility timeouts, exponential backoff, and dead letter queues, often preferred over Kafka for simpler retry use cases.
- **SSE (Server-Sent Events)**: A unidirectional streaming protocol from server to client over standard HTTP, lightweight and firewall-friendly, preferred for broadcast scenarios (e.g., live comments) where bidirectional communication is unnecessary.
- **SSTable (Sorted String Table)**: An immutable, on-disk data structure containing sorted key-value pairs, produced when a MemTable is flushed; the foundation of LSM-tree storage engines.
- **StatefulSet**: A Kubernetes workload controller for managing stateful applications that require stable, unique network identities (pod-0, pod-1, ...), ordered deployment/scaling/deletion, and persistent storage via volumeClaimTemplates; used for databases, message brokers, and distributed systems.
- **Sticky Session**: A load balancer configuration that routes all requests from a particular client to the same backend server, necessary for stateful applications using session data.
- **StorageClass**: A Kubernetes object that defines the parameters for dynamically provisioning PersistentVolumes, including the CSI driver, reclaim policy, volume binding mode, and provider-specific settings (e.g., disk type, IOPS, encryption).
- **Stream Processing**: Continuously processing data events as they arrive in real time, using tools like Flink, Kafka Streams, or Spark Streaming, as opposed to periodic batch processing.
- **Streaming (LLM)**: The practice of delivering LLM output tokens to the client incrementally as they are generated (via SSE or WebSocket) rather than waiting for the full response, reducing perceived latency from seconds to the time-to-first-token.
- **Strong Consistency**: A guarantee that every read reflects the most recent write, requiring synchronous replication and consensus among nodes; mandatory for financial, inventory, and booking systems.
- **System Prompt**: The initial instruction block in an LLM conversation that defines the model's role, constraints, output format, and behavioral boundaries, processed before any user input and typically hidden from the end user.

## T

- **Taint and Toleration**: A Kubernetes scheduling mechanism where taints on nodes repel pods unless those pods have matching tolerations, used to dedicate nodes to specific workloads (GPU, high-memory) or prevent scheduling on control plane nodes.
- **TCP (Transmission Control Protocol)**: A reliable, connection-oriented transport protocol that guarantees ordered delivery of all packets, retransmitting lost data; used for web traffic, file transfers, and databases.
- **Tekton**: A cloud-native, Kubernetes-native CI/CD framework that defines pipeline steps as Task and Pipeline CRDs, running each step as a pod in the cluster, enabling declarative, portable, and reproducible build and deployment workflows.
- **Temperature**: A sampling parameter (typically 0.0-2.0) that controls the randomness of LLM output by scaling the logit distribution before softmax; lower values produce more deterministic output, higher values increase creativity and diversity.
- **Tensor Parallelism**: A model parallelism strategy that shards individual weight matrices across multiple GPUs, with each GPU computing a portion of every layer's output; requires high-bandwidth interconnects (NVLink) due to per-layer all-reduce synchronization.
- **Throughput**: The rate at which a system processes requests or transactions, typically measured in QPS or TPS (transactions per second).
- **TLS (Transport Layer Security)**: The cryptographic protocol (successor to SSL) that provides encrypted communication between clients and servers; TLS termination at a load balancer offloads encryption overhead from application servers.
- **Token**: The atomic unit of text that an LLM processes, typically representing 3-4 characters of English text; every cost, context limit, and latency metric in LLM systems is measured in tokens.
- **Token Bucket Algorithm**: A rate limiting algorithm defined by bucket size (burst capacity) and refill rate (sustained throughput), allowing temporary traffic spikes while enforcing a steady-state rate.
- **Tokenization**: The process of converting raw text into a sequence of discrete integer token IDs using algorithms like BPE or SentencePiece; the first and last transformation in every LLM pipeline, with vocabulary and encoding rules baked immutably into the model at training time.
- **Tombstone**: A marker in append-only databases (e.g., Cassandra, HDFS) indicating that a record has been logically deleted, resolved during compaction.
- **Tool Use**: The capability of an LLM to invoke external tools (APIs, code interpreters, databases, web browsers) via structured function calls, extending the model's abilities beyond text generation to take actions in the world.
- **Top-k / Top-p Sampling**: Decoding strategies that restrict token selection to the k most probable tokens (top-k) or the smallest set of tokens whose cumulative probability exceeds p (top-p / nucleus sampling), balancing quality and diversity.
- **Transformer**: The foundational neural network architecture (Vaswani et al., 2017) behind all modern LLMs, replacing recurrence with self-attention mechanisms to enable fully parallel training and superior performance on language tasks.
- **TTL (Time to Live)**: An expiration duration assigned to data in caches, DNS records, or distributed locks, after which the entry is automatically removed or refreshed.
- **Two-Phase Commit (2PC)**: A distributed transaction protocol where a coordinator asks all participants to prepare, then issues a commit or abort; provides atomicity but introduces a single point of failure at the coordinator.

## U

- **UDP (User Datagram Protocol)**: A connectionless transport protocol that prioritizes speed over reliability by not guaranteeing packet delivery or ordering; used for live streaming, gaming, and DNS lookups.

## V

- **vCluster**: A virtual Kubernetes cluster implementation that runs as a set of pods inside a host cluster, providing each tenant with a fully functional Kubernetes API server and control plane while sharing the underlying infrastructure, enabling strong multi-tenancy isolation without dedicated hardware.
- **Vector Database**: A purpose-built storage system optimized for indexing, storing, and querying high-dimensional vector embeddings at scale using approximate nearest neighbor search; production options include Pinecone, Weaviate, Qdrant, Milvus, and pgvector.
- **Velero**: A CNCF tool for backup and disaster recovery of Kubernetes cluster resources and persistent volumes, supporting scheduled backups, cross-cluster migration, and granular namespace-level restore with storage provider plugins for S3, GCS, and Azure Blob.
- **Vertical Partitioning**: Splitting a database table by columns, moving infrequently accessed or large columns (e.g., blobs) to separate tables to improve query performance on the remaining columns.
- **Vertical Scaling (Scaling Up)**: Increasing the CPU, RAM, or storage of a single machine; simpler but has a hard ceiling defined by hardware limits and creates a catastrophic single point of failure.
- **Virtual Node (vNode)**: In consistent hashing, mapping a single physical server to multiple points on the hash ring to ensure even data distribution and minimize redistribution when nodes are added or removed.
- **Virtual Waiting Room**: A traffic management pattern (e.g., Ticketmaster) that queues users during extreme surges and admits them at a controlled rate, protecting backend services from being overwhelmed.
- **vLLM**: An open-source LLM serving engine that pioneered PagedAttention for efficient KV cache management and continuous batching, achieving 2-4x higher throughput than naive serving implementations; the de facto standard for self-hosted LLM inference.
- **VPA (Vertical Pod Autoscaler)**: A Kubernetes controller that automatically adjusts the CPU and memory requests/limits of pods based on historical usage, right-sizing workloads to improve resource efficiency without manual tuning.
- **VPA (Virtual Payment Address)**: A memorable identifier (e.g., name@bank) used in UPI systems that replaces cumbersome bank account and routing numbers for peer-to-peer payments.

## W

- **WAL (Write-Ahead Log)**: A durability mechanism where changes are first written to a sequential log before being applied to the main data structure, ensuring recovery after crashes.
- **Weaviate**: An open-source vector database with built-in vectorization modules, hybrid search (dense + BM25), multi-tenancy, and GraphQL API, supporting both self-hosted and managed cloud deployment.
- **WebRTC**: A peer-to-peer protocol for real-time audio and video communication directly between browsers, used in video calling but unscalable for large groups without an SFU or MCU.
- **WebSocket**: A full-duplex communication protocol over a persistent TCP connection, enabling bidirectional real-time data exchange between client and server; essential for chat applications but stateful and less scalable than HTTP.
- **Write-Back / Write-Behind Cache**: A caching strategy where writes go to the cache first and are asynchronously flushed to the database in batches, offering high throughput but risking data loss if the cache fails.
- **Write-Through Cache**: A caching strategy where every write simultaneously updates both the cache and the database, guaranteeing consistency at the cost of increased write latency.

## Z

- **Zero-Shot Prompting**: Asking an LLM to perform a task with no examples provided, relying entirely on the model's pre-trained knowledge and instruction-following ability; works well for straightforward tasks but often underperforms few-shot prompting on complex or domain-specific tasks.
- **ZooKeeper**: A distributed coordination service that provides leader election, configuration management, distributed locking, and service discovery using consensus algorithms (Zab protocol), used by Kafka and other distributed systems.
