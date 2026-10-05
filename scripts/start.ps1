docker network inspect distributed-net *> $null
if ($LASTEXITCODE -ne 0) { docker network create --driver bridge distributed-net }
docker compose up -d
docker ps --filter "name=replication-node"
