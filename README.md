# What is this

A toy example of a monorepo that uses [Skaffold](https://skaffold.dev/) managing dev env and deployment.

This is only for personal learning purposes.

# Setup

## [Docker](https://docs.docker.com/get-docker/)

Containerisation tooling. You need at least Docker v20.10.4 for this to work!

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

## [k3d](https://k3d.io/)

Tiny k8s for local development.

```bash
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

## [Kubectl](https://kubernetes.io/docs/tasks/tools/)

Tool to control k8s.

Just follow the instruction on the page.

## [Task](https://taskfile.dev/#/installation)

A task runner written in Go, follow instruction on the page.

For autocomplete:-

- Zsh users - [here](https://github.com/sawadashota/go-task-completions).
- Bash users - [here](https://github.com/bfarayev/task/blob/feature/autocomplete/completion/task.bash).


## [fzf](https://github.com/junegunn/fzf)

A command line fuzzy finder. Used in some scripts within the repo.

## [jq](https://stedolan.github.io/jq/download/)

Need this to process JSON blobs in scripts. 

# Short description of repo

A monorepo that integrates k3d, skaffold, kustomize to provide a local developement environment and more.

We use k3d to manage k3s cluster with docker, so we minimise our footprint on the host machine, lest the host machine already have some critical k8s-related infra there.

We manage a docker registry on the side for this k3s cluster because this improves the image reload cycle drastically, since we no longer have to load the entire image into the cluster every time we an image - just the changed layers are needed.

We mount the repo root onto a predictable path on the host, so we can volume mount for development purposes, this will be handy when you need to propagate changes from pods onto host, such as times when you install packages in the pod or ran a formatter within a pod.

We use skaffold to simplify our devops tooling, it provides a lot of things (and things I have still yet to discover I am sure), for example:-

- Sensible tagging out of the box
- Image hot reload

We use kustomize because it looks like a good way of doing k8s manifest in a relatively pain free way, but it doesn't come with templating - perhaps this will come back and plague us later?

## Project layout 

To be documented when more are added.

# How do I...

## Spin up a working development environment

```bash
task dev:start  # Ensure docker registry is up, k3s cluster is up and kube-context is correct
skaffold dev    # Build all images, apply k8s manifests, repeat when source changes
```

## Obtain a shell in a running pod

Either you find the pod name yourself and exec bash, or use the following in the service/job dir, for example, to get a shell on the pod running our API,

```bash
cd services/fastapi-api
task dev:shell
```

## Install the same python dependencies for IDE's autocomplete

```bash
poetry export -f requirements.txt --output /tmp/a.txt && pip install -r /tmp/a.txt
```
