# Source Inventory

## YouTube Video Reports

### 1.md
Covers foundational distributed systems principles including container orchestration in Kubernetes.

- Container runtimes (OCI, runc, containerd, CRI-O) and Docker Shim deprecation
- Kubernetes cost management (spot instances, affinity rules, HPA)
- Rate limiting and throttling patterns applicable to K8s ingress

**K8s topics informed:** 01-foundations/04-container-runtime, 06-scaling-design/01-horizontal-pod-autoscaling, 11-operations/04-cost-optimization

### 5.md
Covers system metrics, network infrastructure, Kubernetes pillars, auto-scaling, and video streaming architecture.

- Kubernetes five pillars (computation, networking, storage, security, custom resources)
- Auto-scaling with Horizontal Pod Autoscaler (HPA) and metrics server
- Network infrastructure: security groups, subnets, bastion hosts
- Layer 4 vs. Layer 7 load balancing

**K8s topics informed:** 01-foundations/01-kubernetes-architecture, 01-foundations/05-kubernetes-networking-model, 06-scaling-design/01-horizontal-pod-autoscaling, 06-scaling-design/02-vertical-and-cluster-autoscaling, 07-security-design/01-rbac-and-access-control

### 7.md
Covers scaling paradigms, consistency models, Kubernetes observability, and the five pillars of Kubernetes.

- Kubernetes five pillars and custom resources
- Observability: logging (ELK) vs. monitoring (Prometheus/Grafana)
- Service monitoring objects for Prometheus scraping
- Vertical vs. horizontal scaling in Kubernetes context

**K8s topics informed:** 01-foundations/01-kubernetes-architecture, 09-observability-design/01-monitoring-and-metrics, 09-observability-design/02-logging-and-tracing, 12-patterns/03-crd-driven-design

---

## PDF Books (Extracted)

### Kubernetes for Generative AI Solutions (source/GenAI/)
Primary source for GPU and AI-specific Kubernetes workload design.

- GPU scheduling and device plugins in Kubernetes
- Model serving on Kubernetes (KServe, Triton, vLLM)
- Multi-tenancy for ML workloads
- Autoscaling GPU workloads (KEDA, Karpenter)
- Storage patterns for model artifacts

**K8s topics informed:** 03-workload-design/05-gpu-and-accelerator-workloads, 05-storage-design/04-model-and-artifact-delivery, 06-scaling-design/04-gpu-aware-autoscaling, 13-case-studies/07-gpu-cluster-genai-inference

---

## Web Research (Primary Sources)

The Kubernetes pillar was primarily authored using web research from official documentation, CNCF projects, and industry engineering blogs. The following sources informed the content:

### Official Kubernetes Documentation (kubernetes.io)
The canonical reference for all core Kubernetes concepts.

- Architecture: control plane components, kubelet, kube-proxy
- API server design, admission controllers, API aggregation
- etcd as the cluster state store
- Container Runtime Interface (CRI) specification
- Networking model (flat network, CNI contract)
- Service types (ClusterIP, NodePort, LoadBalancer, ExternalName)
- Ingress and Gateway API specifications
- PersistentVolume, PersistentVolumeClaim, StorageClass
- Container Storage Interface (CSI)
- HPA, VPA, Cluster Autoscaler
- RBAC (Roles, ClusterRoles, Bindings)
- NetworkPolicy specification
- Pod Security Standards / Pod Security Admission
- Jobs, CronJobs, DaemonSets, StatefulSets
- Custom Resource Definitions (CRDs) and Operator pattern

**K8s topics informed:** All 64 topic files reference official documentation as baseline

### CNCF Landscape and Project Documentation
Documentation from graduated and incubating CNCF projects.

- **Prometheus / Grafana** -- monitoring and metrics pipelines
- **Envoy / Istio / Linkerd** -- service mesh architecture and data plane
- **Helm** -- package management and chart templating
- **Argo (CD, Rollouts, Workflows)** -- GitOps, progressive delivery, workflow orchestration
- **Flux** -- GitOps continuous delivery
- **KEDA** -- event-driven autoscaling
- **Falco** -- runtime security and threat detection
- **OPA / Gatekeeper** -- policy-as-code admission control
- **Kyverno** -- Kubernetes-native policy engine
- **Velero** -- backup and disaster recovery
- **Crossplane** -- infrastructure-as-code via CRDs
- **Backstage** -- internal developer platform / service catalog
- **cert-manager** -- automated TLS certificate management
- **CoreDNS** -- cluster DNS and service discovery
- **Cilium** -- eBPF-based CNI and network policy
- **Calico** -- CNI networking and network policy
- **Jaeger / OpenTelemetry** -- distributed tracing
- **Fluentd / Fluent Bit** -- log collection and forwarding
- **Thanos / Cortex** -- long-term Prometheus storage

**K8s topics informed:** 04-networking-design/03-service-mesh, 07-security-design/02-policy-engines, 07-security-design/05-runtime-security, 08-deployment-design/01-gitops-and-flux-argocd, 08-deployment-design/02-helm-and-kustomize, 08-deployment-design/04-progressive-delivery, 09-observability-design/01-monitoring-and-metrics, 09-observability-design/02-logging-and-tracing, 10-platform-design/01-internal-developer-platform, 11-operations/02-disaster-recovery, 06-scaling-design/03-keda-and-event-driven-scaling

### Industry Engineering Blogs
Production experiences from organizations running Kubernetes at scale.

- **Spotify Engineering** -- Backstage, internal developer platform, golden paths
- **Airbnb Engineering** -- multi-cluster architecture, service mesh migration
- **Pinterest Engineering** -- Kubernetes cost optimization, spot instance strategies
- **Datadog Engineering** -- cost observability, Kubecost integration
- **OpenAI / Anyscale** -- GPU cluster management, model serving at scale
- **Platform9 / Giant Swarm / Loft Labs** -- multi-tenancy (vCluster, Capsule)
- **Weaveworks** (archived) -- GitOps methodology and Flux origins
- **Shopify Engineering** -- cluster upgrades, zero-downtime migrations
- **Target / Capital One** -- enterprise Kubernetes governance

**K8s topics informed:** 13-case-studies/01-spotify-platform, 13-case-studies/02-airbnb-multi-cluster, 13-case-studies/03-pinterest-cost-optimization, 10-platform-design/02-multi-tenancy, 11-operations/01-cluster-upgrades, 13-case-studies/09-enterprise-kubernetes-at-scale

### Cloud Provider Kubernetes Documentation
Managed Kubernetes service documentation from major cloud providers.

- **AWS EKS** -- managed control plane, Fargate, Karpenter, EBS CSI, EFS CSI
- **Google GKE** -- Autopilot, GKE Gateway, Workload Identity
- **Azure AKS** -- KEDA integration, Azure AD pod identity, Azure Disk CSI

**K8s topics informed:** 02-cluster-design/04-cloud-vs-bare-metal, 05-storage-design/02-csi-drivers-and-storage-classes, 06-scaling-design/02-vertical-and-cluster-autoscaling

### Kubernetes Design Pattern References
Published books and pattern catalogs for Kubernetes design.

- **Kubernetes Patterns** (Ibryam & Huss, O'Reilly) -- foundational, behavioral, structural, and configuration patterns
- **Production Kubernetes** (Rosso et al., O'Reilly) -- cluster design, multi-tenancy, security hardening
- **Kubernetes Best Practices** (Burns et al., O'Reilly) -- operational patterns, monitoring, CI/CD
- **The Kubernetes Book** (Poulton) -- architecture and workload patterns

**K8s topics informed:** 03-workload-design/01-pod-design-patterns, 12-patterns/01-operator-pattern, 12-patterns/02-sidecar-and-ambassador, 12-patterns/04-kubernetes-anti-patterns, 12-patterns/05-migration-patterns
