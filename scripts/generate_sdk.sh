#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/sdk"
docker run --rm -v "$ROOT":/work openapitools/openapi-generator-cli       generate -i /work/openapi.yaml -g python -o /work/sdk/python
echo "SDKs are in ./sdk/"
