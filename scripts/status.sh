#!/usr/bin/env bash
echo "=== Containers ==="
docker ps -a --filter "name=replication-node"
echo
echo "=== Node 1 ==="
curl -s http://localhost:8080/health || true
echo
echo "=== Node 2 ==="
curl -s http://localhost:8081/health || true
echo
echo "=== Node 3 ==="
curl -s http://localhost:8082/health || true
echo
