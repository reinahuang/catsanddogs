# CatsAndDogs 🐾

A Cloud-Native multi-service application (Frontend & Backend) featuring automated GHCR image building with GitHub Actions and GitOps continuous deployment using FluxCD on Kubernetes.

基于 Kubernetes 与 FluxCD 构建的企业级云原生 GitOps 微服务示例项目，支持 GitHub Actions 多镜像语义化打包与自动同步部署。

---

## 🏗️ Architecture & Tech Stack (架构与技术栈)

- **Microservices**: Frontend & Backend services
- **Container Registry**: GitHub Container Registry (GHCR)
- **CI/CD Pipeline**: GitHub Actions (`docker/metadata-action`, `docker/build-push-action`)
- **GitOps Operator**: FluxCD (`source-controller`, `kustomize-controller`)
- **Container Orchestration**: Kubernetes (K8s)

---

## 🚀 Key Features (核心特性)

- **Automated Image Tagging**: Supports Semantic Versioning (`v*`), Commit SHA, and `latest` tags.
- **GitOps Continuous Deployment**: Declarative Kubernetes manifests automated via FluxCD.
- **Microservices Isolation**: Structured separation of application code, K8s manifests, and Helm values.

---

## 📁 Repository Structure (目录结构)

```text
CatsAndDogs/
├── backend/               # 后端服务源码及 Dockerfile
├── frontend/              # 前端服务源码及 Dockerfile
├── k8s/                   # Kubernetes 部署清单 (FluxCD 监听目录)
│   ├── 01-postgres.yaml
│   ├── 02-backend.yaml
│   ├── 03-frontend.yaml
│   ├── flux-system/       # FluxCD 自动生成的同步配置
│   └── values/            # 隔离的 Helm Values 等非 Manifest 配置文件
└── .github/
    └── workflows/         # GitHub Actions 自动化构建工作流
```
