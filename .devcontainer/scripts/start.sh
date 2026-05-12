#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/kr_backend

echo "Starting MuzFlow stack for Codespaces..."
docker compose -f docker-compose.yml -f docker-compose.codespaces.yml down --remove-orphans
docker compose -f docker-compose.yml -f docker-compose.codespaces.yml up -d --build --wait
docker compose -f docker-compose.yml -f docker-compose.codespaces.yml ps

echo ""
echo "MuzFlow is ready. Open the forwarded port 8080."

