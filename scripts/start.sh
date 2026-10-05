#!/usr/bin/env bash
set -e
docker network inspect distributed-net >/dev/null 2>&1 || docker network create --driver bridge distributed-net
docker compose up -d
docker ps --filter "name=replication-node"
