#!/bin/bash

MIN_DURATION_MS=$1

if [ -z "$MIN_DURATION_MS" ]; then
  echo "Usage: ./analyze-traces.sh <min_duration_ms>"
  exit 1
fi

# Query Jaeger for api-gateway traces
RESPONSE=$(curl -s "http://localhost:16686/api/traces?service=api-gateway")

# Filter traces longer than given duration (convert microseconds to milliseconds)
echo "$RESPONSE" | jq -r \
  --argjson min "$MIN_DURATION_MS" '
  .data[] |
  select((.spans[0].duration / 1000) > $min) |
  .traceID
'
