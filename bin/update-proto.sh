#!/bin/bash

set -ex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"
cd "$SCRIPT_DIR/../" || exit 1

# Initialize git submodules
git submodule update --init --recursive --remote --merge

pipenv run python -m grpc_tools.protoc \
  -I vendor \
  -I vendor/github.com/gogo/protobuf/ \
  -I vendor/cri-api/pkg/apis/runtime/ \
  --python_out=src/cri_api \
  --mypy_out=src/cri_api \
  --grpc_python_out=src/cri_api \
  vendor/cri-api/pkg/apis/runtime/v1/api.proto \
  vendor/github.com/gogo/protobuf/gogoproto/gogo.proto

# Note: v1alpha2 is no longer available in the current CRI API
# If you need v1alpha2, you may need to use an older version of the CRI API

find src/cri_api/ -type f -name '*.py' -print0 | xargs -0 -P 1 -I {} sed -i '' -Ee 's/from (v1|github)/from cri_api.\1/' {}
pipenv run black .
