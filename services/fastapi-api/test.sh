#!/bin/bash

set -euxo pipefail

PATHS=$@
if [ -z "$PATHS" ]; then
  PATHS="/app"
fi

pytest $PATHS -W error::UserWarning
