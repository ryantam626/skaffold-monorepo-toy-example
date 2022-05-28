#!/bin/bash

set -euxo pipefail

temp_container_id=$(docker create $SKAFFOLD_IMAGE)
docker cp $temp_container_id:/poetry.lock - > $SKAFFOLD_BUILD_CONTEXT/poetry.lock.tar
tar -xf $SKAFFOLD_BUILD_CONTEXT/poetry.lock.tar -C $SKAFFOLD_BUILD_CONTEXT
rm $SKAFFOLD_BUILD_CONTEXT/poetry.lock.tar
docker rm -v $temp_container_id
