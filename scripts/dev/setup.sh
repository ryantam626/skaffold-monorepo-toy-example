#!/bin/bash

set -euo pipefail

info() {
	printf "\r\033[00;34m $1 \033[0m \n"
}

info "Creating docker volume for local docker registry"
docker volume create local_docker_registry
info "Creating docker registry container (remove the existing container or comment this out if it fails)"
docker container run -d --name docker-registry.local -v local_docker_registry:/var/lib/registry --restart always -p 5000:5000 registry:2
info "Creating k3s cluster with k3d"
k3d cluster create $PROJECT_NAME --registry-config $BASE_DIR/k3d-dev-registries.yaml --volume $BASE_DIR:/mnt/repo
info "Connecting docker registry into k3s network (k3d-$PROJECT_NAME)"
docker network connect k3d-$PROJECT_NAME docker-registry.local

info "Adding $HOSTNAME to your /etc/hosts if required";
HOSTNAME="docker-registry.local"
IP="127.0.0.1"
HOSTS_LINE="$IP\t$HOSTNAME"
if [ -n "$(grep $HOSTNAME /etc/hosts)" ]
    then
        info "$HOSTNAME already exists : $(grep $HOSTNAME /etc/hosts)"
    else
        info "Adding $HOSTNAME to your /etc/hosts for real";
        sudo -- sh -c -e "echo '$HOSTS_LINE' >> /etc/hosts";
fi
