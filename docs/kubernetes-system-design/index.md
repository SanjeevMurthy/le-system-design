# Kubernetes System Design Knowledge Base

A comprehensive, concept-driven knowledge base for Kubernetes system design -- from cluster architecture through production operations. Every topic exists in exactly one canonical file -- no duplication, full cross-linking.

**64 canonical topic files | 9 case studies | 5 design patterns | [Traditional System Design →](../traditional-system-design/index.md) | [GenAI System Design →](../genai-system-design/index.md)**

---

## Learning Path

### Stage 1: Foundations

Start here to build the mental model for how Kubernetes works under the hood.

1. [Kubernetes Architecture](01-foundations/01-kubernetes-architecture.md) — declarative model, control plane vs data plane, reconciliation loop
2. [Control Plane Internals](01-foundations/02-control-plane-internals.md) — scheduler, controller manager, cloud controller, leader election
3. [API Server and etcd](01-foundations/03-api-server-and-etcd.md) — admission controllers, watch mechanism, etcd Raft consensus
4. [Container Runtime](01-foundations/04-container-runtime.md) — CRI, containerd, CRI-O, OCI spec, gVisor, Kata Containers
5. [Kubernetes Networking Model](01-foundations/05-kubernetes-networking-model.md) — flat network contract, CNI plugins, pod-to-pod communication

### Stage 2: Cluster Architecture

Designing clusters for reliability, cost, and operational efficiency.

1. [Cluster Topology](02-cluster-design/01-cluster-topology.md) — single vs multi-zone, HA control plane, stacked vs external etcd
2. [Node Pool Strategy](02-cluster-design/02-node-pool-strategy.md) — instance types, taints/tolerations, affinity, spot vs on-demand
3. [Multi-Cluster Architecture](02-cluster-design/03-multi-cluster-architecture.md) — fleet management, federation, hub-spoke, GitOps multi-cluster
4. [Cloud vs Bare-Metal](02-cluster-design/04-cloud-vs-bare-metal.md) — EKS/GKE/AKS, kubeadm, k3s, RKE2, Talos Linux

### Stage 3: Workload Design

Structuring applications to run well on Kubernetes.

1. [Pod Design Patterns](03-workload-design/01-pod-design-patterns.md) — sidecar, init container, ambassador, adapter, multi-container pods
2. [Deployment Strategies](03-workload-design/02-deployment-strategies.md) — rolling update, recreate, maxSurge/maxUnavailable, rollback
3. [StatefulSets and Stateful Workloads](03-workload-design/03-statefulsets-and-stateful-workloads.md) — ordered deployment, stable identities, headless services
4. [Jobs and Batch Processing](03-workload-design/04-jobs-and-batch-processing.md) — Job, CronJob, parallelism, indexed jobs, TTL controller
5. [GPU and Accelerator Workloads](03-workload-design/05-gpu-and-accelerator-workloads.md) — NVIDIA device plugin, MIG, time-slicing, GPU operator

### Stage 4: Networking

How traffic flows inside and into Kubernetes clusters.

1. [Service Networking](04-networking-design/01-service-networking.md) — ClusterIP, NodePort, LoadBalancer, kube-proxy, iptables/IPVS
2. [Ingress and Gateway API](04-networking-design/02-ingress-and-gateway-api.md) — Ingress controllers, Gateway API, HTTPRoute, TLS termination
3. [Service Mesh](04-networking-design/03-service-mesh.md) — Istio, Linkerd, Envoy, mTLS, traffic management, ambient mesh
4. [DNS and Service Discovery](04-networking-design/04-dns-and-service-discovery.md) — CoreDNS, service FQDN, headless service DNS, ExternalDNS
5. [Network Policies](04-networking-design/05-network-policies.md) — ingress/egress rules, default deny, microsegmentation, Calico, Cilium

### Stage 5: Storage

Persistent data on an ephemeral platform.

1. [Persistent Storage Architecture](05-storage-design/01-persistent-storage-architecture.md) — PV, PVC, StorageClass, dynamic provisioning, access modes
2. [CSI Drivers and Storage Classes](05-storage-design/02-csi-drivers-and-storage-classes.md) — CSI specification, EBS/EFS/Ceph/Longhorn drivers, snapshots
3. [Stateful Data Patterns](05-storage-design/03-stateful-data-patterns.md) — databases on Kubernetes, operator-managed data, local PV, data gravity
4. [Model and Artifact Delivery](05-storage-design/04-model-and-artifact-delivery.md) — model registries, OCI artifacts, init container model pull, caching

### Stage 6: Scaling

Matching capacity to demand automatically.

1. [Horizontal Pod Autoscaling](06-scaling-design/01-horizontal-pod-autoscaling.md) — HPA, metrics server, custom/external metrics, scaling policies
2. [Vertical and Cluster Autoscaling](06-scaling-design/02-vertical-and-cluster-autoscaling.md) — VPA, Cluster Autoscaler, Karpenter, right-sizing, bin-packing
3. [KEDA and Event-Driven Scaling](06-scaling-design/03-keda-and-event-driven-scaling.md) — ScaledObject, ScaledJob, scale-to-zero, external scalers
4. [GPU-Aware Autoscaling](06-scaling-design/04-gpu-aware-autoscaling.md) — DCGM metrics, fractional GPU, Karpenter GPU provisioning

### Stage 7: Security

Defense in depth for cluster and workload security.

1. [RBAC and Access Control](07-security-design/01-rbac-and-access-control.md) — Roles, ClusterRoles, Bindings, ServiceAccounts, OIDC, audit logging
2. [Policy Engines](07-security-design/02-policy-engines.md) — OPA/Gatekeeper, Kyverno, admission controllers, policy-as-code
3. [Supply Chain Security](07-security-design/03-supply-chain-security.md) — Cosign, Sigstore, Trivy, SBOM, image verification
4. [Secrets Management](07-security-design/04-secrets-management.md) — Vault, external-secrets-operator, sealed-secrets, CSI secret store
5. [Runtime Security](07-security-design/05-runtime-security.md) — Falco, Pod Security Standards, seccomp, AppArmor, security contexts

### Stage 8: Deployment

Getting code into clusters safely and repeatably.

1. [GitOps and Flux/ArgoCD](08-deployment-design/01-gitops-and-flux-argocd.md) — pull-based deployment, Git as source of truth, drift detection, sync waves
2. [Helm and Kustomize](08-deployment-design/02-helm-and-kustomize.md) — charts, templates, overlays, strategic merge patches, bases
3. [CI/CD Pipelines](08-deployment-design/03-cicd-pipelines.md) — Tekton, GitHub Actions, Kaniko, artifact and environment promotion
4. [Progressive Delivery](08-deployment-design/04-progressive-delivery.md) — Argo Rollouts, Flagger, canary analysis, metrics-driven promotion

### Stage 9: Observability

Knowing what is happening across the cluster.

1. [Monitoring and Metrics](09-observability-design/01-monitoring-and-metrics.md) — Prometheus, Grafana, kube-state-metrics, PromQL, Thanos/Mimir
2. [Logging and Tracing](09-observability-design/02-logging-and-tracing.md) — Fluent Bit, Loki, OpenTelemetry, Jaeger, Tempo, trace propagation
3. [Cost Observability](09-observability-design/03-cost-observability.md) — Kubecost, OpenCost, cost allocation, showback/chargeback
4. [SLO-Based Operations](09-observability-design/04-slo-based-operations.md) — SLI, SLO, error budgets, burn rate alerting, Pyrra, Sloth

### Stage 10: Platform Engineering

Building the platform that teams build on.

1. [Internal Developer Platform](10-platform-design/01-internal-developer-platform.md) — Backstage, service catalogs, golden paths, platform teams
2. [Multi-Tenancy](10-platform-design/02-multi-tenancy.md) — namespace isolation, vCluster, Capsule, resource quotas, soft vs hard
3. [Self-Service Abstractions](10-platform-design/03-self-service-abstractions.md) — Crossplane, Kratix, XRDs, platform API, environment provisioning
4. [Developer Experience](10-platform-design/04-developer-experience.md) — Tilt, Skaffold, Telepresence, inner loop vs outer loop
5. [Enterprise Kubernetes Platform](10-platform-design/05-enterprise-kubernetes-platform.md) — maturity model, Rancher, OpenShift, Tanzu, governance

### Stage 11: Operations

Day-2 operations that keep clusters running.

1. [Cluster Upgrades](11-operations/01-cluster-upgrades.md) — in-place, blue-green, rolling node, version skew, PodDisruptionBudget
2. [Disaster Recovery](11-operations/02-disaster-recovery.md) — Velero, etcd backup/restore, cross-region failover, RTO/RPO
3. [Troubleshooting Patterns](11-operations/03-troubleshooting-patterns.md) — CrashLoopBackOff, OOMKilled, pending pods, kubectl debug
4. [Cost Optimization](11-operations/04-cost-optimization.md) — spot instances, right-sizing, bin-packing, resource requests/limits, FinOps
5. [Capacity Planning](11-operations/05-capacity-planning.md) — resource estimation, cluster sizing, headroom, growth forecasting

### Stage 12: Patterns and Anti-Patterns

Reusable design patterns and common mistakes to avoid.

| Pattern Reference | Scope |
|------------------|-------|
| [Operator Pattern](12-patterns/01-operator-pattern.md) | Custom controllers, Operator SDK, Kubebuilder, OLM, level-triggered reconciliation |
| [Sidecar and Ambassador](12-patterns/02-sidecar-and-ambassador.md) | Sidecar, ambassador, adapter patterns, Envoy sidecar, sidecar injection |
| [CRD-Driven Design](12-patterns/03-crd-driven-design.md) | Custom Resource Definitions, declarative APIs, informers, work queues |
| [Kubernetes Anti-Patterns](12-patterns/04-kubernetes-anti-patterns.md) | No resource limits, latest tag, single replica, no probes, privileged containers |
| [Migration Patterns](12-patterns/05-migration-patterns.md) | Strangler fig, lift-and-shift, re-platform, dual-write, shadow traffic |

### Stage 13: Case Studies

Real-world Kubernetes architectures that tie everything together. Study these after mastering the building blocks.

| Case Study | Key Patterns | Difficulty |
|-----------|-------------|-----------|
| [Spotify Platform](13-case-studies/01-spotify-platform.md) | Backstage, golden paths, developer self-service, service catalog | Medium |
| [Airbnb Multi-Cluster](13-case-studies/02-airbnb-multi-cluster.md) | Multi-cluster migration, service mesh, traffic shifting | Hard |
| [Pinterest Cost Optimization](13-case-studies/03-pinterest-cost-optimization.md) | Spot fleet, bin-packing, right-sizing, FinOps | Medium |
| [Multi-Tenant Platform Design](13-case-studies/04-designing-multi-tenant-platform.md) | 50+ team tenancy, namespace isolation, quotas, governance | Hard |
| [Monolith to Kubernetes Migration](13-case-studies/05-monolith-to-kubernetes-migration.md) | Strangler fig, incremental containerization, dual-stack | Hard |
| [Stateful Workloads at Scale](13-case-studies/06-stateful-workloads-at-scale.md) | Database operators, Kafka/Cassandra on K8s, data locality | Hard |
| [GPU Cluster for GenAI Inference](13-case-studies/07-gpu-cluster-genai-inference.md) | GPU scheduling, KServe, vLLM, model serving, inference autoscaling | Hard |
| [Edge Kubernetes](13-case-studies/08-edge-kubernetes.md) | K3s, KubeEdge, constrained resources, fleet management | Medium |
| [Enterprise Kubernetes at Scale](13-case-studies/09-enterprise-kubernetes-at-scale.md) | Governance, compliance, multi-cluster ops, platform maturity | Hard |

---

## Quick Reference

- [Glossary](../glossary.md) — system design, GenAI, and Kubernetes terms defined
- [Concept Index](meta/concept-index.md) — master deduplicated concept list for the K8s pillar
- [Source Inventory](meta/source-inventory.md) — catalog of all source materials
- [Source Traceability Map](meta/source-map.md) — which sources informed each topic
- [Traditional System Design →](../traditional-system-design/index.md) — the companion knowledge base for classical distributed systems
- [GenAI System Design →](../genai-system-design/index.md) — the companion knowledge base for Generative AI system design
