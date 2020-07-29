#!/bin/bash

set -ex

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$SCRIPT_DIR/../" || exit 1

git submodule update --init --recursive --remote --merge

pipenv run python -m grpc_tools.protoc \
  -I vendor \
  -I vendor/github.com/gogo/protobuf/ \
  -I vendor/cri-api/pkg/apis/runtime/ \
  --python_out=src/cri_api \
  --grpc_python_out=src/cri_api \
  v1alpha2/api.proto \
  vendor/github.com/gogo/protobuf/gogoproto/gogo.proto

find src/cri_api/ -type f -name '*.py' -print0 | xargs -0 -P 1 -I {} sed -i '' -Ee 's/from (v1alpha2|github)/from cri_api.\1/' {}
