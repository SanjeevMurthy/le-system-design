# Concept Index

## How to Use This Index
Each concept appears ONCE, mapped to its canonical file in the Kubernetes system design knowledge base. The "Content Boundaries" section defines which file owns which concept to prevent duplication. Other files that touch the same concept should cross-link to the canonical file and state which variant or aspect they use, rather than re-explaining the concept from scratch.

## Content Boundaries (Deduplication Rules)

| Concept | Canonical File | Other files may only... |
|---------|---------------|------------------------|
| Kubernetes architecture (control plane, data plane, declarative model) | 01-foundations/01-kubernetes-architecture.md | Cross-link and state which component is relevant |
| Control plane internals (scheduler, controller manager, cloud controller) | 01-foundations/02-control-plane-internals.md | Cross-link only |
| API server and etcd (admission control, watch, API aggregation) | 01-foundations/03-api-server-and-etcd.md | Cross-link only |
| Container runtime (CRI, containerd, OCI, runc) | 01-foundations/04-container-runtime.md | Cross-link only |
| Kubernetes networking model (flat network, CNI contract) | 01-foundations/05-kubernetes-networking-model.md | Cross-link only |
| Pod design patterns (sidecar, init container, ambassador) | 03-workload-design/01-pod-design-patterns.md | Cross-link and state which pattern is used |
| StatefulSet (ordered deployment, stable identities) | 03-workload-design/03-statefulsets-and-stateful-workloads.md | Cross-link only |
| HPA (Horizontal Pod Autoscaler, metrics-driven scaling) | 06-scaling-design/01-horizontal-pod-autoscaling.md | Cross-link only |
| VPA and Cluster Autoscaler (vertical scaling, node provisioning) | 06-scaling-design/02-vertical-and-cluster-autoscaling.md | Cross-link only |
| KEDA (event-driven autoscaling) | 06-scaling-design/03-keda-and-event-driven-scaling.md | Cross-link only |
| RBAC (Roles, ClusterRoles, Bindings, service accounts) | 07-security-design/01-rbac-and-access-control.md | Cross-link only |
| Policy engines (OPA/Gatekeeper, Kyverno) | 07-security-design/02-policy-engines.md | Cross-link only |
| GitOps (Flux, ArgoCD, reconciliation loop) | 08-deployment-design/01-gitops-and-flux-argocd.md | Cross-link only |
| Helm and Kustomize (templating, overlays, chart management) | 08-deployment-design/02-helm-and-kustomize.md | Cross-link only |
| Service mesh (Istio, Linkerd, Envoy, mTLS) | 04-networking-design/03-service-mesh.md | Cross-link only |
| CRD and Operator pattern (custom resources, reconciliation) | 12-patterns/01-operator-pattern.md + 12-patterns/03-crd-driven-design.md | Cross-link only |
| Persistent storage (PV, PVC, StorageClass, CSI) | 05-storage-design/01-persistent-storage-architecture.md | Cross-link only |
| Network policies (ingress/egress rules, microsegmentation) | 04-networking-design/05-network-policies.md | Cross-link only |
| Progressive delivery (canary, blue-green, Argo Rollouts, Flagger) | 08-deployment-design/04-progressive-delivery.md | Cross-link only |

---

## Compute

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Kubernetes architecture | 01-foundations/01-kubernetes-architecture.md | K8s, container orchestration, declarative model, desired state, reconciliation loop, control plane vs data plane | control-plane-internals, api-server-etcd |
| Control plane internals | 01-foundations/02-control-plane-internals.md | kube-scheduler, kube-controller-manager, cloud-controller-manager, scheduler predicates/priorities, leader election | kubernetes-architecture, api-server-etcd |
| API server and etcd | 01-foundations/03-api-server-and-etcd.md | kube-apiserver, admission controllers (validating, mutating), webhook, API aggregation, watch mechanism, etcd cluster, Raft consensus | kubernetes-architecture, control-plane-internals |
| Container runtime | 01-foundations/04-container-runtime.md | CRI (Container Runtime Interface), containerd, CRI-O, OCI (Open Container Initiative), runc, crun, gVisor, Kata Containers, image spec, runtime spec | kubernetes-architecture, pod-design-patterns |
| Pod design patterns | 03-workload-design/01-pod-design-patterns.md | Sidecar container, init container, ambassador container, adapter container, multi-container pod, shared volumes, shared network namespace | container-runtime, service-mesh, deployment-strategies |
| Deployment strategies | 03-workload-design/02-deployment-strategies.md | Rolling update, recreate, maxSurge, maxUnavailable, rollback, revision history, Deployment controller | pod-design-patterns, progressive-delivery |
| StatefulSets and stateful workloads | 03-workload-design/03-statefulsets-and-stateful-workloads.md | Ordered deployment, stable network identity, headless service, volumeClaimTemplates, ordinal index, pod management policy | persistent-storage, dns-service-discovery |
| Jobs and batch processing | 03-workload-design/04-jobs-and-batch-processing.md | Job, CronJob, parallelism, completions, backoffLimit, TTL controller, indexed jobs, job queues | horizontal-pod-autoscaling, keda |
| GPU and accelerator workloads | 03-workload-design/05-gpu-and-accelerator-workloads.md | NVIDIA device plugin, GPU scheduling, nvidia.com/gpu resource, time-slicing, MIG (Multi-Instance GPU), MPS, GPU operator, CUDA | gpu-aware-autoscaling, model-artifact-delivery |
| Cluster topology | 02-cluster-design/01-cluster-topology.md | Single-cluster, multi-zone, multi-region, HA control plane, stacked etcd, external etcd, control plane sizing | multi-cluster-architecture, disaster-recovery |
| Node pool strategy | 02-cluster-design/02-node-pool-strategy.md | Node pools, node groups, instance types, taints and tolerations, node affinity, spot instances, on-demand, node labels, capacity-type | cluster-topology, cost-optimization |
| Multi-cluster architecture | 02-cluster-design/03-multi-cluster-architecture.md | Fleet management, cluster federation, Admiralty, Liqo, Submariner, cluster API, hub-spoke, GitOps multi-cluster | cluster-topology, gitops |
| Cloud vs bare-metal | 02-cluster-design/04-cloud-vs-bare-metal.md | EKS, GKE, AKS, managed Kubernetes, self-managed, kubeadm, k3s, RKE2, Talos Linux | cluster-topology, node-pool-strategy |

## Networking

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Kubernetes networking model | 01-foundations/05-kubernetes-networking-model.md | Flat network, pod-to-pod, CNI (Container Network Interface), pod IP, no-NAT contract, overlay network, underlay network | service-networking, network-policies |
| Service networking | 04-networking-design/01-service-networking.md | ClusterIP, NodePort, LoadBalancer, ExternalName, kube-proxy, iptables, IPVS, endpoints, EndpointSlice, service topology | kubernetes-networking-model, ingress-gateway-api |
| Ingress and Gateway API | 04-networking-design/02-ingress-and-gateway-api.md | Ingress controller, IngressClass, NGINX ingress, Traefik, Gateway API (HTTPRoute, GRPCRoute, TLSRoute), GatewayClass, TLS termination | service-networking, service-mesh |
| Service mesh | 04-networking-design/03-service-mesh.md | Istio, Linkerd, Consul Connect, Envoy proxy, sidecar proxy, mTLS (mutual TLS), traffic management, circuit breaking, retries, observability, sidecarless (ambient mesh, eBPF) | ingress-gateway-api, sidecar-ambassador |
| DNS and service discovery | 04-networking-design/04-dns-and-service-discovery.md | CoreDNS, cluster DNS, service FQDN, headless service DNS, SRV records, ExternalDNS, ndots, DNS caching | service-networking, statefulsets |
| Network policies | 04-networking-design/05-network-policies.md | NetworkPolicy, ingress rules, egress rules, pod selectors, namespace selectors, CIDR blocks, default deny, microsegmentation, Calico, Cilium | kubernetes-networking-model, rbac |
| CNI plugins | 01-foundations/05-kubernetes-networking-model.md (section within) | Calico, Cilium, Flannel, Weave Net, AWS VPC CNI, Azure CNI, eBPF, VXLAN, BGP | service-networking, network-policies |

## Storage

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Persistent storage architecture | 05-storage-design/01-persistent-storage-architecture.md | PersistentVolume (PV), PersistentVolumeClaim (PVC), StorageClass, dynamic provisioning, volume modes (Filesystem, Block), access modes (RWO, ROX, RWX), reclaim policies | csi-drivers, stateful-data-patterns |
| CSI drivers and storage classes | 05-storage-design/02-csi-drivers-and-storage-classes.md | Container Storage Interface (CSI), EBS CSI, EFS CSI, GCE PD CSI, Azure Disk CSI, Ceph CSI, Longhorn, OpenEBS, Rook, volume snapshots, volume cloning | persistent-storage, statefulsets |
| Stateful data patterns | 05-storage-design/03-stateful-data-patterns.md | Database on Kubernetes, operator-managed databases, local PV, topology-aware scheduling, backup strategies, data gravity | persistent-storage, statefulsets, operator-pattern |
| Model and artifact delivery | 05-storage-design/04-model-and-artifact-delivery.md | Model registry, OCI artifacts, init container model pull, shared volume model loading, S3/GCS model storage, model caching, warm-up | gpu-accelerator-workloads, gpu-aware-autoscaling |

## Scaling

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Horizontal Pod Autoscaling | 06-scaling-design/01-horizontal-pod-autoscaling.md | HPA, metrics server, CPU/memory-based scaling, custom metrics, external metrics, scaling policies, stabilization window, behavior configuration | vpa-cluster-autoscaling, keda |
| Vertical and Cluster Autoscaling | 06-scaling-design/02-vertical-and-cluster-autoscaling.md | VPA (Vertical Pod Autoscaler), Cluster Autoscaler, Karpenter, node provisioning, right-sizing, bin-packing, scale-from-zero, provisioner/NodePool CRD | horizontal-pod-autoscaling, node-pool-strategy |
| KEDA and event-driven scaling | 06-scaling-design/03-keda-and-event-driven-scaling.md | KEDA (Kubernetes Event-Driven Autoscaling), ScaledObject, ScaledJob, external scalers, Kafka scaler, Prometheus scaler, cron scaler, scale-to-zero | horizontal-pod-autoscaling, jobs-batch |
| GPU-aware autoscaling | 06-scaling-design/04-gpu-aware-autoscaling.md | GPU utilization scaling, DCGM metrics, fractional GPU, GPU sharing, Karpenter GPU provisioning, scale-to-zero GPU, inference autoscaling | gpu-accelerator-workloads, keda |

## Security

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| RBAC and access control | 07-security-design/01-rbac-and-access-control.md | Role, ClusterRole, RoleBinding, ClusterRoleBinding, ServiceAccount, token projection, OIDC integration, least privilege, audit logging | policy-engines, secrets-management |
| Policy engines | 07-security-design/02-policy-engines.md | OPA (Open Policy Agent), Gatekeeper, Kyverno, admission controllers, ConstraintTemplate, ClusterPolicy, validate/mutate/generate rules, policy-as-code | rbac, supply-chain-security |
| Supply chain security | 07-security-design/03-supply-chain-security.md | Image signing, Cosign, Sigstore, Notary, image scanning (Trivy, Grype, Snyk), SBOM (Software Bill of Materials), admission policies for image verification, base image hardening | policy-engines, runtime-security |
| Secrets management | 07-security-design/04-secrets-management.md | Kubernetes Secrets, external-secrets-operator, HashiCorp Vault, AWS Secrets Manager, sealed-secrets, CSI secret store driver, encryption at rest, secret rotation | rbac, persistent-storage |
| Runtime security | 07-security-design/05-runtime-security.md | Falco, Pod Security Standards (baseline/restricted/privileged), Pod Security Admission, seccomp, AppArmor, SELinux, read-only root filesystem, non-root containers, security contexts | policy-engines, network-policies |

## Deployment

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| GitOps and Flux/ArgoCD | 08-deployment-design/01-gitops-and-flux-argocd.md | GitOps, Flux CD, ArgoCD, pull-based deployment, Git as source of truth, reconciliation, Application CRD, Kustomization CRD, drift detection, sync waves, app-of-apps | helm-kustomize, cicd-pipelines |
| Helm and Kustomize | 08-deployment-design/02-helm-and-kustomize.md | Helm charts, Chart.yaml, values.yaml, templates, helm install/upgrade/rollback, Kustomize overlays, patches, bases, strategic merge patch, JSON patch | gitops, cicd-pipelines |
| CI/CD pipelines | 08-deployment-design/03-cicd-pipelines.md | Continuous Integration, Continuous Delivery, Tekton, GitHub Actions, Jenkins X, pipeline stages, container image build (Kaniko, Buildah), artifact promotion, environment promotion | gitops, helm-kustomize |
| Progressive delivery | 08-deployment-design/04-progressive-delivery.md | Canary deployment, blue-green deployment, A/B testing, Argo Rollouts, Flagger, analysis templates, metrics-driven promotion, automated rollback | deployment-strategies, monitoring-metrics |

## Observability

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Monitoring and metrics | 09-observability-design/01-monitoring-and-metrics.md | Prometheus, Grafana, kube-state-metrics, node-exporter, ServiceMonitor, PodMonitor, PromQL, alerting rules, Alertmanager, Thanos, Cortex, Mimir, golden signals | logging-tracing, slo-based-operations |
| Logging and tracing | 09-observability-design/02-logging-and-tracing.md | EFK stack (Elasticsearch, Fluentd, Kibana), Fluent Bit, Loki, Grafana, OpenTelemetry, Jaeger, Tempo, distributed tracing, trace context propagation, log aggregation | monitoring-metrics, service-mesh |
| Cost observability | 09-observability-design/03-cost-observability.md | Kubecost, OpenCost, cost allocation, showback, chargeback, namespace cost attribution, idle cost, shared cost, cloud billing integration | cost-optimization, monitoring-metrics |
| SLO-based operations | 09-observability-design/04-slo-based-operations.md | SLO (Service Level Objective), SLI (Service Level Indicator), error budget, burn rate alerting, SLO controller, Pyrra, Sloth, multi-window multi-burn-rate | monitoring-metrics, progressive-delivery |

## Platform Engineering

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Internal developer platform | 10-platform-design/01-internal-developer-platform.md | IDP, Backstage, service catalog, software templates, golden paths, platform team, developer self-service, platform API | self-service-abstractions, developer-experience |
| Multi-tenancy | 10-platform-design/02-multi-tenancy.md | Namespace isolation, vCluster, Capsule, Hierarchical Namespace Controller, resource quotas, LimitRange, tenant isolation, soft vs hard multi-tenancy | rbac, network-policies, cost-observability |
| Self-service abstractions | 10-platform-design/03-self-service-abstractions.md | Crossplane, Kratix, composition, XRD (Composite Resource Definition), infrastructure-as-code, platform API, environment provisioning | internal-developer-platform, crd-driven-design |
| Developer experience | 10-platform-design/04-developer-experience.md | Tilt, Skaffold, Telepresence, DevSpace, inner loop vs outer loop, hot reload, local-to-cluster development, developer onboarding | internal-developer-platform, cicd-pipelines |
| Enterprise Kubernetes platform | 10-platform-design/05-enterprise-kubernetes-platform.md | Platform maturity model, governance, compliance, multi-cluster management, Rancher, OpenShift, Tanzu, cost management | multi-tenancy, multi-cluster-architecture |

## Operations

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Cluster upgrades | 11-operations/01-cluster-upgrades.md | In-place upgrade, blue-green cluster upgrade, rolling node upgrade, version skew policy, control plane upgrade, node drain, PodDisruptionBudget | disaster-recovery, deployment-strategies |
| Disaster recovery | 11-operations/02-disaster-recovery.md | Velero, etcd backup/restore, cluster backup, cross-region failover, RTO/RPO, backup schedules, volume snapshots, namespace-level restore | cluster-upgrades, persistent-storage |
| Troubleshooting patterns | 11-operations/03-troubleshooting-patterns.md | CrashLoopBackOff, ImagePullBackOff, OOMKilled, pending pods, evicted pods, kubectl debug, ephemeral containers, node not ready, DNS resolution failures | monitoring-metrics, logging-tracing |
| Cost optimization | 11-operations/04-cost-optimization.md | Spot instances, reserved instances, right-sizing, bin-packing, resource requests/limits, overprovisioning, cost allocation, FinOps | cost-observability, node-pool-strategy, capacity-planning |
| Capacity planning | 11-operations/05-capacity-planning.md | Resource estimation, cluster sizing, headroom calculation, burst capacity, resource quotas, namespace budgets, growth forecasting | cost-optimization, horizontal-pod-autoscaling |

## Patterns and Anti-Patterns

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Operator pattern | 12-patterns/01-operator-pattern.md | Custom controller, Operator SDK, Kubebuilder, operator-lifecycle-manager (OLM), level-triggered reconciliation, idempotent reconciliation, status subresource | crd-driven-design, stateful-data-patterns |
| Sidecar and ambassador | 12-patterns/02-sidecar-and-ambassador.md | Sidecar pattern, ambassador pattern, adapter pattern, log shipper sidecar, proxy sidecar, Envoy sidecar, sidecar injection | pod-design-patterns, service-mesh |
| CRD-driven design | 12-patterns/03-crd-driven-design.md | Custom Resource Definition (CRD), custom resources, API extensions, declarative APIs, controller pattern, informers, work queues | operator-pattern, self-service-abstractions |
| Kubernetes anti-patterns | 12-patterns/04-kubernetes-anti-patterns.md | No resource limits, latest tag, single replica, no health probes, hardcoded configs, privileged containers, no PodDisruptionBudget, monolithic Helm charts | pod-design-patterns, deployment-strategies, security |
| Migration patterns | 12-patterns/05-migration-patterns.md | Strangler fig, lift-and-shift, re-platform, re-architect, VM-to-container, monolith decomposition, dual-write, shadow traffic | deployment-strategies, progressive-delivery |

## Case Studies

| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| Spotify platform | 13-case-studies/01-spotify-platform.md | Backstage, golden paths, developer experience, internal platform, service catalog at scale | internal-developer-platform, developer-experience |
| Airbnb multi-cluster | 13-case-studies/02-airbnb-multi-cluster.md | Multi-cluster migration, service mesh adoption, cluster federation, traffic shifting | multi-cluster-architecture, service-mesh |
| Pinterest cost optimization | 13-case-studies/03-pinterest-cost-optimization.md | Spot instance fleet, bin-packing, resource right-sizing, cost reduction at scale | cost-optimization, cost-observability |
| Designing multi-tenant platform | 13-case-studies/04-designing-multi-tenant-platform.md | 50+ team multi-tenancy, namespace isolation, resource quotas, tenant onboarding, platform governance | multi-tenancy, rbac, policy-engines |
| Monolith to Kubernetes migration | 13-case-studies/05-monolith-to-kubernetes-migration.md | Strangler fig, incremental migration, service extraction, containerization, dual-stack operation | migration-patterns, deployment-strategies |
| Stateful workloads at scale | 13-case-studies/06-stateful-workloads-at-scale.md | Database operators, Kafka on K8s, Cassandra on K8s, stateful scaling, data locality | statefulsets, operator-pattern, persistent-storage |
| GPU cluster for GenAI inference | 13-case-studies/07-gpu-cluster-genai-inference.md | GPU scheduling, model serving, KServe, vLLM on K8s, multi-model serving, inference autoscaling | gpu-accelerator-workloads, gpu-aware-autoscaling |
| Edge Kubernetes | 13-case-studies/08-edge-kubernetes.md | K3s, KubeEdge, edge clusters, constrained resources, intermittent connectivity, fleet management | cluster-topology, multi-cluster-architecture |
| Enterprise Kubernetes at scale | 13-case-studies/09-enterprise-kubernetes-at-scale.md | Enterprise governance, compliance, multi-cluster operations, platform maturity, organizational patterns | enterprise-kubernetes-platform, multi-tenancy |

---

## Cross-Pillar References (Traditional System Design)

The following K8s concepts extend or specialize topics that also exist in the traditional system design knowledge base:

| K8s Concept | K8s Canonical File | Related Traditional File | Relationship |
|---|---|---|---|
| HPA / autoscaling | 06-scaling-design/01-horizontal-pod-autoscaling.md | traditional/02-scalability/02-autoscaling.md | K8s-specific autoscaling mechanics |
| Service mesh | 04-networking-design/03-service-mesh.md | traditional/06-architecture/02-microservices.md | K8s-native service mesh implementation |
| RBAC | 07-security-design/01-rbac-and-access-control.md | traditional/09-security/01-authentication-authorization.md | K8s-specific RBAC model |
| Monitoring (Prometheus) | 09-observability-design/01-monitoring-and-metrics.md | traditional/10-observability/01-monitoring.md | K8s-specific monitoring stack |
| Container runtime | 01-foundations/04-container-runtime.md | traditional/06-architecture/02-microservices.md | K8s container runtime internals |
| Progressive delivery | 08-deployment-design/04-progressive-delivery.md | traditional/08-resilience/04-feature-flags.md | K8s-native canary/blue-green |

## Cross-Pillar References (GenAI System Design)

| K8s Concept | K8s Canonical File | Related GenAI File | Relationship |
|---|---|---|---|
| GPU workloads | 03-workload-design/05-gpu-and-accelerator-workloads.md | genai/02-llm-architecture/02-gpu-compute.md | K8s GPU scheduling for LLM serving |
| GPU-aware autoscaling | 06-scaling-design/04-gpu-aware-autoscaling.md | genai/13-case-studies/06-kubernetes-genai.md | K8s autoscaling for inference |
| Model artifact delivery | 05-storage-design/04-model-and-artifact-delivery.md | genai/02-llm-architecture/01-model-serving.md | K8s model loading patterns |

---

## Source Coverage Matrix

| Source | Key K8s Concepts Covered |
|--------|------------------------|
| YouTube Report 1 | Container runtimes (CRI, runc, containerd), K8s HPA cost management, spot instances, affinity rules |
| YouTube Report 5 | Kubernetes five pillars, HPA + metrics server, network infrastructure, auto-scaling |
| YouTube Report 7 | Kubernetes five pillars, custom resources, Prometheus/Grafana observability, ServiceMonitor |
| K8s for GenAI (PDF) | GPU device plugins, GPU scheduling, KServe, model serving, ML multi-tenancy, KEDA |
| Official K8s docs | All core concepts: architecture, API server, etcd, CRI, networking, storage, security, scaling |
| CNCF project docs | Prometheus, Istio, Helm, ArgoCD, Flux, KEDA, Falco, OPA, Kyverno, Velero, Crossplane, Backstage |
| Cloud provider docs | EKS, GKE, AKS, Karpenter, managed K8s patterns, CSI drivers |
| Industry blogs | Spotify (Backstage), Airbnb (multi-cluster), Pinterest (cost), enterprise governance |
| K8s pattern books | Pod patterns, operator pattern, sidecar, anti-patterns, migration strategies |
