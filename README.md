# TP1 — Session 2 — Réplication distribuée V2

Mini-TP pédagogique : **réplication automatique et récupération après panne**.

## Objectif

Montrer avec Docker + Flask comment une donnée peut être copiée sur plusieurs nœuds et comment un nœud qui disparaît peut récupérer automatiquement les données depuis un autre réplica **sans être redémarré**.

Architecture :

```text
                    Client
                      |
                      v
                +-----------+
                |   Node 1  |
                +-----+-----+
                      |
          +-----------+-----------+
          |                       |
          v                       v
     +---------+             +---------+
     | Node 2  |             | Node 3  |
     +---------+             +---------+
```

Les 3 nœuds stockent une copie des données. Une écriture sur n'importe quel nœud est propagée aux pairs disponibles.

> Cette implémentation est une **simulation pédagogique**. Elle ne reproduit pas les garanties d'un SGBD distribué comme Cassandra.

## Démarrage

Si le réseau existe déjà :

```bash
docker compose up -d
```

Sinon :

```bash
docker network create --driver bridge distributed-net
docker compose up -d
```

Vérifier :

```bash
docker ps
```

## Tester la réplication

Écrire sur Node 1 :

```bash
curl -X POST http://localhost:8080/data   -H "Content-Type: application/json"   -d '{"key":"order-1","value":"Laptop - quantity=2 - price=1200"}'
```

Vérifier :

```bash
curl http://localhost:8080/data
curl http://localhost:8081/data
curl http://localhost:8082/data
```

Les trois nœuds doivent contenir `order-1`.

## Simuler une panne

Arrêter Node 2 :

```bash
docker stop replication-node-2
```

Écrire une nouvelle donnée sur Node 1 :

```bash
curl -X POST http://localhost:8080/data   -H "Content-Type: application/json"   -d '{"key":"order-2","value":"Smartphone - quantity=1 - price=800"}'
```

Node 1 et Node 3 doivent recevoir `order-2`. Node 2 est indisponible.

## Récupération sans redémarrer le nœud

Supprimer complètement Node 2 :

```bash
docker rm -f replication-node-2
```

Le service reste disponible sur Node 1 et Node 3.

Créer un nouveau nœud 2 avec le même service :

```bash
docker compose up -d replication-node-2
```

Le nouveau Node 2 démarre vide puis récupère automatiquement les données depuis un pair disponible.

Vérifier après quelques secondes :

```bash
curl http://localhost:8081/data
```

Il doit récupérer `order-1` et `order-2`.

## Nettoyage

```bash
docker compose down
```

Le réseau externe n'est pas supprimé.
