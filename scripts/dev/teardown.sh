#!/bin/bash

set -euo pipefail

info() {
	printf "\r\033[00;34m $1 \033[0m \n"
}

info "Stopping docker registry"
docker stop docker-registry.local
K3S_RUNNING_SERVERS=$(k3d cluster list -o json | jq -c ".[] | select ( .name | contains(\"${PROJECT_NAME}\")) | .serversRunning")
if [ "$K3S_RUNNING_SERVERS" -eq "0" ]; then
  info "k3s cluster already stopped."
else
  info "Stopping k3s cluster managed by k3d"
  k3d cluster stop $PROJECT_NAME
fi
