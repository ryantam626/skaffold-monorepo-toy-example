#!/bin/bash

set -euo pipefail

info() {
	printf "\r\033[00;34m $1 \033[0m \n"
}

info "Stopping docker registry"
docker rm docker-registry.local -f
info "Stopping k3s cluster managed by k3d"
k3d cluster delete $PROJECT_NAME

HOSTNAME="docker-registry.local"
info "Remove $HOSTNAME from your /etc/hosts";
sudo sed -i".bak" "/$HOSTNAME/d" /etc/hosts

