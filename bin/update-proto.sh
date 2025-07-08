#!/bin/bash

set -ex

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$SCRIPT_DIR/../" || exit 1

# Commented out until 1.26 is fully supported
# git submodule update --init --recursive --remote --merge


# find all prot files under the vendor/cri-api/pkg/apis/runtime/ directory
# strip vendor/cri-api/pkg/apis/runtime/ leaving only the folder before
# vendor/cri-api/pkg/apis/runtime/v1/api.proto becomes
# v1/api.proto
find vendor/cri-api/pkg/apis/runtime/ -name '*.proto' | sed 's|vendor/cri-api/pkg/apis/runtime/||' | \
xargs pipenv run python -m grpc_tools.protoc \
  -I vendor \
  -I vendor/github.com/gogo/protobuf/ \
  -I vendor/cri-api/pkg/apis/runtime/ \
  --python_out=src/cri_api \
  --mypy_out=src/cri_api \
  --grpc_python_out=src/cri_api \
  vendor/github.com/gogo/protobuf/gogoproto/gogo.proto


# replace from v1 or from github with cri_api
find src/cri_api/ -type f -name '*.py' -print0 | xargs -0 -P 1 -I {} sed -i '' -Ee 's/from (v1|github)/from cri_api.\1/' {}
pipenv run black .
