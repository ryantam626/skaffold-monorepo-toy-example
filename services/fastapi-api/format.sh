#!/bin/bash

set -euxo pipefail

PATHS=$@
if [ -z "$PATHS" ]; then
  PATHS="/app"
fi

function finish {
  # Formatting command would have been ran under root, which effectively changes user to root
  # revert this manually instead of messing around with users.
  chown -R 1000 $PATHS
}
trap finish EXIT

isort --profile black $PATHS
black -l 110 $PATHS
