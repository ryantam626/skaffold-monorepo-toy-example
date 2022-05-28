#!/bin/bash

set -euo pipefail

info() {
	printf "\r\033[00;34m $1 \033[0m \n"
}

info "Starting docker registry"
docker start docker-registry.local

K3S_RUNNING_SERVERS=$(k3d cluster list -o json | jq -c ".[] | select ( .name | contains(\"${PROJECT_NAME}\")) | .serversRunning")
if [ "$K3S_RUNNING_SERVERS" -eq "0" ]; then
  info "Starting k3s cluster with k3d"
  k3d cluster start $PROJECT_NAME
else
  info "k3s cluster already running."
fi
info "Configuring kube context to k3s cluster (k3d-$PROJECT_NAME context)"
kubectl config use-context k3d-$PROJECT_NAME

