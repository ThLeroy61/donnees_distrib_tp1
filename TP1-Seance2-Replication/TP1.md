# TP 1 — Mini-TP : comprendre la réplication

**Module :** Données distribuées — M2 Big Data & IA  
**Séance :** 2 — Architecture & bases de données distribuées  
**Durée :** 1h maximum  
**Format :** binôme  
**Technologies :** Docker, Docker Compose, Python/Flask

---

## 1. Objectif

Dans le TP de la séance 1, vous avez observé la distribution, les nœuds et les pannes.

Dans ce mini-TP, on se concentre sur une notion :

> **La réplication : conserver plusieurs copies d'une même donnée sur plusieurs nœuds.**

Vous allez observer :

- plusieurs nœuds ;
- une écriture ;
- le principe de réplication ;
- une panne de nœud ;
- la continuité du service ;
- la différence entre distribution et réplication.

**Important :** ce TP est indépendant de Cassandra. Cassandra sera étudié ensuite.

---

## 2. Architecture

```text
                         Client
                           │
                           ▼
                    ┌─────────────┐
                    │    Leader   │
                    └──────┬──────┘
                           │
                  réplication des données
                    ┌──────┴──────┐
                    ▼             ▼
              ┌──────────┐  ┌──────────┐
              │Follower 1│  │Follower 2│
              └──────────┘  └──────────┘

                  Réseau Docker
```

Dans cette simulation, le Leader reçoit les écritures et les Followers représentent les copies de données.

---

# 3. Étape 1 — Créer le réseau

Dans le dossier du repository :

```bash
docker network inspect distributed-net > /dev/null 2>&1 || docker network create --driver bridge distributed-net```

Vérifiez :

```bash
docker network ls
```

---

# 4. Étape 2 — Démarrer les trois nœuds

```bash
docker compose up -d
```

Vérifiez :

```bash
docker ps
```

Vous devez retrouver :

```text
node-leader
node-follower-1
node-follower-2
```

---

# 5. Étape 3 — Vérifier les nœuds

```bash
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
```

Résultat attendu :

```json
{"node":"leader","role":"leader","status":"UP"}
```

```json
{"node":"follower-1","role":"follower","status":"UP"}
```

```json
{"node":"follower-2","role":"follower","status":"UP"}
```

### Question

Quel est le rôle de chaque nœud ?

---

# 6. Étape 4 — Écrire une donnée

Envoyez une commande au Leader :

```bash
curl -X POST http://localhost:8080/data \
  -H "Content-Type: application/json" \
  -d '{"key":"order-1","value":"Laptop - quantity=2 - price=1200"}'
```

Puis :

```bash
curl http://localhost:8080/data
```

### Question

Sur quel nœud la donnée a-t-elle été envoyée ?

---

# 7. Étape 5 — Comprendre le principe de réplication

Le principe est :

```text
                  order-1
                     │
                     ▼
                  Leader
                  /     \
                 /       \
                ▼         ▼
          Follower 1   Follower 2
            order-1      order-1
```

### À retenir

```text
Distribution :
les données sont réparties entre plusieurs nœuds.

Réplication :
une même donnée possède plusieurs copies.
```

### Question

Pourquoi conserver plusieurs copies d'une donnée ?

---

# 8. Étape 6 — Simuler une panne

Arrêtez le premier follower :

```bash
docker stop node-follower-1
```

Vérifiez :

```bash
curl http://localhost:8081/health
```

La requête doit échouer.

---

# 9. Étape 7 — Vérifier la continuité du service

Envoyez une nouvelle donnée au Leader :

```bash
curl -X POST http://localhost:8080/data \
  -H "Content-Type: application/json" \
  -d '{"key":"order-2","value":"Smartphone - quantity=1 - price=800"}'
```

Puis :

```bash
curl http://localhost:8080/data
```

### Questions

1. Quel nœud est tombé ?
2. Le Leader est-il toujours disponible ?
3. Pourquoi plusieurs nœuds peuvent-ils améliorer la résilience ?
4. Que pourrait-il se passer si le Leader était lui aussi indisponible ?

---

# 10. Étape 8 — Remettre le nœud en service

```bash
docker start node-follower-1
```

Vérifiez :

```bash
curl http://localhost:8081/health
```

Puis :

```bash
docker ps
```

Les trois nœuds doivent être actifs.

---

# 11. Bilan — 5 minutes

| Notion | Observation |
|---|---|
| Nœud | Instance participant au système |
| Leader | Reçoit les écritures dans la simulation |
| Follower | Représente une copie de la donnée |
| Réplication | Plusieurs copies d'une même donnée |
| Panne | Un nœud devient indisponible |
| Résilience | Le système peut continuer malgré une panne |

### Questions finales

1. Quelle est la différence entre **distribution** et **réplication** ?
2. Pourquoi répliquer une donnée ?
3. Quel est le principal avantage de la réplication en cas de panne ?
4. Quel problème peut apparaître si les copies ne sont pas synchronisées ?
5. Pourquoi un système distribué doit-il gérer la communication entre les nœuds ?

---

# 12. À retenir

```text
              SYSTÈME DISTRIBUÉ
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     Distribution            Réplication
     plusieurs nœuds         plusieurs copies
          │                     │
          ▼                     ▼
      Scalabilité             Résilience
                              Disponibilité
```

