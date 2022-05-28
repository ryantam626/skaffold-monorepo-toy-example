#!/bin/sh

info() {
	printf "\r\033[00;34m $1 \033[0m \n"
}

warning() {
	printf "\r\033[2K  \033[0;31m $1 \033[0m \n"
}

NUM_POD_LINES=$(kubectl get pods | egrep ${POD_PATTERN} | wc -l)

if [ "$NUM_POD_LINES" -eq "0" ]; then
  warning "No running pod detected!"
  exit 1
fi

if [ "$NUM_POD_LINES" -eq "1" ]; then
  POD_LINE=$(kubectl get pods | egrep ${POD_PATTERN})
  POD=$(echo $POD_LINE | cut -f1 -d' ')
  info "Only one pod detected, automatically selecting it."
  kubectl exec -it $POD -- $@
  exit 0
fi

POD_LINE=$(kubectl get pods | egrep ${POD_PATTERN} | fzf)
POD=$(echo $POD_LINE | cut -f1 -d' ')
kubectl exec -it $POD -- $@
