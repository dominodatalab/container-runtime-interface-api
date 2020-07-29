#!/bin/bash

set -ex

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$SCRIPT_DIR/../" || exit 1

git submodule update --init --recursive --remote --merge

pipenv run python -m grpc_tools.protoc \
  -I vendor/ \
  -I vendor/cri-api/pkg/apis/runtime/v1alpha2 \
  --python_out=src/ \
  --grpc_python_out=src/ \
  vendor/cri-api/pkg/apis/runtime/v1alpha2/api.proto \
  vendor/github.com/gogo/protobuf/gogoproto/gogo.proto
