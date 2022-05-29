#!/bin/bash

set -euxo pipefail

PATHS=$@
if [ -z "$PATHS" ]; then
  PATHS="/app"
fi

black -l 110 --check $PATHS
isort --profile black --check-only $PATHS
