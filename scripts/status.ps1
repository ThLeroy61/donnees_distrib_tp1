docker ps -a --filter "name=replication-node"
Write-Host "`n=== Node 1 ==="
curl.exe -s http://localhost:8080/health
Write-Host "`n=== Node 2 ==="
curl.exe -s http://localhost:8081/health
Write-Host "`n=== Node 3 ==="
curl.exe -s http://localhost:8082/health
