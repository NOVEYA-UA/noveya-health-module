#!/usr/bin/env bash
set -euo pipefail

# NOVEYA • Health Module — SDK generator
# Env knobs (optional):
#   SDK_VERSION=0.3.1
#   OPENAPI_GENERATOR_VERSION=v7.8.0
#   GENERATE_TS=1   # set to 0 to skip TS client

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPENAPI="${OPENAPI:-$ROOT/openapi.yaml}"
SDK_VERSION="${SDK_VERSION:-0.3.1}"
GEN_VERSION="${OPENAPI_GENERATOR_VERSION:-v7.8.0}"

if [[ ! -f "$OPENAPI" ]]; then
  echo "❌ openapi.yaml not found at: $OPENAPI"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "❌ Docker is required (Docker Desktop on Windows/macOS, docker-ce on Linux)."
  exit 1
fi

SDK_DIR="$ROOT/sdk"
PY_OUT="$SDK_DIR/python"
TS_OUT="$SDK_DIR/ts"
mkdir -p "$SDK_DIR"

# Clean previous builds
rm -rf "$PY_OUT" "$TS_OUT"

# Use current user so generated files aren't owned by root (safe to skip on Windows if it errors)
USER_FLAG=()
if command -v id >/dev/null 2>&1; then
  USER_FLAG=( -u "$(id -u):$(id -g)" )
fi

# Make sure we have a stable generator version
docker pull "openapitools/openapi-generator-cli:${GEN_VERSION}" >/dev/null

# --- Python client ---
docker run --rm "${USER_FLAG[@]}" -v "$ROOT":/work "openapitools/openapi-generator-cli:${GEN_VERSION}" \
  generate -i /work/openapi.yaml -g python -o /work/sdk/python \
  --additional-properties=packageName=noveya_health_client,projectName=noveya-health-client,packageVersion="${SDK_VERSION}",hideGenerationTimestamp=true \
  --global-property=apiTests=false,modelTests=false,apiDocs=false,modelDocs=false

# --- TypeScript client (optional; set GENERATE_TS=0 to skip) ---
GENERATE_TS="${GENERATE_TS:-1}"
if [[ "$GENERATE_TS" == "1" ]]; then
  docker run --rm "${USER_FLAG[@]}" -v "$ROOT":/work "openapitools/openapi-generator-cli:${GEN_VERSION}" \
    generate -i /work/openapi.yaml -g typescript-fetch -o /work/sdk/ts \
    --additional-properties=npmName=@noveya/health-client,npmVersion="${SDK_VERSION}",supportsES6=true
fi

echo "✅ SDKs generated:"
echo "  - Python: $PY_OUT (package noveya_health_client @ ${SDK_VERSION})"
if [[ "$GENERATE_TS" == "1" ]]; then
  echo "  - TypeScript: $TS_OUT (@noveya/health-client @ ${SDK_VERSION})"
fi
echo "ℹ️  You can override versions via env: SDK_VERSION, OPENAPI_GENERATOR_VERSION."
