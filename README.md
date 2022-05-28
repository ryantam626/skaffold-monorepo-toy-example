# What is this

A toy example of a monorepo that uses [Skaffold](https://skaffold.dev/) managing dev env and deployment.

This is only for personal learning purposes.

# Setup

## [Docker](https://docs.docker.com/get-docker/)

Containerisation tooling.

## [Skaffold](https://skaffold.dev/)

Google's k8s management helper.

Install with the following command:-

```bash
# For Linux x86_64 (amd64)
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/

# For macOS on x86_64 (amd64)
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-darwin-amd64 && \
sudo install skaffold /usr/local/bin/
```

## [Minikube](https://minikube.sigs.k8s.io/docs/)

Local k8s offering.

Install with the following command:-

```bash
# For Linux x86_64 (amd64)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && \
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# For macOS on x86_64 (amd64)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 && \
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

## [Kubectl](https://kubernetes.io/docs/tasks/tools/)

Tool to control k8s.

Just follow the instruction on the page.
