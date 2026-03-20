# Source Traceability Map

This document maps each canonical topic file in the Kubernetes system design knowledge base to the source files and references that informed it.

---

## 01-foundations/

### 01-kubernetes-architecture.md
- source/youtube-video-reports/5.md (Kubernetes five pillars: computation, networking, storage, security, custom resources)
- source/youtube-video-reports/7.md (Kubernetes five pillars and custom resources)
- Official Kubernetes documentation: concepts/overview, concepts/architecture
- Kubernetes Patterns (Ibryam & Huss) -- foundational patterns, declarative model
- Production Kubernetes (Rosso et al.) -- architecture deep dive

### 02-control-plane-internals.md
- Official Kubernetes documentation: concepts/architecture/control-plane-components
- Official Kubernetes documentation: reference/command-line-tools-reference (kube-scheduler, kube-controller-manager)
- Production Kubernetes (Rosso et al.) -- control plane sizing and HA
- The Kubernetes Book (Poulton) -- control plane walkthrough

### 03-api-server-and-etcd.md
- Official Kubernetes documentation: concepts/architecture/api-server, reference/using-api
- Official Kubernetes documentation: tasks/administer-cluster/configure-upgrade-etcd
- etcd documentation: architecture, Raft consensus
- Production Kubernetes (Rosso et al.) -- etcd operations, backup/restore

### 04-container-runtime.md
- source/youtube-video-reports/1.md (container runtimes: OCI, runc, containerd, CRI-O; Docker Shim deprecation)
- Official Kubernetes documentation: concepts/containers/runtime-class
- OCI specification: image-spec, runtime-spec
- containerd documentation, CRI-O documentation

### 05-kubernetes-networking-model.md
- source/youtube-video-reports/5.md (network infrastructure, security groups, subnets)
- Official Kubernetes documentation: concepts/cluster-administration/networking
- CNI specification and plugin documentation (Calico, Cilium, Flannel)
- Kubernetes Networking (Domingus & Arundel) -- networking model deep dive

---

## 02-cluster-design/

### 01-cluster-topology.md
- Official Kubernetes documentation: setup/production-environment, concepts/architecture
- Production Kubernetes (Rosso et al.) -- cluster sizing, HA topologies
- Cloud provider documentation: EKS, GKE, AKS cluster architecture

### 02-node-pool-strategy.md
- source/youtube-video-reports/1.md (spot instances, affinity rules, Kubernetes cost management)
- Official Kubernetes documentation: concepts/scheduling-eviction (taints, tolerations, affinity)
- AWS EKS documentation: managed node groups, Karpenter NodePools
- GKE documentation: node pools, autopilot

### 03-multi-cluster-architecture.md
- Airbnb Engineering blog -- multi-cluster migration
- Official Kubernetes documentation: concepts/architecture/multi-cluster
- Cluster API documentation, Admiralty documentation, Liqo documentation
- GitOps multi-cluster patterns (ArgoCD ApplicationSets, Flux multi-cluster)

### 04-cloud-vs-bare-metal.md
- Cloud provider documentation: EKS, GKE, AKS managed vs self-managed
- Official Kubernetes documentation: setup/production-environment
- kubeadm, k3s, RKE2, Talos Linux documentation
- Production Kubernetes (Rosso et al.) -- managed vs self-managed tradeoffs

---

## 03-workload-design/

### 01-pod-design-patterns.md
- Kubernetes Patterns (Ibryam & Huss) -- sidecar, init container, ambassador, adapter
- Official Kubernetes documentation: concepts/workloads/pods (multi-container pods)
- Kubernetes Best Practices (Burns et al.) -- pod design

### 02-deployment-strategies.md
- Official Kubernetes documentation: concepts/workloads/controllers/deployment
- Kubernetes Best Practices (Burns et al.) -- deployment strategies
- Production Kubernetes (Rosso et al.) -- rolling update tuning

### 03-statefulsets-and-stateful-workloads.md
- Official Kubernetes documentation: concepts/workloads/controllers/statefulset
- Kubernetes Patterns (Ibryam & Huss) -- stateful service pattern
- Production Kubernetes (Rosso et al.) -- stateful workload operations

### 04-jobs-and-batch-processing.md
- Official Kubernetes documentation: concepts/workloads/controllers/job, concepts/workloads/controllers/cron-jobs
- Official Kubernetes documentation: concepts/workloads/controllers/indexed-job
- Kubernetes Best Practices (Burns et al.) -- batch workloads

### 05-gpu-and-accelerator-workloads.md
- source/GenAI/Kubernetes for Generative AI Solutions.pdf (GPU device plugins, scheduling, MIG, time-slicing)
- NVIDIA GPU Operator documentation
- NVIDIA device plugin for Kubernetes documentation
- Official Kubernetes documentation: tasks/manage-gpus/scheduling-gpus

---

## 04-networking-design/

### 01-service-networking.md
- Official Kubernetes documentation: concepts/services-networking/service
- Official Kubernetes documentation: reference/networking/virtual-ips
- Kubernetes Networking (Domingus & Arundel) -- service internals (iptables, IPVS)

### 02-ingress-and-gateway-api.md
- Official Kubernetes documentation: concepts/services-networking/ingress
- Gateway API documentation: gateway-api.sigs.k8s.io
- NGINX Ingress Controller documentation, Traefik documentation

### 03-service-mesh.md
- Istio documentation: architecture, traffic management, security (mTLS)
- Linkerd documentation: architecture, getting started
- Envoy proxy documentation
- Cilium service mesh (eBPF-based, sidecarless)
- Kubernetes Best Practices (Burns et al.) -- service mesh chapter

### 04-dns-and-service-discovery.md
- Official Kubernetes documentation: concepts/services-networking/dns-pod-service
- CoreDNS documentation: plugins, configuration
- ExternalDNS documentation

### 05-network-policies.md
- Official Kubernetes documentation: concepts/services-networking/network-policies
- Calico documentation: network policy, GlobalNetworkPolicy
- Cilium documentation: network policy, CiliumNetworkPolicy

---

## 05-storage-design/

### 01-persistent-storage-architecture.md
- Official Kubernetes documentation: concepts/storage/persistent-volumes, concepts/storage/storage-classes
- CSI specification documentation
- Production Kubernetes (Rosso et al.) -- storage architecture

### 02-csi-drivers-and-storage-classes.md
- CSI specification and driver list (kubernetes-csi.github.io)
- AWS EBS CSI, AWS EFS CSI documentation
- Rook/Ceph documentation, Longhorn documentation, OpenEBS documentation

### 03-stateful-data-patterns.md
- Production Kubernetes (Rosso et al.) -- database on Kubernetes patterns
- Operator documentation: CloudNativePG, Strimzi (Kafka), CassKop
- Kubernetes Patterns (Ibryam & Huss) -- stateful service pattern

### 04-model-and-artifact-delivery.md
- source/GenAI/Kubernetes for Generative AI Solutions.pdf (model storage, OCI artifacts, model caching)
- KServe documentation: model serving, storage initializer
- NVIDIA Triton Inference Server documentation

---

## 06-scaling-design/

### 01-horizontal-pod-autoscaling.md
- source/youtube-video-reports/1.md (Kubernetes HPA, 80% threshold strategy)
- source/youtube-video-reports/5.md (HPA, metrics server, CPU/memory thresholds)
- Official Kubernetes documentation: tasks/run-application/horizontal-pod-autoscale
- Official Kubernetes documentation: reference/kubernetes-api/workload-resources/horizontal-pod-autoscaler

### 02-vertical-and-cluster-autoscaling.md
- source/youtube-video-reports/5.md (auto-scaling in Kubernetes context)
- VPA documentation: kubernetes/autoscaler/vertical-pod-autoscaler
- Cluster Autoscaler documentation: kubernetes/autoscaler/cluster-autoscaler
- Karpenter documentation: karpenter.sh

### 03-keda-and-event-driven-scaling.md
- KEDA documentation: keda.sh (ScaledObject, ScaledJob, scalers catalog)
- source/GenAI/Kubernetes for Generative AI Solutions.pdf (KEDA for ML workloads)
- Official Kubernetes documentation: tasks/run-application/horizontal-pod-autoscale (external metrics)

### 04-gpu-aware-autoscaling.md
- source/GenAI/Kubernetes for Generative AI Solutions.pdf (GPU autoscaling patterns)
- NVIDIA DCGM Exporter documentation
- Karpenter documentation: GPU provisioning, accelerator support
- KEDA documentation: Prometheus scaler for GPU metrics

---

## 07-security-design/

### 01-rbac-and-access-control.md
- source/youtube-video-reports/5.md (Kubernetes security pillar)
- Official Kubernetes documentation: reference/access-authn-authz/rbac
- Official Kubernetes documentation: reference/access-authn-authz/authentication
- Production Kubernetes (Rosso et al.) -- RBAC hardening

### 02-policy-engines.md
- OPA / Gatekeeper documentation: open-policy-agent.github.io
- Kyverno documentation: kyverno.io
- Official Kubernetes documentation: reference/access-authn-authz/admission-controllers

### 03-supply-chain-security.md
- Sigstore / Cosign documentation
- Trivy documentation, Grype documentation
- SLSA framework documentation (slsa.dev)
- Official Kubernetes documentation: concepts/containers/images (image pull policies)

### 04-secrets-management.md
- Official Kubernetes documentation: concepts/configuration/secret
- HashiCorp Vault documentation: Vault Agent Injector, CSI provider
- external-secrets-operator documentation
- sealed-secrets documentation (Bitnami)

### 05-runtime-security.md
- Falco documentation: falco.org
- Official Kubernetes documentation: concepts/security/pod-security-standards
- Official Kubernetes documentation: concepts/security/pod-security-admission
- gVisor documentation, Kata Containers documentation

---

## 08-deployment-design/

### 01-gitops-and-flux-argocd.md
- ArgoCD documentation: argo-cd.readthedocs.io
- Flux documentation: fluxcd.io
- Weaveworks GitOps methodology (archived)
- OpenGitOps principles documentation

### 02-helm-and-kustomize.md
- Helm documentation: helm.sh
- Kustomize documentation: kustomize.io
- Official Kubernetes documentation: tasks/manage-kubernetes-objects/kustomization
- Kubernetes Best Practices (Burns et al.) -- packaging and deployment

### 03-cicd-pipelines.md
- Tekton documentation: tekton.dev
- GitHub Actions documentation: Kubernetes deployment workflows
- Jenkins X documentation
- Kaniko documentation, Buildah documentation

### 04-progressive-delivery.md
- Argo Rollouts documentation: argoproj.github.io/argo-rollouts
- Flagger documentation: flagger.app
- Official Kubernetes documentation: concepts/workloads/controllers/deployment (rolling update)

---

## 09-observability-design/

### 01-monitoring-and-metrics.md
- source/youtube-video-reports/7.md (Prometheus/Grafana, ServiceMonitor, observability stack)
- Prometheus documentation: prometheus.io
- Grafana documentation, kube-state-metrics documentation
- Thanos documentation, Cortex/Mimir documentation

### 02-logging-and-tracing.md
- source/youtube-video-reports/7.md (ELK stack, logging vs monitoring)
- Fluentd / Fluent Bit documentation
- Grafana Loki documentation
- OpenTelemetry documentation, Jaeger documentation, Grafana Tempo documentation

### 03-cost-observability.md
- Kubecost documentation: kubecost.com
- OpenCost documentation: opencost.io
- Datadog Engineering blog -- cost observability patterns
- FinOps Foundation documentation

### 04-slo-based-operations.md
- Google SRE Book -- SLO chapter
- Pyrra documentation, Sloth documentation
- Prometheus recording rules for SLO calculation
- OpenSLO specification

---

## 10-platform-design/

### 01-internal-developer-platform.md
- Backstage documentation: backstage.io
- Spotify Engineering blog -- Backstage origin and adoption
- Platform Engineering community resources (platformengineering.org)
- CNCF Platform White Paper

### 02-multi-tenancy.md
- Official Kubernetes documentation: concepts/security/multi-tenancy
- vCluster documentation: vcluster.com
- Capsule documentation: capsule.clastix.io
- Hierarchical Namespace Controller documentation

### 03-self-service-abstractions.md
- Crossplane documentation: crossplane.io
- Kratix documentation: kratix.io
- Official Kubernetes documentation: concepts/extend-kubernetes (API extensions)

### 04-developer-experience.md
- Tilt documentation: tilt.dev
- Skaffold documentation: skaffold.dev
- Telepresence documentation: telepresence.io
- DevSpace documentation: devspace.sh

### 05-enterprise-kubernetes-platform.md
- Rancher documentation: rancher.com
- OpenShift documentation: docs.openshift.com
- VMware Tanzu documentation
- Production Kubernetes (Rosso et al.) -- enterprise patterns

---

## 11-operations/

### 01-cluster-upgrades.md
- Official Kubernetes documentation: tasks/administer-cluster/cluster-upgrade
- Official Kubernetes documentation: setup/release/version-skew-policy
- Shopify Engineering blog -- zero-downtime cluster upgrades
- Production Kubernetes (Rosso et al.) -- upgrade strategies

### 02-disaster-recovery.md
- Velero documentation: velero.io
- Official Kubernetes documentation: tasks/administer-cluster/configure-upgrade-etcd (backup/restore)
- Production Kubernetes (Rosso et al.) -- DR planning

### 03-troubleshooting-patterns.md
- Official Kubernetes documentation: tasks/debug
- Kubernetes Best Practices (Burns et al.) -- troubleshooting chapter
- kubectl reference: debug, describe, logs, events

### 04-cost-optimization.md
- source/youtube-video-reports/1.md (Kubernetes cost management, spot instances, affinity rules)
- Pinterest Engineering blog -- cost optimization
- Kubecost documentation, FinOps Foundation
- AWS Spot Instance best practices, GKE preemptible VMs documentation

### 05-capacity-planning.md
- Official Kubernetes documentation: concepts/configuration/manage-resources-containers
- Production Kubernetes (Rosso et al.) -- capacity planning
- Kubernetes Best Practices (Burns et al.) -- resource management

---

## 12-patterns/

### 01-operator-pattern.md
- Official Kubernetes documentation: concepts/extend-kubernetes/operator
- Operator SDK documentation: sdk.operatorframework.io
- Kubebuilder documentation: kubebuilder.io
- Kubernetes Patterns (Ibryam & Huss) -- operator pattern

### 02-sidecar-and-ambassador.md
- Kubernetes Patterns (Ibryam & Huss) -- sidecar, ambassador, adapter patterns
- Official Kubernetes documentation: concepts/workloads/pods/sidecar-containers
- Istio documentation: sidecar injection

### 03-crd-driven-design.md
- source/youtube-video-reports/7.md (Kubernetes custom resources)
- Official Kubernetes documentation: tasks/extend-kubernetes/custom-resources
- Kubebuilder documentation: CRD development

### 04-kubernetes-anti-patterns.md
- Kubernetes Best Practices (Burns et al.) -- common mistakes
- Production Kubernetes (Rosso et al.) -- anti-patterns
- Community resources: learnk8s.io, k8s-at-home patterns

### 05-migration-patterns.md
- Production Kubernetes (Rosso et al.) -- migration strategies
- Kubernetes Best Practices (Burns et al.) -- migration chapter
- Strangler fig pattern documentation (Martin Fowler)

---

## 13-case-studies/

### 01-spotify-platform.md
- Spotify Engineering blog -- Backstage announcement, adoption, and lessons learned
- Backstage documentation and CNCF case study
- KubeCon presentations: Spotify platform engineering talks

### 02-airbnb-multi-cluster.md
- Airbnb Engineering blog -- Kubernetes migration series
- KubeCon presentations: Airbnb multi-cluster architecture
- Service mesh adoption case study

### 03-pinterest-cost-optimization.md
- Pinterest Engineering blog -- Kubernetes cost optimization series
- KubeCon presentations: Pinterest infrastructure talks
- FinOps community case studies

### 04-designing-multi-tenant-platform.md
- Production Kubernetes (Rosso et al.) -- multi-tenancy chapter
- CNCF multi-tenancy working group recommendations
- vCluster and Capsule case studies
- Official Kubernetes documentation: concepts/security/multi-tenancy

### 05-monolith-to-kubernetes-migration.md
- Strangler fig pattern (Martin Fowler)
- Production Kubernetes (Rosso et al.) -- migration chapter
- Industry migration case studies (Shopify, Wealthsimple)

### 06-stateful-workloads-at-scale.md
- CloudNativePG, Strimzi, CassKop operator documentation
- KubeCon presentations: stateful workloads on Kubernetes
- Production Kubernetes (Rosso et al.) -- stateful services

### 07-gpu-cluster-genai-inference.md
- source/GenAI/Kubernetes for Generative AI Solutions.pdf
- NVIDIA GPU Operator and device plugin documentation
- KServe, vLLM, Triton Inference Server documentation
- OpenAI / Anyscale engineering blogs -- GPU cluster management

### 08-edge-kubernetes.md
- K3s documentation: k3s.io
- KubeEdge documentation: kubeedge.io
- Official Kubernetes documentation: concepts/architecture (edge considerations)
- CNCF edge computing white paper

### 09-enterprise-kubernetes-at-scale.md
- Target, Capital One engineering blogs -- enterprise Kubernetes governance
- Rancher, OpenShift, Tanzu documentation
- Production Kubernetes (Rosso et al.) -- enterprise patterns
- KubeCon presentations: enterprise Kubernetes at scale
