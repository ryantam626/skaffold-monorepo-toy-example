#!/bin/bash

set -euxo pipefail

PATHS=$@
if [ -z "$PATHS" ]; then
  PATHS="/app"
fi

PYTEST=1 pytest $PATHS -W error::UserWarning
