#!/bin/sh

BASE_DIR="$(git rev-parse --show-toplevel)"

POD_LINE=$(kubectl get pods | grep fastapi-api | fzf)
POD=$(echo $POD_LINE | cut -f1 -d' ')
kubectl cp $POD:poetry.lock $BASE_DIR/services/fastapi-api/poetry.lock
kubectl cp $POD:pyproject.toml $BASE_DIR/services/fastapi-api/pyproject.toml
