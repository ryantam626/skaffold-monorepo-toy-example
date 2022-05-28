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

A monorepo that integrates k3d, skaffold, kustomize to provide a local developement environment.

## Why docker registry
