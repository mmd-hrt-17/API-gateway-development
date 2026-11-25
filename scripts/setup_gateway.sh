#!/usr/bin/env bash
set -euo pipefail

ADMIN_URL="http://127.0.0.1:9180/apisix/admin"
ADMIN_KEY="edd1c9f034335f136f87ad84b625c8f1"

COMMON_PLUGINS='{
  "limit-count": {
    "count": 5,
    "time_window": 60,
    "rejected_code": 429,
    "rejected_msg": "Too Many Requests: Rate limit of 5 requests per minute exceeded.",
    "policy": "local",
    "show_limit_quota_header": true
  },
  "request-id": {
    "include_in_response": true
  }
}'

echo -e "\n[2/4] Registering Route 1: /api/products* -> service3:8003..."
curl -s -X PUT "${ADMIN_URL}/routes/1" \
  -H "X-API-KEY: ${ADMIN_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"products-route\",
    \"uris\": [\"/api/products\", \"/api/products/*\"],
    \"methods\": [\"GET\", \"POST\", \"PUT\", \"DELETE\"],
    \"plugins\": ${COMMON_PLUGINS},
    \"upstream\": {
      \"type\": \"roundrobin\",
      \"nodes\": {
        \"service3:8003\": 1
      }
    }
  }"