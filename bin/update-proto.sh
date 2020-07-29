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
  vendor/cri-api/pkg/apis/runtime/v1alpha2/api.proto

find src/cri_api/pkg -type f -name '*.py' -print0 | xargs -0 -P 1 -I {} sed -i '' -e 's/from github/from cri_api.github/' {}

pipenv run python -m grpc_tools.protoc \
  -I vendor/ \
  --python_out=src/cri_api \
  --grpc_python_out=src/cri_api \
  vendor/github.com/gogo/protobuf/gogoproto/gogo.proto
